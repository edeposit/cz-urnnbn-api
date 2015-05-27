#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from cz_urnnbn_api.api_structures import tools


# Tests =======================================================================
def test_to_list():
    assert tools.to_list(1) == [1]

    assert tools.to_list([1]) == [1]
    assert tools.to_list((1,)) == (1,)


def test_both_set_and_different():
    assert not tools.both_set_and_different(None, 1)
    assert not tools.both_set_and_different(1, None)
    assert not tools.both_set_and_different(None, None)

    assert not tools.both_set_and_different(1, 1)
    assert tools.both_set_and_different(1, 2)
