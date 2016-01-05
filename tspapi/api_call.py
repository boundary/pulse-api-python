#
# Copyright 2015 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import requests
import urllib
import logging


def _handle_api_results(api_result):
    result = None
    # Only process if we get HTTP result of 200
    if api_result.status_code == requests.codes.ok:
        result = json.loads(api_result.text)
        return result


class ApiCall(object):
    def __init__(self, api_host=None, email=None, api_token=None):
        """
        :param api_host: api end point host
        :param email: TrueSight Pulse account e-mail
        :param api_token: TrueSight Pulse api token
        :return: returns nothing

        :Example:

        from boundary import API

        api = API(email="foo@bary.com", api_token="api.xxxxxxxxxx-yyyy"
        """
        self._kwargs = None
        self._methods = {"DELETE": self._do_delete,
                         "GET": self._do_get,
                         "POST": self._do_post,
                         "PUT": self._do_put}

        self._api_host = api_host
        self._email = email
        self._api_token = api_token

        # All member variables related to REST CALL
        self._scheme = "https"
        self._method = "GET"
        self._headers = None
        self._data = None
        self._url = None
        self._path = None
        self._url_parameters = None

        self._api_result = None

        # Set the api_host, email, api token set by environment
        # variables then override with those passed in
        self._get_environment()
        if api_host is not None:
            self._api_host = api_host
        if email is not None:
            self._email = email
        if api_token is not None:
            self._api_token = api_token

    def _get_environment(self):
        pass

    #
    # data
    #

    @property
    def data(self):
        """
        Value of the HTTP payload
        :return:
        """
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    #
    # headers
    #

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers
    #
    # method
    #

    @property
    def method(self):
        """
        """
        return self._method

    @method.setter
    def method(self, value):
        """
        Before assigning the value validate that is in one of the
        HTTP methods we implement
        """
        keys = self._methods.keys()
        if value not in keys:
            raise AttributeError("Method value not in " + str(keys))
        else:
            self._method = value

    #
    # path
    #

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    #
    # url_parameters
    #

    @property
    def url_parameters(self):
        return self._url_parameters

    @url_parameters.setter
    def url_parameters(self, url_parameters):
        self._url_parameters = url_parameters

    def _get_url_parameters(self):
        """
        Encode URL parameters
        """
        url_parameters = ''
        if self._url_parameters is not None:
            url_parameters = '?' + urllib.urlencode(self._url_parameters)
        return url_parameters

    def _do_get(self):
        """
        HTTP Get Request
        """
        return requests.get(self._url, data=self._data, headers=self._headers, auth=(self._email, self._api_token))

    def _do_delete(self):
        """
        HTTP Delete Request
        """
        return requests.delete(self._url, data=self._data, headers=self._headers, auth=(self._email, self._api_token))

    def _do_post(self):
        """
        HTTP Post Request
        """
        return requests.post(self._url, data=self._data, headers=self._headers, auth=(self._email, self._api_token))

    def _do_put(self):
        """
        HTTP Put Request
        """
        return requests.put(self._url, data=self._data, headers=self._headers, auth=(self._email, self._api_token))

    def good_response(self, status_code):
        """
        Determines what status codes represent a good response from an API call.
        """
        return status_code == requests.codes.ok

    def form_url(self):
        return "{0}://{1}/{2}{3}".format(self._scheme, self._api_host, self._path, self._get_url_parameters())

    def _call_api(self):
        """
        Make an API call to get the metric definition
        """

        self._url = self.form_url()
        if self._headers is not None:
            logging.debug(self._headers)
        if self._data is not None:
            logging.debug(self._data)
        if len(self._get_url_parameters()) > 0:
            logging.debug(self._get_url_parameters())

        result = self._methods[self._method]()

        if not self.good_response(result.status_code):
            logging.error(self._url)
            logging.error(self._method)
            logging.error(self._headers)
            if self._data is not None:
                logging.error(self._data)
            logging.error(result)
        self._api_result = result

    def api_call(self, handle_results=_handle_api_results):
        self._call_api()
        return handle_results(self._api_result)
