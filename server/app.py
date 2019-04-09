
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

import logging
import tornado.ioloop
import tornado.web
import tornado.locks
import hashlib

from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from tornado.options import define, options
from utils import createLogger

define("port", default=5000, help="run on the given port", type=int)

# Configure logging
logger = createLogger(__name__, level=logging.DEBUG)


class NoResultError(Exception):
    pass


class BaseHandler(tornado.web.RequestHandler):
    pass


class WeixinHandler(BaseHandler):
    """WeChat signature verification。

    Args:
      signature: WeChat encryption signature, including the user supplied token，the timestamp and nonce parameter
      echostr: a random string
      timestamp: time stamp
      nonce:  a random number
    
    Returns:
      The echostr
    """
    async def get(self):
        signature = self.get_argument("signature")
        echostr = self.get_argument("echostr")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")

        logger.debug("%s: get signature: %s, echostr: %s, timestamp: %s, nonce: %s", __class__, signature, echostr, timestamp, nonce)
           
        conf = WechatConf(
            token='weixin',
            appid='wx2033ac8b479c9fa0',
            appsecret='0adc2c7ab0764d402a0f33840e1eff49',
        )

        wechat_instance = WechatBasic(conf=conf)
        if wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            logger.info('signature verification success.')
            self.write(echostr)
        else:
            raise tornado.web.HTTPError(403, "invalid signature")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/weixin", WeixinHandler)
        ]
        settings = dict(
            xsrf_cookies=False,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


async def main():

    app = Application()
    app.listen(options.port)

    logger.info(f"http://127.0.0.1:{ options.port }/")
    logger.info("Press Ctrl+C to quit")

    # In this demo the server will simply run until interrupted
    # with Ctrl-C, but if you want to shut down more gracefully,
    # call shutdown_event.set().
    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
