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
from hamcrest import assert_that, equal_to, calling, raises, close_to

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

    def test_correct_slurry_rate_volume_unit_from_known_unit(self):
        units_to_test = ['bbl/min', 'm^3/min', 'm\u00b3/min']
        volume_units = ['bbl', 'm^3', 'm\u00b3']
        for unit, expected in zip(units_to_test, volume_units):
            with self.subTest(unit=unit, expected=expected):
                assert_that(om.slurry_rate_volume_unit(unit), equal_to(expected))

    def test_raises_error_if_unknown_slurry_rate_unit(self):
        unknown_units = ['bbl/m', 'm^3/min\f', '\tbbl/min']
        message_units = ['bbl/m', r'm\^3/min\f', '\tbbl/min']
        for unknown_unit, message_unit in zip(unknown_units, message_units):
            with self.subTest(unknown_unit=unknown_unit, message_unit=message_unit):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.slurry_rate_volume_unit).with_args(unknown_unit),
                            raises(ValueError, pattern=f'"{message_unit}".*[uU]nrecognized'))

    def test_raises_error_if_invalid_slurry_rate_unit(self):
        invalid_units = [None, '', '\r']
        for invalid_unit in invalid_units:
            with self.subTest(invalid_unit=invalid_unit):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.slurry_rate_volume_unit).with_args(invalid_unit), raises(deal.PreContractError))

    def test_correct_proppant_concentration_mass_unit_from_known_unit(self):
        units_to_test = ['lb/gal (U.S.)', 'kg/m^3', 'kg/m\u00b3']
        mass_units = ['lb', 'kg', 'kg']
        for unit, expected in zip(units_to_test, mass_units):
            with self.subTest(unit=unit, expected=expected):
                assert_that(om.proppant_concentration_mass_unit(unit), equal_to(expected))

    def test_raises_error_if_unknown_proppant_concentration_unit(self):
        unknown_units = ['lb/gal', 'kg/m^3\f', '  lb/gal (U.S.)']
        message_units = ['lb/gal', r'kg/m\^3\f', r'  lb/gal \(U.S.\)']
        for unknown_unit, message_unit in zip(unknown_units, message_units):
            with self.subTest(unknown_unit=unknown_unit, message_unit=message_unit):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.proppant_concentration_mass_unit).with_args(unknown_unit),
                            raises(ValueError, pattern=f'"{message_unit}".*[uU]nrecognized'))

    def test_raises_error_if_invalid_proppant_concentration_unit(self):
        invalid_units = [None, '', '\r']
        for invalid_unit in invalid_units:
            with self.subTest(invalid_unit=invalid_unit):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.proppant_concentration_mass_unit).with_args(invalid_unit),
                            raises(deal.PreContractError))

    def test_convert_single_item_values_returns_converted_single_item_values(self):
        # The 6's in the following tolerances are caused by the round half-even that we use in expected values
        for (source_value, source_unit, target_value, target_unit, tolerance) in \
                [(81.4196, 'bbl/min', 1.35699, 'bbl/s', 6e-5),
                 (18.1424, 'm\u00b3/min', 0.302373, 'm^3/s', 6e-7),
                 (18.1424, 'm\u00b3/min', 0.302373, 'm\u00b3/s', 6e-7),
                 (98.4873, 'bbl/min', 68.9411, 'gal/s', 6e-5),
                 (1.04125, 'bbl/s', 43.7325, 'gal/s', 6e-5)]:
            with self.subTest(source_source_unit=source_unit, target_unit=target_unit):
                assert_that(source_value * om.get_conversion_factor(source_unit, target_unit),
                            close_to(target_value, tolerance))

    def test_convert_raises_error_if_source_unit_unknown(self):
        for ((unknown_source, known_target), (source_pattern, target_pattern)) in \
                [(('m^3/m', 'm^3/min'), ('m\\^3/m', 'm\\^3/min')),
                 (('bbl/sec', 'gal/s'), ('bbl/sec', 'gal/s'))]:
            with self.subTest(unknown_source=unknown_source, known_target=known_target,
                              source_pattern=source_pattern, target_pattern=target_pattern):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.get_conversion_factor).with_args(unknown_source, known_target),
                            raises(KeyError, pattern=f"('{source_pattern}', '{target_pattern}')"))

    def test_convert_raises_error_if_target_unit_unknown(self):
        for ((known_source, unknown_target), (source_pattern, target_pattern)) in \
                [(('m^3/min', 'm^3/m'), ('m\\^3/min', 'm\\^3/m')),
                 (('bbl/min', 'gao/s'), ('bbl/min', 'gao/s'))]:
            with self.subTest(known_source=known_source, unknown_target=unknown_target,
                              source_pattern=source_pattern, target_pattern=target_pattern):
                # noinspection SpellCheckingInspection
                assert_that(calling(om.get_conversion_factor).with_args(known_source, unknown_target),
                            raises(KeyError, pattern=f"('{source_pattern}', '{target_pattern}')"))

    def test_convert_raises_error_if_source_unit_invalid(self):
        for invalid_source_unit in [None, '', '\n']:
            with self.subTest(invalid_source_unit=invalid_source_unit):
                assert_that(calling(om.get_conversion_factor).with_args(invalid_source_unit, 'bbl/min'),
                            raises(deal.PreContractError))

    def test_convert_raises_error_if_target_unit_invalid(self):
        for invalid_target_unit in [None, '', '\n']:
            with self.subTest(invalid_target_unit=invalid_target_unit):
                assert_that(calling(om.get_conversion_factor).with_args('m^3/min', invalid_target_unit),
                            raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
