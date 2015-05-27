#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from tools import both_set_and_different


# Functions & classes =========================================================
class DigitalLibrary(object):
    """
    Container used to hold informations about given digital library, where the
    document to which the URN:NBN points, stored.

    Attributes:
        url (str): URL of the library.
        uid (str): ID of the library.
        name (str): Name of the digital library.
        created (str): ISO 8601 string.
        description (str): Free text description of the library.
    """
    def __init__(self, uid, name, description=None, url=None, created=None):
        self.url = url
        self.uid = uid
        self.name = name
        self.created = created
        self.description = description

    def __eq__(self, other):
        if self.uid != other.uid or self.name != other.name:
            return False

        return not any([
            both_set_and_different(self.description, other.description),
            both_set_and_different(self.url, other.url),
            both_set_and_different(self.created, other.created),
        ])

    def __ne__(self, other):
        return not self.__eq__(other)
