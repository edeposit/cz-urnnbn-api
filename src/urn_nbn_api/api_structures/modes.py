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
