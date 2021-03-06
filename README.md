BMC TrueSight Pulse API for Python
==================================

TrueSight Pulse API for Python provides bindings for the python language

Visit [http://boundary.github.io/pulse-api-python](http://boundary.github.io/pulse-api-python) for documentation.


[![Build Status](https://travis-ci.org/boundary/pulse-api-python.svg?branch=master)](https://travis-ci.org/boundary/pulse-api-python)
[![PyPI Version](http://img.shields.io/pypi/v/tspapi.svg)](https://pypi.python.org/pypi/tspapi)
[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg?maxAge=2592000)]()


© Copyright 2005-2016 BMC Software, Inc. Use of this software signifies your acceptance of BMC's Terms of Use, Privacy Policy and Cookie Notice. BMC, BMC Software, the BMC logos, and other BMC marks are trademarks or registered trademarks of BMC Software, Inc. in the U.S. and/or certain other countries.

## Installing

```
$ pip install tspapi
```

## Examples

### Create a Metric

```
import tspapi
from datetime import datetime

# The following assumes the following environment variables are set
# export TSP_EMAIL='joe@example.com'
# export TSP_API_TOKEN=<your api token>
api = tspapi.API()

api.measurement_create(metric='MY_METRIC', source='MySource', value=3.14, timestamp=datetime.now())
```

### Create a Measurement

```
import tspapi

# The following assumes the following environment variables are set
# export TSP_EMAIL='joe@example.com'
# export TSP_API_TOKEN=<your api token>
api = tspapi.API()

metric = api.measurement_create(metric='MY_METRIC', source='MySource', value=3.14)
```

