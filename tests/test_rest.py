#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from urn_nbn_api import rest

from test_xml_composer import mono_out_example


# Functions & classes =========================================================



# Tests =======================================================================
def test_valid_reg_code():
    assert rest.is_valid_reg_code()
    assert not rest.is_valid_reg_code("azgabash")


def test_register(mono_out_example):
    mono_out_example = """<?xml version="1.0" encoding="UTF-8"?>
<r:import xmlns:r="http://resolver.nkp.cz/v3/">
    <r:monograph>
        <r:titleInfo>
            <r:title>Babička</r:title>
            <r:subTitle>Obrazy z venkovského života</r:subTitle>
        </r:titleInfo>
        <r:ccnb>cnb002251177</r:ccnb>
        <r:isbn>8090119964</r:isbn>
        <r:otherId>DOI:TODO</r:otherId>
        <r:documentType>kniha</r:documentType>
        <r:digitalBorn>false</r:digitalBorn>
        <r:primaryOriginator type="AUTHOR">Božena Němcová</r:primaryOriginator>
        <r:otherOriginator>Adolf Kašpar</r:otherOriginator>
        <r:publication>
            <r:publisher>Československý spisovatel</r:publisher>
            <r:place>V Praze</r:place>
            <r:year>2011</r:year>
        </r:publication>
    </r:monograph>
    <r:digitalDocument>
        <r:archiverId>3</r:archiverId>
    </r:digitalDocument>
</r:import>
"""
    print rest.register(mono_out_example)
