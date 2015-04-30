#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from urn_nbn_api import api
from urn_nbn_api import api_structures

from test_xml_composer import data_context
from test_xml_composer import mono_out_example


# Fixtures ====================================================================
@pytest.fixture
def iter_registrars_data():
    return data_context("iter_registrars_data.xml")


# Tests =======================================================================
def test_is_valid_reg_code():
    assert api.is_valid_reg_code()
    assert not api.is_valid_reg_code("azgabash")


def test_iter_registrars(monkeypatch, iter_registrars_data):
    def send_request(*args, **kwargs):
        return iter_registrars_data

    monkeypatch.setattr(api, "_send_request", send_request)

    registrars = list(api.iter_registrars())

    assert len(registrars) == 2

    assert registrars[0] == api_structures.Registrar(
        code="boa001",
        uid="8",
        name="MZK",
        description=u"Moravská zemská knihovna",
        created="2012-04-18T23:19:17.727+02:00",
        modified="2012-10-29T10:39:30.882+01:00",
        modes=api_structures.Modes(
            by_resolver=True,
            by_registrar=True,
            by_reservation=True,
        )
    )

    assert registrars[1] == api_structures.Registrar(
        code="aba001",
        uid="9",
        name="NKP",
        description=u"Národní knihovna Praha",
        created="2012-04-18T23:19:16.143+02:00",
        modes=api_structures.Modes(
            by_resolver=False,
            by_registrar=True,
            by_reservation=False,
        )
    )

    assert registrars[1] != api_structures.Registrar(
        code="aba001",
        uid="9",
        name="NKP",
        description=u"Národní knihovna Praha",
        created="2012-04-18T23:19:16.143+02:00",
        modes=api_structures.Modes(
            by_resolver=True,
            by_registrar=True,
            by_reservation=False,
        )
    )


    assert registrars[1] != api_structures.Registrar(
        code="aba001a",
        uid="9",
        name="NKP",
        description=u"Národní knihovna Praha",
        created="2012-04-18T23:19:16.143+02:00",
        modes=api_structures.Modes(
            by_resolver=False,
            by_registrar=True,
            by_reservation=False,
        )
    )


# def test_register(mono_out_example):
#     mono_out_example = """<?xml version="1.0" encoding="UTF-8"?>
# <r:import xmlns:r="http://resolver.nkp.cz/v3/">
#     <r:monograph>
#         <r:titleInfo>
#             <r:title>Babička</r:title>
#             <r:subTitle>Obrazy z venkovského života</r:subTitle>
#         </r:titleInfo>
#         <r:ccnb>cnb002251177</r:ccnb>
#         <r:isbn>8090119964</r:isbn>
#         <r:otherId>DOI:TODO</r:otherId>
#         <r:documentType>kniha</r:documentType>
#         <r:digitalBorn>false</r:digitalBorn>
#         <r:primaryOriginator type="AUTHOR">Božena Němcová</r:primaryOriginator>
#         <r:otherOriginator>Adolf Kašpar</r:otherOriginator>
#         <r:publication>
#             <r:publisher>Československý spisovatel</r:publisher>
#             <r:place>V Praze</r:place>
#             <r:year>2011</r:year>
#         </r:publication>
#     </r:monograph>
#     <r:digitalDocument>
#         <r:archiverId>3</r:archiverId>
#     </r:digitalDocument>
# </r:import>
# """
#     print rest.register(mono_out_example)
