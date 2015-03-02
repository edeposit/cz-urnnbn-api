#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import xmltodict
import dhtmlparser


# Variables ===================================================================
# Functions & classes =========================================================
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
    output = {
        "r:import": {
            "@xmlns:r": "http://resolver.nkp.cz/v3/",
            "r:monograph": {
                "r:titleInfo": {
                    "title": title,
                },
                "r:primaryOriginator": {
                    "@type": "AUTHOR",
                    "#text": author
                },
            },
        }
    }
    mono_root = output["r:import"]["r:monograph"]

    # get part title
    part_title = xdom["mods:mods"]["mods:titleInfo"].get("mods:partName", None)
    if part_title:
        mono_root["r:titleInfo"]["r:subTitle"] = part_title

    # parse form
    forms = dom.match("mods:mods", "mods:physicalDescription", "mods:form")
    if forms:
        forms = filter(lambda x: x.params.get("authority", "") == "gmd", forms)

        if forms:
            mono_root["r:documentType"] = forms[0].getContent().decode("utf-8")

    # parse publication info
    description = xdom["mods:mods"].get("mods:originInfo", None)
    if description:
        place = description.get("mods:place", None)
        if place:
            place = description["mods:place"].get("mods:placeTerm", None)
        publisher = description.get("mods:publisher", None)
        year = description.get("mods:dateIssued", None)

        if any([place, publisher, year]):
            mono_root["r:publication"] = {}

        if year:
            mono_root["r:publication"]["r:year"] = year
        if place:
            mono_root["r:publication"]["r:place"] = place["#text"]
        if publisher:
            mono_root["r:publication"]["r:publisher"] = publisher

    # parse identifiers
    identifiers = xdom["mods:mods"].get("mods:identifier", [])

    # handle ccnb
    ccnb = filter(lambda x: x.get("@type", False) == "ccnb", identifiers)
    if ccnb:
        mono_root["r:ccnb"] = ccnb

    # handle isbn
    isbn = filter(lambda x: x.get("@type", False) == "isbn", identifiers)
    if isbn:
        mono_root["r:isbn"] = isbn

    # handle uuid
    uuid = filter(lambda x: x.get("@type", False) == "uuid", identifiers)
    if uuid:
        mono_root["r:otherId"] = uuid

    return xmltodict.unparse(output, pretty=True)
