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

from hamcrest import assert_that, equal_to, close_to


from orchid import (measurement as om,
                    net_quantity as onq,
                    physical_quantity as opq,
                    unit_system as units)

import tests.custom_matchers as tcm

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import (ProppantConcentration, SlurryRate)
# noinspection PyUnresolvedReferences
from System import (DateTime, Decimal)
# noinspection PyUnresolvedReferences
import UnitsNet


def assert_that_net_power_quantities_close_to(actual, expected_net_quantity, tolerance=6e-3):
    assert_that(tcm.get_net_unit(actual), equal_to(tcm.get_net_unit(expected_net_quantity)))
    to_test_actual = decimal.Decimal(onq.net_decimal_to_float(actual.Value))
    to_test_expected = decimal.Decimal(onq.net_decimal_to_float(expected_net_quantity.Value))
    to_test_tolerance = decimal.Decimal(tolerance)
    assert_that(to_test_actual, close_to(to_test_expected, to_test_tolerance))


def is_power_measurement(measurement):
    return measurement.unit == units.UsOilfield.POWER or measurement.unit == units.Metric.POWER


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
             306.08, units.Common.ANGLE, decimal.Decimal('0.01')),
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414)), opq.PhysicalQuantity.DURATION,
             1.414, units.Common.DURATION, decimal.Decimal('0.001')),
            (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(0.05)),
             opq.PhysicalQuantity.DENSITY, 0.05, units.UsOilfield.DENSITY, decimal.Decimal('0.01')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(3257.82)),
             opq.PhysicalQuantity.DENSITY, 3257.82, units.Metric.DENSITY, decimal.Decimal('0.01')),
            (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(4.312e10)),
             opq.PhysicalQuantity.ENERGY, 4.312e10, units.UsOilfield.ENERGY, decimal.Decimal('0.001e10')),
            (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(14220)), opq.PhysicalQuantity.ENERGY,
             14220, units.Metric.ENERGY, decimal.Decimal('10')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(44.49)), opq.PhysicalQuantity.FORCE,
             44.49, units.UsOilfield.FORCE, decimal.Decimal('0.01')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(13.56)), opq.PhysicalQuantity.FORCE,
             13.56, units.Metric.FORCE, decimal.Decimal('0.01')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(100994)),
             opq.PhysicalQuantity.FORCE, 100994, units.UsOilfield.FORCE, decimal.Decimal('1')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(441172)),
             opq.PhysicalQuantity.FORCE, 441172, units.Metric.FORCE, decimal.Decimal('1')),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49)), opq.PhysicalQuantity.LENGTH,
             44.49, units.UsOilfield.LENGTH, decimal.Decimal('0.01')),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(13.56)), opq.PhysicalQuantity.LENGTH,
             13.56, units.Metric.LENGTH, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(30.94)), opq.PhysicalQuantity.MASS,
             30.94, units.UsOilfield.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(68.21)), opq.PhysicalQuantity.MASS,
             68.21, units.Metric.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(23276)),
             opq.PhysicalQuantity.POWER, 23276, units.UsOilfield.POWER, decimal.Decimal('1')),
            (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(21.05)), opq.PhysicalQuantity.POWER,
             21.05, units.Metric.POWER, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(49.70)),
             opq.PhysicalQuantity.PRESSURE, 49.70, units.UsOilfield.PRESSURE, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(342.67)),
             opq.PhysicalQuantity.PRESSURE, 342.67, units.Metric.PRESSURE, decimal.Decimal('0.01')),
            (ProppantConcentration(3.82, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION, 3.82, units.UsOilfield.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.01')),
            (ProppantConcentration(457.35, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION, 457.35, units.Metric.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.01')),
            (SlurryRate(114.59, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             opq.PhysicalQuantity.SLURRY_RATE, 114.59, units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.01')),
            (SlurryRate(18.22, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             opq.PhysicalQuantity.SLURRY_RATE, 18.22, units.Metric.SLURRY_RATE, decimal.Decimal('0.01')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(153.6)),
             opq.PhysicalQuantity.TEMPERATURE, 153.6, units.UsOilfield.TEMPERATURE, decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(4.618)),
             opq.PhysicalQuantity.TEMPERATURE, 4.618, units.Metric.TEMPERATURE, decimal.Decimal('0.001')),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(83.48)),
             opq.PhysicalQuantity.VOLUME, 83.48, units.UsOilfield.VOLUME, decimal.Decimal('0.01')),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(13.27)),
             opq.PhysicalQuantity.VOLUME, 13.27, units.Metric.VOLUME, decimal.Decimal('0.01')),
        ]:
            with self.subTest():
                actual = onq.as_measurement(to_convert_net_quantity, to_convert_physical_quantity)
                expected = om.make_measurement(expected_value, expected_unit)
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
            (om.make_measurement(67.07, units.Common.ANGLE),
             UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(67.07))),
            (om.make_measurement(1.414, units.Common.DURATION),
             UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414))),
            (om.make_measurement(17.17, units.UsOilfield.DENSITY),
             UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(17.17))),
            (om.make_measurement(2.72, units.Metric.DENSITY),
             UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(2.72))),
            (om.make_measurement(36.26e9, units.UsOilfield.ENERGY),
             UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(36.26e9))),
            (om.make_measurement(17650, units.Metric.ENERGY),
             UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(17650))),
            (om.make_measurement(147900, units.UsOilfield.FORCE),
             UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(147900))),
            (om.make_measurement(363900, units.Metric.FORCE),
             UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(363900))),
            (om.make_measurement(113.76, units.UsOilfield.LENGTH),
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(113.76))),
            (om.make_measurement(72.98, units.Metric.LENGTH),
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(72.98))),
            (om.make_measurement(7922.36, units.UsOilfield.MASS),
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(7922.36))),
            (om.make_measurement(133965.71, units.Metric.MASS),
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(133965.71))),
            (om.make_measurement(18.87, units.UsOilfield.POWER),
             UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(18.87))),
            (om.make_measurement(14017, units.Metric.POWER),
             UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(14017))),
            (om.make_measurement(6888.89, units.UsOilfield.PRESSURE),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6888.89))),
            (om.make_measurement(59849.82, units.Metric.PRESSURE),
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(59849.82))),
            (om.make_measurement(3.55, units.UsOilfield.PROPPANT_CONCENTRATION),
             ProppantConcentration(3.55, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon)),
            (om.make_measurement(425.03, units.Metric.PROPPANT_CONCENTRATION),
             ProppantConcentration(425.03, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter)),
            (om.make_measurement(96.06, units.UsOilfield.SLURRY_RATE),
             SlurryRate(96.06, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute)),
            (om.make_measurement(0.80, units.Metric.SLURRY_RATE),
             SlurryRate(0.80, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute)),
            (om.make_measurement(157.9, units.UsOilfield.TEMPERATURE),
             UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(157.9))),
            (om.make_measurement(68.99, units.Metric.TEMPERATURE),
             UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(68.99))),
            (om.make_measurement(7216.94, units.UsOilfield.VOLUME),
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(7216.94))),
            (om.make_measurement(1017.09, units.Metric.VOLUME),
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1017.09))),
        ]:
            with self.subTest(f'Converting measurement to UnitsNet Quantity'):
                actual = onq.as_net_quantity(to_convert_measurement)

                # UnitsNet Quantities involving the physical quantity power have magnitudes expressed in the
                # .NET Decimal type which Python.NET **does not** to a Python type (like float) and so must be
                # handled separately.
                if is_power_measurement(to_convert_measurement):
                    assert_that_net_power_quantities_close_to(actual, expected_net_quantity)
                else:
                    tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

    def test_as_net_quantity_in_same_unit(self):
        for to_convert_measurement, expected_net_quantity in [
            (om.make_measurement(27.18, units.Common.DURATION),
             UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(27.18))),
            (om.make_measurement(44.49, units.UsOilfield.LENGTH),
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49))),
            (om.make_measurement(25.93, units.Metric.LENGTH),
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(25.93))),
            (om.make_measurement(5334.31, units.UsOilfield.MASS),
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(5334.31))),
            (om.make_measurement(145461.37, units.Metric.MASS),
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(145461.37))),
            (om.make_measurement(8303.37, units.UsOilfield.PRESSURE),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(8303.37))),
            (om.make_measurement(64.32, units.Metric.PRESSURE),
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(64.32))),
            (om.make_measurement(6944.35, units.UsOilfield.VOLUME),
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(6944.35))),
            (om.make_measurement(880.86, units.Metric.VOLUME),
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(880.86))),
        ]:
            with self.subTest(to_convert_measurement=to_convert_measurement,
                              expected_net_quantity=expected_net_quantity):
                actual = onq.as_net_quantity_in_different_unit(to_convert_measurement, to_convert_measurement.unit)
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

    def test_as_net_quantity_in_different_unit(self):
        for to_convert_measurement, target_unit, expected_net_quantity, tolerance in [
            (om.make_measurement(2638, units.Metric.DENSITY), units.UsOilfield.DENSITY,
             UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(164.7)),
             decimal.Decimal('0.06')),  # same relative error assuming an exact conversion
            (om.make_measurement(164.7, units.UsOilfield.DENSITY), units.Metric.DENSITY,
             UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(2638)),
             decimal.Decimal('2')),
            (om.make_measurement(53.58e9, units.UsOilfield.ENERGY), units.Metric.ENERGY,
             UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(72.65e9)),
             decimal.Decimal('0.01e9')),
            (om.make_measurement(72.65e9, units.Metric.ENERGY), units.UsOilfield.ENERGY,
             UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(53.58e9)),
             decimal.Decimal('0.01e9')),
            (om.make_measurement(507366, units.Metric.FORCE), units.UsOilfield.FORCE,
             UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(114060)),
             decimal.Decimal('1')),
            (om.make_measurement(114060, units.UsOilfield.FORCE), units.Metric.FORCE,
             UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(507366)),
             decimal.Decimal('4')),
            (om.make_measurement(43.13, units.Metric.LENGTH), units.UsOilfield.LENGTH,
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(141.51)), decimal.Decimal('0.03')),
            (om.make_measurement(141.51, units.UsOilfield.LENGTH), units.Metric.LENGTH,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(43.13)), decimal.Decimal('0.01')),
            (om.make_measurement(4107.64, units.UsOilfield.MASS), units.Metric.MASS,
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1863.19)), decimal.Decimal('0.01')),
            (om.make_measurement(1863.19, units.Metric.MASS), units.UsOilfield.MASS,
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(4107.64)), decimal.Decimal('0.01')),
            (om.make_measurement(13.66, units.UsOilfield.POWER), units.Metric.POWER,
             UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(10180)), decimal.Decimal('8')),
            (om.make_measurement(10180, units.Metric.POWER), units.UsOilfield.POWER,
             UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(13.66)),
             decimal.Decimal('0.02')),
            (om.make_measurement(6984.02, units.UsOilfield.PRESSURE), units.Metric.PRESSURE,
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(48153.12)), decimal.Decimal('7')),
            (om.make_measurement(48153.12, units.Metric.PRESSURE), units.UsOilfield.PRESSURE,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6984.02)),
             decimal.Decimal('2')),
            (om.make_measurement(486.4, units.Metric.PROPPANT_CONCENTRATION), units.UsOilfield.PROPPANT_CONCENTRATION,
             ProppantConcentration(4.060, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             decimal.Decimal('0.001')),
            (om.make_measurement(4.060, units.UsOilfield.PROPPANT_CONCENTRATION), units.Metric.PROPPANT_CONCENTRATION,
             ProppantConcentration(486.4, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             decimal.Decimal('0.2')),
            (om.make_measurement(11.14, units.Metric.SLURRY_RATE), units.UsOilfield.SLURRY_RATE,
             SlurryRate(70.08, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             decimal.Decimal('0.06')),
            (om.make_measurement(70.08, units.UsOilfield.SLURRY_RATE), units.Metric.SLURRY_RATE,
             SlurryRate(11.14, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             decimal.Decimal('0.01')),
            (om.make_measurement(35.61, units.UsOilfield.TEMPERATURE), units.Metric.TEMPERATURE,
             UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(2.004)),
             decimal.Decimal('0.006')),
            (om.make_measurement(2.004, units.Metric.TEMPERATURE), units.UsOilfield.TEMPERATURE,
             UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(35.61)),
             decimal.Decimal('0.02')),
            (om.make_measurement(8722.45, units.UsOilfield.VOLUME), units.Metric.VOLUME,
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1386.76)), decimal.Decimal('0.01')),
            (om.make_measurement(1386.76, units.Metric.VOLUME), units.UsOilfield.VOLUME,
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8722.45)), decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Converting .NET quantity, {to_convert_measurement}, to {target_unit}'):
                actual = onq.as_net_quantity_in_different_unit(to_convert_measurement, target_unit)
                # UnitsNet Quantities involving the physical quantity power have magnitudes expressed in the
                # .NET Decimal type which Python.NET **does not** to a Python type (like float) and so must be
                # handled separately.
                if is_power_measurement(to_convert_measurement):
                    assert_that_net_power_quantities_close_to(actual, expected_net_quantity, tolerance)
                else:
                    tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, tolerance)

    def test_convert_net_quantity_to_same_unit(self):
        for net_unit, target_unit in [
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(0.1717)), units.Common.DURATION),
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


if __name__ == '__main__':
    unittest.main()
