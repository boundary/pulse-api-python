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
import tspapi


class AggregateTest(TestCase):

    def test_avg(self):
        self.assertEqual('AVG', tspapi.aggregates.AVG)

    def test_min(self):
        self.assertEqual('MIN', tspapi.aggregates.MIN)

    def test_max(self):
        self.assertEqual('MAX', tspapi.aggregates.MAX)

    def test_sum(self):
        self.assertEqual('SUM', tspapi.aggregates.SUM)
