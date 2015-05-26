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
from xml_composer import MonographComposer

from api_structures import *  # this is here to simplify working with API

# those are actually used in this module
from api_structures import URN_NBN
from api_structures import Registrar
from api_structures import DigitalInstance


# Functions & classes =========================================================
def _send_request(method, url, data=None, params=None):
    """
    Send request with data to server.

    Args:
        method (str): HTTP method - GET/POST/..
        url (str): URL of the resource where you wish to send request.
        data (dict, default None): This will be sent in body of the request.
        params (dict, default None): This may be sent as parameters.

    Raises:
        ValueError: In case that ``<error>`` tag was detected in output.
        requests.HTTPError: In case of HTTP error.

    Returns:
        str: Data returned from server.
    """
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


def _get_content_or_str(tag, alt="", pick=lambda x: x[0]):
    """
    Get content of the `tag`, or return alternative defined by `alt`.

    In case that tag is instance of ``list`` or ``tuple``, `pick` function is
    applied.

    Args:
        tag (HTMLElement/list): Instance of HTMLElement or list.
        alt (obj, default ""): Alternative value for tag ``if not tag``.
        pick (fn, default lambda): Pick item from list of `tag`. Default lambda
             that picks first item.

    Return:
        str: Content of `tag`.
    """
    if not tag:
        return alt

    if isinstance(tag, list) or isinstance(tag, tuple):
        tag = pick(tag)

    return tag.getContent()


# API =========================================================================
def is_valid_reg_code(reg_code=settings.REG_CODE):
    """
    Check whether `reg_code` is valid registrar code.

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


def iter_registrars():
    """
    Iterate over all registrars.

    Yields:
        obj: :class:`.Registrar` instance with basic informations.
    """
    data = _send_request(
        method="GET",
        url=urljoin(settings.URL, "registrars")
    )

    xdom = xmltodict.parse(data)

    for registrar_tag in xdom["response"]["registrars"]["registrar"]:
        yield Registrar.from_xmldict(registrar_tag)


def get_registrar_info(reg_code):
    """
    Get detailed informations about registrar with `reg_code`.

    Args:
        reg_code (str): Code identifier of registrar.

    Returns:
        obj: :class:`.Registrar` instance with all informations.
    """
    data = _send_request(
        method="GET",
        url=urljoin(settings.REG_URL, reg_code)
    )

    xdom = xmltodict.parse(data)
    reg_tag = xdom["response"]["registrar"]

    return Registrar.from_xmldict(reg_tag)


def register_document_obj(xml_composer, reg_code=settings.REG_CODE):
    """
    Register document in mode ``BY_RESOLVER`` - let the resolver give you
    URN:NBN code.

    Args:
        xml_composer (obj): Instance of the :class:`MonographComposer`.
        reg_code (str, default settings.REG_CODE): Registrar's code.

    Returns:
        obj: Instance of :class:`.URN_NBN` which contains assinged URN:NBN \
             code.
    """
    msg = "`xml_composer` parameter have to by subclass of MonographComposer!"
    assert isinstance(xml_composer, MonographComposer), msg

    return register_document(xml_composer.to_xml(), reg_code)


def register_document(xml, reg_code=settings.REG_CODE):
    """
    Register document in mode ``BY_RESOLVER`` - let the resolver give you
    URN:NBN code.

    Args:
        xml (str): XML, which will be used for registration. See
                   :mod:`xml_composer` for details.
        reg_code (str, default settings.REG_CODE): Registrar's code.

    Returns:
        obj: Instance of :class:`.URN_NBN` which contains assinged URN:NBN \
             code.
    """
    result = _send_request(
        method="POST",
        url=urljoin(settings.URL, "registrars/%s/digitalDocuments") % reg_code,
        data=xml
    )

    return URN_NBN.from_xmldict(
        xmltodict.parse(result)
    )


def register_digital_instance_obj(urn_nbn, digital_instance):
    """
    Register `digital_instance` object as new digital instance of the
    document for given `urn_nbn`

    Args:
        urn_nbn (str): URN:NBN identifier of registered document.
        digital_instance (obj): :class:`DigitalInstance` instance.

    Returns:
        obj: :class:`DigitalInstance` with more informations.
    """
    assert isinstance(digital_instance, DigitalInstance)

    result = _send_request(
        method="POST",
        url=urljoin(settings.URL, "resolver/%s/digitalInstances") % urn_nbn,
        data=digital_instance.to_xml()
    )

    return DigitalInstance.from_xml(result)[0]


def register_digital_instance(urn_nbn, url, digital_library_id, format=None,
                              accessibility=None):
    """
    Compose and register new digital instance of document.

    Args:
        urn_nbn (str): URN:NBN identifier of registered document.
        url (str): URL of the digital instance.
        digital_library_id (str): ID of the digital library.
        format (str, def. None): Format of the instance - ``pdf`` for example.
        accessibility (str, def. None): Is the registration neccessary to \
                      access this instance?

    Returns:
        obj: :class:`DigitalInstance` with more informations.
    """
    di = DigitalInstance(
        url=url,
        digital_library_id=digital_library_id,
        format=format,
        accessibility=accessibility
    )

    return register_digital_instance_obj(urn_nbn, di)


def get_digital_instances(urn_nbn):
    """
    Get list of :class:`.DigitalInstance` objects for given `urn_nbn`.

    DigitalInstances are `pointers` to :class:`.DigitalLibrary`, where the
    instance of document is stored. There should be always a link to the
    document in ``url`` property.

    Returns:
        list: :class:`.DigitalInstance` objects or blank list.
    """
    result = _send_request(
        method="GET",
        url=urljoin(settings.URL, "resolver/%s/digitalInstances") % urn_nbn
    )

    return DigitalInstance.from_xml(result)


def get_urn_nbn_info(urn_nbn):
    """
    For given `urn_nbn` string, return parsed :class:`URN_NBN` object.

    Args:
        urn_nbn (str): String.

    Return:
        obj: :class:`URN_NBN` object with additional info in properties.
    """
    result = _send_request(
        method="GET",
        url=urljoin(settings.URL, "urnnbn/%s") % urn_nbn
    )

    return URN_NBN.from_xmldict(
        xmltodict.parse(result)
    )


def get_full_urn_nbn_record(urn_nbn):
    """
    Return full record for given `urn_nbn`.

    Warning:
        This function doesn't yet return ORM data, just plain string.

    Args:
        urn_nbn (str): String.

    Returns:
        str: XML with full informations about URN:NBN record.
    """
    nbn_url = "resolver/%s?action=show&format=xml" % urn_nbn
    result = _send_request(
        method="GET",
        url=urljoin(settings.URL, nbn_url)
    )

    return result  # TODO: create ORM for the XML
