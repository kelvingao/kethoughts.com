
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
import hashlib
import json

from wx.sign import Sign
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from utils import createLogger, config

# Configure logging
logger = createLogger(__name__)


class NoResultError(Exception):
    pass


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """
        response the right CORS headers
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


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
        token = config['weixin']['token'] # user supplied
        
        logger.info("get signature: %s, echostr: %s, timestamp: %s, nonce: %s", signature, echostr, timestamp, nonce)
           
        try:
            check_signature(token, signature, timestamp, nonce)
            logger.info('WeChat signature, OK.')
            self.write(echostr)
        except InvalidSignatureException:
            raise tornado.web.HTTPError(403, "invalid WeChat signature")

    async def post(self):
        """Server responses to a client jssdk request.

        Args:
            url: a client request url
        
        Returns:
            The signature, timestamp, noncestr and appid
        """
        data = json.loads(self.request.body)
        logger.debug('authentication request from : %s', data['url'])

        appId = config['weixin']['appId']
        appSecret = config['weixin']['appSecret']

        # sign it
        s = Sign(appId, appSecret)
        resp = s.get_jsapi_signature(data['url'])

        self.write(json.dumps(resp))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/weixin/verify", WeixinHandler),
            (r"/api/weixin/signature", WeixinHandler)
        ]
        settings = dict(
            xsrf_cookies=False,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


async def main():

    port = config['server']['port']

    app = Application()
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
