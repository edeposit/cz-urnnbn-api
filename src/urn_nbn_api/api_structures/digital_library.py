#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class DigitalLibrary(object):
    def __init__(self, uid, name, description=None, url=None, created=None):
        self.url = url
        self.uid = uid
        self.name = name
        self.created = created
        self.description = description
