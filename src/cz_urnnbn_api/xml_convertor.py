#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains convertors for converting MODS to XML required by URN\:NBN
project.

See:
    - http://resolver.nkp.cz/api/v3/digDocRegistration.xsd
    - https://code.google.com/p/czidlo/wiki/ApiV3
"""
# Imports =====================================================================
import xmltodict
import dhtmlparser

from xml_composer import MonographComposer
from xml_composer import MultiMonoComposer


# Functions & classes =========================================================
class MonographPublication(object):
    """
    This class accepts MODS monographic data, which can then convert to XML
    for URN\:NBN.
    """
    def __init__(self, mods_xml):
        self.mods_xml = mods_xml
        self.dom = dhtmlparser.parseString(mods_xml)
        self.xdom = xmltodict.parse(mods_xml)

        self.composer = MonographComposer()

    def _get_title_info(self):
        return self.xdom["mods:mods"]["mods:titleInfo"]

    def get_title(self):
        """
        Returns:
            str: Title
        """
        title = self._get_title_info()["mods:title"]

        if type(title) in [tuple, list]:
            return title[0]

        return title

    def get_subtitle(self):
        """
        Returns:
            str: Subtitle
        """
        subtitle = self._get_title_info().get("mods:subTitle", None)

        if not subtitle:
            return None

        if type(subtitle) in [tuple, list]:
            return subtitle[0]

        return subtitle

    def get_author(self):
        """
        Returns:
            str: Author's name.
        """
        author = self.dom.match(
            "mods:mods",
            ["mods:name", {"type": "personal", "usage": "primary"}],
            {
                "tag_name": "mods:namePart",
                "fn": lambda x: x.params.get("type", "") != "date"
            }
        )
        if not author:
            author = self.dom.match(
                "mods:mods",
                ["mods:name", {"type": "corporate"}]
            )
        if not author:
            author = self.dom.match(
                "mods:mods",
                ["mods:name", {"type": 'conference'}]
            )
        if not author:
            raise ValueError("Can't find namePart for author!")

        return author[0].getContent().decode("utf-8")

    def get_form(self):
        """
        Returns:
            str: Form of the book. Electronic source, and so on..
        """
        forms = self.dom.match(
            "mods:mods",
            "mods:physicalDescription",
            {
                "tag_name": "mods:form",
                "fn": lambda x: x.params.get("authority", "") == "gmd"
            }
        )
        if not forms:
            return

        return forms[0].getContent().decode("utf-8")

    def _get_description(self):
        return self.xdom["mods:mods"].get("mods:originInfo", None)

    def get_place(self):
        """
        Returns:
            str: Place where the book was released.
        """
        place = self.dom.match(
            "mods:originInfo",
            "mods:place",
            ["mods:placeTerm", {"type": "text"}]
        )
        if not place:
            return

        return place[0].getContent().decode("utf-8")

    def get_publisher(self):
        """
        Returns:
            str: Name of the publisher.
        """
        if not self._get_description():
            return

        return self._get_description().get("mods:publisher", None)

    def get_year(self):
        """
        Returns:
            str: Year when the book was released.
        """
        if not self._get_description():
            return

        year = self._get_description().get("mods:dateIssued", None)

        if "#text" in year:
            return year["#text"]

        return year

    def get_identifier(self, name):
        """
        Returns:
            str: Identifier from ``<mods:identifier>`` which has \
                 ``@type == name``.
        """
        identifier = filter(
            lambda x: x.get("@type", False) == name,
            self.xdom["mods:mods"].get("mods:identifier", [])
        )

        if not identifier:
            return

        return identifier[0]["#text"]

    def get_ccnb(self):
        """
        Returns:
            str: CCNB identification string.
        """
        return self.get_identifier("ccnb")

    def get_isbn(self):
        """
        Returns:
            str: ISBN.
        """
        return self.get_identifier("isbn")

    def get_uuid(self):
        """
        Returns:
            str: UUID.
        """
        return self.get_identifier("uuid")

    def compose(self):
        """
        Convert `self` to nested ordered dicts, which may be serialized to XML
        using ``xmltodict`` module.

        Returns:
            OrderedDict: XML parsed to ordered dicts.
        """
        self.composer.title = self.get_title()
        self.composer.subtitle = self.get_subtitle()
        self.composer.ccnb = self.get_ccnb()
        self.composer.isbn = self.get_isbn()
        self.composer.other_id = self.get_uuid()
        self.composer.document_type = self.get_form()
        self.composer.digital_born = True

        if self.get_author():
            self.composer.author = self.get_author()

        self.composer.place = self.get_place()
        self.composer.publisher = self.get_publisher()
        self.composer.year = self.get_year()

    def add_format(self, file_format):
        """
        Add informations about `file_format` to internal XML dict.

        Args:
            file_format (str): ``PDF``, ``jpeg``, etc..
        """
        self.composer.format = file_format

    def to_xml(self):
        """
        Convert itself to XML unicode string.

        Returns:
            unicode: XML.
        """
        self.compose()
        return self.composer.to_xml()

    def __str__(self):
        return self.to_xml()


class MonographVolume(MonographPublication):
    """
    Conversion of Multi-monograph data to XML required by URN\:NBN.
    """
    def __init__(self, mods_xml):
        super(MonographVolume, self).__init__(mods_xml)

        self.composer = MultiMonoComposer()

    def get_volume_title(self):
        """
        Returns:
            str: Title of the whole volume.
        """
        title_info = self.dom.match(
            "mods:mods",
            "mods:titleInfo",
            "mods:partNumber"
        )

        if not title_info:
            title_info = self.dom.match(
                "mods:mods",
                "mods:titleInfo",
                "mods:partName"
            )

        if not title_info:
            raise ValueError("Can't find volumeTitle!")

        return title_info[0].getContent().decode("utf-8")

    def compose(self):
        """
        Convert `self` to nested ordered dicts, which may be serialized to XML
        using ``xmltodict`` module.

        Returns:
            OrderedDict: XML parsed to ordered dicts.
        """
        super(MonographVolume, self).compose()
        self.composer.volume_title = self.get_volume_title()


def convert_mono_xml(mods_xml, file_format):
    """
    Convert MODS monograph record to XML, which is required by URN:NBN
    resolver.

    Args:
        mods_xml (str): MODS volume XML.

    Returns:
        str: XML for URN:NBN resolver.

    Raises:
        ValueError: If can't find required data in MODS (author, title).
    """
    pub = MonographPublication(mods_xml)
    pub.add_format(file_format)

    return pub.to_xml()


def convert_mono_volume_xml(mods_volume_xml, file_format):
    """
    Convert MODS monograph, multi-volume record to XML, which is required by
    URN:NBN resolver.

    Args:
        mods_volume_xml (str): MODS volume XML.

    Returns:
        str: XML for URN:NBN resolver.

    Raises:
        ValueError: If can't find required data in MODS (author, title).
    """
    pub = MonographVolume(mods_volume_xml)
    pub.add_format(file_format)

    return pub.to_xml()
