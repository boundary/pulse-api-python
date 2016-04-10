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


class UnitTest(TestCase):

    def test_bytecount(self):
        self.assertEqual('bytecount', tspapi.units.bytecount)

    def test_duration(self):
        self.assertEqual('duration', tspapi.units.duration)

    def test_number(self):
        self.assertEqual('number', tspapi.units.number)

    def test_percent(self):
        self.assertEqual('percent', tspapi.units.percent)
