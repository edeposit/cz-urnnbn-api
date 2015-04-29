#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from modes import Modes


# Functions & classes =========================================================
class Registrar(object):
    def __init__(self, code, uid, name=None, description=None, created=None,
                 modified=None, modes=None):
        self.uid = uid
        self.code = code
        self.name = name
        self.created = created
        self.modified = modified
        self.description = description

        self.modes = modes if modes else Modes()
        self.catalogs = []
        self.digital_libraries = []

    def __repr__(self):
        return "%s:%s" % (self.__class__.__name__, self.code)
