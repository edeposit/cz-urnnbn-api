#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains convertors for converting MODS to XML required by URN:NBN
project.

See:
    - http://resolver.nkp.cz/api/v3/digDocRegistration.xsd
    - https://code.google.com/p/czidlo/wiki/ApiV3
"""
# Imports =====================================================================
import xmltodict
import dhtmlparser
from odictliteral import odict


# Functions & classes =========================================================
class MonographPublication(object):
    def __init__(self, mods_xml):
        self.mods_xml = mods_xml
        self.dom = dhtmlparser.parseString(mods_xml)
        self.xdom = xmltodict.parse(mods_xml)

    def _get_title_info(self):
        return self.xdom["mods:mods"]["mods:titleInfo"]

    def get_title(self):
        title = self._get_title_info()["mods:title"]

        if type(title) in [tuple, list]:
            return title[0]

        return title

    def get_subtitle(self):
        subtitle = self._get_title_info().get("mods:subTitle", None)

        if not subtitle:
            return None

        if type(subtitle) in [tuple, list]:
            return subtitle[0]

        return subtitle

    def get_author(self):
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
        place = self.dom.match(
            "mods:originInfo",
            "mods:place",
            ["mods:placeTerm", {"type": "text"}]
        )
        if not place:
            return

        return place[0].getContent().decode("utf-8")

    def get_publisher(self):
        if not self._get_description():
            return

        return self._get_description().get("mods:publisher", None)

    def get_year(self):
        if not self._get_description():
            return

        return self._get_description().get("mods:dateIssued", None)

    def get_identifier(self, name):
        identifier = filter(
            lambda x: x.get("@type", False) == name,
            self.xdom["mods:mods"].get("mods:identifier", [])
        )

        if not identifier:
            return

        return identifier[0]["#text"]

    def get_ccnb(self):
        return self.get_identifier("ccnb")

    def get_isbn(self):
        return self.get_identifier("isbn")

    def get_uuid(self):
        return self.get_identifier("uuid")

    def _assign_pattern(self, where, key, what):
        if what:
            where[key] = what

    def _add_identifier_to_mono(self, mono_root, identifier, out=None):
        out = out if out is not None else identifier

        tmp = self.get_identifier(identifier)
        if tmp:
            mono_root["r:" + out] = tmp

    def to_xml_dict(self):
        # compose output template
        output = odict[
            "r:import": odict[
                "@xmlns:r": "http://resolver.nkp.cz/v3/",
                "r:monograph": odict[
                    "r:titleInfo": odict[
                        "r:title": self.get_title(),
                    ],
                ],
            ]
        ]
        mono_root = output["r:import"]["r:monograph"]

        self._assign_pattern(
            mono_root["r:titleInfo"],
            "r:subTitle",
            self.get_subtitle()
        )

        # handle ccnb, isbn, uuid
        self._add_identifier_to_mono(mono_root, "ccnb")
        self._add_identifier_to_mono(mono_root, "isbn")
        self._add_identifier_to_mono(mono_root, "uuid", out="otherId")

        # add form of the book
        self._assign_pattern(mono_root, "r:documentType", self.get_form())

        mono_root["r:digitalBorn"] = "true"

        if self.get_author():
            mono_root["r:primaryOriginator"] = odict[
                "@type": "AUTHOR",
                "#text": self.get_author()
            ]

        if self._get_description() and any([self.get_place(),
                                            self.get_publisher(),
                                            self.get_year()]):
            publ = odict()

            self._assign_pattern(publ, "r:publisher", self.get_publisher())
            self._assign_pattern(publ, "r:place", self.get_place())
            self._assign_pattern(publ, "r:year", self.get_year())

            mono_root["r:publication"] = publ

        return output

    def __str__(self):
        return xmltodict.unparse(self.to_xml_dict(), pretty=True)


class MonographVolume(MonographPublication):
    def get_volume_title(self):
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

    def to_xml_dict(self):
        # compose output template
        output = odict[
            "r:import": odict[
                "@xmlns:r": "http://resolver.nkp.cz/v3/",
                "r:monographVolume": odict[
                    "r:titleInfo": odict[
                        "r:monographTitle": self.get_title(),
                        "r:volumeTitle": self.get_volume_title(),
                    ],
                ],
            ]
        ]
        mono_root = output["r:import"]["r:monographVolume"]

        # handle ccnb, isbn, uuid
        self._add_identifier_to_mono(mono_root, "ccnb")
        self._add_identifier_to_mono(mono_root, "isbn")
        self._add_identifier_to_mono(mono_root, "uuid", out="otherId")

        # add form of the book
        self._assign_pattern(mono_root, "r:documentType", self.get_form())

        mono_root["r:digitalBorn"] = "true"

        if self.get_author():
            mono_root["r:primaryOriginator"] = odict[
                "@type": "AUTHOR",
                "#text": self.get_author()
            ]

        if self._get_description() and any([self.get_place(),
                                            self.get_publisher(),
                                            self.get_year()]):
            publ = odict()

            self._assign_pattern(publ, "r:publisher", self.get_publisher())
            self._assign_pattern(publ, "r:place", self.get_place())
            self._assign_pattern(publ, "r:year", self.get_year())

            mono_root["r:publication"] = publ

        return output


def compose_mono_xml(mods_xml):
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
    return MonographPublication(mods_xml).__str__()


def compose_mono_volume_xml(mods_volume_xml):
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
    return MonographVolume(mods_volume_xml).__str__()
