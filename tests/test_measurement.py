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

import unittest

import deal
from hamcrest import assert_that, equal_to, calling, raises, empty
import numpy as np
import numpy.testing as npt
import toolz.curried as toolz

import orchid.measurement as om


class TestMeasurement(unittest.TestCase):
    """Implements the unit tests for the orchid.measurement module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_has_magnitude_set_in_ctor(self):
        sut = om.make_measurement(74.168, 'm')
        assert_that(74.168, sut.magnitude)

    def test_has_unit_set_in_ctor(self):
        sut = om.make_measurement(74.168, 'm')
        assert_that('m', sut.unit)

    def test_ctor_raises_error_if_invalid_magnitude(self):
        for invalid_magnitude in [None, [], 7 - 3j]:
            with self.subTest(invalid_magnitude=invalid_magnitude):
                assert_that(calling(om.make_measurement).with_args(invalid_magnitude, 'psi'),
                            raises(deal.PreContractError))

    def test_ctor_raises_error_if_invalid_unit(self):
        for invalid_unit in [None, '', '\v']:
            with self.subTest(invalid_unit=invalid_unit):
                assert_that(calling(om.make_measurement).with_args(1, invalid_unit), raises(deal.PreContractError))

    def test_correct_volume_unit_from_known_unit(self):
        units = ['bbl/min', 'm^3/min']
        volume_units = ['bbl', 'm^3']
        for unit, expected in zip(units, volume_units):
            with self.subTest(unit=unit, expected=expected):
                assert_that(om.volume_unit(unit), equal_to(expected))

    def test_raises_error_if_unknown_unit(self):
        unknown_units = ['bbl/m', 'm^3/min\f', '\tbbl/min']
        message_units = ['bbl/m', 'm\\^3/min\f', '\tbbl/min']
        for unknown_unit, message_unit in zip(unknown_units, message_units):
            with self.subTest(unknown_unit=unknown_unit, message_unit=message_unit):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.volume_unit).with_args(unknown_unit),
                            raises(ValueError, pattern=f'"{message_unit}".*[uU]nrecognized'))

    def test_raises_error_if_invalid_unit(self):
        invalid_units = [None, '', '\r']
        for invalid_unit in invalid_units:
            with self.subTest(invalid_unit=invalid_unit):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.volume_unit).with_args(invalid_unit), raises(deal.PreContractError))

    def test_convert_empty_np_values_returns_empty_values(self):
        source_unit = 'm^3/min'
        target_unit = 'm^3/s'
        source_values = []

        assert_that(om.convert_np_values(np.array(source_values, dtype=np.uint32), source_unit, target_unit), empty())

    def test_convert_single_item_values_returns_converted_single_item_values(self):
        source_unit = 'm^3/min'
        target_unit = 'm^3/s'
        source_values = [18.1424]
        target_values = [0.302373]

        npt.assert_allclose(om.convert_np_values(np.array(source_values), source_unit, target_unit),
                            np.array(target_values), atol=5e-7)

    def test_convert_many_items_values_returns_converted_many_items_values(self):
        source_unit = 'bbl/min'
        target_unit = 'bbl/s'
        source_values = [81.4196, 87.7374, 75.9090]
        target_values = [1.35699, 1.46229, 1.26515]

        npt.assert_allclose(om.convert_np_values(np.array(source_values), source_unit, target_unit),
                            np.array(target_values), atol=5e-6)

    def test_convert_raises_error_if_source_unit_unknown(self):
        # noinspection SpellCheckingInspection
        assert_that(calling(om.convert_np_values).with_args(np.array([3.14]), 'm^3/m', 'm^3/min'),
                    raises(ValueError, pattern=f'"m\\^3/m".*[uU]nrecognized'))

    def test_convert_raises_error_if_target_unit_unknown(self):
        # noinspection SpellCheckingInspection
        assert_that(calling(om.convert_np_values).with_args(np.array([3.14]), 'm^3/min', 'm^3/m'),
                    raises(ValueError, pattern=f'"m\\^3/m".*[uU]nrecognized'))

    def test_convert_raises_error_if_values_is_none(self):
        assert_that(calling(om.convert_np_values).with_args(None, '', ''), raises(deal.PreContractError))

    def test_convert_raises_error_if_values_invalid(self):
        for invalid_values in toolz.map(np.array, [['a'], [True], [3 + 5j]]):
            with self.subTest(invalid_values=invalid_values):
                assert_that(calling(om.convert_np_values).with_args(invalid_values, '', ''),
                            raises(deal.PreContractError))

    def test_convert_raises_error_if_source_unit_invalid(self):
        for invalid_source_unit in [None, '', '\n']:
            with self.subTest(invalid_source_unit=invalid_source_unit):
                assert_that(calling(om.convert_np_values).with_args(np.array([2.72]), invalid_source_unit, 'bbl/min'),
                            raises(deal.PreContractError))

    def test_convert_raises_error_if_target_unit_invalid(self):
        for invalid_target_unit in [None, '', '\n']:
            with self.subTest(invalid_target_unit=invalid_target_unit):
                assert_that(calling(om.convert_np_values).with_args(np.array([2.72]), 'm^3/min', invalid_target_unit),
                            raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
