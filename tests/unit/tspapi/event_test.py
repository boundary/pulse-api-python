#!/usr/bin/env python
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

from tspapi import API
from tspapi import Source
from tspapi import Sender
from tspapi import Measurement
import tspapi.event
from unittest import TestCase
from tspapi import RawEvent
from datetime import datetime
import random
import os
import sys
import json

_path = os.path.dirname(__file__)
sys.path.append(_path)
from api_test_utils import TestUtils


class RawEventTest(TestCase):

    def setUp(self):
        self.api = API()

    def test_default_constructor(self):
        raw_event = RawEvent()
        self.assertIsNone(raw_event.created_at)
        self.assertIsNone(raw_event.event_id)
        self.assertIsNone(raw_event.fingerprint_fields)
        self.assertIsNone(raw_event.id)
        self.assertIsNone(raw_event.message)
        self.assertIsNone(raw_event.properties)
        self.assertIsNone(raw_event.received_at)
        self.assertIsNone(raw_event.sender)
        self.assertIsNone(raw_event.severity)
        self.assertIsNone(raw_event.source)
        self.assertIsNone(raw_event.status)
        self.assertIsNone(raw_event.tags)
        self.assertIsNone(raw_event.tenant_id)
        self.assertIsNone(raw_event.title)

    def test_constructor_args(self):
        created_at = int(datetime.now().strftime('%s'))
        event_id = random.randrange(1, 1000000000)
        fingerprint_fields = '@title'
        id = random.randrange(1, 1000000000)
        raw_event = RawEvent(
            created_at=created_at,
            event_id=event_id,
            fingerprint_fields=fingerprint_fields,
        )

        self.assertEqual(created_at, raw_event.created_at)

    def test_repr_(self):
        created_at = int(datetime.now().strftime('%s'))
        event_id = random.randrange(1, 1000000000)
        fingerprint_fields = '@title'
        id = random.randrange(1, 1000000000)
        event_class = 'CHANGE'
        message = TestUtils.random_string(32)
        properties = {"foo": "bar", "color": "red"}
        received_at = int(datetime.now().strftime('%s'))
        sender = TestUtils.random_string(10)
        severity = 'INFO'
        source = Source(ref=TestUtils.random_string(10), _type='host', name='foobar')
        status = 'OPEN'
        tags = {"foo": "bar", "color": "red"}
        tenant_id = random.randrange(1, 10000000)
        title = TestUtils.random_string(16)
        raw_event = RawEvent(
            created_at=created_at,
            event_id=event_id,
            event_class=event_class,
            fingerprint_fields=fingerprint_fields,
            id=id,
            message=message,
            properties=properties,
            received_at=received_at,
            sender=sender,
            severity=severity,
            source=source,
            status=status,
            tags=tags,
            tenant_id=tenant_id,
            title=title
        )
        expected = []
        expected.append("RawEvent(created_at={0}".format(created_at, event_id))
        expected.append(", event_id='{0}'".format(event_id))
        expected.append(", event_class='{0}'".format(event_class))
        expected.append(", fingerprint_fields='{0}'".format(fingerprint_fields))
        expected.append(", id='{0}'".format(id))
        expected.append(", message='{0}'".format(message))
        expected.append(", properties={0}".format(properties))
        expected.append(", source='{0}'".format(source))
        expected.append(", sender='{0}'".format(sender))
        expected.append(", severity='{0}'".format(severity))
        expected.append(", status='{0}'".format(status))
        expected.append(", tags='{0}'".format(tags))
        expected.append(", tenant_id={0}".format(tenant_id))
        expected.append(", title='{0}')".format(title))

        expected = "".join(expected)

        self.assertEqual(expected, raw_event.__repr__())

    def test_create_event(self):
        source = Source(ref='localhost', _type='host', name='bubba')
        self.api.event_create(title='Hello World', fingerprint_fields=['@title'], source=source)

    def test_create_event_with_date(self):
        source = Source(ref='localhost', _type='host', name='bubba')
        dt = datetime.now()
        self.api.event_create(created_at=dt, title='Hello World', fingerprint_fields=['@title'], source=source)

    def test_create_event_with_finger_print_fields(self):
        fingerprint_fields = ['@message']
        source = Source(ref='localhost', _type='host', name='bubba')
        message = 'hello' + TestUtils.random_string(6)
        dt = datetime.now()
        self.api.event_create(message=message, created_at=dt, title='Hello World', fingerprint_fields=fingerprint_fields, source=source)

    def test_create_event_with_properties(self):
        source = Source(ref='localhost', _type='host', name='bubba')
        title = 'sending tags'
        properties = {"foo": "bar"}
        self.api.event_create(title=title, fingerprint_fields=['@title'], source=source, properties=properties)

    def test_create_event_with_class(self):
        source = Source(ref='localhost', _type='host', name='bubba')
        title = 'Event class'
        event_class = 'MyClass'
        self.api.event_create(title=title, fingerprint_fields=['@title'], source=source, event_class=event_class)

    def test_create_event_with_sender(self):
        source = Source(ref='localhost', _type='host', name='bubba')
        sender = Sender(ref='localhost', _type='host', name='bubba')
        self.api.event_create(title='Hello World', fingerprint_fields=['@title'], source=source, sender=sender)

    def test_create_bad_source(self):
        try:
            ref = 'Hello World'
            self.api.event_create(title='Hello World', fingerprint_fields=['@title'], source=ref)
            self.assertTrue(False)
        except ValueError:
            pass

    def test_create_bad_sender(self):
        try:
            source = Source(ref='localhost', _type='host', name='bubba')
            ref = 'Hello World'
            self.api.event_create(title='Hello World', fingerprint_fields=['@title'], source=source, sender=ref)
            self.assertTrue(False)
        except ValueError:
            pass

    def test_event_get(self):
        events = self.api.event_list()
        for event in events:
            print(event)

    def test_to_json(self):
        ref = 'device'
        _type = 'blah'
        name = 'hello'
        properties = {'red': 1, 'blue': 'foo', 'green': 1.0}
        source = Source(ref=ref, _type=_type, name=name, properties=properties)
        event = RawEvent(title='Hello World', fingerprint_fields=['@title'], source=source)
        output = json.dumps(event, sort_keys=True, default=tspapi.event.serialize_instance)
        expected = '{"source": {"name": "hello", "properties": {"blue": "foo", "green": 1.0, "red": 1}, ' + \
                   '"ref": "device", "type": "blah"}, "title": "Hello World"}'
        self.assertEqual(expected, output)

    def test_parse_date_datetime(self):
        d = datetime.now()
        expected = int(d.strftime('%s'))
        timestamp = Measurement.parse_timestamp(d)
        self.assertEqual(expected, timestamp)

    def test_parse_date_epoch(self):
        expected = int(datetime.now().strftime('%s'))
        timestamp = Measurement.parse_timestamp(expected)
        self.assertEqual(expected, timestamp)

    def test_parse_date_ymd(self):
        s = '2015-06-30'
        timestamp = Measurement.parse_timestamp(s)
        expected = int(datetime(2015, 6, 30).strftime('%s'))
        self.assertEqual(expected, timestamp)

    def test_parse_date_ymd_hms24(self):
        s = '2014-06-30 14:27:16'
        timestamp = Measurement.parse_timestamp(s)
        expected = int(datetime(2014, 6, 30, 14, 27, 16).strftime('%s'))
        self.assertEqual(expected, timestamp)

    def test_parse_date_ymd_hms(self):
        s = '2014-06-30 02:27:16PM'
        timestamp = Measurement.parse_timestamp(s)
        expected = int(datetime(2014, 6, 30, 14, 27, 16).strftime('%s'))
        self.assertEqual(expected, timestamp)

    def test_parse_date_bad_date_format(self):
        try:
            s = 'foobar'
            timestamp = Measurement.parse_timestamp(s)
            self.assertTrue(False)
        except ValueError:
            pass



