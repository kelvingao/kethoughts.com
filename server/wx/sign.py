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

import random
import string
import time

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatJSAPI
from utils import createLogger

# Configure logging
logger = createLogger(__name__)


class Sign:
    def __init__(self, appId, appSecret):
        self.appId = appId
        self.appSecret = appSecret

        self.wechat_client = WeChatClient(self.appId, self.appSecret)
        self.wechat_jsapi = WeChatJSAPI(self.wechat_client)

    def get_jsapi_signature(self, url):

        noncestr = self.__create_nonce_str()
        timestamp = self.__create_timestamp()
        jsapi_ticket = self.wechat_jsapi.get_jsapi_ticket()

        try:
            signature = self.wechat_jsapi.get_jsapi_signature(noncestr, jsapi_ticket, timestamp, url)
            logger.debug('WeChat sign: %s', signature)

            resp = dict()
            resp['signature'] = signature
            resp['timestamp'] = timestamp
            resp['noncestr'] = noncestr
            resp['appid'] = self.appId

            return resp
        except Exception as e:
            logger.error('WeChat sign failed. %s', e)

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())
