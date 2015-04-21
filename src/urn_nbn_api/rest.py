#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from urlparse import urljoin

import attribute_wrapper
import requests
import json

import settings


# Variables ===================================================================
class HTTPWrapper(attribute_wrapper.GenericWrapper):
    """
    Example of :class:`GenericWrapper`, which translates all calls and given
    data to HTTP form parameters.
    """
    def download_handler(self, method, url, data):
        resp = requests.request(method, url, params=data, verify=False)

        # handle http errors
        resp.raise_for_status()

        return resp.text


BASE_URL = "https://resolver-test.nkp.cz/api/v3/registrars"
REST_CLIENT = HTTPWrapper("%s/%s" % (BASE_URL, settings.REG_CODE))


# Functions & classes =========================================================
def valid_reg_code(reg_code=settings.REG_CODE):
    """
    Returns True, if the registration code defined in :attr:`settings.REG_CODE`
    is valid registration code.
    """
    reg_url = urljoin(settings.URL, "registrars/")
    try:
        HTTPWrapper(urljoin(reg_url, reg_code)).get()
    except requests.exceptions.HTTPError:
        return False

    return True


def register(xml):
    return REST_CLIENT.digitalDocuments.post(data=xml)
