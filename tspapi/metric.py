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
import requests
import json
import logging


class Metric(object):
    def __init__(self, *args, **kwargs):
        if 'name' not in kwargs:
            raise ValueError("name not specified")

        self._name = kwargs['name'] if 'name' in kwargs else None
        self._display_name = kwargs['display_name'] if 'display_name' in kwargs else self._name
        self._display_name_short = kwargs['display_name_short'] if 'display_name_short' in kwargs else self._name
        self._description = kwargs['description'] if 'description' in kwargs else self._name
        self._default_aggregate = kwargs['default_aggregate'] if 'default_aggregate' in kwargs else 'avg'
        self._default_resolution = kwargs['default_resolution'] if 'default_resolution' in kwargs else 1000
        self._is_disabled = kwargs['is_disabled'] if 'is_disabled' in kwargs else False
        self._unit = kwargs['unit'] if 'unit' in kwargs else 'number'
        self._type = kwargs['_type'] if '_type' in kwargs else None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{0}(name='{1}'" \
               ", display_name='{2}'" \
               ", display_name_short='{3}'" \
               ", description='{4}'" \
               ", default_aggregate='{5}'" \
               ", default_resolution={6}" \
               ", unit='{7}'" \
               ", _type='{8}'" \
               ", is_disabled='{9}'" \
               ")".format(
                self.__class__.__name__,
                self._name,
                self._display_name,
                self._display_name_short,
                self._description,
                self._default_aggregate,
                self._default_resolution,
                self._unit,
                self._type,
                self._is_disabled)

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_name_short(self):
        return self._display_name_short

    @property
    def description(self):
        return self._description

    @property
    def default_aggregate(self):
        return self._default_aggregate

    @property
    def default_resolution(self):
        return self._default_resolution

    @property
    def is_disabled(self):
        return self._is_disabled

    @property
    def unit(self):
        return self._unit

    @property
    def type(self):
        return self._type


def serialize_instance(obj):
    d = {}
    d['name'] = obj.name
    d['displayName'] = obj.display_name
    d['displayNameShort'] = obj.display_name_short
    d['description'] = obj.description
    d['defaultAggregate'] = obj.default_aggregate
    d['defaultResolutionMS'] = obj.default_resolution
    d['unit'] = obj.unit
    if obj.type is not None:
        d['type'] = obj.type
    d['isDisabled'] = obj.is_disabled
    return d


def metric_get_handle_results(api_result, context=None):
    logging.debug("metric_get_handle_results")
    result = None
    # Only process if we get HTTP result of 200
    if api_result.status_code == requests.codes.ok:
        results = json.loads(api_result.text)
        metrics = []
        for metric in results['result']:
            metrics.append(Metric(name=metric['name'],
                                  display_name=metric['displayName'],
                                  display_name_short=metric['displayNameShort'],
                                  description=metric['description'],
                                  default_aggregate=metric['defaultAggregate'],
                                  default_resolution=metric['defaultResolutionMS'],
                                  unit=metric['unit'],
                                  _type=metric['type'] if 'type' in metric else None,
                                  is_disabled=metric['isDisabled']))

        return metrics
