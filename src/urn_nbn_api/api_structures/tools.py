#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
def both_set_and_different(first, second):
    """
    If any of both arguments are unset (=``None``), return ``False``. Otherwise
    return result of unequality comparsion.

    Returns:
        bool: True if both arguments are set and different.
    """
    if first is None:
        return False

    if second is None:
        return False

    return first != second


def to_list(tag):
    """
    Put `tag` to list if it ain't list/tuple already.

    Args:
        tag (obj): Anything.

    Returns:
        list: Tag.
    """
    if isinstance(tag, tuple) or isinstance(tag, list):
        return tag

    return [tag]
