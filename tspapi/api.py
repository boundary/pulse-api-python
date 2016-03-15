#
# Copyright 2016 BMC Software, Inc.
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
from tspapi.api_call import _ApiCall
import tspapi.measurement as measurement


class API(_ApiCall):

    def __init__(self, api_host=None, email=None, api_token=None):
        self._get_environment()
        _ApiCall.__init__(self, api_host=api_host, email=email, api_token=api_token)

    def _get_environment(self):
        """
        Gets the configuration stored in environment variables
        """
        if 'TSP_EMAIL' in os.environ:
            self._email = os.environ['TSP_EMAIL']
        if 'TSP_API_TOKEN' in os.environ:
            self._api_token = os.environ['TSP_API_TOKEN']
        if 'TSP_API_HOST' in os.environ:
            self._api_host = os.environ['TSP_API_HOST']
        else:
            self._api_host = 'api.truesight.bmc.com'

    def measurement_create(self, metric, value, source=None, timestamp=None):
        """
        Creates a new measurement in TrueSight Pulse instance.

        Identifies which `metric` to use to add a measurement.

        :param value: Value of the measurement
        :param source: Origin of the measurement
        :param timestamp: Time of the occurrence of the measurement
        :return: None
        """
        self._method = 'POST'
        payload = {}
        payload['metric'] = metric
        payload['measure'] = float(value)
        if source is not None:
            payload['source'] = source
        if timestamp is not None:
            payload['timestamp'] = int(timestamp)
        self._data = json.dumps(payload, sort_keys=True)
        self._headers = {'Content-Type': 'application/json', "Accept": "application/json"}
        self._path = "v1/measurements"
        self._api_call()

    def measurement_create_batch(self, measurements):
        """
        :param measurements: List of measurements
        :return: None
        """
        self._method = 'POST'
        self._data = json.dumps(measurements, default=measurement.serialize_instance)
        self._headers = {'Content-Type': 'application/json', "Accept": "application/json"}
        self._path = "v1/measurements"
        self._api_call()

    def create_event(self):
        pass

    def hostgroup_create(self, name, sources=[]):

        payload = {}
        payload['name'] = name
        payload['hostnames'] = sources

        self._method = 'POST'
        self._data = json.dumps(payload)
        self._headers = {'Content-Type': 'application/json', "Accept": "application/json"}
        self._path = "v1/hostgroups"
        self._api_call()
