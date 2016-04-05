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


class BaseEvent(object):

    def __init__(self, *args, **kwargs):
        self._event_id = kwargs['event_id'] if 'event_id' in kwargs else None
        self._fingerprint_fields = kwargs['fingerprint_fields'] if 'fingerprint_fields' in kwargs else None
        self._id = kwargs['id'] if 'id' in kwargs else None
        self._message = kwargs['message'] if 'message' in kwargs else None
        self._properties = kwargs['properties'] if 'properties' in kwargs else None
        self._source = kwargs['source'] if 'source' in kwargs else None
        self._sender = kwargs['sender'] if 'sender' in kwargs else None
        self._severity = kwargs['severity'] if 'severity' in kwargs else None
        self._status = kwargs['status'] if 'status' in kwargs else None
        self._tags = kwargs['tags'] if 'tags' in kwargs else None
        self._tenant_id = kwargs['tenant_id'] if 'tenant_id' in kwargs else None
        self._title = kwargs['title'] if 'title' in kwargs else None

        self._received_at = kwargs['received_at'] if 'received_at' in kwargs else None

    @property
    def event_id(self):
        return self._event_id

    @property
    def fingerprint_fields(self):
        return self._fingerprint_fields

    @property
    def id(self):
        return self._id

    @property
    def message(self):
        return self._message

    @property
    def properties(self):
        return self._properties

    @property
    def received_at(self):
        return self._received_at

    @property
    def title(self):
        return self._title

    @property
    def sender(self):
        return self._sender

    @property
    def severity(self):
        return self._severity

    @property
    def source(self):
        return self._source

    @property
    def status(self):
        return self._status

    @property
    def tags(self):
        return self._tags

    @property
    def tenant_id(self):
        return self._tenant_id


class RawEvent(BaseEvent):

    def __init__(self, *args, **kwargs):
        super(RawEvent, self).__init__(*args, **kwargs)


class Event(BaseEvent):

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._id = None

    @property
    def id(self):
        return self._id


def serialize_instance(obj):
    d = []
    d.append(obj.source)
    d.append(obj.metric)
    d.append(obj.value)
    d.append(obj.timestamp)
    d.append(obj.properties)
    return d


