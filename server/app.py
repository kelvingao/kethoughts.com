# MIT License

# Copyright (c) 2019 Kelvin Gao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import tornado.ioloop
import tornado.web
import tornado.locks
import json
import jwt
import aiomysql
import bcrypt
import datetime

from wx.sign import Sign
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from utils import createLogger, config
from auth import authenticated
from qiniu import Auth

# Configure logging
logger = createLogger(__name__)


class NoResultError(Exception):
    pass


async def maybe_create_tables(db):
    try:
        async with db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT COUNT(*) FROM kt_posts LIMIT 1")
                await cur.fetchone()
    except aiomysql.ProgrammingError:
        with open("schema.sql") as f:
            schema = f.read()
        async with db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(schema)


class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            (r"/api/auth/login", LoginHandler),
            (r"/api/users", UsersHandler),
            (r"/api/posts", PostsHandler),
            (r"/api/weixin/verify", WeixinHandler),
            (r"/api/weixin/signature", WeixinHandler),
            (r"/api/qiniu", QiniuHandler)
        ]
        settings = dict(
            xsrf_cookies=False,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def row_to_obj(self, row, cur):
        """Convert a SQL row to an object supporting dict and attribute access."""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc[0]] = val
        return obj

    async def execute(self, stmt, *args):
        """Execute a SQL statement.

        Must be called with ``await self.execute(...)``
        """
        async with self.application.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(stmt, args)

    async def query(self, stmt, *args):
        """Query for a list of results.

        Typical usage::

            results = await self.query(...)

        Or::

            for row in await self.query(...)
        """
        async with self.application.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(stmt, args)
                return [self.row_to_obj(row, cur) for row in await cur.fetchall()]

    async def queryone(self, stmt, *args):
        """Query for exactly one result.

        Raises NoResultError if there are no results, or ValueError if
        there are more than one.
        """
        results = await self.query(stmt, *args)
        if len(results) == 0:
            raise NoResultError()
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]

    def set_default_headers(self):
        """Response with right CORS headers."""

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class LoginHandler(BaseHandler):
    async def post(self):
        """Login authentification."""
        data = json.loads(self.request.body)
        logger.info('%s: login request...', __class__.__name__)

        try:
            user = await self.queryone(
                "SELECT * FROM kt_users WHERE email = %s", data['email']
            )
            logger.info('%s: user found', __class__.__name__)
        except NoResultError:
            raise tornado.web.HTTPError(401)

        hashed_password = await tornado.ioloop.IOLoop.current().run_in_executor(
            None,
            bcrypt.hashpw,
            tornado.escape.utf8(data['password']),
            tornado.escape.utf8(user.password),
        )
        hashed_password = tornado.escape.to_unicode(hashed_password)

        if hashed_password == user.password:
            encoded_jwt = jwt.encode({
                'user': {'id': user.id, 'name': user.name},
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                config['server']['secret'],
                algorithm='HS256'
            )
            resp = {
                'token': str(encoded_jwt, encoding='utf-8'),
            }
            self.write(resp)

        else:
            raise tornado.web.HTTPError(401)


class datetimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.timestamp()
        return json.JSONEncoder.default(self, obj)


class UsersHandler(BaseHandler):
    async def get(self):
        """ Get all users information."""

        users = await self.query(
            "SELECT U.id, U.name, U.email, R.role_name, U.created, U.last_ip, U.login_count FROM kt_users U, kt_roles R;"
        )
        if not users:
            return

        self.write(json.dumps(users, cls=datetimeJSONEncoder))


class PostsHandler(BaseHandler):
    async def get(self):
        id = self.get_argument("id", None)
        slug = self.get_argument("slug", None)
        visibility = self.get_argument("visibility", None)
        post = None

        if id:
            post = await self.queryone("SELECT * FROM kt_posts WHERE id = %s", int(id))
            logger.info('%s: get post of id: %s', __class__.__name__, id)
            self.write(json.dumps(post, cls=datetimeJSONEncoder))

        elif slug:
            post = await self.queryone("SELECT * FROM kt_posts WHERE slug = %s", slug)
            logger.info('%s: get post of slug : %s', __class__.__name__, slug)

            await self.execute("UPDATE kt_posts SET views = views + 1 WHERE slug = %s", slug),
            self.write(json.dumps(post, cls=datetimeJSONEncoder))

        else:
            if(visibility == 'all'):
                posts = await self.query(
                    "SELECT P.id, P.title, P.slug, P.content, U.name, P.status, P.type, P.views, P.created, P.modified FROM kt_posts P, kt_users U ORDER BY modified DESC"
                )
            else:
                posts = await self.query(
                    "SELECT P.id, P.title, P.slug, P.content, U.name, P.status, P.type, P.views, P.created, P.modified FROM kt_posts P, kt_users U WHERE P.status = 'publish' ORDER BY modified DESC"
                )
            if not posts:
                return
            logger.info('%s: get all posts...', __class__.__name__)
            self.write(json.dumps(posts, cls=datetimeJSONEncoder))

    @authenticated
    async def delete(self):
        id = self.get_argument("id")
        logger.info('%s: delete post of id : %s', __class__.__name__, id)

        if id:
            await self.execute("DELETE FROM kt_posts WHERE id = %s", int(id))
        else:
            raise tornado.web.HTTPError(412)

    @authenticated
    async def post(self):
        # retrieve parameters
        data = json.loads(self.request.body)

        id = data["id"]
        slug = data["slug"]
        text = data["content"]
        title = data["title"]
        excerpt = data["excerpt"]
        featured_image = data["featured_image"]
        status = data["status"]

        if id:
            logger.info('edit post...')
            try:
                await self.queryone(
                    "SELECT * FROM kt_posts WHERE id = %s", int(id)
                )
            except NoResultError:
                raise tornado.web.HTTPError(404)

            await self.execute(
                "UPDATE kt_posts SET title = %s, content = %s, slug = %s, featured_image = %s, status = %s, modified = now()"
                "WHERE id = %s",
                title,
                text,
                slug,
                featured_image,
                status,
                int(id),
            )

            resp = {'result': 'ok', 'content': 'edit done'}
            self.write(resp)
        else:
            if not slug:
                raise tornado.web.HTTPError(412)
            while True:
                e = await self.query("SELECT * FROM kt_posts WHERE slug = %s", slug)
                if not e:
                    logger.info('%s: create new post...', __class__.__name__)
                    break
                logger.warn('%s: post slug duplicated...', __class__.__name__)
                slug += "-2"  # duplicate slug
            await self.execute(
                "INSERT INTO kt_posts (author_id,title,slug,content,excerpt,status,featured_image,created,modified)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                self.current_user['id'],
                title,
                slug,
                text,
                excerpt,
                status,
                featured_image
            )
            logger.info('%s: new post created', __class__.__name__)

            resp = {'result': 'ok', 'content': 'post created'}
            self.write(resp)


class WeixinHandler(BaseHandler):
    async def get(self):
        """WeChat signature verification.

        Args:
            signature: WeChat encryption signature, including a user token，timestamp and a nonce
            echostr: a random string
            timestamp: time stamp
            nonce:  a random number

        Returns:
            The echostr
        """
        signature = self.get_argument("signature")
        echostr = self.get_argument("echostr")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        token = config['weixin']['token']  # user supplied

        logger.info("%s: WeChat signature verification request...", __class__.__name__)

        try:
            check_signature(token, signature, timestamp, nonce)
            logger.info('%s: WeChat signature, OK.', __class__.__name__)
            self.write(echostr)
        except InvalidSignatureException:
            raise tornado.web.HTTPError(403)

    async def post(self):
        """Server responses to a client jssdk request.

        Args:
            url: a client request url

        Returns:
            The signature, timestamp, noncestr and appid
        """
        data = json.loads(self.request.body)
        logger.debug('%s: signature request from : %s', __class__.__name__, data['url'])

        appId = config['weixin']['appId']
        appSecret = config['weixin']['appSecret']

        # sign it
        s = Sign(appId, appSecret)
        resp = s.get_jsapi_signature(data['url'])

        self.write(json.dumps(resp))


class QiniuHandler(BaseHandler):
    async def get(self):
        bucket_name = self.get_argument("bucket")
        key = self.get_argument("filename")

        access_key = config['qiniu']['accesskey']
        secret_key = config['qiniu']['secretkey']
        q = Auth(access_key, secret_key)

        # put policy
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        policy = {}
        logger.info('%s: upload token request...', __class__.__name__)
        token = q.upload_token(
            bucket_name,
            key,
            3600,  # expired time: 1 hour
            policy)

        self.write(token)


async def main():

    # Create the global connection pool.
    async with aiomysql.create_pool(
        host=config['mysql']['host'],
        port=config['mysql']['port'],
        user=config['mysql']['user'],
        password=config['mysql']['password'],
        db=config['mysql']['database'],
        autocommit=True,
    ) as db:
        await maybe_create_tables(db)

        port = config['server']['port']
        app = Application(db)
        app.listen(port)

        logger.info(f"http://127.0.0.1:{ port }")
        logger.info("Press Ctrl+C to quit")

        # In this demo the server will simply run until interrupted
        # with Ctrl-C, but if you want to shut down more gracefully,
        # call shutdown_event.set().
        shutdown_event = tornado.locks.Event()
        await shutdown_event.wait()


if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
