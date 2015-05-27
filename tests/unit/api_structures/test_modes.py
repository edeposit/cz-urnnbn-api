#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from cz_urnnbn_api.api_structures import Modes


# Tests =======================================================================
def test_modes_creation():
    m = Modes(
        by_resolver=True,
        by_registrar=True,
        by_reservation=True,
    )

    assert m.by_resolver
    assert m.by_registrar
    assert m.by_reservation


    m = Modes(
        by_resolver=False,
        by_registrar=True,
        by_reservation=False,
    )

    assert not m.by_resolver
    assert m.by_registrar
    assert not m.by_reservation


def test_modes_op_equal():
    m = Modes(
        by_resolver=True,
        by_registrar=True,
        by_reservation=True,
    )

    m2 = Modes(
        by_resolver=False,
        by_registrar=True,
        by_reservation=False,
    )

    assert not m == m2
    assert m != m2


def test_modes_op_equal_same_params():
    m = Modes(
        by_resolver=True,
        by_registrar=True,
        by_reservation=True,
    )

    m2 = Modes(
        by_resolver=True,
        by_registrar=True,
        by_reservation=True,
    )

    assert m == m2
    assert not m != m2
