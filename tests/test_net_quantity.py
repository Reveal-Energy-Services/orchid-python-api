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


UNIT_CREATE_NET_UNIT_MAP = {
    units.UsOilfield.LENGTH: lambda q: UnitsNet.Length.FromFeet(q),
    units.Metric.LENGTH: lambda q: UnitsNet.Length.FromMeters(q),
    units.UsOilfield.MASS: lambda q: UnitsNet.Mass.FromPounds(q),
    units.Metric.MASS: lambda q: UnitsNet.Mass.FromKilograms(q),
    units.UsOilfield.PRESSURE: lambda q: UnitsNet.Pressure.FromPoundsForcePerSquareInch(q),
    units.Metric.PRESSURE: lambda q: UnitsNet.Pressure.FromKilopascals(q),
    units.UsOilfield.VOLUME: lambda q: UnitsNet.Volume.FromOilBarrels(q),
    units.Metric.VOLUME: lambda q: UnitsNet.Volume.FromCubicMeters(q),
}


def make_net_quantity(magnitude, unit):
    quantity = UnitsNet.QuantityValue.op_Implicit(magnitude)
    return UNIT_CREATE_NET_UNIT_MAP[unit](quantity)


class TestNetMeasurement(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_datetime(self):
        net_time_point = DateTime(2020, 8, 5, 6, 59, 41, 726)
        actual = as_datetime(net_time_point)

        assert_that(actual, equal_to(datetime(2020, 8, 5, 6, 59, 41, 726000)))

    def test_as_measurement(self):
        for value, unit in [(44.49, units.UsOilfield.LENGTH), (13.56, units.Metric.LENGTH),
                            (30.94, units.UsOilfield.MASS), (68.21, units.Metric.MASS),
                            (49.70, units.UsOilfield.PRESSURE), (342.67, units.Metric.PRESSURE),
                            (83.48, units.UsOilfield.VOLUME), (13.27, units.Metric.VOLUME)
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
        for to_convert_measurement, expected_net_quantity in \
                [(make_measurement(113.76, units.UsOilfield.LENGTH),
                  make_net_quantity(113.76, units.UsOilfield.LENGTH)),
                 # (make_measurement(72.98, units.Metric.LENGTH),
                 #  make_net_quantity(72.98, units.Metric.LENGTH)),
                 # (make_measurement(7922.36, units.UsOilfield.MASS),
                 #  make_net_quantity(7922.36, units.UsOilfield.MASS)),
                 # (make_measurement(133965.71, units.Metric.MASS),
                 #  make_net_quantity(133965.71, units.Metric.MASS)),
                 # (make_measurement(6888.89, units.UsOilfield.PRESSURE),
                 #  make_net_quantity(6888.89, units.UsOilfield.PRESSURE)),
                 # (make_measurement(59849.82, units.Metric.PRESSURE),
                 #  make_net_quantity(59849.82, units.Metric.PRESSURE)),
                 # (make_measurement(7216.94, units.UsOilfield.VOLUME),
                 #  make_net_quantity(7216.94, units.UsOilfield.VOLUME)),
                 # (make_measurement(1017.09, units.Metric.VOLUME),
                 #  make_net_quantity(1017.09, units.Metric.VOLUME)),
                 ]:
            with self.subTest(to_convert=to_convert_measurement, expected=expected_net_quantity):
                print(f'{to_convert_measurement=}')
                actual = as_net_quantity(to_convert_measurement)
                print(f'actual={str(actual)}')
                print(f'expected_net_quantity={str(expected_net_quantity)}')
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

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
