# -*- coding: utf-8 -*-

#    Copyright 2017 DST Controls
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
osisoftpy.tests.test_int_api.py
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""
import pytest
import requests

import osisoftpy
from osisoftpy.webapi import PIWebAPI

test = type('Test', (object,), {})()
test.url = 'https://sbb03.eecs.berkeley.edu/piwebapi'
test.authtype = 'basic'
test.username = 'albertxu'
test.password = 'Welcome2pi'


def test_get_webapi_returns_PIWebAPI_object():
    webapi = osisoftpy.webapi(test.url, authtype=test.authtype,
                              username=test.username,
                              password=test.password)
    assert type(webapi) == PIWebAPI

def test_PIWebAPI_for_self_url():
    webapi = osisoftpy.webapi(test.url, authtype=test.authtype,
                              username=test.username,
                              password=test.password)
    print(', '.join("%s: %s" % item for item in vars(webapi).items()))
    assert webapi.url == test.url + '/'