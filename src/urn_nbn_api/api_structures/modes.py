#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class Modes(object):
    def __init__(self, by_resolver=False, by_registrar=False,
                 by_reservation=False):
        self.by_resolver = by_resolver
        self.by_registrar = by_registrar
        self.by_reservation = by_reservation

    def __eq__(self, other):
        return all([
            self.by_resolver == other.by_resolver,
            self.by_registrar == other.by_registrar,
            self.by_reservation == other.by_reservation,
        ])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Modes(%r%r%r)" % (
            self.by_resolver,
            self.by_registrar,
            self.by_reservation
        )
