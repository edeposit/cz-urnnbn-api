#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import xmltodict
from odictliteral import odict
from kwargs_obj import KwargsObj

from tools import both_set_and_different


# Functions & classes =========================================================
class DigitalInstance(KwargsObj):
    """
    Container used to hold informations about instances of the documents in
    digital library - this is pointer to document in digital library.

    Attributes:
        uid (str): ID of the library.
        url (str): URL of the library.
        digital_library_id (str): Id of the digitial library.
        active (bool, def. None): Is the record active?
        created (str, def. None): ISO 8601 string with date.
        deactivated (str, def. None): ISO 8601 string representation of date.
        format (str, def. None): Format of the book. ``jpg;pdf`` for example.
        accessibility (str, def. None): Free description of accessibility.
    """
    def __init__(self, url, digital_library_id, **kwargs):
        self.url = url
        self.digital_library_id = digital_library_id
        self.uid = None
        self.active = None
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

    def to_xml(self):
        """
        Convert self to XML, which can be send to API to register new digital
        instance.

        Returns:
            str: UTF-8 encoded string with XML representation.

        Raises:
            AssertionError: If :attr:`url` or :attr:`digital_library_id` is \
                            not set.
        """
        assert self.url, "You have to set .url!"
        assert self.digital_library_id, "You have to set .digital_library_id!"

        root = odict[
            "digitalInstance": odict[
                "@xmlns": "http://resolver.nkp.cz/v3/",
                "url": self.url,
                "digitalLibraryId": self.digital_library_id,
                "format": self.format,
                "accessibility": self.accessibility,
            ]
        ]

        if not self.format:
            del root["digitalInstance"]["format"]
        if not self.accessibility:
            del root["digitalInstance"]["accessibility"]

        return xmltodict.unparse(root, pretty=True).encode("utf-8")

    @staticmethod
    def instance_from_xmldict(dict_tag):
        """
        Create DigitalInstance from nested dicts (result of xmltodict).

        Args:
            dict_tag (dict): Nested dicts.

        Returns:
            obj: :class:`DigitalInstance` object.
        """
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
        """
        Parse `xml` string and DigitalInstances.

        Args:
            xml (str): Unicode/utf-8 XML.

        Returns:
            list: List of :class:`DigitalInstance` objects.
        """
        xdom = xmltodict.parse(xml)

        di = xdom["response"]["digitalInstances"]

        if not di.get("digitalInstance", False):
            return []

        return [
            DigitalInstance.instance_from_xmldict(dig_instance_tag)
            for dig_instance_tag in di["digitalInstance"]
        ]
