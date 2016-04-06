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
import tspapi.metric as metric


class API(_ApiCall):

    def __init__(self, api_host=None, email=None, api_token=None):
        (api_host, email, api_token) = self._get_environment(api_host, email, api_token)
        _ApiCall.__init__(self, api_host=api_host, email=email, api_token=api_token)

    def _get_environment(self, api_host, email, api_token):
        """
        Gets the configuration stored in environment variables
        """
        if email is None and 'TSP_EMAIL' in os.environ:
            email = os.environ['TSP_EMAIL']
        if api_token is None and 'TSP_API_TOKEN' in os.environ:
            api_token = os.environ['TSP_API_TOKEN']
        if api_host is None and 'TSP_API_HOST' in os.environ:
            api_host = os.environ['TSP_API_HOST']
        else:
            api_host = 'api.truesight.bmc.com'

        return api_host, email, api_token

    def measurement_create(self, metric, value, source=None, timestamp=None, properties=None):
        """
        Creates a new measurement in TrueSight Pulse instance.

        :param metric: Identifies the metric to use to add a measurement
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
        if properties is not None:
            payload['metadata'] = properties
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

    def metric_create(self,
                      name=None,
                      display_name=None,
                      display_name_short=None,
                      description=None,
                      default_aggregate='avg',
                      default_resolution=1000,
                      unit='number',
                      is_disabled=False,
                      _type=None):

        if name is None:
            raise ValueError("name not specified")

        if display_name is None:
            display_name = name

        if display_name_short is None:
            display_name_short = name

        if description is None:
            description = name

        metric = {
            "name": name,
            "displayName": display_name,
            "displayNameShort": display_name_short,
            "description": description,
            "defaultAggregate": default_aggregate,
            "defaultResolutionMS": default_resolution,
            "unit": unit,
            "isDisabled": is_disabled,
            "type": _type
        }
        print(metric)

        self._method = 'POST'
        self._data = json.dumps(metric)
        self._headers = {'Content-Type': 'application/json', "Accept": "application/json"}
        self._path = "v1/metrics"
        self._api_call()

    def metric_create_batch(self, metrics):
        self._method = 'POST'
        self._data = json.dumps(metrics, default=metric.serialize_instance)
        self._headers = {'Content-Type': 'application/json', "Accept": "application/json"}
        self._path = "v1/batch/metrics"
        self._api_call()

    def metric_delete(self, name, remove_alarms=False):
        self._method = 'DELETE'
        self._headers = {'Content-Type': 'application/json', "Accept": "application/json"}
        data = { "removeAlarms": remove_alarms}
        self._data = json.dumps(data)
        self._path = "v1/metrics/{0}".format(name)
        self._api_call()

    def metric_list(self):
        pass

    def metric_update(self):
        pass

    def event_create(self):
        pass

    def event_get(self):
        pass

    def event_list(self):
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
