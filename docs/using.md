Using
=====

The TrueSight Pulse API for Python is easy to use and obviates the need to understand REST and JSON.
Those already familar with Python will be generating new measurements into TrueSight Pulse in minutes.

## Installation

```bash
$ pip install tspapi
```

## Example

First import the Python package that contains the API

```python
import tspapi
```

Next allocate an instance of `API` class. The TrueSight Pulse APIs require an e-mail
and the API token associated with the account. Credentials can be added programmatically
as shown here:

```python
api = tspapi.API(email='joe@example.com', api_tokens='api.f8843b57e9-7482')
```

or omitted if you set the the `TSP_EMAIL` and `TSP_API_TOKEN` with e-mail and API token
respectively:

```python
api = tspapi.API()
```


Call the api in this example the creation


## Exceptions

