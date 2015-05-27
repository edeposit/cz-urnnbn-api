#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import pytest

from cz_urnnbn_api import api
from cz_urnnbn_api import api_structures

from test_xml_composer import data_context
from test_xml_composer import mono_out_example


# Fixtures ====================================================================
@pytest.fixture
def iter_registrars_data():
    return data_context("iter_registrars_data.xml")


@pytest.fixture
def registrar_data():
    return data_context("registrar_data.xml")


@pytest.fixture
def registration_response():
    return data_context("registration_response.xml")


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
        description="Moravská zemská knihovna",
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
        description="Národní knihovna Praha",
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
        description="Národní knihovna Praha",
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
        description="Národní knihovna Praha",
        created="2012-04-18T23:19:16.143+02:00",
        modes=api_structures.Modes(
            by_resolver=False,
            by_registrar=True,
            by_reservation=False,
        )
    )


def test_get_registrar_info(monkeypatch, registrar_data):
    def send_request(*args, **kwargs):
        return registrar_data

    monkeypatch.setattr(api, "_send_request", send_request)

    registrar = api.get_registrar_info("asd")

    assert registrar.name == "Moravská zemská knihovna - stará digitalizace"
    assert registrar.description == "Před rokem 2012."
    assert registrar.created == "2012-04-11T11:15:37.613+02:00"
    assert registrar.modified == "2013-01-10T09:01:03.690+01:00"
    assert registrar.name == "Moravská zemská knihovna - stará digitalizace"
    assert registrar.name == "Moravská zemská knihovna - stará digitalizace"

    assert registrar.modes == api_structures.Modes(
        by_resolver=True,
        by_registrar=True,
        by_reservation=False,
    )

    assert len(registrar.digital_libraries) == 2

    assert registrar.digital_libraries[0] == api_structures.DigitalLibrary(
        uid="13",
        name="Kramerius 4",
        description="aktuální verze knihovny Kramerius",
        url="http://kramerius.mzk.cz",
        created="2012-04-11T11:15:37.638+02:00",
    )

    assert registrar.digital_libraries[1] == api_structures.DigitalLibrary(
        uid="14",
        name="Kramerius 3",
        description="předchozí verze knihovny Kramerius",
        url="http://kramerius3.mzk.cz",
        created="2012-04-11T11:15:37.660+02:00",
    )

    assert len(registrar.catalogs) == 1

    assert registrar.catalogs[0] == api_structures.Catalog(
        uid="2",
        name="Aleph MZK",
        created="2012-04-11T11:15:38.525+02:00",
        url_prefix="http://aleph.mzk.cz"
    )


def test_register_document(monkeypatch, registration_response):
    def send_request(*args, **kwargs):
        return registration_response

    monkeypatch.setattr(api, "_send_request", send_request)

    response = api.register_document("something")

    assert response == "urn:nbn:cz:edep-00000j"

    assert response.value == "urn:nbn:cz:edep-00000j"
    assert response.status == "ACTIVE"
    assert response.registered == "2015-04-29T17:43:48.399+02:00"
    assert response.country_code == "cz"
    assert response.document_code == "00000j"
    assert response.registrar_code == "edep"
    assert response.digital_document_id == "52974"
