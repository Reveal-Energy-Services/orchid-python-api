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

from datetime import datetime
import unittest

from hamcrest import assert_that, equal_to, close_to

from orchid.measurement import make_measurement
from orchid.net_quantity import (as_datetime, as_measurement, as_net_date_time, as_net_quantity,
                                 as_net_quantity_in_different_unit, convert_net_quantity_to_different_unit)
import orchid.unit_system as units

import tests.custom_matchers as tcm

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime
# noinspection PyUnresolvedReferences
import UnitsNet


class TestNetMeasurement(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_datetime(self):
        net_time_point = DateTime(2020, 8, 5, 6, 59, 41, 726)
        actual = as_datetime(net_time_point)

        assert_that(actual, equal_to(datetime(2020, 8, 5, 6, 59, 41, 726000)))

    def test_as_measurement(self):
        def make_net_quantity(magnitude, abbreviation):
            quantity = UnitsNet.QuantityValue.op_Implicit(magnitude)
            if abbreviation == 'ft':
                return UnitsNet.Length.From(quantity, UnitsNet.Units.LengthUnit.Foot)
            elif abbreviation == 'm':
                return UnitsNet.Length.From(quantity, UnitsNet.Units.LengthUnit.Meter)
            elif abbreviation == 'lb':
                return UnitsNet.Mass.From(quantity, UnitsNet.Units.MassUnit.Pound)
            elif abbreviation == 'kg':
                return UnitsNet.Mass.From(quantity, UnitsNet.Units.MassUnit.Kilogram)
            elif abbreviation == 'psi':
                return UnitsNet.Pressure.From(quantity, UnitsNet.Units.PressureUnit.PoundForcePerSquareInch)
            elif abbreviation == 'kPa':
                return UnitsNet.Pressure.From(quantity, UnitsNet.Units.PressureUnit.Kilopascal)
            elif abbreviation == 'MPa':
                return UnitsNet.Pressure.From(quantity, UnitsNet.Units.PressureUnit.Megapascal)
            elif abbreviation == 'bbl':
                return UnitsNet.Volume.From(quantity, UnitsNet.Units.VolumeUnit.OilBarrel)
            elif abbreviation == 'm^3':
                return UnitsNet.Volume.From(quantity, UnitsNet.Units.VolumeUnit.CubicMeter)
            else:
                raise ValueError(f'Unhandled abbreviation {abbreviation}')

        for value, unit in [(44.49, 'ft'), (13.56, 'm'),  # length
                            (30.94, 'lb'), (68.21, 'kg'),  # mass
                            (49.70, 'psi'), (342.67, 'kPa'), (0.6071, 'MPa'),  # pressure
                            (83.48, 'bbl'), (13.27, 'm^3')  # volume
                            ]:
            with self.subTest(value=value, unit=unit):
                net_quantity = make_net_quantity(value, unit)
                actual = as_measurement(net_quantity)
                expected = make_measurement(value, unit)
                tcm.assert_that_scalar_quantities_close_to(actual, expected, 6e-3)

    def test_as_net_date_time(self):
        for expected, time_point in [(DateTime(2017, 3, 22, 3, 0, 37, 23),
                                      datetime(2017, 3, 22, 3, 0, 37, 23124)),
                                     (DateTime(2020, 9, 20, 22, 11, 51, 655),
                                      datetime(2020, 9, 20, 22, 11, 51, 654859)),
                                     # The Python `round` function employs "half-even" rounding; however, the
                                     # following test rounds to an *odd* value instead. See the "Note" in the
                                     # Python documentation of `round` for an explanation of this (unexpected)
                                     # behavior.
                                     (DateTime(2022, 2, 2, 23, 35, 39, 979),
                                      datetime(2022, 2, 2, 23, 35, 39, 978531)),
                                     (DateTime(2019, 2, 7, 10, 18, 17, 488),
                                      datetime(2019, 2, 7, 10, 18, 17, 487500)),
                                     (DateTime(2022, 1, 14, 20, 29, 18, 852),
                                      datetime(2022, 1, 14, 20, 29, 18, 852500))
                                     ]:
            with self.subTest(expected=expected, time_point=time_point):
                actual = as_net_date_time(time_point)
                assert_that(actual.Year, equal_to(expected.Year))
                assert_that(actual.Month, equal_to(expected.Month))
                assert_that(actual.Day, equal_to(expected.Day))
                assert_that(actual.Hour, equal_to(expected.Hour))
                assert_that(actual.Minute, equal_to(expected.Minute))
                assert_that(actual.Second, equal_to(expected.Second))
                assert_that(actual.Millisecond, equal_to(expected.Millisecond))

    def test_as_net_quantity(self):
        for measurement, expected_magnitude, expected_unit in \
                [(make_measurement(113.76, units.UsOilfield.LENGTH.abbreviation),
                  113.76, UnitsNet.Units.LengthUnit.Foot),
                 (make_measurement(72.98, units.Metric.LENGTH.abbreviation), 72.98, UnitsNet.Units.LengthUnit.Meter),
                 (make_measurement(6888.89, units.UsOilfield.PRESSURE.abbreviation),
                  6888.89, UnitsNet.Units.PressureUnit.PoundForcePerSquareInch),
                 (make_measurement(59849.82, units.Metric.PRESSURE.abbreviation),
                  59849.82, UnitsNet.Units.PressureUnit.Kilopascal),
                 (make_measurement(42.92, 'MPa'), 42.92, UnitsNet.Units.PressureUnit.Megapascal),
                 (make_measurement(7216.94, 'bbl'), 7216.94, UnitsNet.Units.VolumeUnit.OilBarrel),
                 (make_measurement(1017.09, 'm^3'), 1017.09, UnitsNet.Units.VolumeUnit.CubicMeter)]:
            with self.subTest(actual=measurement, expected_magnitude=expected_magnitude, expected_unit=expected_unit):
                actual = as_net_quantity(measurement)
                assert_that(actual.Unit, equal_to(expected_unit))
                assert_that(actual.Value, close_to(expected_magnitude, 5e-3))

    def test_as_net_length_quantity_in_original_unit(self):
        for measurement in [make_measurement(44.49, 'ft'), make_measurement(25.93, 'm')]:
            with self.subTest(measurement=measurement):
                actual = as_net_quantity(measurement)
                expected_unit = (UnitsNet.Units.LengthUnit.Foot if measurement.unit == 'ft'
                                 else UnitsNet.Units.LengthUnit.Meter)
                assert_that(actual.Unit, equal_to(expected_unit))
                assert_that(actual.As(expected_unit), close_to(measurement.magnitude, 5e-3))

    def test_as_net_length_quantity_in_specified_unit(self):
        for measurement, expected_value, to_unit_abbreviation in [(make_measurement(44.49, 'ft'), 13.56, 'm'),
                                                                  (make_measurement(25.93, 'm'), 85.07, 'ft')]:
            with self.subTest(measurement=measurement, expected_value=expected_value,
                              to_unit_abbreviation_abbreviation=to_unit_abbreviation):
                actual = as_net_quantity_in_different_unit(measurement, to_unit_abbreviation)
                expected_unit = (UnitsNet.Units.LengthUnit.Foot if to_unit_abbreviation == 'ft'
                                 else UnitsNet.Units.LengthUnit.Meter)
                assert_that(actual.Unit, equal_to(expected_unit))
                assert_that(actual.As(expected_unit), close_to(expected_value, 5e-3))

    def test_convert_net_quantity_to_specified_unit(self):
        for measurement, expected_value, to_unit_abbreviation in [(make_measurement(31.44, 'ft'), 31.44, 'ft'),
                                                                  (make_measurement(88.28, 'm'), 88.28, 'm'),
                                                                  (make_measurement(44.49, 'ft'), 13.56, 'm'),
                                                                  (make_measurement(25.93, 'm'), 85.07, 'ft')]:
            with self.subTest(measurement=measurement, expected_value=expected_value,
                              to_unit_abbreviation_abbreviation=to_unit_abbreviation):
                actual_net = as_net_quantity(measurement)
                actual = convert_net_quantity_to_different_unit(actual_net, to_unit_abbreviation)
                expected_unit = (UnitsNet.Units.LengthUnit.Foot if to_unit_abbreviation == 'ft'
                                 else UnitsNet.Units.LengthUnit.Meter)
                assert_that(actual.Unit, equal_to(expected_unit))
                assert_that(actual.As(expected_unit), close_to(expected_value, 5e-3))


if __name__ == '__main__':
    unittest.main()
