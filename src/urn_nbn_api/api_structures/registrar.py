#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from modes import Modes


# Functions & classes =========================================================
def _both_set_and_different(first, second):
    if first is None:
        return False

    if second is None:
        return False

    return first != second


class Registrar(object):
    def __init__(self, code, uid, name=None, description=None, created=None,
                 modified=None, modes=None):
        self.uid = uid
        self.code = code
        self.name = name
        self.created = created
        self.modified = modified
        self.description = description

        self.modes = modes
        self.catalogs = []
        self.digital_libraries = []

    def __repr__(self):
        return "%s:%s" % (self.__class__.__name__, self.code)

    def __eq__(self, other):
        if not (self.uid == other.uid and self.code == other.code):
            return False

        not_important_checks = any([
            _both_set_and_different(self.name, other.name),
            _both_set_and_different(self.description, other.description),
            _both_set_and_different(self.created, other.created),
            _both_set_and_different(self.modified, other.modified),
            _both_set_and_different(self.modes, other.modes),
        ])

        if not_important_checks:
            return False

        return all([
            set(self.catalogs) == set(other.catalogs),
            set(self.digital_libraries) == set(other.digital_libraries)
        ])

    def __ne__(self, other):
        return not self.__eq__(other)
