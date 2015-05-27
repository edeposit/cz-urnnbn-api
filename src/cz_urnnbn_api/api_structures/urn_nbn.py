#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class URN_NBN(str):
    """
    Class used to hold URN:NBN string and also other informations returned
    from server.

    Note:
        This class subclasses ``str``, so URN:NBN string can be obtained
        painlessly.

    Attributes:
        value (str): Whole URN:NBN string.
        status (str): ``ACTIVE`` for example.
        registered (str): ISO 8601 date string.
        country_code (str): Code of the country (``cz`` for URN:NBN).
        document_code (str): Part of the URN:NBN holding the code.
        registrar_code (str): Identification of registrar.
        digital_document_id (str): ID of the document.
    """
    def __new__(self, value, *args, **kwargs):
        return super(URN_NBN, self).__new__(self, value)

    def __init__(self, value, status=None, country_code=None,
                 registrar_code=None, document_code=None,
                 digital_document_id=None, registered=None):
        self.value = value

        super(URN_NBN, self).__init__(value)

        self.status = status
        self.registered = registered
        self.country_code = country_code
        self.document_code = document_code
        self.registrar_code = registrar_code
        self.digital_document_id = digital_document_id

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @staticmethod
    def from_xmldict(xdom, tag_picker=lambda x: x["response"]["urnNbn"]):
        """
        Parse itself from `xmldict` structure.
        """
        urn_nbn_tag = tag_picker(xdom)

        return URN_NBN(
            value=urn_nbn_tag["value"],
            status=urn_nbn_tag["status"],
            registered=urn_nbn_tag.get("registered", None),
            country_code=urn_nbn_tag.get("countryCode", None),
            document_code=urn_nbn_tag.get("documentCode", None),
            registrar_code=urn_nbn_tag.get("registrarCode", None),
            digital_document_id=urn_nbn_tag.get("digitalDocumentId", None),
        )
