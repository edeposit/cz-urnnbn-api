#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
XML specification: http://resolver.nkp.cz/api/v3/digDocRegistration.xsd
"""
# Imports =====================================================================

import xmltodict
import dhtmlparser
from odictliteral import odict

# TODO: přepsat na hromadu getterů
# TODO: @utf8 decorator / nějak pořešit


# Functions & classes =========================================================
class MonographPublication(object):
    def __init__(self, mods_xml):
        self.mods_xml = mods_xml
        self.dom = dhtmlparser.parseString(mods_xml)
        self.xdom = xmltodict.parse(mods_xml)

    def get_title(self):
        title = self.xdom["mods:mods"]["mods:titleInfo"]["mods:title"]

        if type(title) in [tuple, list]:
            return title[0]

        return title

    def get_author(self):
        author = self.dom.find(
            "mods:name",
            {"type": "personal", "usage": "primary"},
            fn=lambda x: x.params.get("type", "") != "date"
        )

        if not author:
            raise ValueError("Can't find 'author' in given MODS!")

        # filter proper <mods:namePart> tag (one which doesn't contain
        # type="date" attribute)
        author = filter(
            lambda x: x.params.get("type", False) != "date",
            author[0].find("mods:namePart")
        )
        if not author:
            raise ValueError("Can't find namePart for author!")

        return author[0].getContent().decode("utf-8")

    def get_part_title(self):
        title_info = self.xdom["mods:mods"]["mods:titleInfo"]

        return title_info.get("mods:partName", None)

    def get_form(self):
        # parse form
        forms = self.dom.match(
            "mods:mods",
            "mods:physicalDescription",
            "mods:form"
        )
        if not forms:
            return

        forms = filter(lambda x: x.params.get("authority", "") == "gmd", forms)

        if not forms:
            return

        return forms[0].getContent().decode("utf-8")

    def _get_description(self):
        return self.xdom["mods:mods"].get("mods:originInfo", None)

    def get_place(self):
        description = self._get_description()
        if not description:
            return

        place = description.get("mods:place", None)

        if not place:
            return

        place = description["mods:place"].get("mods:placeTerm", None)

        if not place:
            return

        return place["#text"]

    def get_publisher(self):
        description = self._get_description()
        if not description:
            return

        return description.get("mods:publisher", None)

    def get_year(self):
        description = self._get_description()
        if not description:
            return

        return description.get("mods:dateIssued", None)

    def _add_identifier_to_mono(self, mono_root, identifier, out=None):
        identifiers = self.xdom["mods:mods"].get("mods:identifier", [])
        out = out if out is not None else identifier

        tmp = filter(
            lambda x: x.get("@type", False) == identifier,
            identifiers
        )
        if tmp:
            mono_root["r:" + out] = tmp[0]["#text"]

    def to_xml_dict(self):
        # compose output template
        output = odict[
            "r:import": odict[
                "@xmlns:r": "http://resolver.nkp.cz/v3/",
                "r:monograph": odict[
                    "r:titleInfo": odict[
                        "r:title": self.get_title(),
                    ],
                    "r:primaryOriginator": odict[
                        "@type": "AUTHOR",
                        "#text": self.get_author()
                    ],
                ],
            ]
        ]
        mono_root = output["r:import"]["r:monograph"]

        if self.get_part_title():
            mono_root["r:titleInfo"]["r:subTitle"] = self.get_part_title()

        # handle ccnb, isbn, uuid
        self._add_identifier_to_mono(mono_root, "ccnb")  # TODO: rewrite to getters
        self._add_identifier_to_mono(mono_root, "isbn")
        self._add_identifier_to_mono(mono_root, "uuid", out="otherId")

        if self.get_form():
            mono_root["r:documentType"] = self.get_form()

        mono_root["r:digitalBorn"] = "true"

        if self._get_description():
            place = self.get_place()
            publisher = self.get_publisher()
            year = self.get_year()

            if any([place, publisher, year]):
                mono_root["r:publication"] = odict()

            if publisher:
                mono_root["r:publication"]["r:publisher"] = publisher
            if place:
                mono_root["r:publication"]["r:place"] = place
            if year:
                mono_root["r:publication"]["r:year"] = year

        return output

    def __str__(self):
        return xmltodict.unparse(self.to_xml_dict(), pretty=True)


def compose_mono_xml(mods_volume_xml):
    """
    Convert MODS to XML, which is required by URN:NBN resolver.

    See:
        - http://resolver.nkp.cz/api/v3/digDocRegistration.xsd
        - https://code.google.com/p/czidlo/wiki/ApiV3

    Args:
        mods_volume_xml (str): MODS volume XML.

    Returns:
        str: XML for URN:NBN resolver.

    Raises:
        ValueErrro: If can't find required data in MODS (author, title).
    """
    return MonographPublication(mods_volume_xml).__str__()


def compose_periodical_xml(mods_volume_xml):
    pass
