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
import tspapi


class MeasurementTest(TestCase):

    def setUp(self):
        self.api = tspapi.API()

    def test_measurement_create(self):
        metric_id = 'CPU'
        value = 0.75
        source = 'API_TEST_SOURCE'
        timestamp = datetime.now().strftime('%s')
        self.api.measurement_create(metric_id, value, source, timestamp)

