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

import cz_urnnbn_api
from cz_urnnbn_api.xml_composer import MonographComposer
from cz_urnnbn_api.xml_composer import MultiMonoComposer


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
def mono_out_example():
    return data_context("mono_output.xml")


@pytest.fixture
def multimono_out_example():
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

    assert out.to_xml() == mono_out_example


def test_mono_xml_without_uuid(mono_out_example):
    out = MonographComposer(
        title="Dračí doupě plus",
        ccnb="cnb001852175",
        isbn="978-80-85979-67-1",
        document_type="elektronický zdroj",
        digital_born="true",
        author="Ježek, Matouš",
        publisher="Altar",
        place="Ostrava",
        year="2012",
        format="pdf",
    )

    # remove uuid
    mono = mono_out_example.decode("utf-8").splitlines()
    del mono[8]
    mono = "\n".join(mono)

    assert out.to_xml().decode("utf-8") == mono


def test_mono_xml_without_invalid_parameter():
    with pytest.raises(ValueError):
        MonographComposer(
            title="Dračí doupě plus",
            ccnb="cnb001852175",
            isbn="978-80-85979-67-1",
            azgabash="elektronický zdroj"
        )


def test_swap_keys():
    original = odict[
        "somekey": "azgabash",
        "oldkey": "something",
        "another_key": "asd"
    ]

    new_dict = MultiMonoComposer._swap_keys(original, "oldkey", "newkey")

    assert new_dict == odict[
        "somekey": "azgabash",
        "newkey": "something",
        "another_key": "asd"
    ]


def test_mono_volume_xml_conversion(multimono_out_example):
    out = MultiMonoComposer(
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
        volume_title="1",
    )

    assert out.to_xml() == multimono_out_example


def test_create_path():
    r = odict(key="hello")

    MonographComposer._create_path(r, odict, ["subpath", "more"])

    assert r == odict[
        "key": "hello",
        "subpath": odict[
            "more": odict()
        ]
    ]


def test_create_path_existing_keys():
    r = odict(key="hello")

    more = MonographComposer._create_path(r, odict, ["key", "subpath", "more"])

    assert r == odict[
        "key": odict[
            "subpath": odict[
                "more": odict()
            ]
        ]
    ]

    more["asd"] = "val"
    assert more["asd"] == r["key"]["subpath"]["more"]["asd"]


def test_assign_pattern():
    r = odict(key="hello")

    MonographComposer._assign_pattern(r, "otherkey", False)

    assert r == odict(key="hello")

    MonographComposer._assign_pattern(r, "otherkey", "hi")

    assert r == odict[
        "key": "hello",
        "otherkey": "hi"
    ]


def test_setting_uset_is_disabled():
    mc = MonographComposer()
    mmc = MultiMonoComposer()

    with pytest.raises(ValueError):
        mc.azgabash = True

    with pytest.raises(ValueError):
        mmc.azgabash = True
