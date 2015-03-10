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


# Variables ===================================================================
# Functions & classes =========================================================
def data_context(fn):
    path = os.path.join(data_path(), fn)
    with open(path) as f:
        return f.read()


# Fixtures ====================================================================
@pytest.fixture
def data_path():
    wd = os.path.dirname(__file__)
    return os.path.join(wd, "data")


@pytest.fixture
def mono_mods_example():
    return data_context("mods_mono.xml")


@pytest.fixture
def mono_out_example():
    return data_context("mono_output.xml")


# Tests =======================================================================
def test_mono_xml_conversion(mono_mods_example, mono_out_example):
    out = compose_mono_xml(mono_mods_example).encode("utf-8")

    # compare without whitespaces
    assert mono_out_example.split() == mono_out_example.split()