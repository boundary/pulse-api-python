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
from tspapi import API
from tspapi import Metric
import tspapi.metric as metric
from utils import TestUtils
import json
import string
import logging


class MetricTest(TestCase):

    def setUp(self):
        self.api = API()

    def test_default_constructor(self):
        metric = Metric()

        self.assertIsNone(metric.name)
        self.assertIsNone(metric.display_name)
        self.assertIsNone(metric.display_name_short)
        self.assertIsNone(metric.description)
        self.assertEqual(metric.default_aggregate, 'avg')
        self.assertEqual(metric.default_resolution, 1000)
        self.assertEqual(metric.unit, 'number')
        self.assertIsNone(metric.type)

    def test_metric_to_json(self):
        m = Metric(name="TEST")
        data = json.dumps(m, default=metric.serialize_instance)
        s = []
        s.append('{"displayName": "TEST", "description": "TEST", "isDisabled": false, "displayNameShort": "TEST",')
        s.append(' "defaultAggregate": "avg", "unit": "number", "defaultResolutionMS": 1000, "name": "TEST"}')
        expected = string.join(s, sep='')
        self.assertEqual(data, expected)

    def test_metric_list_to_json(self):
        l = []
        l.append(Metric(name="ONE"))
        l.append(Metric(name="TWO"))
        s = []
        s.append('[{"displayName": "ONE", "description": "ONE", "isDisabled": false, "displayNameShort": "ONE",')
        s.append(' "defaultAggregate": "avg", "unit": "number", "defaultResolutionMS": 1000, "name": "ONE"},')
        s.append(' {"displayName": "TWO", "description": "TWO", "isDisabled": false, "displayNameShort": "TWO",')
        s.append(' "defaultAggregate": "avg", "unit": "number", "defaultResolutionMS": 1000, "name": "TWO"}]')
        expected = string.join(s, sep='')

        data = json.dumps(l, default=metric.serialize_instance)
        print(data)
        self.assertEqual(data, expected)

    def test_metric_empty_name(self):
        try:
            self.api.metric_create()
        except ValueError as e:
            pass

    def test_metric_create(self):
        self.api.metric_create(name="FOOBAR" + TestUtils.random_string(6))

    def test_metric_create_one_batch(self):
        # logging.basicConfig(level=logging.DEBUG)
        metric1 = Metric(name='METRIC' + TestUtils.random_string(6),
                         display_name='BATCH',
                         display_name_short='BATCH')
        self.api.metric_create_batch([metric1])

