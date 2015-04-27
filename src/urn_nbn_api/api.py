#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from urlparse import urljoin

import requests
import xmltodict
import dhtmlparser

import settings

from api_structures.registrar import Registrar


# Functions & classes =========================================================
def _get_content_or_str(tag):
    if not tag:
        return ""

    if isinstance(tag, list) or isinstance(tag, tuple):
        tag = tag[0]

    return tag.getContent()


def _send_request(method, url, data=None, params=None):
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


# API =========================================================================
def is_valid_reg_code(reg_code=settings.REG_CODE):
    """
    Check whether `reg_code` is valid registration code.

    Args:
        reg_code (str): Producent's registration code.

    Returns:
        bool: True, if the `reg_code` is valid.
    """
    try:
        return _send_request(
            method="GET",
            url=urljoin(settings.REG_URL, reg_code),
        )
    except (requests.exceptions.HTTPError, ValueError):
        return False

    return True


def get_list_of_registrars():
    data = _send_request(
        method="GET",
        url=urljoin(settings.URL, "registrars")
    )

    xdom = xmltodict.parse(data)

    for registrar_tag in xdom["response"]["registrars"]["registrar"]:
        print registrar_tag
        print registrar_tag["@code"]
        print registrar_tag["@id"]
        print registrar_tag["name"]
        print registrar_tag.get("description", None)
        print registrar_tag["created"]
        print registrar_tag.get("modified", None)

        print registrar_tag["registrationModes"]["@name=BY_RESOLVER"]
        print registrar_tag["registrationModes"]["@name=BY_REGISTRAR"]
        print registrar_tag["registrationModes"]["@name=BY_RESERVATION"]
        print



def get_registrator_info(reg_code):
    pass


def register_document(xml, reg_code=settings.REG_CODE):
    return _send_request(
        method="POST",
        url=urljoin(settings.URL, "registrars/%s/digitalDocuments") % reg_code,
        data=xml
    )

    # TODO: parsování vrácených dat, vrácení URN:NBN kódu



# TODO: kód na přehled ohlášených epublikací

print get_list_of_registrars()