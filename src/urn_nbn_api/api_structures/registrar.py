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

    def __eq__(self, other):
        core = self.uid == other.uid and self.code == other.code

        rest = True
        if self.name and other.name:
            rest = rest and self.name == other.name

        if self.description and other.description:
            rest = rest and self.description == other.description

        if self.created and other.created:
            rest = rest and self.created == other.created

        if self.modified and other.modified:
            rest = rest and self.modified == other.modified

        if self.modes and other.modes:
            rest = rest and self.modes == other.modes

        return all([
            core,
            rest,
            set(self.catalogs) == set(other.catalogs),
            set(self.digital_libraries) == set(other.digital_libraries)
        ])
