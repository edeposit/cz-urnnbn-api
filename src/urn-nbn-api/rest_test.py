#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import attribute_wrapper
import requests
import json


# Variables ===================================================================



# Functions & classes =========================================================
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


# Main program ================================================================
if __name__ == '__main__':
    w = HTTPWrapper("https://resolver.nkp.cz/api/v3")

    import code
    code.interact(None, None, locals())