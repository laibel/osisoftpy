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
osisoftpy.tests.test_point_insert.py
~~~~~~~~~~~~

Tests for the update_value and update_values functions 
in the`osisoftpy.point` module.
"""
import osisoftpy
import pytest
import time
import pytz
from osisoftpy.exceptions import MismatchEntriesError
from datetime import datetime

# TODO Convert timestamps to UTC

def _compare_pi_and_local_datetime(pidatetime, localdatetime):
    pi = datetime.strptime(pidatetime, '%Y-%m-%dT%H:%M:%SZ')
    local = datetime.strptime(localdatetime, '%Y-%m-%d %H:%M')
    localtimezone = pytz.timezone('America/Los_Angeles')
    localmoment = localtimezone.localize(local, is_dst=None)
    utcmoment = localmoment.astimezone(pytz.utc)
    # print(utcmoment.strftime('%Y-%m-%d %H:%M'))
    # print(pi.strftime('%Y-%m-%d %H:%M'))
    assert utcmoment.strftime('%Y-%m-%d %H:%M') == pi.strftime('%Y-%m-%d %H:%M')

# Testing values
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00', '2017-03-05 15:00', '2017-04-15 17:00'])
@pytest.mark.parametrize('value', [2017, 6, 549])
def test_point_update_value_single(webapi, query, timestamp, value):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        points.pop(0)
        point.update_value(timestamp, value)
        v = point.recordedattime(time=timestamp)
        assert v.value == value
        _compare_pi_and_local_datetime(v.timestamp, timestamp)
        
# Testing "good"
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('good', [True, False])
def test_point_update_good_flag(webapi, query, timestamp, value, good):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, value, good=good)
        p = point.recordedattime(time=timestamp)
        assert p.good == good

# Testing "questionable"
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('questionable', [True, False])
def test_point_update_questionable_flag(webapi, query, timestamp, value, questionable):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, value, questionable=questionable)
        p = point.recordedattime(time=timestamp)
        assert p.questionable == questionable


# Testing "unitsabbreviation"
@pytest.mark.skipif(True, reason="units of measure aren't being written")
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('unitsabbreviation', ['m', 's', 'm/s', 'A', 'K'])
def test_point_update_unitsabbreviation(webapi, query, timestamp, value, unitsabbreviation):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, value, unitsabbreviation=unitsabbreviation)
        p = point.recordedattime(time=timestamp)
        assert p.unitsabbreviation == unitsabbreviation

# Testing "updateoption" Replace
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('updateoption', ['Replace'])
def test_point_update_updatereplace(webapi, query, timestamp, value, updateoption):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        point.update_value(timestamp, value, updateoption=updateoption)
        p = point.recordedattime(time=timestamp)
        assert p.value == value

# Testing "updateoption" Insert
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('updateoption', ['Insert'])
def test_point_update_updateinsert(webapi, query, timestamp, value, updateoption):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        point.update_value(timestamp, value, updateoption=updateoption)
        p = point.recordedattime(time=timestamp)
        assert p.value == value

# Testing "updateoption" NoReplace
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('updateoption', ['NoReplace'])
def test_point_update_updatenoreplace(webapi, query, timestamp, value, updateoption):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        point.update_value(timestamp, value, updateoption=updateoption)
        p = point.recordedattime(time=timestamp)
        assert p.value == 0

# Testing "updateoption" ReplaceOnly
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('updateoption', ['ReplaceOnly'])
def test_point_update_updatereplaceonly(webapi, query, timestamp, value, updateoption):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        point.update_value(timestamp, value, updateoption=updateoption)
        p = point.recordedattime(time=timestamp)
        assert p.value == 0

# Testing "updateoption" InsertNoCompression
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('updateoption', ['InsertNoCompression'])
def test_point_update_updateinsertnocomp(webapi, query, timestamp, value, updateoption):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        point.update_value(timestamp, value, updateoption=updateoption)
        p = point.recordedattime(time=timestamp)
        assert p.value == value

# Testing "updateoption" Remove
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('updateoption', ['Remove'])
def test_point_update_updateremove(webapi, query, timestamp, value, updateoption):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        point.update_value(timestamp, value, updateoption=updateoption)
        p = point.recordedattime(time=timestamp)
        assert p.value == 0

#update_values
# Test Multiple Inputs
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamps', [['2017-02-01 06:00','2017-02-01 07:00','2017-02-01 08:00','2017-02-01 09:00','2017-02-01 10:00']])
@pytest.mark.parametrize('values', [[2017,2018,2019,2020,2021]])
def test_point_multiple_update(webapi, query, timestamps, values):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    for point in points:
        point.update_values(timestamps, values)
        for timestamp, value in zip(timestamps, values):
            p = point.recordedattime(time=timestamp)
            assert p.value == value

# Test Mismatched arrays (Timestamps and Values)
@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamps', [['2017-02-01 06:00','2017-02-01 07:00','2017-02-01 08:00','2017-02-01 09:00','2017-02-01 10:00']])
@pytest.mark.parametrize('values', [[2017,2018,2019,2020]])
def test_point_multiple_mismatch(webapi, query, timestamps, values):
    points = webapi.points(query=query)
    assert(len(points) == 1)
    with pytest.raises(MismatchEntriesError) as err:
        for point in points:
            point.update_values(timestamps, values)
