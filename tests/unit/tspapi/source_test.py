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

from unittest import TestCase
from tspapi import Source
from tspapi import Sender
import tspapi.source
import json


class SourceTest(TestCase):

    def test_default_contructor(self):
        source = Source()
        self.assertIsNone(source.ref)
        self.assertIsNone(source.type)
        self.assertIsNone(source.name)
        self.assertIsNone(source.properties)

    def test_constructor_args(self):
        ref = 'foo'
        _type = 'host'
        name = 'bar'
        properties = {'red': 1, 'blue': 'foo', 'green': 1.0}
        source = Source(ref=ref, _type=_type, name=name, properties=properties)

        self.assertEqual(source.ref, ref)
        self.assertEqual(source.type, _type)
        self.assertEqual(source.name, name)
        self.assertEqual(source.properties, properties)

    def test_ref(self):
        ref = 'bar'
        source = Source(ref=ref)
        self.assertEqual(source.ref, ref)

    def test_type(self):
        _type = 'blah'
        source = Source(_type=_type)
        self.assertEqual(source.type, _type)

    def test_name(self):
        name = 'hello'
        source = Source(name=name)
        self.assertEqual(source.name, name)

    def test_properties(self):
        properties = {'red': 1, 'blue': 'foo', 'green': 1.0}
        source = Source(properties=properties)
        self.assertEqual(1, properties['red'])
        self.assertEqual('foo', properties['blue'])
        self.assertEqual(1.0, properties['green'])

    def test_to_json(self):
        ref = 'device'
        _type = 'blah'
        name = 'hello'
        properties = {'red': 1, 'blue': 'foo', 'green': 1.0}
        source = Source(ref=ref, _type=_type, name=name, properties=properties)

        output = json.dumps(source, sort_keys=True, default=tspapi.source.serialize_instance)
        expected = '{"name": "hello", "properties": {"blue": "foo", "green": 1.0, "red": 1}, ' + \
                   '"ref": "device", "type": "blah"}'
        self.assertEqual(expected, output)


class SenderTest(TestCase):

    def test_default_constructor(self):
        sender = Sender()
        self.assertIsNone(sender.ref)
        self.assertIsNone(sender.type)
        self.assertIsNone(sender.name)
        self.assertIsNone(sender.properties)

    def test_constructor_args(self):
        ref = 'foo'
        _type = 'host'
        name = 'bar'
        properties = {'red': 1, 'blue': 'foo', 'green': 1.0}
        sender = Sender(ref=ref, _type=_type, name=name, properties=properties)

        self.assertEqual(sender.ref, ref)
        self.assertEqual(sender.type, _type)
        self.assertEqual(sender.name, name)
        self.assertEqual(sender.properties, properties)

    def test_ref(self):
        ref = 'bar'
        sender = Sender(ref=ref)
        self.assertEqual(sender.ref, ref)

    def test_type(self):
        _type = 'blah'
        sender = Sender(_type=_type)
        self.assertEqual(sender.type, _type)

    def test_name(self):
        name = 'hello'
        sender = Sender(name=name)
        self.assertEqual(sender.name, name)

    def test_properties(self):
        properties = {'red': 1, 'blue': 'foo', 'green': 1.0}
        sender = Sender(properties=properties)
        self.assertEqual(1, properties['red'])
        self.assertEqual('foo', properties['blue'])
        self.assertEqual(1.0, properties['green'])

    def test_to_json(self):
        ref = 'device'
        _type = 'blah'
        name = 'hello'
        properties = {'red': 1, 'blue': 'foo', 'green': 1.0}
        sender = Sender(ref=ref, _type=_type, name=name, properties=properties)

        output = json.dumps(sender, sort_keys=True, default=tspapi.source.serialize_instance)
        expected = '{"name": "hello", "properties": {"blue": "foo", "green": 1.0, "red": 1}, ' + \
                   '"ref": "device", "type": "blah"}'
        self.assertEqual(expected, output)





