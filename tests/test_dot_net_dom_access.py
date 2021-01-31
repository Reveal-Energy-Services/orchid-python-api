#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import datetime
import unittest.mock
import uuid

import dateutil.tz
import deal
from hamcrest import assert_that, equal_to, calling, raises, close_to, is_, none, not_none

from orchid import (
    dot_net_dom_access as dna,
    net_quantity as onq,
    obs_unit_system as units,
)

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, Guid


def increment(n):
    return n + 1


class StubDomObject(dna.DotNetAdapter):
    stub_property = dna.dom_property('stub_property', '')
    stub_date_time = dna.transformed_dom_property('stub_date_time', '', onq.as_datetime)
    stub_transformed_iterator = dna.transformed_dom_property_iterator('stub_transformed_iterator', '', increment)


class DotNetAdapterTest(unittest.TestCase):
    @staticmethod
    def test_canary():
        assert_that(2 + 2, equal_to(4))

    @staticmethod
    def test_dom_object_returns_adaptee():
        stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
        sut = dna.DotNetAdapter(stub_adaptee)

        assert_that(sut.dom_object, equal_to(stub_adaptee))

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

    @staticmethod
    def test_maybe_project_units_returns_none_if_net_project_callable_none():
        stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
        sut = dna.DotNetAdapter(stub_adaptee)

        assert_that(sut.maybe_project_units, is_(none()))

    @unittest.mock.patch('orchid.obs_unit_system.as_unit_system')
    def test_maybe_project_units_returns_none_if_net_project_callable_not_none(self, mock_as_unit_system):
        mock_as_unit_system.return_value = units.Metric
        stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
        sut = dna.DotNetAdapter(stub_adaptee, unittest.mock.MagicMock(name='net_project_callable'))

        assert_that(sut.maybe_project_units, is_(not_none()))


class DomPropertyTest(unittest.TestCase):
    @staticmethod
    def test_canary():
        assert_that(2 + 2, equal_to(4))

    def test_dom_property_returns_int(self):
        expected_values = [-31459, 2.718, 'distractus multum']
        for expected in expected_values:
            with self.subTest(f'Test dom_property() returns {expected}'):
                stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
                stub_adaptee.StubProperty = expected
                sut = StubDomObject(stub_adaptee)

                assert_that(sut.stub_property, equal_to(expected))

    @staticmethod
    def test_transformed_dom_property_returns_datetime():
        expected = datetime.datetime(2016, 10, 16, 1, 44, 56, 305000, tzinfo=dateutil.tz.UTC)
        actual = DateTime(2016, 10, 16, 1, 44, 56, 305, DateTimeKind.Utc)
        stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
        stub_adaptee.StubDateTime = actual
        sut = StubDomObject(stub_adaptee)

        assert_that(sut.stub_date_time, equal_to(expected))

    def test_transformed_dom_property_iterator_returns_transformed(self):
        all_original_values = [[], [-34159], [2.718, -1.414, 1.717]]
        all_expected_values = [[], [-34158], [3.718, -0.414, 2.717]]
        for original_values, expected_values in zip(all_original_values, all_expected_values):
            with self.subTest(f'Test transformed_dom_property returns values, {original_values}, incremented by one.'):
                stub_adaptee = unittest.mock.MagicMock(name='stub_adaptee')
                stub_adaptee.StubTransformedIterator.Items = original_values
                sut = StubDomObject(stub_adaptee)
                actual_values = list(sut.stub_transformed_iterator)

                for actual, expected in zip(actual_values, expected_values):
                    assert_that(actual, close_to(expected, 6e-4))


if __name__ == '__main__':
    unittest.main()
