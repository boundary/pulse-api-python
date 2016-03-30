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


class Measurement(object):

    def __init__(self, metric=None, value=None, source=None, timestamp=None, properties=None):
        self._metric = None
        self._value = None
        self._source = None
        self._timestamp = None
        self._properties = None
        self.metric = metric
        self.value = value
        self.source = source
        self.timestamp = timestamp
        self.properties = properties

    def __repr__(self):
        return "Measurement({0}, {1}, {2}, {3})".format(self.metric, self.value, self.source, self.timestamp)

    @property
    def metric(self):
        return self._metric

    @metric.setter
    def metric(self, metric):
        self._metric = metric

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = properties


def serialize_instance(obj):
    d = []
    d.append(obj.source)
    d.append(obj.metric)
    d.append(obj.value)
    d.append(obj.timestamp)
    d.append(obj.properties)
    return d


def serialize_instance(obj):
    d = []
    d.append(obj.source)
    d.append(obj.metric)
    d.append(obj.value)
    d.append(obj.timestamp)
    d.append(obj.properties)
    return d
