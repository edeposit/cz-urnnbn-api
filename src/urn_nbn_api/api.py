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

from api_structures.registrar import Modes
from api_structures.registrar import Catalog
from api_structures.registrar import Registrar
from api_structures.registrar import DigitalLibrary


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


def _by_attr(xdom, attr):
    out = []

    for tag in xdom:
        for attr_name, val in attr.iteritems():
            if attr_name not in tag:
                break

            if val is not None and tag[attr_name] != val:
                break

            out.append(tag)

    return out[0] if len(out) == 1 else out


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


def _parse_registrar(reg_tag):
    # parse modes
    modes_tag = reg_tag["registrationModes"]["mode"]

    by_resolver = _by_attr(modes_tag, attr={"@name": "BY_RESOLVER"})
    by_registrar = _by_attr(modes_tag, attr={"@name": "BY_REGISTRAR"})
    by_reservation = _by_attr(modes_tag, attr={"@name": "BY_RESERVATION"})

    modes = Modes(
        by_resolver=by_resolver["@enabled"],
        by_registrar=by_registrar["@enabled"],
        by_reservation=by_reservation["@enabled"],
    )

    # parse Registrar data
    return Registrar(
        code=reg_tag["@code"],
        uid=reg_tag["@id"],
        name=reg_tag["name"],
        description=reg_tag.get("description", None),
        created=reg_tag["created"],
        modified=reg_tag.get("modified", None),
        modes=modes
    )


def iter_registrars():
    data = _send_request(
        method="GET",
        url=urljoin(settings.URL, "registrars")
    )

    xdom = xmltodict.parse(data)

    for registrar_tag in xdom["response"]["registrars"]["registrar"]:
        yield _parse_registrar(registrar_tag)


def _to_list(tag):
    if isinstance(tag, tuple) or isinstance(tag, list):
        return tag

    return [tag]


def get_registrar_info(reg_code):
    data = _send_request(
        method="GET",
        url=urljoin(settings.REG_URL, reg_code)
    )

    xdom = xmltodict.parse(data)
    reg_tag = xdom["response"]["registrar"]

    registrar = _parse_registrar(reg_tag)

    if not reg_tag.get("digitalLibraries", None):
        return registrar

    # parse digital_libraries
    for dl_tag in _to_list(reg_tag["digitalLibraries"]["digitalLibrary"]):
        registrar.digital_libraries.append(
            DigitalLibrary(
                uid=dl_tag["@id"],
                name=dl_tag["name"],
                description=dl_tag.get("description", None),
                url=dl_tag.get("url", None),
                created=dl_tag.get("created", None),
            )
        )

    if not reg_tag.get("catalogs", None):
        return registrar

    # parse catalogs
    for catalog_tag in _to_list(reg_tag["catalogs"]["catalog"]):
        registrar.catalogs.append(
            Catalog(
                uid=catalog_tag["@id"],
                name=catalog_tag["name"],
                url_prefix=catalog_tag.get("urlPrefix", None),
                created=catalog_tag.get("created", None),
            )
        )

    return registrar


def register_document(xml, reg_code=settings.REG_CODE):
    return _send_request(
        method="POST",
        url=urljoin(settings.URL, "registrars/%s/digitalDocuments") % reg_code,
        data=xml
    )

    # TODO: parsování vrácených dat, vrácení URN:NBN kódu



# TODO: kód na přehled ohlášených epublikací

print get_registrar_info("boa001")
print get_registrar_info("boa001").digital_libraries