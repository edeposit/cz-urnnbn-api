#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class Catalog(object):
    def __init__(self, uid, name, url_prefix, created):
        self.uid = uid
        self.name = name
        self.created = created
        self.url_prefix = url_prefix
