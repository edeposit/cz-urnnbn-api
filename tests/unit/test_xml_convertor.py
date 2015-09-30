#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os

import pytest

from cz_urnnbn_api.xml_convertor import convert_mono_xml
from cz_urnnbn_api.xml_convertor import MonographPublication
from cz_urnnbn_api.xml_convertor import convert_mono_volume_xml

from test_xml_composer import data_context
from test_xml_composer import mono_out_example
from test_xml_composer import multimono_out_example


# Fixtures ====================================================================
@pytest.fixture
def mono_mods_example():
    return data_context("mods_mono.xml")


# Tests =======================================================================
def test_mono_xml_conversion(mono_mods_example, mono_out_example):
    out = convert_mono_xml(mono_mods_example, "pdf")

    assert out == mono_out_example


def test_mono_volume_xml_conversion(mono_mods_example, multimono_out_example):
    out = convert_mono_volume_xml(mono_mods_example, "pdf")

    assert out == multimono_out_example


def test_year_with_attribute():
    example = """<?xml version="1.0" encoding="UTF-8"?>
<mods:mods>
  <mods:originInfo>
    <mods:place>
      <mods:placeTerm type="code" authority="marccountry">xr-</mods:placeTerm>
    </mods:place>
    <mods:dateIssued encoding="marc">2011</mods:dateIssued>
    <mods:edition>1. elektronické vydání</mods:edition>
    <mods:issuance>multipart monograph</mods:issuance>
  </mods:originInfo>
</mods:mods>"""

    mp = MonographPublication(example)

    assert mp.get_year() == "2011"
