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
import tspapi
from datetime import datetime

# The following assumes the following environment variables are set
# export TSP_EMAIL='joe@example.com'
# export TSP_API_TOKEN=<your api token>
api = tspapi.API()

# Create a measurement and let the timestamp by sent by the API:
api.measurement_create(metric='MY_METRIC',
                       source='MySource',
                       value=3.14)

# Create a measurement and set the timestamp
api.measurement_create(metric='MY_METRIC',
                       source='MySource',
                       value=9.80665,
                       timestamp=datetime.now())

# Create a measurement with properties
properties = {"app_id": "myapp"}
api.measurement_create(metric='MY_METRIC',
                       source='MySource',
                       value=22.7,
                       timestamp=datetime.now(),
                       properties=properties)

