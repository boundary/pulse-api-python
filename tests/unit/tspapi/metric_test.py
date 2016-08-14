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
import sys
import os

from unittest import TestCase
from tspapi import API
from tspapi import Metric
from tspapi import HTTPResponseError
from tspapi import aggregates
from tspapi import units
import tspapi.metric
import json
import random
import requests
import logging

_path = os.path.dirname(__file__)
sys.path.append(_path)
from api_test_utils import TestUtils


class MetricTest(TestCase):

    def setUp(self):
        self.api = API()
        logging.basicConfig(level=logging.DEBUG)
        self.name = 'TEST_' + TestUtils.random_string(6)
        self.display_name = 'green'
        self.display_name_short = 'blue'
        self.description = 'magenta'
        self.default_aggregate = aggregates.SUM
        self.default_resolution = 60000
        self.unit = units.DURATION
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

        self.api.metric_create_batch([self.metric])

        logging.basicConfig(level=logging.INFO)

    def tearDown(self):
        self.api.metric_delete(self.metric.name)

    def test_minimal_constructor(self):
        name = 'FOO'
        m = Metric(name=name)

        self.assertEqual(name, m.name)
        self.assertEqual(name, m.display_name)
        self.assertEqual(name, m.display_name_short)
        self.assertEqual('', m.description)
        self.assertEqual(m.default_aggregate, aggregates.AVG)
        self.assertEqual(m.default_resolution, 1000)
        self.assertEqual(m.unit, units.NUMBER)
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
        expected = ["Metric(name='{0}', display_name='green', display_name_short='blue',".format(self.metric.name),
                    " description='magenta', default_aggregate='sum', default_resolution=60000,",
                    " unit='duration', _type='FOOBAR', is_disabled='False')"]
        self.assertEqual("".join(expected), self.metric.__repr__())

    def test_metric_to_json(self):
        m = Metric(name="TEST")
        data = json.dumps(m, sort_keys=True, default=tspapi.metric.serialize_instance)
        s = ['{"defaultAggregate": "avg", "defaultResolutionMS": 1000, "description": "",',
             ' "displayName": "TEST", "displayNameShort": "TEST", "isDisabled": false, "name": "TEST",',
             ' "unit": "number"}']
        expected = "".join(s)
        self.assertEqual(expected, data)

    def test_metric_list_to_json(self):
        l = [Metric(name="ONE"), Metric(name="TWO")]
        self.maxDiff = None
        s = ['[{"defaultAggregate": "avg", "defaultResolutionMS": 1000, "description": "", "displayName": "ONE",',
             ' "displayNameShort": "ONE", "isDisabled": false, "name": "ONE",',
             ' "unit": "number"},',
             ' {"defaultAggregate": "avg", "defaultResolutionMS": 1000, "description": "", "displayName": "TWO",',
             ' "displayNameShort": "TWO", "isDisabled": false, "name": "TWO",',
             ' "unit": "number"}]']
        expected = "".join(s)

        data = json.dumps(l, sort_keys=True, default=tspapi.metric.serialize_instance)
        self.assertEqual(expected, data)

    def test_metric_instance_empty_name(self):
        """
        Ensure that creating a metric with an empty name throws a
        ValueError exception
        :return:
        """
        try:
            m = Metric()
            print(m)
            self.assertTrue(False)
        except ValueError:
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
        except ValueError:
            pass

    def test_metric_create(self):
        name = "TEST_CREATE_FOOBAR" + TestUtils.random_string(6)
        display_name = "TEST_METRIC_CREATE" + TestUtils.random_string(6)
        display_name_short = "TEST_METRIC" + TestUtils.random_string(6)
        description = TestUtils.random_string(32)
        default_aggregate = aggregates.AVG
        default_resolution = 60000
        unit = units.DURATION
        _type = 'FOO'
        is_disabled = True
        metric = self.api.metric_create(name=name,
                                        display_name=display_name,
                                        display_name_short=display_name_short,
                                        description=description,
                                        default_aggregate=default_aggregate,
                                        default_resolution=default_resolution,
                                        unit=unit,
                                        _type=_type,
                                        is_disabled=is_disabled)
        self.assertEqual(name, metric.name)
        self.assertEqual(display_name, metric.display_name)
        self.assertEqual(display_name_short, metric.display_name_short)
        self.assertEqual(description, metric.description)
        self.assertEqual(default_aggregate.upper(), metric.default_aggregate)
        self.assertEqual(default_resolution, metric.default_resolution)
        self.assertEqual(unit, metric.unit)
        self.assertEqual(_type, metric.type)
        self.assertEqual(is_disabled, metric.is_disabled)

    def test_metric_create_one_batch(self):
        name = 'TEST_CREATE_BATCH_ONE_FOOBAR' + TestUtils.random_string(6)
        display_name = "BATCH" + TestUtils.random_string(6)
        display_name_short = "BATCH" + TestUtils.random_string(3)
        description = TestUtils.random_string(32)
        default_aggregate = aggregates.SUM
        default_resolution = random.randrange(1000, 60000)
        unit = units.PERCENT
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
        self.assertEqual(len(metrics), 1)

        m = metrics[0]
        self.assertEqual(name, m.name)
        self.assertEqual(display_name, m.display_name)
        self.assertEqual(display_name_short, m.display_name_short)
        self.assertEqual(description, m.description)
        self.assertEqual(default_aggregate.upper(), m.default_aggregate)
        self.assertEqual(default_resolution, m.default_resolution)
        self.assertEqual(unit, m.unit)
        self.assertEqual(_type, m.type)
        self.assertEqual(is_disabled, m.is_disabled)

        self.api.metric_delete(name)

    def test_metric_large_display_name(self):
        """
        Test to see that we can handle a display name up to 1K characters
        :return:
        """
        try:
            name = 'TEST_CREATE' + TestUtils.random_string(6)
            display_name = TestUtils.random_string(1024*1024)
            metric = self.api.metric_create(name=name, display_name=display_name)
            self.assertTrue(True)
        except HTTPResponseError as e:
            self.assertEqual(requests.codes.request_entity_too_large, e.status_code)

    def test_metric_large_short_display_name(self):
        """
        Test on the limit of the short display name
        :return:
        """
        try:
            name = 'TEST_CREATE' + TestUtils.random_string(6)
            display_name_short = TestUtils.random_string(1024*1024)
            metric = self.api.metric_create(name=name, display_name_short=display_name_short)
            self.assertTrue(True)
        except HTTPResponseError as e:
            self.assertEqual(requests.codes.request_entity_too_large, e.status_code)

    def test_metric_bad_aggregate(self):
        try:
            name = 'TEST_CREATE' + TestUtils.random_string(6)
            display_name = TestUtils.random_string(32)
            metric = self.api.metric_create(name=name,
                                            display_name=display_name,
                                            default_aggregate='foo')
            self.assertTrue(False)
        except HTTPResponseError as e:
            self.assertEqual(requests.codes.unprocessable_entity, e.status_code)

    def test_metric_bad_unit(self):
        try:
            name = 'TEST_CREATE' + TestUtils.random_string(6)
            display_name = TestUtils.random_string(32)
            metric = self.api.metric_create(name=name,
                                            display_name=display_name,
                                            unit='foo')
            self.assertTrue(False)
        except HTTPResponseError as e:
            self.assertEqual(requests.codes.unprocessable_entity, e.status_code)

    def test_metric_create_multiple_batch(self):
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

        default_aggregate1 = aggregates.AVG
        default_aggregate2 = aggregates.MIN
        default_aggregate3 = aggregates.MAX
        default_aggregate4 = aggregates.SUM

        default_resolution1 = random.randrange(1000, 60000)
        default_resolution2 = random.randrange(1000, 60000)
        default_resolution3 = random.randrange(1000, 60000)
        default_resolution4 = random.randrange(1000, 60000)

        unit1 = units.BYTECOUNT
        unit2 = units.DURATION
        unit3 = units.NUMBER
        unit4 = units.PERCENT

        is_disabled1 = True
        is_disabled2 = False
        is_disabled3 = True
        is_disabled4 = False

        _type1 = TestUtils.random_string(6)
        _type2 = TestUtils.random_string(6)
        _type3 = TestUtils.random_string(6)
        _type4 = TestUtils.random_string(6)

        new_metrics = [Metric(name=name1,
                              display_name=display_name1,
                              display_name_short=display_name_short1,
                              description=description1,
                              default_aggregate=default_aggregate1,
                              default_resolution=default_resolution1,
                              unit=unit1,
                              _type=_type1,
                              is_disabled=is_disabled1),

                       Metric(name=name2,
                              display_name=display_name2,
                              display_name_short=display_name_short2,
                              description=description2,
                              default_aggregate=default_aggregate2,
                              default_resolution=default_resolution2,
                              unit=unit2,
                              _type=_type2,
                              is_disabled=is_disabled2),
                       Metric(name=name3,
                              display_name=display_name3,
                              display_name_short=display_name_short3,
                              description=description3,
                              default_aggregate=default_aggregate3,
                              default_resolution=default_resolution3,
                              unit=unit3,
                              _type=_type3,
                              is_disabled=is_disabled3),

                       Metric(name=name4,
                              display_name=display_name4,
                              display_name_short=display_name_short4,
                              description=description4,
                              default_aggregate=default_aggregate4,
                              default_resolution=default_resolution4,
                              unit=unit4,
                              _type=_type4,
                              is_disabled=is_disabled4)]

        metrics = self.api.metric_create_batch(new_metrics)

        self.assertEqual(4, len(metrics))

    def test_metric_create_batch_from_file(self):
        self.api.metric_create_batch(path="tests/unit/tspapi/metric_batch.json")

    def test_metric_get(self):
        metrics = self.api.metric_get()
        self.assertIsNotNone(metrics)

    def test_metric_delete(self):
        name = 'TEST_DELETE_FOOBAR' + TestUtils.random_string(6)
        self.api.metric_create(name=name)
        self.api.metric_delete(name)

    def test_metric_delete_no_name(self):
        try:
            self.api.metric_delete()
            self.assertTrue(False)
        except ValueError:
            pass

    def test_metric_delete_name_does_not_exist(self):
        try:
            self.api.metric_delete(TestUtils.random_string(10))
        except HTTPResponseError as e:
            self.assertEqual(requests.codes.unprocessable_entity, e.status_code)

    def test_metric_update(self):
        name = 'TEST_UPDATE_' + TestUtils.random_string(6)
        display_name = TestUtils.random_string(8)
        display_name_short = TestUtils.random_string(16)
        description = TestUtils.random_string(16)
        default_aggregate = aggregates.SUM
        default_resolution = 60000
        unit = units.PERCENT
        is_disabled = False
        _type = 'DEVICE'
        self.api.metric_create(name=name,
                               display_name=display_name,
                               display_name_short=display_name_short,
                               description=description,
                               default_aggregate=default_aggregate,
                               default_resolution=default_resolution,
                               unit=unit,
                               is_disabled=is_disabled,
                               _type=_type
                               )

        display_name = TestUtils.random_string(8)
        display_name_short = TestUtils.random_string(16)
        description = TestUtils.random_string(16)
        default_aggregate = aggregates.MAX
        default_resolution = 30000
        unit = units.DURATION
        is_disabled = True
        _type = 'HOST'
        metric = self.api.metric_update(name=name,
                                        display_name=display_name,
                                        display_name_short=display_name_short,
                                        description=description,
                                        default_aggregate=default_aggregate,
                                        default_resolution=default_resolution,
                                        unit=unit,
                                        is_disabled=is_disabled,
                                        _type=_type
                                        )

        self.assertEqual(name, metric.name)
        self.assertEqual(display_name, metric.display_name)
        self.assertEqual(display_name_short, metric.display_name_short)
        self.assertEqual(description, metric.description)
        self.assertEqual(default_aggregate.upper(), metric.default_aggregate)
        self.assertEqual(default_resolution, metric.default_resolution)
        self.assertEqual(unit, metric.unit)
        self.assertEqual(_type, metric.type)
        self.assertEqual(is_disabled, metric.is_disabled)

        self.api.metric_delete(name)

    def test_metric_batch_update(self):
        pass
