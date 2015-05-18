#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import xmltodict

from tools import both_set_and_different
from kwarg_obj import KwargObj


# Functions & classes =========================================================
class DigitalInstance(KwargObj):
    """
    Container used to hold informations about instances of the documents in
    digital library - this is pointer to document in digital library.

    Atrributes:
        uid (str): ID of the library.
        url (str): URL of the library.
        active (bool): Is the record active?
        digital_library_id (str): Id of the digitial library.
        created (str): ISO 8601 string with date.
        deactivated (str) ISO 8601 string with date.
        format (str): Format of the book. ``jpg;pdf`` for example.
        accessibility (str): Free description of accessibility.
    """
    def __init__(self, uid, active, url, digital_library_id, **kwargs):
        self.uid = uid
        self.active = active
        self.url = url
        self.digital_library_id = digital_library_id
        self.format = None
        self.created = None
        self.accessibility = None
        self.deactivated = None

        self._all_set = True
        self._kwargs_to_attributes(kwargs)

    def __eq__(self, other):
        tests = [
            self.uid != other.uid,
            self.active != other.active,
            self.digital_library_id != other.digital_library_id,
            self.url != other.url,
            self.deactivated != other.deactivated,
        ]
        if any(tests):
            return False

        return not any([
            both_set_and_different(self.format, other.format),
            both_set_and_different(self.created, other.created),
            both_set_and_different(self.accessibility, other.accessibility),
        ])

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def instance_from_xmldict(dict_tag):
        return DigitalInstance(
            uid=dict_tag["@id"],
            active=dict_tag["@active"].lower() == "true",
            url=dict_tag.get("url", None),
            digital_library_id=dict_tag["digitalLibraryId"],
            format=dict_tag.get("format", None),
            created=dict_tag.get("created", None),
            deactivated=dict_tag.get("deactivated", None),
            accessibility=dict_tag.get("accessibility", None),
        )

    @staticmethod
    def from_xml(xml):
        xdom = xmltodict.parse(xml)

        di = xdom["response"]["digitalInstances"]

        if not di.get("digitalInstance", False):
            return []

        return [
            DigitalInstance.instance_from_xmldict(dig_instance_tag)
            for dig_instance_tag in di["digitalInstance"]
        ]
