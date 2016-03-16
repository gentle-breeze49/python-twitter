# Copyright 2016 The Python-Twitter Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import twitter

CONSUMER_KEY = 'WWWWWWWW'
CONSUMER_SECRET = 'XXXXXXXX'
ACCESS_TOKEN = 'YYYYYYYY'
ACCESS_TOKEN_SECRET = 'ZZZZZZZZ'


# Create an Api instance.
api = twitter.Api(consumer_key='consumer_key',
                  consumer_secret='consumer_secret',
                  access_token_key='access_token',
                  access_token_secret='access_token_secret')

users = api.GetFriends()

print([u.screen_name for u in users])
