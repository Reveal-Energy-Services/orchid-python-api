#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

import unittest

import deal
from hamcrest import assert_that, equal_to, calling, raises, close_to

import orchid.measurement as om
import orchid.unit_system as units


class TestMeasurement(unittest.TestCase):
    """Implements the unit tests for the orchid.measurement module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_magnitude_is_supplied_magnitude_to_make_measurement(self):
        for magnitude, unit in [(877.26, units.Metric.PRESSURE),
                                (3, units.UsOilfield.VOLUME)  # Testing an integral magnitude against contract
                                ]:
            with self.subTest(magnitude=magnitude, unit=unit):
                sut = om.make_measurement(magnitude, unit)

                assert_that(sut.magnitude, equal_to(magnitude))

    def test_unit_is_supplied_unit_to_make_measurement(self):
        sut = om.make_measurement(138.44, units.UsOilfield.LENGTH)

        assert_that(sut.unit, equal_to(units.UsOilfield.LENGTH))

    def test_make_measurement_raises_exception_if_invalid_magnitude(self):
        assert_that(calling(om.make_measurement).with_args(complex(3.14, 2.72), units.UsOilfield.VOLUME),
                    raises(deal.PreContractError))

    def test_make_measurement_raises_exception_if_invalid_unit(self):
        assert_that(calling(om.make_measurement).with_args(1.717, 'm^3'),
                    raises(deal.PreContractError))

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
                 (1.04125, 'bbl/s', 43.7325, 'gal/s', 6e-5),
                 (13.5354, 'm\u00b3', 85.1351, 'bbl', 6e-5),
                 (445.683, 'kg', 982.562, 'lb', 6e-4),
                 (165.501, 'kPa', 24.0039, 'psi', 6e-5)]:
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
