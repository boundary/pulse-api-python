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
import random


class MetricTest(TestCase):
    def setUp(self):
        # logging.basicConfig(level=logging.DEBUG)
        self.api = API()

        self.name = 'red'
        self.display_name = 'green'
        self.display_name_short = 'blue'
        self.description = 'magenta'
        self.default_aggregate = 'sum'
        self.default_resolution = 60000
        self.unit = 'duration'
        self.type = 'FOOBAR'
        self.is_disabled = False
        self.metric = Metric(name=self.name,
                             display_name=self.display_name,
                             display_name_short=self.display_name_short,
                             description=self.description,
                             default_aggregate=self.default_aggregate,
                             default_resolution=self.default_resolution,
                             unit=self.unit,
                             _type=self.type,
                             is_disabled=self.is_disabled)

    def test_minimal_constructor(self):
        name = 'FOO'
        m = Metric(name=name)

        self.assertEqual(name, m.name)
        self.assertEqual(name, m.display_name)
        self.assertEqual(name, m.display_name_short)
        self.assertEqual(name, m.description)
        self.assertEqual(m.default_aggregate, 'avg')
        self.assertEqual(m.default_resolution, 1000)
        self.assertEqual(m.unit, 'number')
        self.assertIsNone(m.type)

    def test_constructor_arguments(self):
        self.assertEqual(self.name, self.metric.name)
        self.assertEqual(self.display_name, self.metric.display_name)
        self.assertEqual(self.display_name_short, self.metric.display_name_short)
        self.assertEqual(self.description, self.metric.description)
        self.assertEqual(self.default_aggregate, self.metric.default_aggregate)
        self.assertEqual(self.default_resolution, self.metric.default_resolution)
        self.assertEqual(self.unit, self.metric.unit)
        self.assertEqual(self.type, self.metric.type)
        self.assertEqual(self.is_disabled, self.metric.is_disabled)

    def test_representation_string(self):
        """
        Test the output of the __repr__ method
        :param self:
        :return:
        """
        expected = "Metric(name='red', display_name='green', display_name_short='blue', description='magenta', default_aggregate='sum', default_resolution=60000, unit='duration', _type='FOOBAR', is_disabled='False')"
        self.assertEqual(expected, self.metric.__repr__())

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
        self.assertEqual(data, expected)

    def test_metric_instance_empty_name(self):
        """
        Ensure that creating a metric with an empty name throws a
        ValueError exception
        :return:
        """
        try:
            m = Metric()
            self.assertTrue(False)
        except ValueError as e:
            pass

    def test_metric_empty_name(self):
        """
        Ensure that trying to call the create metric API with an empty name
        throws a ValueError exception
        :return:
        """
        try:
            self.api.metric_create()
            self.assertTrue(False)
        except ValueError as e:
            pass

    def test_metric_create(self):
        self.api.metric_create(name="TEST_CREATE_FOOBAR" + TestUtils.random_string(6))

    def test_metric_create_one_batch(self):
        # logging.basicConfig(level=logging.DEBUG)
        name = 'TEST_CREATE_BATCH_ONE_FOOBAR' + TestUtils.random_string(6)
        display_name = "BATCH" + TestUtils.random_string(6)
        display_name_short = "BATCH" + TestUtils.random_string(3)
        description = TestUtils.random_string(32)
        default_aggregate = 'sum'
        default_resolution = random.randrange(1000, 60000)
        unit = 'percent'
        _type = 'FOO'
        is_disabled = True

        metric1 = Metric(name=name,
                         display_name=display_name,
                         display_name_short=display_name_short,
                         description=description,
                         default_aggregate=default_aggregate,
                         default_resolution=default_resolution,
                         unit=unit,
                         _type=_type,
                         is_disabled=is_disabled)

        metrics = self.api.metric_create_batch([metric1])

        m = metrics[0]
        self.assertEqual(len(metrics), 1)
        self.assertEqual(name, metrics[0].name)
        self.assertEqual(display_name, metrics[0].display_name)
        self.assertEqual(display_name_short, metrics[0].display_name_short)
        self.assertEqual(description, metrics[0].description)
        self.assertEqual(default_aggregate.upper(), metrics[0].default_aggregate)
        self.assertEqual(default_resolution, metrics[0].default_resolution)
        self.assertEqual(unit, metrics[0].unit)
        self.assertEqual(_type, metrics[0].type)
        self.assertEqual(is_disabled, metrics[0].is_disabled)

        self.api.metric_delete(name)

    def test_metric_create_multiple_batch(self):
        new_metrics = []
        name1 = 'TEST_CREATE_BATCH_ONE_FOOBAR' + TestUtils.random_string(6)
        name2 = 'TEST_CREATE_BATCH_TWO_FOOBAR' + TestUtils.random_string(6)
        name3 = 'TEST_CREATE_BATCH_THREE_FOOBAR' + TestUtils.random_string(6)
        name4 = 'TEST_CREATE_BATCH_FOUR_FOOBAR' + TestUtils.random_string(6)

        display_name1 = 'TEST_DISPLAY_NAME' + TestUtils.random_string(6)
        display_name2 = 'TEST_DISPLAY_NAME' + TestUtils.random_string(6)
        display_name3 = 'TEST_DISPLAY_NAME' + TestUtils.random_string(6)
        display_name4 = 'TEST_DISPLAY_NAME' + TestUtils.random_string(6)

        display_name_short1 = 'TEST_SHORT' + TestUtils.random_string(10)
        display_name_short2 = 'TEST_SHORT' + TestUtils.random_string(10)
        display_name_short3 = 'TEST_SHORT' + TestUtils.random_string(10)
        display_name_short4 = 'TEST_SHORT' + TestUtils.random_string(10)

        description1 = TestUtils.random_string(32)
        description2 = TestUtils.random_string(32)
        description3 = TestUtils.random_string(32)
        description4 = TestUtils.random_string(32)

        default_aggregate1 = 'avg'
        default_aggregate2 = 'min'
        default_aggregate3 = 'max'
        default_aggregate4 = 'sum'

        default_resolution1 = random.randrange(1000, 60000)
        default_resolution2 = random.randrange(1000, 60000)
        default_resolution3 = random.randrange(1000, 60000)
        default_resolution4 = random.randrange(1000, 60000)

        unit1= 'bytecount'
        unit2= 'duration'
        unit3= 'number'
        unit4= 'percent'

        is_disabled1 = True
        is_disabled2 = False
        is_disabled3 = True
        is_disabled4 = False

        _type1 = TestUtils.random_string(6)
        _type2 = TestUtils.random_string(6)
        _type3 = TestUtils.random_string(6)
        _type4 = TestUtils.random_string(6)

        new_metrics.append(Metric(name=name1,
                                  display_name=display_name1,
                                  display_name_short=display_name_short1,
                                  description=description1,
                                  default_aggregate=default_aggregate1,
                                  default_resolution=default_resolution1,
                                  unit=unit1,
                                  _type=_type1,
                                  is_disabled=is_disabled1))
        new_metrics.append(Metric(name=name2,
                                  display_name=display_name2,
                                  display_name_short=display_name_short2,
                                  description=description2,
                                  default_aggregate=default_aggregate2,
                                  default_resolution=default_resolution2,
                                  unit=unit2,
                                  _type=_type2,
                                  is_disabled=is_disabled2))
        new_metrics.append(Metric(name=name3,
                                  display_name=display_name3,
                                  display_name_short=display_name_short3,
                                  description=description3,
                                  default_aggregate=default_aggregate3,
                                  default_resolution=default_resolution3,
                                  unit=unit3,
                                  _type=_type3,
                                  is_disabled=is_disabled3))

        new_metrics.append(Metric(name=name4,
                                  display_name=display_name4,
                                  display_name_short=display_name_short4,
                                  description=description4,
                                  default_aggregate=default_aggregate4,
                                  default_resolution=default_resolution4,
                                  unit=unit4,
                                  _type=_type4,
                                  is_disabled=is_disabled4))

        metrics = self.api.metric_create_batch(new_metrics)

        metric = metrics[0]

        self.assertEqual(name1, metrics[0].name)
        self.assertEqual(display_name1, metrics[0].display_name)
        self.assertEqual(display_name_short1, metrics[0].display_name_short)
        self.assertEqual(description1, metrics[0].description)
        self.assertEqual(default_aggregate1.upper(), metrics[0].default_aggregate)
        self.assertEqual(default_resolution1, metrics[0].default_resolution)
        self.assertEqual(unit1, metrics[0].unit)
        self.assertEqual(_type1, metrics[0].type)
        self.assertEqual(is_disabled1, metrics[0].is_disabled)

        for m in metrics:
            self.api.metric_delete(m.name)

    def test_metric_get(self):
        name = 'TEST_GET_FOOBAR' + TestUtils.random_string(6)
        metrics = self.api.metric_get()
        self.assertIsNotNone(metrics)

    def test_metric_delete(self):
        name = 'TEST_DELETE_FOOBAR' + TestUtils.random_string(6)
        self.api.metric_create(name=name)
        self.api.metric_delete(name)

    def test_metric_update(self):
        name = 'TEST_UPDATE_' + TestUtils.random_string(6)
        self.api.metric_create(name=name)
