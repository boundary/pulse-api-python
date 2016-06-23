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
from datetime import datetime


class ApiTest(TestCase):

    def test_parse_timestamp_date_string_yymmddhhmm(self):
        s = '2016-01-27 3:38AM'
        d = API._parse_time_date(s)
        self.assertEqual(type(d), int)
        self.assertEqual(d, 1453894680)

    def test_parse_timestamp_date_string_yymmddhhmmss(self):
        s = '2016-01-27 3:38:25AM'
        d = API._parse_time_date(s)
        self.assertEqual(type(d), int)
        self.assertEqual(d, 1453894705)

    def test_parse_timestamp_date_string_yymmddHHMM(self):
        s = '2003-08-16 20:06:01'
        d = API._parse_time_date(s)
        self.assertEqual(type(d), int)
        self.assertEqual(d, 1061089561)

    def test_parse_timestamp_date_string_yymmddHHMMSS(self):
        s = '2001-03-27 19:07:32'
        d = API._parse_time_date(s)
        self.assertEqual(type(d), int)
        self.assertEqual(d, 985748852)

    def test_parse_timestamp_date_string_epoch_time(self):
        s = '1466704787'
        d = API._parse_time_date(s)
        self.assertEqual(type(d), int)
        self.assertEqual(d, 1466704787)

