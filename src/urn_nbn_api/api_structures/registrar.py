#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from modes import Modes


# Functions & classes =========================================================
def _both_set_and_different(first, second):
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


class Registrar(object):
    """
    Class holding informations about Registrar.

    Attributes:
        uid (str): Id of the registrar in URN:NBN system.
        code (str): Code of the registrar. Each organization has own.
        name (str): Full name of the registrar.
        created (str): ISO 8601 date string.
        modified (str): ISO 8601 date string.
        description (str): Description of the registrar.
        modes (obj): :class:`.Modes` instance with informations about allowed
                     modes.
        catalogs (list): List of :class:`.Catalog` instances with informations
                 about catalogs used by this registrar.
        digital_libraries (list): List of :class:`.DigitalLibrary` instances
                          with informations about digital libraries used by
                          registrar.
    """
    def __init__(self, code, uid, name=None, description=None, created=None,
                 modified=None, modes=None):
        self.uid = uid
        self.code = code
        self.name = name
        self.created = created
        self.modified = modified
        self.description = description

        self.modes = modes
        self.catalogs = []
        self.digital_libraries = []

    def __repr__(self):
        return "%s:%s" % (self.__class__.__name__, self.code)

    def __eq__(self, other):
        if not (self.uid == other.uid and self.code == other.code):
            return False

        not_important_checks = any([
            _both_set_and_different(self.name, other.name),
            _both_set_and_different(self.description, other.description),
            _both_set_and_different(self.created, other.created),
            _both_set_and_different(self.modified, other.modified),
            _both_set_and_different(self.modes, other.modes),
        ])
        if not_important_checks:
            return False

        return all([
            set(self.catalogs) == set(other.catalogs),
            set(self.digital_libraries) == set(other.digital_libraries)
        ])

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def from_xml_ordereddict(reg_tag):
        """
        Parse basic information about registrar.

        Args:
            reg_tag (obj): OrderedDict returned from :mod:`xmltodict`.

        Returns:
            obj: :class:`.Registrar` instance with basic informations.
        """
        # parse modes
        modes_tag = reg_tag["registrationModes"]["mode"]

        by_resolver = _by_attr(modes_tag, attr={"@name": "BY_RESOLVER"})
        by_registrar = _by_attr(modes_tag, attr={"@name": "BY_REGISTRAR"})
        by_reservation = _by_attr(modes_tag, attr={"@name": "BY_RESERVATION"})

        modes = Modes(
            by_resolver=by_resolver["@enabled"].lower() == "true",
            by_registrar=by_registrar["@enabled"].lower() == "true",
            by_reservation=by_reservation["@enabled"].lower() == "true",
        )

        # parse Registrar data
        return Registrar(
            code=reg_tag["@code"],
            uid=reg_tag["@id"],
            name=reg_tag["name"],
            description=reg_tag.get("description", None),
            created=reg_tag["created"],
            modified=reg_tag.get("modified", None),
            modes=modes
        )
