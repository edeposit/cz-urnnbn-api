#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class Modes(object):
    def __init__(self, by_resolver=False, by_registrar=False,
                 by_reservation=False):
        self.by_resolver = by_resolver
        self.by_registrar = by_registrar
        self.by_reservation = by_reservation


class DigitalLibrary(object):
    def __init__(self, uid, name, description=None, url=None, created=None):
        self.url = url
        self.uid = uid
        self.name = name
        self.created = created
        self.description = description

        # <digitalLibrary id="14">
        #     <name>Kramerius 3</name>
        #     <description>předchozí verze knihovny Kramerius</description>
        #     <url>http://kramerius3.mzk.cz</url>
        #     <created>2012-04-11T11:15:37.660+02:00</created>
        # </digitalLibrary>


class Registrar(object):
    def __init__(self, code, uid, name=None, description=None, created=None,
                 modified=None, modes=None):
        self.uid = uid
        self.code = code
        self.name = name
        self.created = created
        self.modified = modified
        self.description = description

        self.modes = modes if modes else Modes()
        self.digital_libraries = []

    def __repr__(self):
        return "%s:%s" % (self.__class__.__name__, self.code)

        # <registrar code="boa001" id="8">
        #     <name>MZK</name>
        #     <description>Moravská zemská knihovna</description>
        #     <created>2012-04-18T23:19:17.727+02:00</created>
        #     <modified>2012-10-29T10:39:30.882+01:00</modified>
        #     <registrationModes>
        #         <mode name="BY_RESOLVER" enabled="true" />
        #         <mode name="BY_REGISTRAR" enabled="true" />
        #         <mode name="BY_RESERVATION" enabled="true" />
        #     </registrationModes>
        # </registrar>