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
osisoftpy.structures
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""

import collections
from osisoftpy.internal import wrapt_handle_exceptions


class Points(list):

    @wrapt_handle_exceptions
    def current(self, time=None):
        """
        Returns the value of the stream at the specified time. By default, 
        this is usually the current value. 

        :param time: An optional time. The default time context is 
            determined from the owning object - for example, the time range of 
            the event frame or transfer which holds this attribute. Otherwise, 
            the implementation of the Data Reference determines the meaning of 
            no context. For Points or simply configured PI Point Data 
            References, this means the snapshot value of the PI Point on the 
            Data Server.
        :return: :class:`OSIsoftPy <osisoftpy.Point>` object
        :rtype: osisoftpy.Point
        """
        payload = {'time': time}
        return self._get_value(payload=payload, endpoint='value')


class TypedList(collections.MutableSequence):
    """A ``list``-like object with one or more specified Type(s)
    
    Implements all methods and operations of
    ``collections.MutableSequence`` as well as dict's ``copy``. Also
    provides for Type validation against provided Type(s) ``lower_items``.
    
    """

    def __init__(self, validtypes, *args):
        # type: (any, *str) -> None
        """

        :rtype: list
        :param validtypes: Provide a type for this TypedList object
        :param args: 
        """
        self.validtypes = validtypes
        self.list = list()
        self.extend(list(args))

    def validate_type(self, value):
        if not isinstance(value, self.validtypes):
            raise TypeError('The object "{}" is not of type "{}"'.format(
                value, self.validtypes))

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, value):
        self.validate_type(value)
        self.list[key] = value

    def __delitem__(self, key):
        del self.list[key]

    def __len__(self):
        return len(self.list)

    def insert(self, key, value):
        self.validate_type(value)
        self.list.insert(key, value)

    def __str__(self):
        return str(self.list)