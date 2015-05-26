#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from modes import Modes
from catalog import Catalog
from digital_library import DigitalLibrary

from tools import to_list
from tools import both_set_and_different


# Functions & classes =========================================================
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
            both_set_and_different(self.name, other.name),
            both_set_and_different(self.description, other.description),
            both_set_and_different(self.created, other.created),
            both_set_and_different(self.modified, other.modified),
            both_set_and_different(self.modes, other.modes),
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
    def from_xmldict(reg_tag):
        """
        Parse basic information about registrar.

        Args:
            reg_tag (obj): OrderedDict returned from :mod:`xmltodict`.

        Returns:
            obj: :class:`.Registrar` instance with basic informations.
        """
        # parse Registrar data
        registrar = Registrar(
            code=reg_tag["@code"],
            uid=reg_tag["@id"],
            name=reg_tag["name"],
            description=reg_tag.get("description", None),
            created=reg_tag["created"],
            modified=reg_tag.get("modified", None),
            modes=Modes.from_xmldict(
                reg_tag["registrationModes"]["mode"]
            )
        )

        if not reg_tag.get("digitalLibraries", None):
            return registrar

        # parse digital_libraries
        for dl_tag in to_list(reg_tag["digitalLibraries"]["digitalLibrary"]):
            registrar.digital_libraries.append(
                DigitalLibrary(
                    uid=dl_tag["@id"],
                    name=dl_tag["name"],
                    description=dl_tag.get("description", None),
                    url=dl_tag.get("url", None),
                    created=dl_tag.get("created", None),
                )
            )

        if not reg_tag.get("catalogs", None):
            return registrar

        # parse catalogs
        for catalog_tag in to_list(reg_tag["catalogs"]["catalog"]):
            registrar.catalogs.append(
                Catalog(
                    uid=catalog_tag["@id"],
                    name=catalog_tag["name"],
                    url_prefix=catalog_tag.get("urlPrefix", None),
                    created=catalog_tag.get("created", None),
                )
            )

        return registrar
