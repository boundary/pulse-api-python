#!/usr/bin/env python
#
# Copyright 2015 BMC Software, Inc.
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
from datetime import datetime
from tspapi import API
from tspapi import Measurement
from tspapi.measurement import serialize_instance
import json
from datetime import datetime


class MeasurementTest(TestCase):

    def setUp(self):
        self.api = API()

    def test_measurement_constructor(self):
        metric = 'CPU'
        value = 0.5
        source = 'foobar'
        timestamp=int(datetime.now().strftime('%s'))
        measurement = Measurement(metric=metric, value=value, source=source, timestamp=timestamp)

        self.assertEqual(metric, measurement.metric)
        self.assertEqual(value, measurement.value)
        self.assertEqual(source, measurement.source)
        self.assertEqual(timestamp, measurement.timestamp)

    def test_measurement_defaults(self):
        measurement = Measurement()

        self.assertIsNone(measurement.metric)
        self.assertIsNone(measurement.value)
        self.assertIsNone(measurement.source)
        self.assertIsNone(measurement.value)

    def test_measurement_create(self):
        metric_id = 'CPU'
        value = 0.75
        source = 'API_TEST_SOURCE'
        timestamp = datetime.now().strftime('%s')
        self.api.measurement_create(metric_id, value, source, timestamp)

    def test_measurement_create_batch(self):
        measurements = []
        timestamp = int(datetime.now().strftime('%s'))
        measurements.append(Measurement(metric='CPU', value=0.5, source='red', timestamp=timestamp))
        measurements.append(Measurement(metric='CPU', value=0.6, source='green', timestamp=timestamp))
        measurements.append(Measurement(metric='CPU', value=0.7, source='blue', timestamp=timestamp))
        self.api.measurement_create_batch(measurements)


