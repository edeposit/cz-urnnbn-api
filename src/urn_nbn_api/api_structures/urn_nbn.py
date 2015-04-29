#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class URN_NBN(str):
    def __new__(self, value, *args, **kwargs):
        return super(URN_NBN, self).__new__(self, value)

    def __init__(self, value, status=None, country_code=None,
                 registrar_code=None, document_code=None,
                 digital_document_id=None, registered=None):
        self.value = value

        super(URN_NBN, self).__init__(value)

        self.status = status
        self.registered = registered
        self.country_code = country_code
        self.document_code = document_code
        self.registrar_code = registrar_code
        self.digital_document_id = digital_document_id

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
