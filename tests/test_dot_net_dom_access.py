#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest.mock
import uuid

import deal
from hamcrest import assert_that, equal_to, calling, raises

import orchid.dot_net_dom_access as dna

# noinspection PyUnresolvedReferences
from System import Guid


class StubDomObject(dna.DotNetAdapter):
    stub_property = dna.dom_property('stub_property', '')


class DotNetAdapterTest(unittest.TestCase):
    @staticmethod
    def test_canary():
        assert_that(2 + 2, equal_to(4))

    @staticmethod
    def test_dom_object_returns_adaptee():
        stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
        sut = dna.DotNetAdapter(stub_adaptee)

        assert_that(sut.dom_object(), equal_to(stub_adaptee))

    @staticmethod
    def test_object_id_returns_adaptee_object_id():
        stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
        expected_uuid_text = '218d3a65-edbb-402c-bbd3-c241cf721031'
        stub_adaptee.ObjectId = Guid.Parse(expected_uuid_text)
        sut = dna.DotNetAdapter(stub_adaptee)

        assert_that(sut.object_id, equal_to(uuid.UUID(expected_uuid_text)))

    @staticmethod
    def test_dom_object_no_adapter_raises_error():
        assert_that(calling(dna.DotNetAdapter).with_args(None), raises(deal.PreContractError))


class DomPropertyTest(unittest.TestCase):
    @staticmethod
    def test_canary():
        assert_that(2 + 2, equal_to(4))

    def test_dom_property_returns_int(self):
        expected_values = [-31459, 2.718, 'distractus multum']
        for expected in expected_values:
            with self.subTest(expected=expected):
                stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
                stub_adaptee.StubProperty = expected
                sut = StubDomObject(stub_adaptee)

                assert_that(sut.stub_property, equal_to(expected))


if __name__ == '__main__':
    unittest.main()
