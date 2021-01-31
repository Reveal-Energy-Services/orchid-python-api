#  Copyright 2017-2021 Reveal Energy Services, Inc 
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

from hamcrest import assert_that, equal_to, close_to, calling, raises
import dateutil.tz as duz


from orchid import (
    measurement as om,
    obs_measurement as obs_om,
    net_quantity as onq,
    physical_quantity as opq,
    obs_unit_system as units,
)

from tests import (custom_matchers as tcm,
                   stub_net as tsn)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import (ProppantConcentration, SlurryRate)
# noinspection PyUnresolvedReferences
from System import (DateTime, DateTimeKind, Decimal)
# noinspection PyUnresolvedReferences
import UnitsNet


def assert_that_net_power_quantities_close_to(actual, expected_net_quantity, tolerance=6e-3):
    assert_that(tcm.get_net_unit(actual), equal_to(tcm.get_net_unit(expected_net_quantity)))
    to_test_actual = decimal.Decimal(onq.net_decimal_to_float(actual.Value))
    to_test_expected = decimal.Decimal(onq.net_decimal_to_float(expected_net_quantity.Value))
    to_test_tolerance = decimal.Decimal(tolerance)
    assert_that(to_test_actual, close_to(to_test_expected, to_test_tolerance))


def is_power_measurement(measurement):
    return is_power_unit(measurement.unit)


def is_power_unit(unit):
    return unit == units.UsOilfield.POWER or unit == units.Metric.POWER


# Test ideas
# - well.frac_gradient (property - appears to return "ratio unit", `FracGradient`)
#   (Consider not exposing this property because we expect it to change.)
# - well.shmin (property - returns `Nullable<Pressure?>`)
#   (Consider not exposing this property because of `Nullable<T>`.)
# - stage.md_top, md_bottom (adjust existing)
# - stage.get_stage_location_center and similar (adjust existing)
# - stage_port.isip (property)
class TestNetMeasurement(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_datetime_net_time_point_kind_utc(self):
        net_time_point = DateTime(2020, 8, 5, 6, 59, 41, 726, DateTimeKind.Utc)
        actual = onq.as_datetime(net_time_point)

        assert_that(actual, equal_to(datetime.datetime(2020, 8, 5, 6, 59, 41, 726000, tzinfo=duz.UTC)))

    def test_as_datetime_net_time_point_kind_local(self):
        net_time_point = DateTime(2024, 11, 24, 18, 56, 35, 45, DateTimeKind.Local)
        expected_error_message = f'{net_time_point.ToString("O")}.'
        assert_that(calling(onq.as_datetime).with_args(net_time_point),
                    raises(onq.NetQuantityLocalDateTimeKindError, pattern=expected_error_message))

    def test_as_datetime_net_time_point_kind_unspecified_throws_exception(self):
        net_time_point = tsn.StubDateTime(2023, 7, 31, 1, 11, 26, 216, tsn.StubDateTimeKind.UNSPECIFIED)
        expected_error_message = f'{net_time_point.ToString("O")}'
        assert_that(calling(onq.as_datetime).with_args(net_time_point),
                    raises(onq.NetQuantityUnspecifiedDateTimeKindError, pattern=expected_error_message))

    def test_as_datetime_net_time_point_kind_unknown_throws_exception(self):
        net_time_point = tsn.StubDateTime(2019, 2, 10, 9, 36, 36, 914, tsn.StubDateTimeKind.INVALID)
        expected_error_pattern = f'Unknown .NET DateTime.Kind, {tsn.StubDateTimeKind.INVALID}.'
        assert_that(calling(onq.as_datetime).with_args(net_time_point), raises(ValueError,
                                                                               pattern=expected_error_pattern))

    def test_as_measurement(self):
        for to_convert_net_quantity, to_convert_physical_quantity, expected, tolerance in [
            (UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(306.1)), opq.PhysicalQuantity.ANGLE,
             306.1 * om.registry.deg, decimal.Decimal('0.1')),
            # (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414)), opq.PhysicalQuantity.DURATION,
            #  tsn.StubMeasurement(1.414, units.Common.DURATION), decimal.Decimal('0.001')),
            # (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(0.05)),
            #  opq.PhysicalQuantity.DENSITY, tsn.StubMeasurement(0.05, units.UsOilfield.DENSITY),
            #  decimal.Decimal('0.01')),
            # (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(3257.82)),
            #  opq.PhysicalQuantity.DENSITY, tsn.StubMeasurement(3257.82, units.Metric.DENSITY),
            #  decimal.Decimal('0.01')),
            # (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(4.312e10)),
            #  opq.PhysicalQuantity.ENERGY, tsn.StubMeasurement(4.312e10, units.UsOilfield.ENERGY),
            #  decimal.Decimal('0.001e10')),
            # (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(14220)), opq.PhysicalQuantity.ENERGY,
            #  tsn.StubMeasurement(14220, units.Metric.ENERGY), decimal.Decimal('10')),
            # (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(100994)),
            #  opq.PhysicalQuantity.FORCE, tsn.StubMeasurement(100994, units.UsOilfield.FORCE), decimal.Decimal('1')),
            # (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(441172)),
            #  opq.PhysicalQuantity.FORCE, tsn.StubMeasurement(441172, units.Metric.FORCE), decimal.Decimal('1')),
            # (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49)), opq.PhysicalQuantity.LENGTH,
            #  tsn.StubMeasurement(44.49, units.UsOilfield.LENGTH), decimal.Decimal('0.01')),
            # (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(13.56)), opq.PhysicalQuantity.LENGTH,
            #  tsn.StubMeasurement(13.56, units.Metric.LENGTH), decimal.Decimal('0.01')),
            # (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(30.94)), opq.PhysicalQuantity.MASS,
            #  tsn.StubMeasurement(30.94, units.UsOilfield.MASS), decimal.Decimal('0.01')),
            # (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(68.21)), opq.PhysicalQuantity.MASS,
            #  tsn.StubMeasurement(68.21, units.Metric.MASS), decimal.Decimal('0.01')),
            # (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(23276)),
            #  opq.PhysicalQuantity.POWER, tsn.StubMeasurement(23276, units.UsOilfield.POWER), decimal.Decimal('1')),
            # (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(21.05)), opq.PhysicalQuantity.POWER,
            #  tsn.StubMeasurement(21.05, units.Metric.POWER), decimal.Decimal('0.01')),
            # (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(49.70)),
            #  opq.PhysicalQuantity.PRESSURE, tsn.StubMeasurement(49.70, units.UsOilfield.PRESSURE),
            #  decimal.Decimal('0.01')),
            # (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(342.67)),
            #  opq.PhysicalQuantity.PRESSURE, tsn.StubMeasurement(342.67, units.Metric.PRESSURE),
            #  decimal.Decimal('0.01')),
            # (ProppantConcentration(3.82, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
            #  opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
            #  tsn.StubMeasurement(3.82, units.UsOilfield.PROPPANT_CONCENTRATION), decimal.Decimal('0.01')),
            # (ProppantConcentration(457.35, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
            #  opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
            #  tsn.StubMeasurement(457.35, units.Metric.PROPPANT_CONCENTRATION), decimal.Decimal('0.01')),
            # (SlurryRate(114.59, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
            #  opq.PhysicalQuantity.SLURRY_RATE,
            #  tsn.StubMeasurement(114.59, units.UsOilfield.SLURRY_RATE), decimal.Decimal('0.01')),
            # (SlurryRate(18.22, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
            #  opq.PhysicalQuantity.SLURRY_RATE, tsn.StubMeasurement(18.22, units.Metric.SLURRY_RATE),
            #  decimal.Decimal('0.01')),
            # (UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(153.6)),
            #  opq.PhysicalQuantity.TEMPERATURE,
            #  tsn.StubMeasurement(153.6, units.UsOilfield.TEMPERATURE), decimal.Decimal('0.1')),
            # (UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(4.618)),
            #  opq.PhysicalQuantity.TEMPERATURE,
            #  tsn.StubMeasurement(4.618, units.Metric.TEMPERATURE), decimal.Decimal('0.001')),
            # (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(83.48)),
            #  opq.PhysicalQuantity.VOLUME, tsn.StubMeasurement(83.48, units.UsOilfield.VOLUME), decimal.Decimal('0.01')),
            # (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(13.27)),
            #  opq.PhysicalQuantity.VOLUME, tsn.StubMeasurement(13.27, units.Metric.VOLUME), decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Test as_measurement for {expected.magnitude} {expected.units:~P}'):
                actual = onq.as_measurement(to_convert_physical_quantity, to_convert_net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    def test_obs_as_measurement(self):
        for to_convert_net_quantity, to_convert_physical_quantity, expected, tolerance in [
            (UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(306.08)), opq.PhysicalQuantity.ANGLE,
             tsn.StubMeasurement(306.08, units.Common.ANGLE), decimal.Decimal('0.01')),
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414)), opq.PhysicalQuantity.DURATION,
             tsn.StubMeasurement(1.414, units.Common.DURATION), decimal.Decimal('0.001')),
            (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(0.05)),
             opq.PhysicalQuantity.DENSITY, tsn.StubMeasurement(0.05, units.UsOilfield.DENSITY),
             decimal.Decimal('0.01')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(3257.82)),
             opq.PhysicalQuantity.DENSITY, tsn.StubMeasurement(3257.82, units.Metric.DENSITY),
             decimal.Decimal('0.01')),
            (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(4.312e10)),
             opq.PhysicalQuantity.ENERGY, tsn.StubMeasurement(4.312e10, units.UsOilfield.ENERGY),
             decimal.Decimal('0.001e10')),
            (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(14220)), opq.PhysicalQuantity.ENERGY,
             tsn.StubMeasurement(14220, units.Metric.ENERGY), decimal.Decimal('10')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(100994)),
             opq.PhysicalQuantity.FORCE, tsn.StubMeasurement(100994, units.UsOilfield.FORCE), decimal.Decimal('1')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(441172)),
             opq.PhysicalQuantity.FORCE, tsn.StubMeasurement(441172, units.Metric.FORCE), decimal.Decimal('1')),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49)), opq.PhysicalQuantity.LENGTH,
             tsn.StubMeasurement(44.49, units.UsOilfield.LENGTH), decimal.Decimal('0.01')),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(13.56)), opq.PhysicalQuantity.LENGTH,
             tsn.StubMeasurement(13.56, units.Metric.LENGTH), decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(30.94)), opq.PhysicalQuantity.MASS,
             tsn.StubMeasurement(30.94, units.UsOilfield.MASS), decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(68.21)), opq.PhysicalQuantity.MASS,
             tsn.StubMeasurement(68.21, units.Metric.MASS), decimal.Decimal('0.01')),
            (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(23276)),
             opq.PhysicalQuantity.POWER, tsn.StubMeasurement(23276, units.UsOilfield.POWER), decimal.Decimal('1')),
            (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(21.05)), opq.PhysicalQuantity.POWER,
             tsn.StubMeasurement(21.05, units.Metric.POWER), decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(49.70)),
             opq.PhysicalQuantity.PRESSURE, tsn.StubMeasurement(49.70, units.UsOilfield.PRESSURE),
             decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(342.67)),
             opq.PhysicalQuantity.PRESSURE, tsn.StubMeasurement(342.67, units.Metric.PRESSURE),
             decimal.Decimal('0.01')),
            (ProppantConcentration(3.82, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             tsn.StubMeasurement(3.82, units.UsOilfield.PROPPANT_CONCENTRATION), decimal.Decimal('0.01')),
            (ProppantConcentration(457.35, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             tsn.StubMeasurement(457.35, units.Metric.PROPPANT_CONCENTRATION), decimal.Decimal('0.01')),
            (SlurryRate(114.59, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             opq.PhysicalQuantity.SLURRY_RATE,
             tsn.StubMeasurement(114.59, units.UsOilfield.SLURRY_RATE), decimal.Decimal('0.01')),
            (SlurryRate(18.22, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             opq.PhysicalQuantity.SLURRY_RATE, tsn.StubMeasurement(18.22, units.Metric.SLURRY_RATE),
             decimal.Decimal('0.01')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(153.6)),
             opq.PhysicalQuantity.TEMPERATURE,
             tsn.StubMeasurement(153.6, units.UsOilfield.TEMPERATURE), decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(4.618)),
             opq.PhysicalQuantity.TEMPERATURE,
             tsn.StubMeasurement(4.618, units.Metric.TEMPERATURE), decimal.Decimal('0.001')),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(83.48)),
             opq.PhysicalQuantity.VOLUME, tsn.StubMeasurement(83.48, units.UsOilfield.VOLUME), decimal.Decimal('0.01')),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(13.27)),
             opq.PhysicalQuantity.VOLUME, tsn.StubMeasurement(13.27, units.Metric.VOLUME), decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Test obs_as_measurement for {expected.magnitude} {expected.unit.value.unit:~P}'):
                actual = onq.obs_as_measurement(to_convert_physical_quantity, to_convert_net_quantity)
                tcm.obs_assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_measurement_in_common_unit(self):
        for to_convert_net_quantity, to_unit, expected, tolerance in [
            (UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(306.08)), units.Common.ANGLE,
             tsn.StubMeasurement(306.08, units.Common.ANGLE), decimal.Decimal('0.01')),
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414)), units.Common.DURATION,
             tsn.StubMeasurement(1.414, units.Common.DURATION), decimal.Decimal('0.001')),
        ]:
            with self.subTest(f'Test obs_as_measurement_in_common_unit for {expected.magnitude}'
                              f' {expected.unit.value.unit:~P}'):
                actual = onq.obs_as_measurement(to_unit, to_convert_net_quantity)
                tcm.obs_assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_measurement_in_specified_same_unit(self):
        for to_convert_net_quantity, to_unit, expected, tolerance in [
            (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(40.79)),
             units.UsOilfield.DENSITY, tsn.StubMeasurement(40.79, units.UsOilfield.DENSITY),
             decimal.Decimal('0.001')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(921.4)),
             units.Metric.DENSITY, tsn.StubMeasurement(921.4, units.Metric.DENSITY),
             decimal.Decimal('0.01')),
            (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(43.12e9)),
             units.UsOilfield.ENERGY, tsn.StubMeasurement(43.12e9, units.UsOilfield.ENERGY),
             decimal.Decimal('0.001e9')),
            (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(14220)), units.Metric.ENERGY,
             tsn.StubMeasurement(14220, units.Metric.ENERGY), decimal.Decimal('10')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(100994)),
             units.UsOilfield.FORCE, tsn.StubMeasurement(100994, units.UsOilfield.FORCE), decimal.Decimal('1')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(441172)),
             units.Metric.FORCE, tsn.StubMeasurement(441172, units.Metric.FORCE), decimal.Decimal('1')),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49)), units.UsOilfield.LENGTH,
             tsn.StubMeasurement(44.49, units.UsOilfield.LENGTH), decimal.Decimal('0.01')),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(13.56)), units.Metric.LENGTH,
             tsn.StubMeasurement(13.56, units.Metric.LENGTH), decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(30.94)), units.UsOilfield.MASS,
             tsn.StubMeasurement(30.94, units.UsOilfield.MASS), decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(68.21)), units.Metric.MASS,
             tsn.StubMeasurement(68.21, units.Metric.MASS), decimal.Decimal('0.01')),
            (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(23276)),
             units.UsOilfield.POWER, tsn.StubMeasurement(23276, units.UsOilfield.POWER), decimal.Decimal('1')),
            (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(21.05)), units.Metric.POWER,
             tsn.StubMeasurement(21.05, units.Metric.POWER), decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(49.70)),
             units.UsOilfield.PRESSURE, tsn.StubMeasurement(49.70, units.UsOilfield.PRESSURE), decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(342.67)),
             units.Metric.PRESSURE, tsn.StubMeasurement(342.67, units.Metric.PRESSURE), decimal.Decimal('0.01')),
            (ProppantConcentration(3.82, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             units.UsOilfield.PROPPANT_CONCENTRATION,
             tsn.StubMeasurement(3.82, units.UsOilfield.PROPPANT_CONCENTRATION), decimal.Decimal('0.01')),
            (ProppantConcentration(457.35, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             units.Metric.PROPPANT_CONCENTRATION,
             tsn.StubMeasurement(457.35, units.Metric.PROPPANT_CONCENTRATION), decimal.Decimal('0.01')),
            (SlurryRate(114.59, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             units.UsOilfield.SLURRY_RATE,
             tsn.StubMeasurement(114.59, units.UsOilfield.SLURRY_RATE), decimal.Decimal('0.01')),
            (SlurryRate(18.22, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             opq.PhysicalQuantity.SLURRY_RATE, tsn.StubMeasurement(18.22, units.Metric.SLURRY_RATE),
             decimal.Decimal('0.01')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(153.6)),
             opq.PhysicalQuantity.TEMPERATURE,
             tsn.StubMeasurement(153.6, units.UsOilfield.TEMPERATURE), decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(4.618)),
             opq.PhysicalQuantity.TEMPERATURE,
             tsn.StubMeasurement(4.618, units.Metric.TEMPERATURE), decimal.Decimal('0.001')),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(83.48)),
             opq.PhysicalQuantity.VOLUME, tsn.StubMeasurement(83.48, units.UsOilfield.VOLUME),
             decimal.Decimal('0.01')),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(13.27)),
             opq.PhysicalQuantity.VOLUME, tsn.StubMeasurement(13.27, units.Metric.VOLUME), decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Test as_measurement_in_specified_same_unit for {expected.magnitude}'
                              f' {expected.unit.value.unit:~P}'):
                actual = onq.obs_as_measurement(to_unit, to_convert_net_quantity)
                tcm.obs_assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_measurement_in_specified_different_unit(self):
        for to_convert_net_quantity, to_unit, expected, tolerance in [
            (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(62.30)),
             units.Metric.DENSITY, tsn.StubMeasurement(998.0, units.Metric.DENSITY),
             decimal.Decimal('0.2')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(998.0)),
             units.UsOilfield.DENSITY, tsn.StubMeasurement(62.30, units.UsOilfield.DENSITY),
             decimal.Decimal('0.006')),
            (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(2.024)),
             units.Metric.ENERGY, tsn.StubMeasurement(2.744, units.Metric.ENERGY), decimal.Decimal('0.002')),
            (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(2.744)), units.UsOilfield.ENERGY,
             tsn.StubMeasurement(2.024, units.UsOilfield.ENERGY), decimal.Decimal('7e-4')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(107.8e3)),
             units.Metric.FORCE, tsn.StubMeasurement(479.5e3, units.Metric.FORCE), decimal.Decimal('0.5e3')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(479.5e3)),
             units.UsOilfield.FORCE, tsn.StubMeasurement(107.8e3, units.UsOilfield.FORCE), decimal.Decimal('0.02e3')),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(155.2)),
             units.Metric.LENGTH, tsn.StubMeasurement(47.30, units.Metric.LENGTH), decimal.Decimal('0.04')),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(47.30)),
             units.UsOilfield.LENGTH, tsn.StubMeasurement(155.2, units.UsOilfield.LENGTH), decimal.Decimal('0.03')),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(7987)),
             units.Metric.MASS, tsn.StubMeasurement(3622, units.Metric.MASS), decimal.Decimal('0.5e3')),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(3.622e3)),
             units.UsOilfield.MASS, tsn.StubMeasurement(7.987e3, units.UsOilfield.MASS), decimal.Decimal('2')),
            (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(9.254)),
             units.Metric.POWER, tsn.StubMeasurement(6901, units.Metric.POWER), decimal.Decimal('0.8')),
            (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(6901)),
             units.UsOilfield.POWER, tsn.StubMeasurement(9.254, units.UsOilfield.POWER), decimal.Decimal('0.002')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6972)),
             units.Metric.PRESSURE, tsn.StubMeasurement(48.07e3, units.Metric.PRESSURE), decimal.Decimal('7')),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(48.07e3)),
             units.UsOilfield.PRESSURE, tsn.StubMeasurement(6972, units.UsOilfield.PRESSURE), decimal.Decimal('2')),
            (ProppantConcentration(5.017, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             units.Metric.PROPPANT_CONCENTRATION,
             tsn.StubMeasurement(601.2, units.Metric.PROPPANT_CONCENTRATION), decimal.Decimal('0.2')),
            (ProppantConcentration(601.2, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             units.UsOilfield.PROPPANT_CONCENTRATION,
             tsn.StubMeasurement(5.017, units.UsOilfield.PROPPANT_CONCENTRATION), decimal.Decimal('0.0008')),
            (SlurryRate(100.9, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             units.Metric.SLURRY_RATE,
             tsn.StubMeasurement(16.04, units.Metric.SLURRY_RATE), decimal.Decimal('0.02')),
            (SlurryRate(16.04, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             units.UsOilfield.SLURRY_RATE,
             tsn.StubMeasurement(100.9, units.UsOilfield.SLURRY_RATE), decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(156.2)),
             units.Metric.TEMPERATURE,
             tsn.StubMeasurement(69.00, units.Metric.TEMPERATURE), decimal.Decimal('0.05')),
            (UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(69.00)),
             units.UsOilfield.TEMPERATURE,
             tsn.StubMeasurement(156.2, units.UsOilfield.TEMPERATURE), decimal.Decimal('0.3')),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8951)),
             units.Metric.VOLUME, tsn.StubMeasurement(1423, units.Metric.VOLUME), decimal.Decimal('0.2')),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1423)),
             units.UsOilfield.VOLUME, tsn.StubMeasurement(8951, units.UsOilfield.VOLUME), decimal.Decimal('7')),
        ]:
            with self.subTest(f'Test as_measurement_in_specified_different_unit for {expected.magnitude}'
                              f' {expected.unit.value.unit:~P}'):
                actual = onq.obs_as_measurement(to_unit, to_convert_net_quantity)
                tcm.obs_assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_net_date_time(self):
        for expected, time_point in [(DateTime(2017, 3, 22, 3, 0, 37, 23, DateTimeKind.Utc),
                                      datetime.datetime(2017, 3, 22, 3, 0, 37, 23124, duz.UTC)),
                                     (DateTime(2020, 9, 20, 22, 11, 51, 655, DateTimeKind.Utc),
                                      datetime.datetime(2020, 9, 20, 22, 11, 51, 654859, duz.UTC)),
                                     # The Python `round` function employs "half-even" rounding; however, the
                                     # following test rounds to an *odd* value instead. See the "Note" in the
                                     # Python documentation of `round` for an explanation of this (unexpected)
                                     # behavior.
                                     (DateTime(2022, 2, 2, 23, 35, 39, 979, DateTimeKind.Utc),
                                      datetime.datetime(2022, 2, 2, 23, 35, 39, 978531, duz.UTC)),
                                     (DateTime(2019, 2, 7, 10, 18, 17, 488, DateTimeKind.Utc),
                                      datetime.datetime(2019, 2, 7, 10, 18, 17, 487500, duz.UTC)),
                                     (DateTime(2022, 1, 14, 20, 29, 18, 852, DateTimeKind.Utc),
                                      datetime.datetime(2022, 1, 14, 20, 29, 18, 852500, duz.UTC))
                                     ]:
            with self.subTest(f'Test as_net_date_time for {expected}'):
                actual = onq.as_net_date_time(time_point)
                assert_that(actual, tcm.equal_to_net_date_time(expected))

    def test_as_net_date_time_raises_error_if_not_utc(self):
        to_test_datetime = datetime.datetime(2025, 12, 21, 9, 15, 7, 896671)
        assert_that(calling(onq.as_net_date_time).with_args(to_test_datetime),
                    raises(onq.NetQuantityNoTzInfoError, pattern=to_test_datetime.isoformat()))

    def test_as_net_quantity(self):
        for to_convert_measurement, expected_net_quantity in [
            (obs_om.make_measurement(units.Common.ANGLE, 67.07),
             UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(67.07))),
            (obs_om.make_measurement(units.Common.DURATION, 1.414),
             UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414))),
            (obs_om.make_measurement(units.UsOilfield.DENSITY, 17.17),
             UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(17.17))),
            (obs_om.make_measurement(units.Metric.DENSITY, 2.72),
             UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(2.72))),
            (obs_om.make_measurement(units.UsOilfield.ENERGY, 36.26e9),
             UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(36.26e9))),
            (obs_om.make_measurement(units.Metric.ENERGY, 17650),
             UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(17650))),
            (obs_om.make_measurement(units.UsOilfield.FORCE, 147900),
             UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(147900))),
            (obs_om.make_measurement(units.Metric.FORCE, 363900),
             UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(363900))),
            (obs_om.make_measurement(units.UsOilfield.LENGTH, 113.76),
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(113.76))),
            (obs_om.make_measurement(units.Metric.LENGTH, 72.98),
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(72.98))),
            (obs_om.make_measurement(units.UsOilfield.MASS, 7922.36),
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(7922.36))),
            (obs_om.make_measurement(units.Metric.MASS, 133965.71),
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(133965.71))),
            (obs_om.make_measurement(units.UsOilfield.POWER, 18.87),
             UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(18.87))),
            (obs_om.make_measurement(units.Metric.POWER, 14017),
             UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(14017))),
            (obs_om.make_measurement(units.UsOilfield.PRESSURE, 6888.89),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6888.89))),
            (obs_om.make_measurement(units.Metric.PRESSURE, 59849.82),
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(59849.82))),
            (obs_om.make_measurement(units.UsOilfield.PROPPANT_CONCENTRATION, 3.55),
             ProppantConcentration(3.55, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon)),
            (obs_om.make_measurement(units.Metric.PROPPANT_CONCENTRATION, 425.03),
             ProppantConcentration(425.03, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter)),
            (obs_om.make_measurement(units.UsOilfield.SLURRY_RATE, 96.06),
             SlurryRate(96.06, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute)),
            (obs_om.make_measurement(units.Metric.SLURRY_RATE, 0.80),
             SlurryRate(0.80, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute)),
            (obs_om.make_measurement(units.UsOilfield.TEMPERATURE, 157.9),
             UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(157.9))),
            (obs_om.make_measurement(units.Metric.TEMPERATURE, 68.99),
             UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(68.99))),
            (obs_om.make_measurement(units.UsOilfield.VOLUME, 7216.94),
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(7216.94))),
            (obs_om.make_measurement(units.Metric.VOLUME, 1017.09),
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1017.09))),
        ]:
            with self.subTest(f'Test converting measurement, {to_convert_measurement} to a UnitsNet IQuantity'):
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
            (obs_om.make_measurement(units.Common.DURATION, 27.18),
             UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(27.18))),
            (obs_om.make_measurement(units.UsOilfield.LENGTH, 44.49),
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49))),
            (obs_om.make_measurement(units.Metric.LENGTH, 25.93),
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(25.93))),
            (obs_om.make_measurement(units.UsOilfield.MASS, 5334.31),
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(5334.31))),
            (obs_om.make_measurement(units.Metric.MASS, 145461.37),
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(145461.37))),
            (obs_om.make_measurement(units.UsOilfield.PRESSURE, 8303.37),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(8303.37))),
            (obs_om.make_measurement(units.Metric.PRESSURE, 64.32),
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(64.32))),
            (obs_om.make_measurement(units.UsOilfield.VOLUME, 6944.35),
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(6944.35))),
            (obs_om.make_measurement(units.Metric.VOLUME, 880.86),
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(880.86))),
        ]:
            with self.subTest(f'Test measurement, {to_convert_measurement}, as_net_quantity, but in the same units.'):
                actual = onq.as_net_quantity_in_different_unit(to_convert_measurement, to_convert_measurement.unit)
                tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, 6e-3)

    def test_as_net_quantity_in_different_unit(self):
        for to_convert_measurement, target_unit, expected_net_quantity, tolerance in [
            (obs_om.make_measurement(units.Metric.DENSITY, 2638), units.UsOilfield.DENSITY,
             UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(164.7)),
             decimal.Decimal('0.06')),  # same relative error assuming an exact conversion
            (obs_om.make_measurement(units.UsOilfield.DENSITY, 164.7), units.Metric.DENSITY,
             UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(2638)),
             decimal.Decimal('2')),
            (obs_om.make_measurement(units.UsOilfield.ENERGY, 53.58e9), units.Metric.ENERGY,
             UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(72.65e9)),
             decimal.Decimal('0.01e9')),
            (obs_om.make_measurement(units.Metric.ENERGY, 72.65e9), units.UsOilfield.ENERGY,
             UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(53.58e9)),
             decimal.Decimal('0.01e9')),
            (obs_om.make_measurement(units.Metric.FORCE, 507366), units.UsOilfield.FORCE,
             UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(114060)),
             decimal.Decimal('1')),
            (obs_om.make_measurement(units.UsOilfield.FORCE, 114060), units.Metric.FORCE,
             UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(507366)),
             decimal.Decimal('4')),
            (obs_om.make_measurement(units.Metric.LENGTH, 43.13), units.UsOilfield.LENGTH,
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(141.51)), decimal.Decimal('0.03')),
            (obs_om.make_measurement(units.UsOilfield.LENGTH, 141.51), units.Metric.LENGTH,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(43.13)), decimal.Decimal('0.01')),
            (obs_om.make_measurement(units.UsOilfield.MASS, 4107.64), units.Metric.MASS,
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1863.19)), decimal.Decimal('0.01')),
            (obs_om.make_measurement(units.Metric.MASS, 1863.19), units.UsOilfield.MASS,
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(4107.64)), decimal.Decimal('0.01')),
            (obs_om.make_measurement(units.UsOilfield.POWER, 13.66), units.Metric.POWER,
             UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(10180)), decimal.Decimal('8')),
            (obs_om.make_measurement(units.Metric.POWER, 10180), units.UsOilfield.POWER,
             UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(13.66)),
             decimal.Decimal('0.02')),
            (obs_om.make_measurement(units.UsOilfield.PRESSURE, 6984.02), units.Metric.PRESSURE,
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(48153.12)), decimal.Decimal('7')),
            (obs_om.make_measurement(units.Metric.PRESSURE, 48153.12), units.UsOilfield.PRESSURE,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6984.02)),
             decimal.Decimal('2')),
            (obs_om.make_measurement(units.Metric.PROPPANT_CONCENTRATION, 486.4),
             units.UsOilfield.PROPPANT_CONCENTRATION,
             ProppantConcentration(4.060, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             decimal.Decimal('0.001')),
            (obs_om.make_measurement(units.UsOilfield.PROPPANT_CONCENTRATION, 4.060),
             units.Metric.PROPPANT_CONCENTRATION,
             ProppantConcentration(486.4, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             decimal.Decimal('0.2')),
            (obs_om.make_measurement(units.Metric.SLURRY_RATE, 11.14), units.UsOilfield.SLURRY_RATE,
             SlurryRate(70.08, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             decimal.Decimal('0.06')),
            (obs_om.make_measurement(units.UsOilfield.SLURRY_RATE, 70.08), units.Metric.SLURRY_RATE,
             SlurryRate(11.14, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             decimal.Decimal('0.01')),
            (obs_om.make_measurement(units.UsOilfield.TEMPERATURE, 35.61), units.Metric.TEMPERATURE,
             UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(2.004)),
             decimal.Decimal('0.006')),
            (obs_om.make_measurement(units.Metric.TEMPERATURE, 2.004), units.UsOilfield.TEMPERATURE,
             UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(35.61)),
             decimal.Decimal('0.02')),
            (obs_om.make_measurement(units.UsOilfield.VOLUME, 8722.45), units.Metric.VOLUME,
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1386.76)), decimal.Decimal('0.01')),
            (obs_om.make_measurement(units.Metric.VOLUME, 1386.76), units.UsOilfield.VOLUME,
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
        for net_quantity, target_unit in [
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
            with self.subTest(f'Test convert .NET quantity, {net_quantity.ToString()}, to same unit, {target_unit}'):
                actual = onq.convert_net_quantity_to_different_unit(target_unit, net_quantity)
                tcm.assert_that_net_quantities_close_to(actual, net_quantity)

    def test_convert_net_quantity_to_different_unit(self):
        for source_net_quantity, target_unit, target_net_quantity, tolerance in [
            (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(1.953e-2)),
             units.Metric.DENSITY,
             UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(0.3128)),
             decimal.Decimal('0.0002')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(0.3128)),
             units.UsOilfield.DENSITY,
             UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(1.953e-2)),
             decimal.Decimal('0.001e-2')),
            (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(7.045)), units.Metric.ENERGY,
             UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(9.552)), decimal.Decimal('0.001')),
            (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(9.552)), units.UsOilfield.ENERGY,
             UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(7.045)), decimal.Decimal('0.001')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(124300)), units.Metric.FORCE,
             UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(552800)), decimal.Decimal('500')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(552800)), units.UsOilfield.FORCE,
             UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(124300)), decimal.Decimal('30')),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(155.15)), units.Metric.LENGTH,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(47.29)), None),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(47.29)), units.UsOilfield.LENGTH,
             UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(155.15)), None),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(2614.88)), units.Metric.MASS,
             UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1186.09)), None),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(1186.09)), units.UsOilfield.MASS,
             UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(2614.88)), None),
            (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(15.60)), units.Metric.POWER,
             UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(11640)), decimal.Decimal('8')),
            (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(11640)), units.UsOilfield.POWER,
             UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(15.60)),
             decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6428)),
             units.Metric.PRESSURE,
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(44320)), decimal.Decimal('7')),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(44320)), units.UsOilfield.PRESSURE,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(6428)),
             decimal.Decimal('2')),
            (ProppantConcentration(483.3, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             units.UsOilfield.PROPPANT_CONCENTRATION,
             ProppantConcentration(4.033, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             decimal.Decimal('0.001')),
            (ProppantConcentration(4.033, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             units.Metric.PROPPANT_CONCENTRATION,
             ProppantConcentration(483.3, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             decimal.Decimal('0.2')),
            (SlurryRate(477.2, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             units.Metric.SLURRY_RATE,
             SlurryRate(75.87, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             decimal.Decimal('0.02')),
            (SlurryRate(75.87, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             units.UsOilfield.SLURRY_RATE,
             SlurryRate(477.2, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             decimal.Decimal('0.07')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(154.4)),
             units.Metric.TEMPERATURE,
             UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(68.02)),
             decimal.Decimal('0.04')),
            (UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(68.02)),
             units.UsOilfield.TEMPERATURE,
             UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(154.4)),
             decimal.Decimal('0.04')),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8794.21)), units.Metric.VOLUME,
             UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1398.17)), decimal.Decimal('0.003')),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(1398.17)), units.UsOilfield.VOLUME,
             UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(8794.21)), decimal.Decimal('0.07')),
        ]:
            with self.subTest(f'Converting .NET Quantity, {source_net_quantity},'
                              f' to different unit, "{target_unit.value.unit:~P}"'):
                actual = onq.convert_net_quantity_to_different_unit(target_unit, source_net_quantity)
                to_test_tolerance = tolerance if tolerance else decimal.Decimal('0.01')

                # UnitsNet Quantities involving the physical quantity power have magnitudes expressed in the
                # .NET Decimal type which Python.NET **does not** to a Python type (like float) and so must be
                # handled separately.
                if is_power_unit(target_unit):
                    assert_that_net_power_quantities_close_to(actual, target_net_quantity, to_test_tolerance)
                else:
                    tcm.assert_that_net_quantities_close_to(actual, target_net_quantity, to_test_tolerance)


if __name__ == '__main__':
    unittest.main()
