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


class MonographComposer(object):
    def __init__(self, **kwargs):
        self.title = None
        self.subtitle = None
        self.ccnb = None
        self.isbn = None
        self.other_id = None
        self.document_type = None
        self.digital_born = True
        self.author = None
        self.publisher = None
        self.place = None
        self.year = None
        self.format = None

        for key, val in kwargs.iteritems():
            if key in self.__dict__:
                self.__dict__[key] = val
            else:
                raise ValueError("Can't set %s parameter!" % key)

    def _assign_pattern(self, where, key, what):
        if what:
            where[key] = what

    def _add_identifier_to_mono(self, mono_root, identifier, out=None):
        out = out if out is not None else identifier

        if hasattr(self, identifier) and getattr(self, identifier) is not None:
            mono_root["r:" + out] = getattr(self, identifier)

    def to_xml_dict(self):
        root = odict[
            "r:import": odict[
                "@xmlns:r": "http://resolver.nkp.cz/v3/",
                "r:monograph": odict[
                    "r:titleInfo": odict[
                        "r:title": self.title,
                    ],
                ],
            ]
        ]
        mono_root = root["r:import"]["r:monograph"]

        # subtitle
        self._assign_pattern(
            mono_root["r:titleInfo"],
            "r:subTitle",
            self.subtitle
        )

        # handle ccnb, isbn, uuid
        self._add_identifier_to_mono(mono_root, "ccnb")
        self._add_identifier_to_mono(mono_root, "isbn")
        self._add_identifier_to_mono(mono_root, "other_id", out="otherId")

        # add form of the book
        self._assign_pattern(mono_root, "r:documentType", self.document_type)

        mono_root["r:digitalBorn"] = self.digital_born

        if self.author:
            mono_root["r:primaryOriginator"] = odict[
                "@type": "AUTHOR",
                "#text": self.author
            ]

        if any([self.place, self.publisher, self.year]):
            publ = odict()

            self._assign_pattern(publ, "r:publisher", self.publisher)
            self._assign_pattern(publ, "r:place", self.place)
            self._assign_pattern(publ, "r:year", self.year)

            mono_root["r:publication"] = publ

        if self.format:
            format_dict = _create_path(
                root,
                odict,
                [
                    "r:import",
                    "r:digitalDocument",
                    "r:technicalMetadata",
                    "r:format",
                ]
            )

            format_dict["#text"] = self.format

        return root

    def to_xml(self):
        """
        Convert itself to XML string.

        Returns:
            str: XML.
        """
        return xmltodict.unparse(
            self.to_xml_dict(),
            pretty=True
        ).encode("utf-8")

    def __str__(self):
        return self.to_xml()
