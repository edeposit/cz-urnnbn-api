#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import faker  # fake-factory module

from cz_urnnbn_api import api
from cz_urnnbn_api import settings
from cz_urnnbn_api import MonographComposer


# Variables ===================================================================
# Fixtures ====================================================================
@pytest.fixture
def reg_code():
    return "edep"


# Tests =======================================================================
def test_is_valid_reg_code(reg_code):
    assert api.is_valid_reg_code(reg_code)


def test_iter_registrars(reg_code):
    registrars = list(api.iter_registrars())

    assert registrars

    assert any(reg for reg in registrars if reg.code == reg_code)


def test_get_registrar_info(reg_code):
    reg_info = api.get_registrar_info(reg_code)

    assert reg_info
    assert reg_info.code == reg_code
    assert reg_info.name == "Edeposit"
    assert not reg_info.description
    assert reg_info.modes == api.Modes(True, True, True)


def test_register_document_obj():
    fake = faker.Factory.create('cz_CZ')

    urn_nbn = api.register_document_obj(
        MonographComposer(
            title=fake.sentence(nb_words=3),
            author=fake.name(),
            format="pdf"
        )
    )

    assert str(urn_nbn)
    assert urn_nbn == api.get_urn_nbn_info(urn_nbn)

    assert api.get_digital_instances(urn_nbn) == []
