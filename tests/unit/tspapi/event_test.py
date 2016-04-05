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
from tspapi import RawEvent


class RawEventTest(TestCase):

    def test_default_constructor(self):
        source = RawEvent()
        self.assertIsNone(source.created_at)
        self.assertIsNone(source.event_id)
        self.assertIsNone(source.fingerprint_fields)
        self.assertIsNone(source.id)
        self.assertIsNone(source.message)
        self.assertIsNone(source.properties)
        self.assertIsNone(source.received_at)
        self.assertIsNone(source.sender)
        self.assertIsNone(source.severity)
        self.assertIsNone(source.source)
        self.assertIsNone(source.status)
        self.assertIsNone(source.tags)
        self.assertIsNone(source.tenant_id)
        self.assertIsNone(source.title)

    def test_constructor_args(self):
        pass

    def test_ref(self):
        pass

    def test_type(self):
        pass

    def test_name(self):
        pass

