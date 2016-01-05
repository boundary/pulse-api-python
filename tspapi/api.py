#
# Copyright 2015 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import json
import logging
from tspapi import ApiCall


class API(ApiCall):

    def __init__(self, api_host='premium-api.boundary.com', email=None, api_token=None):
        self._get_environment()
        ApiCall.__init__(self, api_host=api_host, email=email, api_token=api_token)

    def _get_environment(self):
        """
        Gets the configuration stored in environment variables
        """
        if 'BOUNDARY_EMAIL' in os.environ:
            self._email = os.environ['BOUNDARY_EMAIL']
        if 'BOUNDARY_API_TOKEN' in os.environ:
            self._api_token = os.environ['BOUNDARY_API_TOKEN']
        if 'BOUNDARY_API_HOST' in os.environ:
            self._api_host = os.environ['BOUNDARY_API_HOST']
        else:
            self._api_host = 'premium-api.boundary.com'

    def measurement_create(self, metric, value, source=None, timestamp=None):
        self.method = 'POST'
        payload = {}
        payload['metric'] = metric
        payload['measure'] = value
        payload['source'] = source
        payload['timestamp'] = int(timestamp)
        self.data = json.dumps(payload, sort_keys=True)
        self.headers = {'Content-Type': 'application/json', "Accept": "application/json"}
        self.path = "v1/measurements"
        self.api_call()

    def create_event(self):
        pass