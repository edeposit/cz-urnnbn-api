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


# Functions & classes =========================================================
class MonographPublication(object):
    def __init__(self, mods_xml):
        self.mods_xml = mods_xml
        self.dom = dhtmlparser.parseString(mods_xml)
        self.xdom = xmltodict.parse(mods_xml)


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
    dom = dhtmlparser.parseString(mods_volume_xml)
    xdom = xmltodict.parse(mods_volume_xml)

    # parse title
    title = xdom["mods:mods"]["mods:titleInfo"]["mods:title"]

    # parse author
    author = dom.find("mods:name", {"type": "personal", "usage": "primary"})
    if not author:
        raise ValueError("Can't find 'author' in given MODS!")

    # filter proper <mods:namePart> tag (one which doesn't contain type="date"
    # attribute)
    author = filter(
        lambda x: x.params.get("type", False) != "date",
        author[0].find("mods:namePart")
    )
    if not author:
        raise ValueError("Can't find namePart for author!")
    author = author[0].getContent().decode("utf-8")

    # compose output template
    output = odict[
        "r:import": odict[
            "@xmlns:r": "http://resolver.nkp.cz/v3/",
            "r:monograph": odict[
                "r:titleInfo": odict[
                    "r:title": title,
                ],
                "r:primaryOriginator": odict[
                    "@type": "AUTHOR",
                    "#text": author
                ],
            ],
        ]
    ]
    mono_root = output["r:import"]["r:monograph"]

    # get part title
    part_title = xdom["mods:mods"]["mods:titleInfo"].get("mods:partName", None)
    if part_title:
        mono_root["r:titleInfo"]["r:subTitle"] = part_title

    # handle ccnb, isbn, uuid
    def add_identifier_to_mono(mono_root, identifier, out=None):
        identifiers = xdom["mods:mods"].get("mods:identifier", [])
        out = out if out is not None else identifier

        tmp = filter(
            lambda x: x.get("@type", False) == identifier,
            identifiers
        )
        if tmp:
            mono_root["r:" + out] = tmp[0]["#text"]

    add_identifier_to_mono(mono_root, "ccnb")
    add_identifier_to_mono(mono_root, "isbn")
    add_identifier_to_mono(mono_root, "uuid", out="otherId")

    # parse form
    forms = dom.match("mods:mods", "mods:physicalDescription", "mods:form")
    if forms:
        forms = filter(lambda x: x.params.get("authority", "") == "gmd", forms)

        if forms:
            mono_root["r:documentType"] = forms[0].getContent().decode("utf-8")

    mono_root["r:digitalBorn"] = "true"

    # parse author
    mono_root["r:primaryOriginator"] = odict[
        "@type": "AUTHOR",
        "#text": author
    ]

    # parse publication info
    description = xdom["mods:mods"].get("mods:originInfo", None)
    if description:
        place = description.get("mods:place", None)
        if place:
            place = description["mods:place"].get("mods:placeTerm", None)
        publisher = description.get("mods:publisher", None)
        year = description.get("mods:dateIssued", None)

        if any([place, publisher, year]):
            mono_root["r:publication"] = odict()

        if publisher:
            mono_root["r:publication"]["r:publisher"] = publisher
        if place:
            mono_root["r:publication"]["r:place"] = place["#text"]
        if year:
            mono_root["r:publication"]["r:year"] = year

    return xmltodict.unparse(output, pretty=True)


def compose_periodical_xml(mods_volume_xml):
    pass
