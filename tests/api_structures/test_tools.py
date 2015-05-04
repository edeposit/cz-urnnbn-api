#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from urn_nbn_api.api_structures import tools


# Fixtures ====================================================================
# @pytest.fixture
# def fixture():
#     pass

# with pytest.raises(Exception):
#     raise Exception()


# Tests =======================================================================
def test_to_list():
    assert tools.to_list(1) == [1]

    assert tools.to_list([1]) == [1]
    assert tools.to_list((1,)) == (1,)
