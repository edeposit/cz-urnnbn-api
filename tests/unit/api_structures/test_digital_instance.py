#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import pytest

from cz_urnnbn_api.api_structures import DigitalInstance

from ..test_xml_composer import data_context


# Fixtures ====================================================================
@pytest.fixture
def dig_inst_xml():
    return data_context("digital_instances.xml")


@pytest.fixture
def no_dig_inst_xml():
    return data_context("no_digital_instance.xml")


# Tests =======================================================================
def test_from_xml(dig_inst_xml):
    res = DigitalInstance.from_xml(dig_inst_xml)

    assert res
    assert len(res) == 3

    assert res[0] == DigitalInstance(
        uid="33",
        active=True,
        url="http://kramerius.mzk.cz/search/handle/uuid:8ffd7a5b-82da-11e0-bc9f-0050569d679d",
        digital_library_id="37",
        created="2012-09-03T00:44:34.603+02:00",
    )

    assert res[1] == DigitalInstance(
        uid="34",
        active=True,
        url="http://kramerius.mzk.cz/search/handle/uuid:8ffd7a5b-82da-11e0-bc9f-0050569d679d",
        digital_library_id="38",
        format="jpg;pdf",
        created="2012-09-19T00:37:25.362+02:00",
        accessibility="volně přístupné",
    )

    assert res[2] == DigitalInstance(
        uid="35",
        active=False,
        url="http://kramerius.mzk.cz/search/handle/uuid:8ffd7a5b-82da-11e0-bc9f-0050569d679d",
        digital_library_id="12",
        format="jpg;pdf",
        created="2012-09-19T00:39:41.117+02:00",
        deactivated="2012-09-19T00:42:30.334+02:00",
        accessibility="volně přístupné",
    )

    # test that access to non-existent attributes is dissabled
    with pytest.raises(ValueError):
        res[2].asd = 1


def test_from_xml_no_dig_instance(no_dig_inst_xml):
    res = DigitalInstance.from_xml(no_dig_inst_xml)

    assert res == []


def test_to_xml():
    di = DigitalInstance(
        url="http://kramerius3.mzk.cz/kramerius/handle/BOA001/935239",
        digital_library_id="4",
        format="jpg;pdf",
        accessibility="volně přístupné",
    )

    assert di.to_xml() == """<?xml version="1.0" encoding="utf-8"?>
<digitalInstance xmlns="http://resolver.nkp.cz/v3/">
\t<url>http://kramerius3.mzk.cz/kramerius/handle/BOA001/935239</url>
\t<digitalLibraryId>4</digitalLibraryId>
\t<format>jpg;pdf</format>
\t<accessibility>volně přístupné</accessibility>
</digitalInstance>""".encode("utf-8")


def test_to_xml_only_required_arguments():
    di = DigitalInstance(
        url="http://kramerius3.mzk.cz/kramerius/handle/BOA001/935239",
        digital_library_id="4",
    )

    assert di.to_xml() == """<?xml version="1.0" encoding="utf-8"?>
<digitalInstance xmlns="http://resolver.nkp.cz/v3/">
\t<url>http://kramerius3.mzk.cz/kramerius/handle/BOA001/935239</url>
\t<digitalLibraryId>4</digitalLibraryId>
</digitalInstance>""".encode("utf-8")


def test_to_xml_required_arguments_are_really_required():
    with pytest.raises(AssertionError):
        DigitalInstance(url="4", digital_library_id=None).to_xml()

    with pytest.raises(AssertionError):
        DigitalInstance(url=None, digital_library_id="4").to_xml()
