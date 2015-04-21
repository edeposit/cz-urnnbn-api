#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from urn_nbn_api import rest


# Functions & classes =========================================================
# @pytest.fixture
# def fixture():
#     pass

# with pytest.raises(Exception):
#     raise Exception()


# Tests =======================================================================
def test_valid_reg_code():
    assert rest.valid_reg_code()
    assert not rest.valid_reg_code("azgabash")
