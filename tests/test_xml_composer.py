#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import sys

import pytest

sys.path.insert(0, "src")
import urn_nbn_api
from urn_nbn_api.xml_composer import compose_mono_xml
from urn_nbn_api.xml_composer import compose_mono_volume_xml


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
def test_mono_xml_conversion(mono_mods_example, mono_out_example):
    out = compose_mono_xml(mono_mods_example).encode("utf-8")

    # compare without whitespaces
    assert out.split() == mono_out_example.split()


def test_mono_volume_xml_conversion(mono_mods_example, mono_vol_out_example):
    out = compose_mono_volume_xml(mono_mods_example).encode("utf-8")

    # compare without whitespaces
    assert out.split() == mono_vol_out_example.split()
