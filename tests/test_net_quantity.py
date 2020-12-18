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

import datetime
import decimal
import unittest

from hamcrest import assert_that, equal_to

from orchid.measurement import make_measurement
from orchid.net_quantity import (as_datetime, as_measurement, as_net_date_time, as_net_quantity,
                                 as_net_quantity_in_different_unit, convert_net_quantity_to_different_unit)
import orchid.unit_system as units

import tests.custom_matchers as tcm

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import (ProppantConcentration, SlurryRate)
# noinspection PyUnresolvedReferences
from System import (DateTime, Double)
# noinspection PyUnresolvedReferences
import UnitsNet


class TestNetMeasurement(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_datetime(self):
        net_time_point = DateTime(2020, 8, 5, 6, 59, 41, 726)
        actual = as_datetime(net_time_point)

        assert_that(actual, equal_to(datetime.datetime(2020, 8, 5, 6, 59, 41, 726000)))

    def test_as_measurement(self):
        for to_convert_net_quantity, expected_value, expected_unit in [
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(3.14)), 3.14, units.DURATION),
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414)), 1.414, units.DURATION),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49)), 44.49, units.UsOilfield.LENGTH),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(13.56)), 13.56, units.Metric.LENGTH),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(30.94)), 30.94, units.UsOilfield.MASS),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(68.21)), 68.21, units.Metric.MASS),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(49.70)),
             49.70, units.UsOilfield.PRESSURE),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(342.67)),
             342.67, units.Metric.PRESSURE),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(83.48)), 83.48, units.UsOilfield.VOLUME),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(13.27)), 13.27, units.Metric.VOLUME),
        ]:
            with self.subTest(expected_value=expected_value, expected_unit=expected_unit,
                              to_convert_net_quantity=to_convert_net_quantity):
                actual = as_measurement(to_convert_net_quantity)
                expected = make_measurement(expected_value, expected_unit)
                tcm.assert_that_scalar_quantities_close_to(actual, expected, 6e-3)

    def test_as_net_date_time(self):
        for expected, time_point in [(DateTime(2017, 3, 22, 3, 0, 37, 23),
                                      datetime.datetime(2017, 3, 22, 3, 0, 37, 23124)),
                                     (DateTime(2020, 9, 20, 22, 11, 51, 655),
                                      datetime.datetime(2020, 9, 20, 22, 11, 51, 654859)),
                                     # The Python `round` function employs "half-even" rounding; however, the
                                     # following test rounds to an *odd* value instead. See the "Note" in the
                                     # Python documentation of `round` for an explanation of this (unexpected)
                                     # behavior.
                                     (DateTime(2022, 2, 2, 23, 35, 39, 979),
                                      datetime.datetime(2022, 2, 2, 23, 35, 39, 978531)),
                                     (DateTime(2019, 2, 7, 10, 18, 17, 488),
                                      datetime.datetime(2019, 2, 7, 10, 18, 17, 487500)),
                                     (DateTime(2022, 1, 14, 20, 29, 18, 852),
                                      datetime.datetime(2022, 1, 14, 20, 29, 18, 852500))
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
                  UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(113.76))),
                 (make_measurement(72.98, units.Metric.LENGTH),
                  UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(72.98))),
                 (make_measurement(7922.36, units.UsOilfield.MASS),
                  UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(7922.36))),
                 (make_measurement(133965.71, units.Metric.MASS),
                  UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(133965.71))),
                 (make_measurement(6888.89, units.UsOilfield.PRESSURE),
                  UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6888.89))),
                 (make_measurement(59849.82, units.Metric.PRESSURE),
                  UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(59849.82))),
                 (make_measurement(3.55, units.UsOilfield.PROPPANT_CONCENTRATION),
                  ProppantConcentration(3.55, units.UsOilfield.MASS.value.net_unit,
                                        units.UsOilfield.VOLUME.value.net_unit)),
                 (make_measurement(425.03, units.Metric.PROPPANT_CONCENTRATION),
                  ProppantConcentration(425.03, units.Metric.MASS.value.net_unit, units.Metric.VOLUME.value.net_unit)),
                 (make_measurement(96.06, units.UsOilfield.SLURRY_RATE),
                  SlurryRate(96.06, units.UsOilfield.VOLUME.value.net_unit, units.DURATION.value.net_unit)),
                 (make_measurement(0.80, units.Metric.SLURRY_RATE),
                  SlurryRate(0.80, units.Metric.VOLUME.value.net_unit, units.DURATION.value.net_unit)),
                 (make_measurement(7216.94, units.UsOilfield.VOLUME),
                  UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(7216.94))),
                 (make_measurement(1017.09, units.Metric.VOLUME),
                  UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1017.09))),
                 ]:
            with self.subTest(to_convert=to_convert_measurement, expected=expected_net_quantity):
                actual = as_net_quantity(to_convert_measurement)
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

    def test_as_net_quantity_in_same_unit(self):
        for to_convert_measurement, expected_net_quantity in [
            (make_measurement(27.18, units.DURATION),
             UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(27.18))),
            (make_measurement(44.49, units.UsOilfield.LENGTH),
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49))),
            (make_measurement(25.93, units.Metric.LENGTH),
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(25.93))),
            (make_measurement(5334.31, units.UsOilfield.MASS),
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(5334.31))),
            (make_measurement(145461.37, units.Metric.MASS),
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(145461.37))),
            (make_measurement(8303.37, units.UsOilfield.PRESSURE),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(8303.37))),
            (make_measurement(64.32, units.Metric.PRESSURE),
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(64.32))),
            (make_measurement(6944.35, units.UsOilfield.VOLUME),
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(6944.35))),
            (make_measurement(880.86, units.Metric.VOLUME),
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(880.86))),
        ]:
            with self.subTest(to_convert_measurement=to_convert_measurement,
                              expected_net_quantity=expected_net_quantity):
                actual = as_net_quantity_in_different_unit(to_convert_measurement, to_convert_measurement.unit)
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

    def test_as_net_quantity_in_different_unit(self):
        for to_convert_measurement, target_unit, expected_net_quantity in [
            (make_measurement(141.51, units.UsOilfield.LENGTH), units.Metric.LENGTH,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(43.13))),
            (make_measurement(43.13, units.Metric.LENGTH), units.UsOilfield.LENGTH,
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(141.51))),
            (make_measurement(4107.64, units.UsOilfield.MASS), units.Metric.MASS,
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1863.19))),
            (make_measurement(1863.19, units.Metric.MASS), units.UsOilfield.MASS,
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(4107.64))),
            (make_measurement(6984.02, units.UsOilfield.PRESSURE), units.Metric.PRESSURE,
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(48153.12))),
            (make_measurement(48153.12, units.Metric.PRESSURE), units.UsOilfield.PRESSURE,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6984.02))),
            (make_measurement(8722.45, units.UsOilfield.VOLUME), units.Metric.VOLUME,
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1386.76))),
            (make_measurement(1386.76, units.Metric.VOLUME), units.UsOilfield.VOLUME,
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8722.45))),
        ]:
            with self.subTest(to_convert_measurement=to_convert_measurement,
                              target_unit=target_unit, expected_net_quantity=expected_net_quantity):
                actual = as_net_quantity_in_different_unit(to_convert_measurement, target_unit)
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, decimal.Decimal('0.01'))

    def test_convert_net_quantity_to_same_unit(self):
        for net_unit, target_unit in [
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(0.1717)), units.DURATION),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(154.67)), units.UsOilfield.LENGTH),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(40.24)), units.Metric.LENGTH),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(3007.29)), units.UsOilfield.MASS),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(123628.53)), units.Metric.MASS),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(7225.05)),
             units.UsOilfield.PRESSURE),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(59.25)), units.Metric.PRESSURE),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8952.96)), units.UsOilfield.VOLUME),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1164.91)), units.Metric.VOLUME),
        ]:
            with self.subTest(net_unit=net_unit, target_unit=target_unit):
                actual = convert_net_quantity_to_different_unit(net_unit, target_unit)
                tcm.assert_that_net_quantities_close_to(actual, net_unit)

    def test_convert_net_quantity_to_different_unit(self):
        for source_net_unit, target_unit, target_net_unit in [
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(155.15)), units.Metric.LENGTH,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(47.29))),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(47.29)), units.UsOilfield.LENGTH,
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(155.15))),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(2614.88)), units.Metric.MASS,
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1186.09))),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1186.09)), units.UsOilfield.MASS,
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(2614.88))),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6427.52)),
             units.Metric.PRESSURE,
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(44316.19))),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(44316.19)), units.UsOilfield.PRESSURE,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6427.52))),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8794.21)), units.Metric.VOLUME,
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1398.17))),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1398.17)), units.UsOilfield.VOLUME,
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8794.21)))
        ]:
            with self.subTest(source_net_unit=source_net_unit, target_unit=target_unit):
                actual = convert_net_quantity_to_different_unit(source_net_unit, target_unit)
                tcm.assert_that_net_quantities_close_to(actual, target_net_unit, decimal.Decimal('0.02'))


if __name__ == '__main__':
    unittest.main()
