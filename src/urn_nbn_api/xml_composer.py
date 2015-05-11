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
def _create_path(root, dict_type, path):
    """
    Create nested dicts in `root` using `dict_type` as constructor. Keys from
    `path` are used to construct the keys for nested dicts.

    Args:
        root (dict instance): Root dictionary, where the nested dicts will be
             created.
        dict_type (dict-like class): Class which will be used to construct
                  dicts - ``dict_type()`.
        path (list/tuple of strings): List of keys for nested ``dict_type``.

    Returns:
        dict: Return last nested dict (dict at last element at `path`).
    """
    for sub_path in path:
        if not isinstance(root.get(sub_path, None), dict):
            root[sub_path] = dict_type()

        root = root[sub_path]

    return root


class MonographPublication(object):
    def __init__(self, mods_xml):
        self.mods_xml = mods_xml
        self.dom = dhtmlparser.parseString(mods_xml)
        self.xdom = xmltodict.parse(mods_xml)

        self.xml_dict = self.to_xml_dict()

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
        """
        Convert `self` to nested ordered dicts, which may be serialized to XML
        using ``xmltodict`` module.

        Returns:
            OrderedDict: XML parsed to ordered dicts.
        """
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

    def add_format(self, file_format):
        """
        Add informations about `file_format` to internal XML dict.

        Args:
            file_format (str): ``PDF``, ``jpeg``, etc..
        """
        format_dict = _create_path(
            self.xml_dict,
            odict,
            [
                "r:import",
                "r:digitalDocument",
                "r:technicalMetadata",
                "r:format",
            ]
        )

        format_dict["#text"] = file_format

    def to_xml(self):
        # print self.xml_dict
        return xmltodict.unparse(self.xml_dict, pretty=True)

    def __str__(self):
        return self.to_xml()


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
        """
        Convert `self` to nested ordered dicts, which may be serialized to XML
        using ``xmltodict`` module.

        Returns:
            OrderedDict: XML parsed to ordered dicts.
        """
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


def compose_mono_xml(mods_xml, file_format):
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


def compose_mono_volume_xml(mods_volume_xml, file_format):
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
