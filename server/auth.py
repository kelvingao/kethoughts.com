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

import jwt
import tornado.web
from utils import createLogger, config

logger = createLogger(__name__)

def authenticated(func):
    async def wrapper(self, *args, **kwargs):
        if not self.current_user:
            logger.info('check user...')
            token = self.request.headers.get("Authorization")
            if token:
                try:
                    decoded = jwt.decode(
                        str(token),
                        config['server']['secret'],
                        algorithm='HS256'
                    )
                    user_id = decoded["user"]["id"]
                except Exception:
                    raise tornado.web.HTTPError(401)  # token invalid, or expired
                else:
                    try:
                        user = await self.queryone(
                            "SELECT * FROM kt_users WHERE id = %s", user_id
                        )
                        logger.info('user found')
                        self.current_user = user
                    except Exception:
                        raise tornado.web.HTTPError(401)  # user not found

                    result = await func(self, *args, **kwargs)
                    return result
            else:
                raise tornado.web.HTTPError(401)  # no token

        else:
            result = await func(self, *args, **kwargs)
            return result
    return wrapper
