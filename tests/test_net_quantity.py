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


from orchid import (measurement as om,
                    net_quantity as onq,
                    physical_quantity as opq,
                    unit_system as units)

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
        actual = onq.as_datetime(net_time_point)

        assert_that(actual, equal_to(datetime.datetime(2020, 8, 5, 6, 59, 41, 726000)))

    def test_as_measurement(self):
        for to_convert_net_quantity, to_convert_physical_quantity, expected_value, expected_unit, tolerance in [
            (UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(306.08)), opq.PhysicalQuantity.ANGLE,
             306.08, units.common[opq.ANGLE], decimal.Decimal('0.01')),
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414)), opq.PhysicalQuantity.DURATION,
             1.414, units.common[opq.DURATION], decimal.Decimal('0.001')),
            (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(0.05)),
             opq.PhysicalQuantity.DENSITY, 0.05, units.us_oilfield[opq.DENSITY], decimal.Decimal('0.01')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(3257.82)),
             opq.PhysicalQuantity.DENSITY, 3257.82, units.metric[opq.DENSITY], decimal.Decimal('0.01')),
            (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(4.312e10)),
             opq.PhysicalQuantity.ENERGY, 4.312e10, units.us_oilfield[opq.ENERGY], decimal.Decimal('0.001e10')),
            (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(14220)), opq.PhysicalQuantity.ENERGY,
             14220, units.metric[opq.ENERGY], decimal.Decimal('10')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(44.49)), opq.PhysicalQuantity.FORCE,
             44.49, units.us_oilfield[opq.FORCE], decimal.Decimal('0.01')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(13.56)), opq.PhysicalQuantity.FORCE,
             13.56, units.metric[opq.FORCE], decimal.Decimal('0.01')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(100994)),
             opq.PhysicalQuantity.FORCE, 100994, units.us_oilfield[opq.FORCE], decimal.Decimal('1')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(441172)),
             opq.PhysicalQuantity.FORCE, 441172, units.metric[opq.FORCE], decimal.Decimal('1')),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49)), opq.PhysicalQuantity.LENGTH,
             44.49, units.us_oilfield[opq.LENGTH], decimal.Decimal('0.01')),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(13.56)), opq.PhysicalQuantity.LENGTH,
             13.56, units.metric[opq.LENGTH], decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(30.94)), opq.PhysicalQuantity.MASS,
             30.94, units.us_oilfield[opq.MASS], decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(68.21)), opq.PhysicalQuantity.MASS,
             68.21, units.metric[opq.MASS], decimal.Decimal('0.01')),
            (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(23276)),
             opq.PhysicalQuantity.POWER, 23276, units.us_oilfield[opq.POWER], decimal.Decimal('1')),
            (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(21.05)), opq.PhysicalQuantity.POWER,
             21.05, units.metric[opq.POWER], decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(49.70)),
             opq.PhysicalQuantity.PRESSURE, 49.70, units.us_oilfield[opq.PRESSURE], decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(342.67)),
             opq.PhysicalQuantity.PRESSURE, 342.67, units.metric[opq.PRESSURE], decimal.Decimal('0.01')),
            (ProppantConcentration(3.82, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION, 3.82, units.us_oilfield[opq.PROPPANT_CONCENTRATION],
             decimal.Decimal('0.01')),
            (ProppantConcentration(457.35, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION, 457.35, units.metric[opq.PROPPANT_CONCENTRATION],
             decimal.Decimal('0.01')),
            (SlurryRate(114.59, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             opq.PhysicalQuantity.SLURRY_RATE, 114.59, units.us_oilfield[opq.SLURRY_RATE], decimal.Decimal('0.01')),
            (SlurryRate(18.22, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             opq.PhysicalQuantity.SLURRY_RATE, 18.22, units.metric[opq.SLURRY_RATE], decimal.Decimal('0.01')),
            # (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(83.48)),
            #  83.48, units.us_oilfield[opq.VOLUME]),
            # (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(13.27)),
            #  13.27, units.metric[opq.VOLUME]),
        ]:
            with self.subTest():
                actual = onq.as_measurement(to_convert_net_quantity, to_convert_physical_quantity)
                expected = expected_value * expected_unit
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

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
                actual = onq.as_net_date_time(time_point)
                assert_that(actual.Year, equal_to(expected.Year))
                assert_that(actual.Month, equal_to(expected.Month))
                assert_that(actual.Day, equal_to(expected.Day))
                assert_that(actual.Hour, equal_to(expected.Hour))
                assert_that(actual.Minute, equal_to(expected.Minute))
                assert_that(actual.Second, equal_to(expected.Second))
                assert_that(actual.Millisecond, equal_to(expected.Millisecond))

    def test_as_net_quantity(self):
        for to_convert_measurement, expected_net_quantity in [
            (67.07 * units.common[opq.ANGLE],
             UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(67.07))),
            (1.414 * units.common[opq.DURATION],
             UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414))),
            (17.17 * units.us_oilfield[opq.DENSITY],
             UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(17.17))),
            (2.72 * units.metric[opq.DENSITY],
             UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(2.72))),
            (113.76 * units.us_oilfield[opq.LENGTH],
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(113.76))),
            (72.98 * units.metric[opq.LENGTH],
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(72.98))),
            (7922.36 * units.us_oilfield[opq.MASS],
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(7922.36))),
            (133965.71 * units.metric[opq.MASS],
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(133965.71))),
            (6888.89 * units.us_oilfield[opq.PRESSURE],
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6888.89))),
            (59849.82 * units.metric[opq.PRESSURE],
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(59849.82))),
            (3.55 * units.us_oilfield[opq.PROPPANT_CONCENTRATION],
             ProppantConcentration(3.55, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon)),
            (425.03 * units.metric[opq.PROPPANT_CONCENTRATION],
             ProppantConcentration(425.03, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter)),
            (96.06 * units.us_oilfield[opq.SLURRY_RATE],
             SlurryRate(96.06, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute)),
            (0.80 * units.metric[opq.SLURRY_RATE],
             SlurryRate(0.80, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute)),
            (7216.94 * units.us_oilfield[opq.VOLUME],
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(7216.94))),
            (1017.09 * units.metric[opq.VOLUME],
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1017.09))),
        ]:
            with self.subTest(to_convert=to_convert_measurement, expected=expected_net_quantity):
                actual = onq.as_net_quantity(to_convert_measurement)
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

    def test_as_net_quantity_in_same_unit(self):
        for to_convert_measurement, expected_net_quantity in [
            (om.make_measurement(27.18, units.common[opq.DURATION]),
             UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(27.18))),
            (om.make_measurement(44.49, units.us_oilfield[opq.LENGTH]),
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49))),
            (om.make_measurement(25.93, units.metric[opq.LENGTH]),
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(25.93))),
            (om.make_measurement(5334.31, units.us_oilfield[opq.MASS]),
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(5334.31))),
            (om.make_measurement(145461.37, units.metric[opq.MASS]),
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(145461.37))),
            (om.make_measurement(8303.37, units.us_oilfield[opq.PRESSURE]),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(8303.37))),
            (om.make_measurement(64.32, units.metric[opq.PRESSURE]),
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(64.32))),
            (om.make_measurement(6944.35, units.us_oilfield[opq.VOLUME]),
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(6944.35))),
            (om.make_measurement(880.86, units.metric[opq.VOLUME]),
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(880.86))),
        ]:
            with self.subTest(to_convert_measurement=to_convert_measurement,
                              expected_net_quantity=expected_net_quantity):
                actual = onq.as_net_quantity_in_different_unit(to_convert_measurement, to_convert_measurement.unit)
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

    def test_as_net_quantity_in_different_unit(self):
        for to_convert_measurement, target_unit, expected_net_quantity in [
            ((141.51 * units.us_oilfield[opq.LENGTH]), units.metric[opq.LENGTH],
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(43.13))),
            (43.13 * units.metric[opq.LENGTH], units.us_oilfield[opq.LENGTH],
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(141.51))),
            (4107.64 * units.us_oilfield[opq.MASS], units.metric[opq.MASS],
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1863.19))),
            (1863.19 * units.metric[opq.MASS], units.us_oilfield[opq.MASS],
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(4107.64))),
            (6984.02 * units.us_oilfield[opq.PRESSURE], units.metric[opq.PRESSURE],
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(48153.12))),
            (48153.12 * units.metric[opq.PRESSURE], units.us_oilfield[opq.PRESSURE],
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6984.02))),
            (8722.45 * units.us_oilfield[opq.VOLUME], units.metric[opq.VOLUME],
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1386.76))),
            (1386.76 * units.metric[opq.VOLUME], units.us_oilfield[opq.VOLUME],
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8722.45))),
        ]:
            with self.subTest(to_convert_measurement=to_convert_measurement,
                              target_unit=target_unit, expected_net_quantity=expected_net_quantity):
                actual = onq.as_net_quantity_in_different_unit(to_convert_measurement, target_unit)
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
                actual = onq.convert_net_quantity_to_different_unit(net_unit, target_unit)
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
                actual = onq.convert_net_quantity_to_different_unit(source_net_unit, target_unit)
                tcm.assert_that_net_quantities_close_to(actual, target_net_unit, decimal.Decimal('0.02'))

    def test_is_minute(self):
        for to_test, expected_is_minute in [
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(107498.21)), False),
            (ProppantConcentration(5.68, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon), False),
            (SlurryRate(12.23, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute), False),
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(31.41)), True),
        ]:
            with self.subTest(to_test=to_test, expected_is_ratio=expected_is_minute):
                actual_is_minute = onq._is_minute_unit(to_test)

                assert_that(actual_is_minute, equal_to(expected_is_minute), f'Is minute for "{str(to_test)}".')

    def test_is_ratio(self):
        for to_test, expected_is_ratio in [
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(170.43)), False),
            (ProppantConcentration(5.68, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon), True),
            (SlurryRate(12.23, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute), True),
        ]:
            with self.subTest(to_test=to_test, expected_is_ratio=expected_is_ratio):
                actual_is_ratio = onq._is_ratio_unit(to_test)

                assert_that(actual_is_ratio, equal_to(expected_is_ratio), f'Is ratio for "{str(to_test)}".')

    def test_ratio_units(self):
        for to_test, expected_ratio_units in [
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(
                UnitsNet.QuantityValue.op_Implicit(7735.08)), ()),
            (ProppantConcentration(5.68, UnitsNet.Units.MassUnit.Pound,
                                   UnitsNet.Units.VolumeUnit.UsGallon),
             (UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon)),
            (SlurryRate(12.32, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             (UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute)),
        ]:
            with self.subTest(to_test=to_test, expected_ratio_units=expected_ratio_units):
                actual_ratio_units = onq._ratio_units(to_test)

                assert_that(actual_ratio_units, equal_to(expected_ratio_units))


if __name__ == '__main__':
    unittest.main()
