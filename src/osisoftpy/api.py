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
osisoftpy.api
~~~~~~~~~~~~
This module implements the OSIsoftPy API.
"""

import logging

from osisoftpy.internal import get
from osisoftpy.factory import Factory, create
from osisoftpy.webapi import WebAPI

log = logging.getLogger(__name__)


def webapi(url, **kwargs):
    try:
        return _get_webapi(url, **kwargs)
    except Exception as e:
        raise e


def response(url, **kwargs):
    try:
        return _get_response(url, **kwargs)
    except Exception as e:
        raise e


def _get_webapi(url, **kwargs):
    r = get(url, **kwargs)
    return create(Factory(WebAPI), r.response.json(), r.session)


def _get_response(url, **kwargs):
    r = get(url, **kwargs)
    return r.response
