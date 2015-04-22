#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from urlparse import urljoin

import requests
import dhtmlparser

import settings


# Variables ===================================================================
def _get_content_or_str(tag):
    if not tag:
        return ""

    if isinstance(tag, list) or isinstance(tag, tuple):
        tag = tag[0]

    return tag.getContent()


def send_request(method, url, data=None, params=None):
    resp = requests.request(
        method,
        url,
        data=data,
        params=params,
        verify=False,  # TODO: remove?
        headers={'Content-type': 'application/xml'},
        auth=(settings.USERNAME, settings.PASSWORD)
    )

    # handle http errors
    try:
        if resp.status_code not in [200, 400]:
            resp.raise_for_status()
    except requests.HTTPError, e:
        raise requests.HTTPError(e.message + "\n" + resp.content)

    # handle API errors
    dom = dhtmlparser.parseString(resp.content)
    if dom.find("error"):
        errors = [
            _get_content_or_str(error.find("code")) + " " +
            _get_content_or_str(error.find("message"))
            for error in dom.find("error")
        ]

        raise ValueError("\n".join(errors))

    return resp.text


# Functions & classes =========================================================
def is_valid_reg_code(reg_code=settings.REG_CODE):
    """
    Returns True, if the registration code defined in :attr:`settings.REG_CODE`
    is valid registration code.
    """
    try:
        return send_request(
            method="GET",
            url=urljoin(settings.REG_URL, reg_code),
        )
    except (requests.exceptions.HTTPError, ValueError):
        return False

    return True


def register(xml, reg_code=settings.REG_CODE):
    return send_request(
        method="POST",
        url=urljoin(settings.URL, "registrars/%s/digitalDocuments") % reg_code,
        data=xml
    )
