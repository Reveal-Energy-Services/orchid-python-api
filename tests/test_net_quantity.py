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

import decimal
import unittest

from hamcrest import assert_that, equal_to, close_to
import toolz.curried as toolz

from orchid import (
    measurement as om,
    net_quantity as onq,
    physical_quantity as opq,
    unit_system as units,
)

from tests import (custom_matchers as tcm)

# noinspection PyUnresolvedReferences
from System import Decimal
# noinspection PyUnresolvedReferences
import UnitsNet


def assert_that_net_power_quantities_close_to(actual, expected_net_quantity, tolerance):
    assert_that(tcm.get_net_unit(actual), equal_to(tcm.get_net_unit(expected_net_quantity)))
    to_test_actual = decimal.Decimal(onq.net_decimal_to_float(actual.Value))
    to_test_expected = decimal.Decimal(onq.net_decimal_to_float(expected_net_quantity.Value))
    to_test_tolerance = decimal.Decimal(tolerance)
    assert_that(to_test_actual, close_to(to_test_expected, to_test_tolerance))


def is_power_measurement(measurement):
    return is_power_unit(measurement.units)


def is_power_unit(unit):
    return unit == om.registry.hp or unit == om.registry.W


# Convenience functions to create `UnitsNet` units for tests
net_angle_from_degrees = toolz.compose(UnitsNet.Angle.FromDegrees, onq.to_net_quantity_value)
net_duration_from_minutes = toolz.compose(UnitsNet.Duration.FromMinutes, onq.to_net_quantity_value)
net_density_from_lbs_per_cu_ft = toolz.compose(UnitsNet.Density.FromPoundsPerCubicFoot,
                                               onq.to_net_quantity_value)
net_density_from_kg_per_cu_m = toolz.compose(UnitsNet.Density.FromKilogramsPerCubicMeter,
                                             onq.to_net_quantity_value)
net_energy_from_ft_lbs = toolz.compose(UnitsNet.Energy.FromFootPounds, onq.to_net_quantity_value)
net_energy_from_J = toolz.compose(UnitsNet.Energy.FromJoules, onq.to_net_quantity_value)
net_force_from_lbf = toolz.compose(UnitsNet.Force.FromPoundsForce, onq.to_net_quantity_value)
net_force_from_N = toolz.compose(UnitsNet.Force.FromNewtons, onq.to_net_quantity_value)
net_length_from_ft = toolz.compose(UnitsNet.Length.FromFeet, onq.to_net_quantity_value)
net_length_from_m = toolz.compose(UnitsNet.Length.FromMeters, onq.to_net_quantity_value)


# Test ideas
# - well.frac_gradient (property - appears to return "ratio unit", `FracGradient`)
#   (Consider not exposing this property because we expect it to change.)
# - well.shmin (property - returns `Nullable<Pressure?>`)
#   (Consider not exposing this property because of `Nullable<T>`.)
# - stage.md_top, md_bottom (adjust existing)
# - stage.get_stage_location_center and similar (adjust existing)
# - stage_port.isip (property)
#
# Although Pint supports the unit `cu_ft`, we have chosen to use the synonym, `ft ** 3` (which is
# printed as 'ft\u00b3` (that is, 'ft' followed by a Unicode superscript 3)). According to a
# citation on [Wikipedia article](https://en.wikipedia.org/wiki/Cubic_foot), this "is the IEEE
# symbol for the cubic foot." Our general rule: we accept the Pint unit `cu_ft` as **input**,
# but, on various conversion, produce the Pint unit `ft**3`.
#
# The behavior resulting from this choice is illustrated in:
# - test_as_measurement
# - test_as_measurement_in_specified_same_unit
# - test_as_measurement_in_specified_different_unit
# - test_as_net_quantity
# - test_as_net_quantity_in_same_unit
# - test_as_net_quantity_in_different_unit
class TestNetQuantity(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_measurement(self):
        for net_quantity, expected, physical_quantity, tolerance in [
            (net_angle_from_degrees(306.1), 306.1 * om.registry.deg,
             opq.PhysicalQuantity.ANGLE, decimal.Decimal('0.1')),
            (net_duration_from_minutes(1.414), 1.414 * om.registry.min,
             opq.PhysicalQuantity.DURATION, decimal.Decimal('0.1')),
            (net_density_from_lbs_per_cu_ft(70.13e-3), 70.13e-3 * om.registry.lb / om.registry.ft ** 3,
             opq.PhysicalQuantity.DENSITY, decimal.Decimal('0.01e-3')),
            (net_density_from_kg_per_cu_m(1.123), 1.123 * om.registry.kg / (om.registry.m ** 3),
             opq.PhysicalQuantity.DENSITY, decimal.Decimal('0.001')),
            (net_energy_from_ft_lbs(43.12e9), 43.12e9 * om.registry.ft_lb,
             opq.PhysicalQuantity.ENERGY, decimal.Decimal('0.01e9')),
            (net_energy_from_J(14.22e3), 14.22e3 * om.registry.J,
             opq.PhysicalQuantity.ENERGY, decimal.Decimal('0.01e3')),
            (net_force_from_lbf(101.0e3), 101.0e3 * om.registry.lbf,
             opq.PhysicalQuantity.FORCE, decimal.Decimal('0.1e3')),
            (net_force_from_N(441.2e3), 441.2e3 * om.registry.N,
             opq.PhysicalQuantity.FORCE, decimal.Decimal('0.1e3')),
            (net_length_from_ft(44.49), 44.49 * om.registry.ft,
             opq.PhysicalQuantity.LENGTH, decimal.Decimal('0.01')),
            (net_length_from_m(13.56), 13.56 * om.registry.m,
             opq.PhysicalQuantity.LENGTH, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromPounds(onq.to_net_quantity_value(30.94)),
             30.94 * om.registry.lb, opq    .PhysicalQuantity.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromKilograms(onq.to_net_quantity_value(68.21)),
             68.21 * om.registry.kg, opq.PhysicalQuantity.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Power.FromMechanicalHorsepower(onq.to_net_quantity_value(23.28e3)),
             23.28e3 * om.registry.hp, opq.PhysicalQuantity.POWER, decimal.Decimal('0.01e3')),
            (UnitsNet.Power.FromWatts(onq.to_net_quantity_value(21.05)),
             21.05 * om.registry.W, opq.PhysicalQuantity.POWER, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(onq.to_net_quantity_value(49.70)),
             49.70 * om.registry.psi, opq.PhysicalQuantity.PRESSURE, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromKilopascals(onq.to_net_quantity_value(342.7)),
             342.7 * om.registry.kPa, opq.PhysicalQuantity.PRESSURE, decimal.Decimal('0.01')),
            (UnitsNet.MassConcentration.FromPoundsPerUSGallon(onq.to_net_quantity_value(3.82)),
             3.82 * om.registry.lb / om.registry.gal, opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.01')),
            (UnitsNet.MassConcentration.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(457.4)),
             457.4 * om.registry.kg / (om.registry.m ** 3), opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.01')),
            (UnitsNet.VolumeFlow.FromOilBarrelsPerMinute(onq.to_net_quantity_value(114.6)),
             114.6 * om.registry.oil_bbl / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE, decimal.Decimal('0.1')),
            (UnitsNet.VolumeFlow.FromCubicMetersPerMinute(onq.to_net_quantity_value(18.22)),
             18.22 * (om.registry.m ** 3) / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE, decimal.Decimal('0.01')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(onq.to_net_quantity_value(153.6)),
             om.Quantity(153.6, om.registry.degF), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesCelsius(onq.to_net_quantity_value(4.618)),
             om.Quantity(4.618, om.registry.degC), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.001')),
            (UnitsNet.Volume.FromOilBarrels(onq.to_net_quantity_value(83.48)),
             83.48 * om.registry.oil_bbl, opq.PhysicalQuantity.VOLUME, decimal.Decimal('0.01')),
            (UnitsNet.Volume.FromCubicMeters(onq.to_net_quantity_value(13.27)),
             13.27 * om.registry.m ** 3, opq.PhysicalQuantity.VOLUME, decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Test as_measurement for {expected.magnitude} {expected.units:~P}'):
                actual = onq.as_measurement(physical_quantity, net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_measurement_in_common_unit(self):
        for to_convert_net_quantity, expected, to_unit, tolerance in [
            (UnitsNet.Angle.FromDegrees(onq.to_net_quantity_value(306.1)),
             306.1 * om.registry.deg, units.Common.ANGLE, decimal.Decimal('0.1')),
            (UnitsNet.Duration.FromMinutes(onq.to_net_quantity_value(1.414)),
             1.414 * om.registry.min, units.Common.DURATION, decimal.Decimal('0.001')),
        ]:
            with self.subTest(f'Test as_measurement_in_common_unit for {expected.magnitude} {expected.units:~P}'):
                actual = onq.as_measurement(to_unit, to_convert_net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_measurement_in_specified_same_unit(self):
        for to_convert_net_quantity, expected, to_unit, tolerance in [
            (UnitsNet.Density.FromPoundsPerCubicFoot(onq.to_net_quantity_value(40.79)),
             40.79 * om.registry.lb / om.registry.ft ** 3, units.UsOilfield.DENSITY, decimal.Decimal('0.01')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(921.4)),
             921.4 * om.registry.kg / (om.registry.m ** 3), units.Metric.DENSITY, decimal.Decimal('0.01')),
            (UnitsNet.Energy.FromFootPounds(onq.to_net_quantity_value(43.12e9)),
             43.12e9 * om.registry.ft_lb, units.UsOilfield.ENERGY, decimal.Decimal('0.001e9')),
            (UnitsNet.Energy.FromJoules(onq.to_net_quantity_value(14.22e3)),
             14.22e3 * om.registry.J, units.Metric.ENERGY, decimal.Decimal('0.01e3')),
            (UnitsNet.Force.FromPoundsForce(onq.to_net_quantity_value(101.0e3)),
             101.0e3 * om.registry.lbf, units.UsOilfield.FORCE, decimal.Decimal('0.1e3')),
            (UnitsNet.Force.FromNewtons(onq.to_net_quantity_value(441.2e3)),
             441.2e3 * om.registry.N, units.Metric.FORCE, decimal.Decimal('0.1e3')),
            (UnitsNet.Length.FromFeet(onq.to_net_quantity_value(44.49)),
             44.49 * om.registry.ft, units.UsOilfield.LENGTH, decimal.Decimal('0.01')),
            (UnitsNet.Length.FromMeters(onq.to_net_quantity_value(13.56)),
             13.56 * om.registry.m, units.Metric.LENGTH, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromPounds(onq.to_net_quantity_value(30.94)),
             30.94 * om.registry.lb, units.UsOilfield.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromKilograms(onq.to_net_quantity_value(68.21)),
             68.21 * om.registry.kg, units.Metric.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Power.FromMechanicalHorsepower(onq.to_net_quantity_value(23.28e3)),
             23.28e3 * om.registry.hp, units.UsOilfield.POWER, decimal.Decimal('1')),
            (UnitsNet.Power.FromWatts(onq.to_net_quantity_value(21.05)),
             21.05 * om.registry.W, units.Metric.POWER, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(onq.to_net_quantity_value(49.70)),
             49.70 * om.registry.psi, units.UsOilfield.PRESSURE, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromKilopascals(onq.to_net_quantity_value(342.7)),
             342.7 * om.registry.kPa, units.Metric.PRESSURE, decimal.Decimal('0.1')),
            (UnitsNet.MassConcentration.FromPoundsPerUSGallon(onq.to_net_quantity_value(4.258)),
             4.258 * om.registry.lb / om.registry.gal,
             units.UsOilfield.PROPPANT_CONCENTRATION, decimal.Decimal('0.01')),
            (UnitsNet.MassConcentration.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(457.4)),
             457.4 * om.registry.kg / (om.registry.m ** 3),
             units.Metric.PROPPANT_CONCENTRATION, decimal.Decimal('0.01')),
            (UnitsNet.VolumeFlow.FromOilBarrelsPerMinute(onq.to_net_quantity_value(114.6)),
             114.6 * om.registry.oil_bbl / om.registry.min, units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.1')),
            (UnitsNet.VolumeFlow.FromCubicMetersPerMinute(onq.to_net_quantity_value(18.22)),
             18.22 * (om.registry.m ** 3) / om.registry.min,
             opq.PhysicalQuantity.SLURRY_RATE, decimal.Decimal('0.01')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(onq.to_net_quantity_value(153.6)),
             om.Quantity(153.6, om.registry.degF), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesCelsius(onq.to_net_quantity_value(4.618)),
             om.Quantity(4.618, om.registry.degC), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.001')),
            (UnitsNet.Volume.FromOilBarrels(onq.to_net_quantity_value(83.48)),
             83.48 * om.registry.oil_bbl, opq.PhysicalQuantity.VOLUME, decimal.Decimal('0.01')),
            (UnitsNet.Volume.FromCubicMeters(onq.to_net_quantity_value(13.27)),
             13.27 * om.registry.m ** 3, opq.PhysicalQuantity.VOLUME, decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Test as_measurement_in_specified_same_unit for {expected.magnitude}'
                              f' {expected.units:~P}'):
                actual = onq.as_measurement(to_unit, to_convert_net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_measurement_in_specified_different_unit(self):
        for to_convert_net_quantity, expected, to_unit, tolerance in [
            (UnitsNet.Density.FromPoundsPerCubicFoot(onq.to_net_quantity_value(62.30)),
             998.0 * om.registry.kg / (om.registry.m ** 3), units.Metric.DENSITY, decimal.Decimal('0.2')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(998.0)),
             62.30 * om.registry.lb / om.registry.ft ** 3, units.UsOilfield.DENSITY, decimal.Decimal('0.006')),
            (UnitsNet.Energy.FromFootPounds(onq.to_net_quantity_value(2.024)),
             2.744 * om.registry.J, units.Metric.ENERGY, decimal.Decimal('0.002')),
            (UnitsNet.Energy.FromJoules(onq.to_net_quantity_value(2.744)),
             2.024 * om.registry.ft_lb, units.UsOilfield.ENERGY, decimal.Decimal('7e-4')),
            (UnitsNet.Force.FromPoundsForce(onq.to_net_quantity_value(107.8e3)),
             479.5e3 * om.registry.N, units.Metric.FORCE, decimal.Decimal('0.5e3')),
            (UnitsNet.Force.FromNewtons(onq.to_net_quantity_value(479.5e3)),
             107.8e3 * om.registry.lbf, units.UsOilfield.FORCE, decimal.Decimal('0.02e3')),
            (UnitsNet.Length.FromFeet(onq.to_net_quantity_value(155.2)),
             47.30 * om.registry.m, units.Metric.LENGTH, decimal.Decimal('0.04')),
            (UnitsNet.Length.FromMeters(onq.to_net_quantity_value(47.30)),
             155.2 * om.registry.ft, units.UsOilfield.LENGTH, decimal.Decimal('0.03')),
            (UnitsNet.Mass.FromPounds(onq.to_net_quantity_value(7987)),
             3622 * om.registry.kg, units.Metric.MASS, decimal.Decimal('0.5e3')),
            (UnitsNet.Mass.FromKilograms(onq.to_net_quantity_value(3.622e3)),
             7.987e3 * om.registry.lb, units.UsOilfield.MASS, decimal.Decimal('2')),
            (UnitsNet.Power.FromMechanicalHorsepower(onq.to_net_quantity_value(9.254)),
             6901 * om.registry.W, units.Metric.POWER, decimal.Decimal('0.8')),
            (UnitsNet.Power.FromWatts(onq.to_net_quantity_value(6901)),
             9.254 * om.registry.hp, units.UsOilfield.POWER, decimal.Decimal('0.002')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(onq.to_net_quantity_value(6972)),
             48.07e3 * om.registry.kPa, units.Metric.PRESSURE, decimal.Decimal('7')),
            (UnitsNet.Pressure.FromKilopascals(onq.to_net_quantity_value(48.07e3)),
             6972 * om.registry.psi, units.UsOilfield.PRESSURE, decimal.Decimal('2')),
            (UnitsNet.MassConcentration.FromPoundsPerUSGallon(onq.to_net_quantity_value(5.017)),
             601.2 * om.registry.kg / (om.registry.m ** 3),
             units.Metric.PROPPANT_CONCENTRATION, decimal.Decimal('0.2')),
            (UnitsNet.MassConcentration.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(601.2)),
             5.017 * om.registry.lb / om.registry.gal,
             units.UsOilfield.PROPPANT_CONCENTRATION, decimal.Decimal('0.0008')),
            (UnitsNet.VolumeFlow.FromOilBarrelsPerMinute(onq.to_net_quantity_value(100.9)),
             16.04 * (om.registry.m ** 3) / om.registry.min, units.Metric.SLURRY_RATE, decimal.Decimal('0.02')),
            (UnitsNet.VolumeFlow.FromCubicMetersPerMinute(onq.to_net_quantity_value(16.04)),
             100.9 * om.registry.oil_bbl / om.registry.min, units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(onq.to_net_quantity_value(156.2)),
             om.Quantity(69.00, om.registry.degC), units.Metric.TEMPERATURE, decimal.Decimal('0.05')),
            (UnitsNet.Temperature.FromDegreesCelsius(onq.to_net_quantity_value(69.00)),
             om.Quantity(156.2, om.registry.degF), units.UsOilfield.TEMPERATURE, decimal.Decimal('0.3')),
            (UnitsNet.Volume.FromOilBarrels(onq.to_net_quantity_value(8951)),
             1423 * om.registry.m ** 3, units.Metric.VOLUME, decimal.Decimal('0.2')),
            (UnitsNet.Volume.FromCubicMeters(onq.to_net_quantity_value(1423)),
             8951 * om.registry.oil_bbl, units.UsOilfield.VOLUME, decimal.Decimal('7')),
        ]:
            with self.subTest(f'Test as_measurement_in_specified_different_unit for {expected.magnitude}'
                              f' {expected.units:~P}'):
                actual = onq.as_measurement(to_unit, to_convert_net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_net_quantity(self):
        for to_convert_measurement, physical_quantity, tolerance, expected_net_quantity in [
            (67.07 * om.registry.deg, opq.PhysicalQuantity.ANGLE, decimal.Decimal('0.01'),
             UnitsNet.Angle.FromDegrees(onq.to_net_quantity_value(67.07))),
            (1.414 * om.registry.min, opq.PhysicalQuantity.DURATION, decimal.Decimal('0.001'),
             UnitsNet.Duration.FromMinutes(onq.to_net_quantity_value(1.414))),
            (17.17 * om.registry.lb / om.registry.cu_ft, opq.PhysicalQuantity.DENSITY, decimal.Decimal('0.01'),
             UnitsNet.Density.FromPoundsPerCubicFoot(onq.to_net_quantity_value(17.17))),
            (17.17 * om.registry.lb / om.registry.ft ** 3, opq.PhysicalQuantity.DENSITY, decimal.Decimal('0.01'),
             UnitsNet.Density.FromPoundsPerCubicFoot(onq.to_net_quantity_value(17.17))),
            (2.72 * om.registry.kg / (om.registry.m ** 3), opq.PhysicalQuantity.DENSITY, decimal.Decimal('0.01'),
             UnitsNet.Density.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(2.72))),
            (36.26e9 * om.registry.ft_lb, opq.PhysicalQuantity.ENERGY, decimal.Decimal('0.01e3'),
             UnitsNet.Energy.FromFootPounds(onq.to_net_quantity_value(36.26e9))),
            (17.65e3 * om.registry.J, opq.PhysicalQuantity.ENERGY, decimal.Decimal('0.01e3'),
             UnitsNet.Energy.FromJoules(onq.to_net_quantity_value(17.650e3))),
            (147.9e3 * om.registry.lbf, opq.PhysicalQuantity.FORCE, decimal.Decimal('0.1e3'),
             UnitsNet.Force.FromPoundsForce(onq.to_net_quantity_value(147.9e3))),
            (363.9e3 * om.registry.N, opq.PhysicalQuantity.FORCE, decimal.Decimal('0.1e3'),
             UnitsNet.Force.FromNewtons(onq.to_net_quantity_value(363.9e3))),
            (113.8 * om.registry.ft, opq.PhysicalQuantity.LENGTH, decimal.Decimal('0.1'),
             UnitsNet.Length.FromFeet(onq.to_net_quantity_value(113.8))),
            (72.98 * om.registry.m, opq.PhysicalQuantity.LENGTH, decimal.Decimal('0.01'),
             UnitsNet.Length.FromMeters(onq.to_net_quantity_value(72.98))),
            (7922 * om.registry.lb, opq.PhysicalQuantity.MASS, decimal.Decimal('1'),
             UnitsNet.Mass.FromPounds(onq.to_net_quantity_value(7922.36))),
            (134.0e3 * om.registry.kg, opq.PhysicalQuantity.MASS, decimal.Decimal('0.1e3'),
             UnitsNet.Mass.FromKilograms(onq.to_net_quantity_value(134.0e3))),
            (18.87 * om.registry.hp, opq.PhysicalQuantity.POWER, decimal.Decimal('0.01'),
             UnitsNet.Power.FromMechanicalHorsepower(onq.to_net_quantity_value(18.87))),
            (14.02e3 * om.registry.W, opq.PhysicalQuantity.POWER, decimal.Decimal('0.01'),
             UnitsNet.Power.FromWatts(onq.to_net_quantity_value(14.02e3))),
            (6889 * om.registry.psi, opq.PhysicalQuantity.PRESSURE, decimal.Decimal('1'),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(onq.to_net_quantity_value(6889))),
            (59.85e3 * om.registry.kPa, opq.PhysicalQuantity.PRESSURE, decimal.Decimal('0.01e3'),
             UnitsNet.Pressure.FromKilopascals(onq.to_net_quantity_value(59.85e3))),
            (3.55 * om.registry.lb / om.registry.gal,
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION, decimal.Decimal('0.01'),
             UnitsNet.MassConcentration.FromPoundsPerUSGallon(onq.to_net_quantity_value(3.55))),
            (425.0 * om.registry.kg / (om.registry.m ** 3),
             opq.PhysicalQuantity.PROPPANT_CONCENTRATION, decimal.Decimal('0.1'),
             UnitsNet.MassConcentration.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(425.0))),
            (96.06 * om.registry.oil_bbl / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE, decimal.Decimal('0.01'),
             UnitsNet.VolumeFlow.FromOilBarrelsPerMinute(onq.to_net_quantity_value(96.06))),
            (0.80 * (om.registry.m ** 3) / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE, decimal.Decimal('0.01'),
             UnitsNet.VolumeFlow.FromCubicMetersPerMinute(onq.to_net_quantity_value(0.80))),
            (om.registry.Quantity(157.9, om.registry.degF), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.1'),
             UnitsNet.Temperature.FromDegreesFahrenheit(onq.to_net_quantity_value(157.9))),
            (om.registry.Quantity(68.99, om.registry.degC), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.01'),
             UnitsNet.Temperature.FromDegreesCelsius(onq.to_net_quantity_value(68.99))),
            (7217 * om.registry.oil_bbl, opq.PhysicalQuantity.VOLUME, decimal.Decimal('1'),
             UnitsNet.Volume.FromOilBarrels(onq.to_net_quantity_value(7217))),
            (1017 * (om.registry.m ** 3), opq.PhysicalQuantity.VOLUME, decimal.Decimal('1'),
             UnitsNet.Volume.FromCubicMeters(onq.to_net_quantity_value(1017.09))),
        ]:
            with self.subTest(f'Test measurement, {to_convert_measurement},'
                              f' of physical quantity, {physical_quantity}'):
                actual = onq.as_net_quantity(physical_quantity, to_convert_measurement)

                # UnitsNet Quantities involving the physical quantity power have magnitudes expressed in the
                # .NET Decimal type which Python.NET **does not** to a Python type (like float) and so must be
                # handled separately.
                if is_power_measurement(to_convert_measurement):
                    assert_that_net_power_quantities_close_to(actual, expected_net_quantity, tolerance)
                else:
                    tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, tolerance)

    def test_as_net_quantity_in_same_unit(self):
        for to_convert_measurement, to_unit, tolerance, expected_net_quantity in [
            (14.14 * om.registry.deg, units.Common.ANGLE, decimal.Decimal('0.01'),
             UnitsNet.Angle.FromDegrees(onq.to_net_quantity_value(14.14))),
            (27.18 * om.registry.min, units.Common.DURATION, decimal.Decimal('0.01'),
             UnitsNet.Duration.FromMinutes(onq.to_net_quantity_value(27.18))),
            (217.7 * om.registry.lb / om.registry.cu_ft, units.UsOilfield.DENSITY, decimal.Decimal('0.1'),
             UnitsNet.Density.FromPoundsPerCubicFoot(onq.to_net_quantity_value(217.7))),
            (217.7 * om.registry.lb / om.registry.ft ** 3, units.UsOilfield.DENSITY, decimal.Decimal('0.1'),
             UnitsNet.Density.FromPoundsPerCubicFoot(onq.to_net_quantity_value(217.7))),
            (3487 * om.registry.kg / om.registry.m ** 3, units.Metric.DENSITY, decimal.Decimal('1'),
             UnitsNet.Density.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(3487))),
            (31.20e9 * om.registry.ft_lb, units.UsOilfield.ENERGY, decimal.Decimal('0.01e9'),
             UnitsNet.Energy.FromFootPounds(onq.to_net_quantity_value(31.20e9))),
            (42.30e9 * om.registry.J, units.Metric.ENERGY, decimal.Decimal('0.01e9'),
             UnitsNet.Energy.FromJoules(onq.to_net_quantity_value(42.30e9))),
            (106.8e3 * om.registry.lbf, units.UsOilfield.FORCE, decimal.Decimal('0.1e3'),
             UnitsNet.Force.FromPoundsForce(onq.to_net_quantity_value(106.8e3))),
            (475.1e3 * om.registry.N, units.Metric.FORCE, decimal.Decimal('0.1e3'),
             UnitsNet.Force.FromNewtons(onq.to_net_quantity_value(475.1e3))),
            (44.49 * om.registry.ft, units.UsOilfield.LENGTH, decimal.Decimal('0.01'),
             UnitsNet.Length.FromFeet(onq.to_net_quantity_value(44.49))),
            (25.93 * om.registry.m, units.Metric.LENGTH, decimal.Decimal('0.01'),
             UnitsNet.Length.FromMeters(onq.to_net_quantity_value(25.93))),
            (5334 * om.registry.lb, units.UsOilfield.MASS, decimal.Decimal('1'),
             UnitsNet.Mass.FromPounds(onq.to_net_quantity_value(5334))),
            (145.5e3 * om.registry.kg, units.Metric.MASS, decimal.Decimal('0.1e3'),
             UnitsNet.Mass.FromKilograms(onq.to_net_quantity_value(145.5e3))),
            (24.18 * om.registry.hp, units.UsOilfield.POWER, decimal.Decimal('0.01'),
             UnitsNet.Power.FromMechanicalHorsepower(onq.to_net_quantity_value(24.18))),
            (18.03e3 * om.registry.W, units.Metric.POWER, decimal.Decimal('0.01e3'),
             UnitsNet.Power.FromWatts(onq.to_net_quantity_value(18.03e3))),
            (8303 * om.registry.psi, units.UsOilfield.PRESSURE, decimal.Decimal('1'),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(onq.to_net_quantity_value(8303))),
            (64.32 * om.registry.kPa, units.Metric.PRESSURE, decimal.Decimal('0.01'),
             UnitsNet.Pressure.FromKilopascals(onq.to_net_quantity_value(64.32))),
            (5.367 * om.registry.lb / om.registry.gal,
             units.UsOilfield.PROPPANT_CONCENTRATION, decimal.Decimal('0.001'),
             UnitsNet.MassConcentration.FromPoundsPerUSGallon(onq.to_net_quantity_value(5.367))),
            (643.1 * om.registry.kg / (om.registry.m ** 3),
             units.Metric.PROPPANT_CONCENTRATION, decimal.Decimal('0.1'),
             UnitsNet.MassConcentration.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(643.1))),
            (97.93 * (om.registry.oil_bbl / om.registry.min), units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.01'),
             UnitsNet.VolumeFlow.FromOilBarrelsPerMinute(onq.to_net_quantity_value(97.93))),
            (15.57 * (om.registry.m ** 3) / om.registry.min, units.Metric.SLURRY_RATE, decimal.Decimal('0.01'),
             UnitsNet.VolumeFlow.FromCubicMetersPerMinute(onq.to_net_quantity_value(15.57))),
            (om.Quantity(154.3, om.registry.degF), units.UsOilfield.TEMPERATURE, decimal.Decimal('0.1'),
             UnitsNet.Temperature.FromDegreesFahrenheit(onq.to_net_quantity_value(154.3))),
            (om.Quantity(67.94, om.registry.degC), units.Metric.TEMPERATURE, decimal.Decimal('0.01'),
             UnitsNet.Temperature.FromDegreesCelsius(onq.to_net_quantity_value(67.94))),
            (6944 * om.registry.oil_bbl, units.UsOilfield.VOLUME, decimal.Decimal('1'),
             UnitsNet.Volume.FromOilBarrels(onq.to_net_quantity_value(6944))),
            (880.9 * om.registry.m ** 3, units.Metric.VOLUME, decimal.Decimal('0.1'),
             UnitsNet.Volume.FromCubicMeters(onq.to_net_quantity_value(880.9))),
        ]:
            with self.subTest(f'Test measurement, {to_convert_measurement}, as_net_quantity, but in the same units.'):
                actual = onq.as_net_quantity(to_unit, to_convert_measurement)

                # UnitsNet Quantities involving the physical quantity power have magnitudes expressed in the
                # .NET Decimal type which Python.NET **does not** to a Python type (like float) and so must be
                # handled separately.
                if is_power_measurement(to_convert_measurement):
                    assert_that_net_power_quantities_close_to(actual, expected_net_quantity, tolerance)
                else:
                    tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, tolerance)

    def test_as_net_quantity_in_different_unit(self):
        for to_convert_measurement, target_unit, tolerance, expected_net_quantity in [
            (2638 * om.registry.kg / (om.registry.m ** 3), units.UsOilfield.DENSITY, decimal.Decimal('0.06'),
             UnitsNet.Density.FromPoundsPerCubicFoot(onq.to_net_quantity_value(164.7))),
            (164.7 * om.registry.lb / om.registry.cu_ft, units.Metric.DENSITY, decimal.Decimal('2'),
             UnitsNet.Density.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(2638))),
            (164.7 * om.registry.lb / om.registry.ft ** 3, units.Metric.DENSITY, decimal.Decimal('2'),
             UnitsNet.Density.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(2638))),
            (53.58e9 * om.registry.ft_lb, units.Metric.ENERGY, decimal.Decimal('0.01e9'),
             UnitsNet.Energy.FromJoules(onq.to_net_quantity_value(72.65e9))),
            (72.65e9 * om.registry.J, units.UsOilfield.ENERGY, decimal.Decimal('0.01e9'),
             UnitsNet.Energy.FromFootPounds(onq.to_net_quantity_value(53.58e9))),
            (507.4e3 * om.registry.N, units.UsOilfield.FORCE, decimal.Decimal('0.1e3'),
             UnitsNet.Force.FromPoundsForce(onq.to_net_quantity_value(114.1e3))),
            (114.1e3 * om.registry.lbf, units.Metric.FORCE, decimal.Decimal('0.4e3'),
             UnitsNet.Force.FromNewtons(onq.to_net_quantity_value(507.4e3))),
            (43.13 * om.registry.m, units.UsOilfield.LENGTH, decimal.Decimal('0.03'),
             UnitsNet.Length.FromFeet(onq.to_net_quantity_value(141.51))),
            (141.5 * om.registry.ft, units.Metric.LENGTH, decimal.Decimal('0.01'),
             UnitsNet.Length.FromMeters(onq.to_net_quantity_value(43.13))),
            (4108 * om.registry.lb, units.Metric.MASS, decimal.Decimal('1'),
             UnitsNet.Mass.FromKilograms(onq.to_net_quantity_value(1863))),
            (1863 * om.registry.kg, units.UsOilfield.MASS, decimal.Decimal('2'),
             UnitsNet.Mass.FromPounds(onq.to_net_quantity_value(4108))),
            (13.66 * om.registry.hp, units.Metric.POWER, decimal.Decimal('0.01e3'),
             UnitsNet.Power.FromWatts(onq.to_net_quantity_value(10.18e3))),
            (10.18e3 * om.registry.W, units.UsOilfield.POWER, decimal.Decimal('0.02'),
             UnitsNet.Power.FromMechanicalHorsepower(onq.to_net_quantity_value(13.66))),
            (6984 * om.registry.psi, units.Metric.PRESSURE, decimal.Decimal('0.01e3'),
             UnitsNet.Pressure.FromKilopascals(onq.to_net_quantity_value(48.15e3))),
            (48.15e3 * om.registry.kPa, units.UsOilfield.PRESSURE, decimal.Decimal('2'),
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(onq.to_net_quantity_value(6984))),
            (486.4 * om.registry.kg / om.registry.m ** 3,
             units.UsOilfield.PROPPANT_CONCENTRATION, decimal.Decimal('0.001'),
             UnitsNet.MassConcentration.FromPoundsPerUSGallon(onq.to_net_quantity_value(4.060))),
            (4.060 * om.registry.lb / om.registry.gal,
             units.Metric.PROPPANT_CONCENTRATION, decimal.Decimal('0.2'),
             UnitsNet.MassConcentration.FromKilogramsPerCubicMeter(onq.to_net_quantity_value(486.4))),
            (11.14 * (om.registry.m ** 3) / om.registry.min, units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.06'),
             UnitsNet.VolumeFlow.FromOilBarrelsPerMinute(onq.to_net_quantity_value(70.08))),
            (70.08 * om.registry.oil_bbl / om.registry.min, units.Metric.SLURRY_RATE, decimal.Decimal('0.01'),
             UnitsNet.VolumeFlow.FromCubicMetersPerMinute(onq.to_net_quantity_value(11.14))),
            (om.Quantity(35.61, om.registry.degF), units.Metric.TEMPERATURE, decimal.Decimal('0.002'),
             UnitsNet.Temperature.FromDegreesCelsius(onq.to_net_quantity_value(2.004))),
            (om.Quantity(2.004, om.registry.degC), units.UsOilfield.TEMPERATURE, decimal.Decimal('0.02'),
             UnitsNet.Temperature.FromDegreesFahrenheit(onq.to_net_quantity_value(35.61))),
            (8722 * om.registry.oil_bbl, units.Metric.VOLUME, decimal.Decimal('1'),
             UnitsNet.Volume.FromCubicMeters(onq.to_net_quantity_value(1387)),),
            (1387 * om.registry.m ** 3, units.UsOilfield.VOLUME, decimal.Decimal('7'),
             UnitsNet.Volume.FromOilBarrels(onq.to_net_quantity_value(8722))),
        ]:
            with self.subTest(f'Converting .NET quantity, {to_convert_measurement}, to {target_unit}'):
                actual = onq.as_net_quantity(target_unit, to_convert_measurement)
                # UnitsNet Quantities involving the physical quantity power have magnitudes expressed in the
                # .NET Decimal type which Python.NET **does not** to a Python type (like float) and so must be
                # handled separately.
                if is_power_measurement(to_convert_measurement):
                    assert_that_net_power_quantities_close_to(actual, expected_net_quantity, tolerance)
                else:
                    tcm.assert_that_net_quantities_close_to(actual, expected_net_quantity, tolerance)


if __name__ == '__main__':
    unittest.main()
