#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
def _by_attr(xdom, attr):
    """
    From `xdom` pick element with attributes defined by `attr`.

    Args:
        xdom (obj): DOM parsed by :mod:`xmltodict`.
        attr (dict): Dictionary defining all the arguments.

    Returns:
        obj: List in case that multiple records were returned, or OrderedDict \
             instance in case that there was only one. Blank array in case of \
             no matching tag.
    """
    out = []

    for tag in xdom:
        for attr_name, val in attr.iteritems():
            if attr_name not in tag:
                break

            if val is not None and tag[attr_name] != val:
                break

            out.append(tag)

    return out[0] if len(out) == 1 else out


class Modes(object):
    """
    Container holding informations about modes which may be used by registrar
    to register documents.

    Attributes:
        by_resolver (bool): True if the mode can be used.
        by_registrar (bool): True if the mode can be used.
        by_reservation (bool): True if the mode can be used.
    """
    def __init__(self, by_resolver=False, by_registrar=False,
                 by_reservation=False):
        self.by_resolver = by_resolver
        self.by_registrar = by_registrar
        self.by_reservation = by_reservation

    def __eq__(self, other):
        return all([
            self.by_resolver == other.by_resolver,
            self.by_registrar == other.by_registrar,
            self.by_reservation == other.by_reservation,
        ])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Modes(%r%r%r)" % (
            self.by_resolver,
            self.by_registrar,
            self.by_reservation
        )

    @staticmethod
    def from_xmldict(modes_tag):
        """
        Parse Modes information from XML.

        Args:
            modes_tags (obj): OrderedDict ``<modes>`` tag returned from
                      :mod:`xmltodict`.

        Returns:
            obj: :class:`.Modes` instance.
        """
        by_resolver = _by_attr(modes_tag, attr={"@name": "BY_RESOLVER"})
        by_registrar = _by_attr(modes_tag, attr={"@name": "BY_REGISTRAR"})
        by_reservation = _by_attr(modes_tag, attr={"@name": "BY_RESERVATION"})

        return Modes(
            by_resolver=by_resolver["@enabled"].lower() == "true",
            by_registrar=by_registrar["@enabled"].lower() == "true",
            by_reservation=by_reservation["@enabled"].lower() == "true",
        )
