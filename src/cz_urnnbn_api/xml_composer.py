#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains composers to allow creation of XML for URN:NBN, so you
don't have to create XML by hand.

See:
    - http://resolver.nkp.cz/api/v3/digDocRegistration.xsd
    - https://code.google.com/p/czidlo/wiki/ApiV3
"""
# Imports =====================================================================
import xmltodict

from odictliteral import odict
from kwargs_obj import KwargsObj


# Functions & classes =========================================================
class MonographComposer(KwargsObj):
    """
    Compostition class for Monograph publications.

    Attributes:
        title (str, required):  Title of the publication.
        subtitle (str): Subtitle of the publication.
        ccnb (str): CCNB number.
        isbn (str): ISBN string. You should validate this first.
        other_id (str): Useful for UUID and so on..
        document_type (str): Electronic? Scan?
        digital_born (bool): Was the publication digitally born, or is it scan?
        author (str): Author of the publication.
        publisher (str): Publishers name.
        place (str): Place where the publication was published (usually city).
        year (str): Year when the publication was published.
        format (str, required): PDF? EPUB?
    """
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

        self._all_set = True
        self._kwargs_to_attributes(kwargs)

    @staticmethod
    def _create_path(root, dict_type, path):
        """
        Create nested dicts in `root` using `dict_type` as constructor. Strings
        in `path` are used to construct the keys for nested dicts.

        Args:
            root (dict instance): Root dictionary, where the nested dicts will
                 be created.
            dict_type (dict-like class): Class which will be used to construct
                      dicts - ``dict_type()`.
            path (list/tuple of strings): List of keys for nested
                 ``dict_type``.

        Returns:
            dict: Return last nested dict (dict at last element at `path`).
        """
        for sub_path in path:
            if not isinstance(root.get(sub_path, None), dict):
                root[sub_path] = dict_type()

            root = root[sub_path]

        return root

    @staticmethod
    def _assign_pattern(where, key, what):
        """
        If `what`, assign `what` into ``where[key]``.

        Args:
            where (dict): Dith onto which the assingment action is performed.
            key (str): Definition of key for `where`.
            what (any): Any value. If evaluated to true, assign it to `where`.
        """
        if what:
            where[key] = what

    def _check_required_fields(self):
        """
        Make sure that all required fields are present.
        """
        assert self.title
        assert self.format

    def _add_identifier(self, mono_root, identifier, out=None):
        """
        Look for `identifier` in `self`. If found, add it to `mono_root` as
        `r:identifier`, or `r:out` if `out` is set. If not found, do nothing.

        Args:
            mono_root (dict): Dict into which you wish to add the `identifier`.
            identifier (str): Name of the attribute in `self`.
            out (str, default None): Optional argument to specify name of the
                key into which the `identifier` will be put.
        """
        out = out if out is not None else identifier

        if hasattr(self, identifier) and getattr(self, identifier) is not None:
            mono_root["r:" + out] = getattr(self, identifier)

    def to_xml_dict(self):
        """
        Compose hierarchical structure from ordered dicts, which will hold the
        XML.

        Returns:
            odict: Structure from ordered dicts.
        """
        self._check_required_fields()

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
        MonographComposer._assign_pattern(
            mono_root["r:titleInfo"],
            "r:subTitle",
            self.subtitle
        )

        # handle ccnb, isbn, uuid
        self._add_identifier(mono_root, "ccnb")
        self._add_identifier(mono_root, "isbn")
        self._add_identifier(mono_root, "other_id", out="otherId")

        # add form of the book
        MonographComposer._assign_pattern(
            mono_root,
            "r:documentType",
            self.document_type
        )

        mono_root["r:digitalBorn"] = "true" if self.digital_born else "false"

        if self.author:
            mono_root["r:primaryOriginator"] = odict[
                "@type": "AUTHOR",
                "#text": self.author
            ]

        if any([self.place, self.publisher, self.year]):
            publ = odict()

            MonographComposer._assign_pattern(
                publ,
                "r:publisher",
                self.publisher
            )
            MonographComposer._assign_pattern(publ, "r:place", self.place)
            MonographComposer._assign_pattern(publ, "r:year", self.year)

            mono_root["r:publication"] = publ

        if self.format:
            format_dict = MonographComposer._create_path(
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


class MultiMonoComposer(MonographComposer):
    """
    Composition class for Multi monograph XMLs for URN:NBN.

    Attributes:
        title (str, required):  Title of the publication.
        volume_title (str, required): Title of the whole volume.
        subtitle (str): Subtitle of the publication.
        ccnb (str): CCNB number.
        isbn (str): ISBN string. You should validate this first.
        other_id (str): Useful for UUID and so on..
        document_type (str): Electronic? Scan?
        digital_born (bool): Was the publication digitally born, or is it scan?
        author (str): Author of the publication.
        publisher (str): Publishers name.
        place (str): Place where the publication was published (usually city).
        year (str): Year when the publication was published.
        format (str, required): PDF? EPUB?
    """
    def __init__(self, **kwargs):
        self.volume_title = None

        super(MultiMonoComposer, self).__init__()
        self._kwargs_to_attributes(kwargs)

    @staticmethod
    def _swap_keys(ordered_dict, old_key, new_key):
        """
        Swap `old_key` for `new_key`, but keep in mind position of key in
        `ordered_dict`.

        Returns:
            odict: Ordered dict with swapped keys.
        """
        return odict(
            (new_key, val) if key == old_key else (key, val)
            for key, val in ordered_dict.iteritems()
        )

    def _check_required_fields(self):
        """
        Make sure that all required fields are present.
        """
        assert self.volume_title
        super(MultiMonoComposer, self)._check_required_fields()

    def to_xml_dict(self):
        """
        Convert itself to XML string.

        Returns:
            str: XML.
        """
        root = super(MultiMonoComposer, self).to_xml_dict()

        # same as mono, except that <r:monograph> is now <r:monographVolume>
        root["r:import"] = MultiMonoComposer._swap_keys(
            root["r:import"],
            "r:monograph",
            "r:monographVolume"
        )

        # same as mono, except that <r:title> is now <r:monographTitle>
        mono_volume = root["r:import"]["r:monographVolume"]
        mono_volume["r:titleInfo"] = MultiMonoComposer._swap_keys(
            mono_volume["r:titleInfo"],
            "r:title",
            "r:monographTitle"
        )

        title_info = root["r:import"]["r:monographVolume"]["r:titleInfo"]
        if self.volume_title:
            title_info["r:volumeTitle"] = self.volume_title

        return root
