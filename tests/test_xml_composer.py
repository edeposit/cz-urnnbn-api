#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import os
import sys

import pytest
from odictliteral import odict

import urn_nbn_api
from urn_nbn_api.xml_composer import _create_path
from urn_nbn_api.xml_composer import MonographComposer
# from urn_nbn_api.xml_composer import compose_mono_volume_xml


# Variables ===================================================================
# Functions & classes =========================================================
def get_data_path():
    wd = os.path.dirname(__file__)
    return os.path.join(wd, "data")


def data_context(fn):
    path = os.path.join(get_data_path(), fn)
    with open(path) as f:
        return f.read()


# Fixtures ====================================================================
@pytest.fixture
def mono_mods_example():
    return data_context("mods_mono.xml")


@pytest.fixture
def mono_out_example():
    return data_context("mono_output.xml")


@pytest.fixture
def mono_vol_out_example():
    return data_context("mono_volume_output.xml")


# Tests =======================================================================
def test_mono_xml_conversion(mono_out_example):
    out = MonographComposer(
        title="Dračí doupě plus",
        ccnb="cnb001852175",
        isbn="978-80-85979-67-1",
        other_id="87d27370-db5b-11e3-b110-005054787e51",
        document_type="elektronický zdroj",
        digital_born="true",
        author="Ježek, Matouš",
        publisher="Altar",
        place="Ostrava",
        year="2012",
        format="pdf",
    )

    # with open("asd.xml", "w") as f:
        # f.write(out.to_xml())

    # compare without whitespaces
    assert out.to_xml() == mono_out_example


# def test_mono_volume_xml_conversion(mono_mods_example, mono_vol_out_example):

#     # compare without whitespaces
#     assert out == mono_vol_out_example


# def test_create_path():
#     r = odict(key="hello")

#     _create_path(r, odict, ["subpath", "more"])

#     assert r == odict[
#         "key": "hello",
#         "subpath": odict[
#             "more": odict()
#         ]
#     ]


# def test_create_path_existing_keys():
#     r = odict(key="hello")

#     more = _create_path(r, odict, ["key", "subpath", "more"])

#     assert r == odict[
#         "key": odict[
#             "subpath": odict[
#                 "more": odict()
#             ]
#         ]
#     ]

#     more["asd"] = "val"
#     assert more["asd"] == r["key"]["subpath"]["more"]["asd"]
