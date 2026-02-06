#  Copyright (c) 2017-2025 KAPPA
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
import math
import unittest

from hamcrest import assert_that, equal_to, close_to, is_, none
import option

from orchid import (
    measurement as om,
    net_quantity as onq,
    physical_quantity as opq,
    unit_system as units,
)

from tests import (custom_matchers as tcm)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import ScriptAdapter
# noinspection PyUnresolvedReferences
from Optional import Option
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
# - test_deprecated_as_measurement_in_specified_same_unit
# - test_as_measurement_in_specified_different_unit
# - test_as_net_quantity
# - test_as_net_quantity_in_same_unit
# - test_as_net_quantity_in_different_unit
class TestNetQuantity(unittest.TestCase):

    # noinspection PyUnresolvedReferences
    def test_as_measurement_in_common_unit(self):
        for to_convert_net_quantity, expected, to_unit, tolerance in [
            (option.Some(onq.net_angle_from_deg(306.1)),
             306.1 * om.registry.deg, units.Common.ANGLE, decimal.Decimal('0.1')),
            (option.Some(onq.net_duration_from_min(1.414)),
             1.414 * om.registry.min, units.Common.DURATION, decimal.Decimal('0.001')),
        ]:
            with self.subTest(f'Test as_measurement_in_common_unit for {expected.magnitude} {expected.units:~P}'):
                actual = onq.as_measurement(to_unit, to_convert_net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    # noinspection PyUnresolvedReferences
    def test_as_measurement_in_same_target_unit(self):
        for to_convert_net_quantity, expected, to_unit, tolerance in [
            (option.Some(onq.net_density_from_lbs_per_cu_ft(40.79)),
             40.79 * om.registry.lb / om.registry.ft ** 3,
             units.UsOilfield.DENSITY, decimal.Decimal('0.01')),
            (option.Some(onq.net_density_from_kg_per_cu_m(921.4)),
             921.4 * om.registry.kg / (om.registry.m ** 3),
             units.Metric.DENSITY, decimal.Decimal('0.01')),
            (option.Some(onq.net_energy_from_ft_lbs(43.12e9)), 43.12e9 * om.registry.ft_lb,
             units.UsOilfield.ENERGY, decimal.Decimal('0.001e9')),
            (option.Some(onq.net_energy_from_J(14.22e3)), 14.22e3 * om.registry.J,
             units.Metric.ENERGY, decimal.Decimal('0.01e3')),
            (option.Some(onq.net_force_from_lbf(101.0e3)), 101.0e3 * om.registry.lbf,
             units.UsOilfield.FORCE, decimal.Decimal('0.1e3')),
            (option.Some(onq.net_force_from_N(441.2e3)), 441.2e3 * om.registry.N,
             units.Metric.FORCE, decimal.Decimal('0.1e3')),
            (option.Some(onq.net_length_from_ft(44.49)), 44.49 * om.registry.ft,
             units.UsOilfield.LENGTH, decimal.Decimal('0.01')),
            (option.Some(onq.net_length_from_m(13.56)), 13.56 * om.registry.m,
             units.Metric.LENGTH, decimal.Decimal('0.01')),
            (option.Some(onq.net_mass_from_lbs(30.94)), 30.94 * om.registry.lb,
             units.UsOilfield.MASS, decimal.Decimal('0.01')),
            (option.Some(onq.net_mass_from_kg(68.21)), 68.21 * om.registry.kg,
             units.Metric.MASS, decimal.Decimal('0.01')),
            (option.Some(onq.net_power_from_hp(23.28e3)), 23.28e3 * om.registry.hp,
             units.UsOilfield.POWER, decimal.Decimal('1')),
            (option.Some(onq.net_power_from_W(21.05)), 21.05 * om.registry.W,
             units.Metric.POWER, decimal.Decimal('0.01')),
            (option.Some(onq.net_pressure_from_psi(49.70)), 49.70 * om.registry.psi,
             units.UsOilfield.PRESSURE, decimal.Decimal('0.01')),
            (option.Some(onq.net_pressure_from_kPa(342.7)), 342.7 * om.registry.kPa,
             units.Metric.PRESSURE, decimal.Decimal('0.1')),
            (option.Some(onq.net_mass_concentration_from_lbs_per_gal(4.258)),
             4.258 * om.registry.lb / om.registry.gal,
             units.UsOilfield.PROPPANT_CONCENTRATION, decimal.Decimal('0.01')),
            (option.Some(onq.net_mass_concentration_from_kg_per_cu_m(457.4)),
             457.4 * om.registry.kg / (om.registry.m ** 3),
             units.Metric.PROPPANT_CONCENTRATION, decimal.Decimal('0.01')),
            (option.Some(onq.net_volume_flow_from_oil_bbl_per_min(114.6)),
             114.6 * om.registry.oil_bbl / om.registry.min,
             units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.1')),
            (option.Some(onq.net_volume_flow_from_cu_m_per_min(18.22)),
             18.22 * (om.registry.m ** 3) / om.registry.min,
             units.Metric.SLURRY_RATE, decimal.Decimal('0.01')),
            (option.Some(onq.net_temperature_from_deg_F(153.6)),
             om.Quantity(153.6, om.registry.degF),
             units.UsOilfield.TEMPERATURE, decimal.Decimal('0.1')),
            (option.Some(onq.net_temperature_from_deg_C(4.618)),
             om.Quantity(4.618, om.registry.degC),
             units.Metric.TEMPERATURE, decimal.Decimal('0.001')),
            (option.Some(onq.net_volume_from_oil_bbl(83.48)),
             83.48 * om.registry.oil_bbl,
             units.UsOilfield.VOLUME, decimal.Decimal('0.01')),
            (option.Some(onq.net_volume_from_cu_m(13.27)),
             13.27 * om.registry.m ** 3,
             units.Metric.VOLUME, decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Test as_measurement_in_specified_same_unit for {expected.magnitude}'
                              f' {expected.units:~P}'):
                actual = onq.as_measurement(to_unit, to_convert_net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    # noinspection PyUnresolvedReferences
    def test_as_measurement_in_target_unit_from_none(self):
        for to_convert_net_quantity, to_unit in [
            (option.NONE, units.UsOilfield.DENSITY),
            (option.NONE, units.Metric.DENSITY),
            (option.NONE, units.UsOilfield.ENERGY),
            (option.NONE, units.Metric.ENERGY),
            (option.NONE, units.UsOilfield.FORCE),
            (option.NONE, units.Metric.FORCE),
            (option.NONE, units.UsOilfield.LENGTH),
            (option.NONE, units.Metric.LENGTH),
            (option.NONE, units.UsOilfield.MASS),
            (option.NONE, units.Metric.MASS),
            (option.NONE, units.UsOilfield.POWER),
            (option.NONE, units.Metric.POWER),
            (option.NONE, units.UsOilfield.PRESSURE),
            (option.NONE, units.Metric.PRESSURE),
            (option.NONE, units.UsOilfield.PROPPANT_CONCENTRATION),
            (option.NONE, units.Metric.PROPPANT_CONCENTRATION),
            (option.NONE, units.UsOilfield.SLURRY_RATE),
            (option.NONE, units.Metric.SLURRY_RATE),
            (option.NONE, units.UsOilfield.TEMPERATURE),
            (option.NONE, units.Metric.TEMPERATURE),
            (option.NONE, units.UsOilfield.VOLUME),
            (option.NONE, units.Metric.VOLUME),
        ]:
            with self.subTest(f'Test as_measurement_in_target_unit for {to_unit.value.unit:~P}'):
                actual = onq.as_measurement(to_unit, to_convert_net_quantity)
                tcm.assert_that_measurement_is_nan(actual, to_unit.value.unit)

    # noinspection PyUnresolvedReferences
    def test_as_measurement_in_specified_different_unit(self):
        for to_convert_net_quantity, expected, to_unit, tolerance in [
            (option.Some(onq.net_density_from_lbs_per_cu_ft(62.30)),
             998.0 * om.registry.kg / (om.registry.m ** 3),
             units.Metric.DENSITY, decimal.Decimal('0.2')),
            (option.Some(onq.net_density_from_kg_per_cu_m(998.0)),
             62.30 * om.registry.lb / om.registry.ft ** 3,
             units.UsOilfield.DENSITY, decimal.Decimal('0.006')),
            (option.Some(onq.net_energy_from_ft_lbs(2.024)),
             2.744 * om.registry.J, units.Metric.ENERGY, decimal.Decimal('0.002')),
            (option.Some(onq.net_energy_from_J(2.744)),
             2.024 * om.registry.ft_lb, units.UsOilfield.ENERGY, decimal.Decimal('7e-4')),
            (option.Some(onq.net_force_from_lbf(107.8e3)),
             479.5e3 * om.registry.N, units.Metric.FORCE, decimal.Decimal('0.5e3')),
            (option.Some(onq.net_force_from_N(479.5e3)),
             107.8e3 * om.registry.lbf, units.UsOilfield.FORCE, decimal.Decimal('0.02e3')),
            (option.Some(onq.net_length_from_ft(155.2)),
             47.30 * om.registry.m, units.Metric.LENGTH, decimal.Decimal('0.04')),
            (option.Some(onq.net_length_from_m(47.30)),
             155.2 * om.registry.ft, units.UsOilfield.LENGTH, decimal.Decimal('0.03')),
            (option.Some(onq.net_mass_from_lbs(7987)),
             3622 * om.registry.kg, units.Metric.MASS, decimal.Decimal('0.5e3')),
            (option.Some(onq.net_mass_from_kg(3.622e3)),
             7.987e3 * om.registry.lb, units.UsOilfield.MASS, decimal.Decimal('2')),
            (option.Some(onq.net_power_from_hp(9.254)),
             6901 * om.registry.W, units.Metric.POWER, decimal.Decimal('0.8')),
            (option.Some(onq.net_power_from_W(6901)),
             9.254 * om.registry.hp, units.UsOilfield.POWER, decimal.Decimal('0.002')),
            (option.Some(onq.net_pressure_from_psi(6972)),
             48.07e3 * om.registry.kPa, units.Metric.PRESSURE, decimal.Decimal('7')),
            (option.Some(onq.net_pressure_from_kPa(48.07e3)),
             6972 * om.registry.psi, units.UsOilfield.PRESSURE, decimal.Decimal('2')),
            (option.Some(onq.net_mass_concentration_from_lbs_per_gal(5.017)),
             601.2 * om.registry.kg / (om.registry.m ** 3),
             units.Metric.PROPPANT_CONCENTRATION, decimal.Decimal('0.2')),
            (option.Some(onq.net_mass_concentration_from_kg_per_cu_m(601.2)),
             5.017 * om.registry.lb / om.registry.gal,
             units.UsOilfield.PROPPANT_CONCENTRATION, decimal.Decimal('0.0008')),
            (option.Some(onq.net_volume_flow_from_oil_bbl_per_min(100.9)),
             16.04 * (om.registry.m ** 3) / om.registry.min,
             units.Metric.SLURRY_RATE, decimal.Decimal('0.02')),
            (option.Some(onq.net_volume_flow_from_cu_m_per_min(16.04)),
             100.9 * om.registry.oil_bbl / om.registry.min,
             units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.1')),
            (option.Some(onq.net_temperature_from_deg_F(156.2)),
             om.Quantity(69.00, om.registry.degC), units.Metric.TEMPERATURE, decimal.Decimal('0.05')),
            (option.Some(onq.net_temperature_from_deg_C(69.00)),
             om.Quantity(156.2, om.registry.degF), units.UsOilfield.TEMPERATURE, decimal.Decimal('0.3')),
            (option.Some(onq.net_volume_from_oil_bbl(8951)),
             1423 * om.registry.m ** 3, units.Metric.VOLUME, decimal.Decimal('0.2')),
            (option.Some(onq.net_volume_from_cu_m(1423)),
             8951 * om.registry.oil_bbl, units.UsOilfield.VOLUME, decimal.Decimal('7')),
        ]:
            with self.subTest(f'Test as_measurement_in_specified_different_unit for {expected.magnitude}'
                              f' {expected.units:~P}'):
                actual = onq.as_measurement(to_unit, to_convert_net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    def test_as_measurement_from_none(self):
        for to_convert_unit, to_unit in [
            (UnitsNet.Duration, units.Common.DURATION),
            (UnitsNet.Density, units.Metric.DENSITY),
            (UnitsNet.Force, units.Metric.FORCE),
            (UnitsNet.MassConcentration, units.Metric.PROPPANT_CONCENTRATION),
            (UnitsNet.Temperature, units.Metric.TEMPERATURE),
        ]:
            to_convert_none = ScriptAdapter.MakeOptionNone[to_convert_unit]()
            with self.subTest(msg=f'Convert no net quantity with unit, {to_convert_unit}, to {to_unit}'):
                actual = onq.as_measurement_from_option(to_unit, to_convert_none)
                tcm.assert_that_measurement_is_nan(actual, to_unit.value.unit)

    # noinspection PyUnresolvedReferences
    def test_as_measurement_from_some(self):
        for some_to_convert, to_unit, expected, tolerance in [
            (Option.Some[UnitsNet.Angle](onq.net_angle_from_deg(298.6)),
             units.Common.ANGLE, 298.6 * om.registry.deg, decimal.Decimal('0.1')),
            (Option.Some[UnitsNet.Duration](onq.net_duration_from_min(57.82)),
             units.Common.DURATION, 57.82 * om.registry.min, decimal.Decimal('0.01')),
            (Option.Some[UnitsNet.Density](onq.net_density_from_lbs_per_cu_ft(27.22e-3)),
             units.Metric.DENSITY, 436.1e-3 * (om.registry.kg / om.registry.m ** 3), decimal.Decimal('0.0001')),
            (Option.Some[UnitsNet.Energy](onq.net_energy_from_ft_lbs(3.378)),
             units.Metric.ENERGY, 4.579 * om.registry.J, decimal.Decimal('0.001')),
            (Option.Some[UnitsNet.Force](onq.net_force_from_lbf(117.2e3)),
             units.Metric.FORCE, 521.3e3 * om.registry.N, decimal.Decimal('0.1e3')),
            (Option.Some[UnitsNet.Length](onq.net_length_from_m(45.96)),
             units.Metric.LENGTH, 45.95 * om.registry.m, decimal.Decimal('0.01')),
            (Option.Some[UnitsNet.Mass](onq.net_mass_from_kg(120.2e3)),
             units.UsOilfield.MASS, 265.0e3 * om.registry.lb, decimal.Decimal('0.1e3')),
            (Option.Some[UnitsNet.Power](onq.net_power_from_W(8807.)),
             units.Metric.POWER, 8807. * om.registry.W, decimal.Decimal('0.1')),
            (Option.Some[UnitsNet.Pressure](onq.net_pressure_from_psi(7874.24)),
             units.Metric.PRESSURE, 54291.0 * om.registry.kPa, decimal.Decimal('0.1')),
            (Option.Some[UnitsNet.MassConcentration](onq.net_mass_concentration_from_kg_per_cu_m(588.0)),
             units.UsOilfield.PROPPANT_CONCENTRATION, 4.907 * (om.registry.lbs / om.registry.gal),
             decimal.Decimal('0.001')),
            (Option.Some[UnitsNet.Temperature](onq.net_temperature_from_deg_F(74.38)),
             units.Metric.TEMPERATURE, om.Quantity(23.54, om.registry.degC), decimal.Decimal('0.01')),
            (Option.Some[UnitsNet.VolumeFlow](onq.net_volume_flow_from_oil_bbl_per_min(91.62)),
             units.UsOilfield.SLURRY_RATE, 91.62 * (om.registry.oil_bbl / om.registry.min),
             decimal.Decimal('0.01')),
            (Option.Some[UnitsNet.Volume](onq.net_volume_from_oil_bbl(5548.)),
             units.Metric.VOLUME, 882.0 * om.registry.m ** 3, decimal.Decimal('0.1')),
        ]:
            with self.subTest(msg=f'Convert {some_to_convert} to {to_unit} correctly.'):
                actual = onq.as_measurement_from_option(to_unit, some_to_convert)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

    # noinspection PyUnresolvedReferences
    def test_as_net_quantity(self):
        for to_convert_measurement, physical_quantity, tolerance, expected_net_quantity in [
            (67.07 * om.registry.deg, opq.PhysicalQuantity.ANGLE,
             decimal.Decimal('0.01'), onq.net_angle_from_deg(67.07)),
            (1.414 * om.registry.min, opq.PhysicalQuantity.DURATION,
             decimal.Decimal('0.001'), onq.net_duration_from_min(1.414)),
            (17.17 * om.registry.lb / om.registry.cu_ft, opq.PhysicalQuantity.DENSITY,
             decimal.Decimal('0.01'), onq.net_density_from_lbs_per_cu_ft(17.17)),
            (17.17 * om.registry.lb / om.registry.ft ** 3, opq.PhysicalQuantity.DENSITY,
             decimal.Decimal('0.01'), onq.net_density_from_lbs_per_cu_ft(17.17)),
            (2.72 * om.registry.kg / (om.registry.m ** 3), opq.PhysicalQuantity.DENSITY,
             decimal.Decimal('0.01'), onq.net_density_from_kg_per_cu_m(2.72)),
            (36.26e9 * om.registry.ft_lb, opq.PhysicalQuantity.ENERGY,
             decimal.Decimal('0.01e3'), onq.net_energy_from_ft_lbs(36.26e9)),
            (17.65e3 * om.registry.J, opq.PhysicalQuantity.ENERGY,
             decimal.Decimal('0.01e3'), onq.net_energy_from_J(17.650e3)),
            (147.9e3 * om.registry.lbf, opq.PhysicalQuantity.FORCE,
             decimal.Decimal('0.1e3'), onq.net_force_from_lbf(147.9e3)),
            (363.9e3 * om.registry.N, opq.PhysicalQuantity.FORCE,
             decimal.Decimal('0.1e3'), onq.net_force_from_N(363.9e3)),
            (113.8 * om.registry.ft, opq.PhysicalQuantity.LENGTH,
             decimal.Decimal('0.1'), onq.net_length_from_ft(113.8)),
            (72.98 * om.registry.m, opq.PhysicalQuantity.LENGTH,
             decimal.Decimal('0.01'), onq.net_length_from_m(72.98)),
            (7922 * om.registry.lb, opq.PhysicalQuantity.MASS,
             decimal.Decimal('1'), onq.net_mass_from_lbs(7922.36)),
            (134.0e3 * om.registry.kg, opq.PhysicalQuantity.MASS,
             decimal.Decimal('0.1e3'), onq.net_mass_from_kg(134.0e3)),
            (18.87 * om.registry.hp, opq.PhysicalQuantity.POWER,
             decimal.Decimal('0.01'), onq.net_power_from_hp(18.87)),
            (14.02e3 * om.registry.W, opq.PhysicalQuantity.POWER,
             decimal.Decimal('0.01'), onq.net_power_from_W(14.02e3)),
            (6889 * om.registry.psi, opq.PhysicalQuantity.PRESSURE,
             decimal.Decimal('1'), onq.net_pressure_from_psi(6889)),
            (59.85e3 * om.registry.kPa, opq.PhysicalQuantity.PRESSURE,
             decimal.Decimal('0.01e3'), onq.net_pressure_from_kPa(59.85e3)),
            (3.55 * om.registry.lb / om.registry.gal, opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.01'), onq.net_mass_concentration_from_lbs_per_gal(3.55)),
            (425.0 * om.registry.kg / (om.registry.m ** 3), opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.1'), onq.net_mass_concentration_from_kg_per_cu_m(425.0)),
            (96.06 * om.registry.oil_bbl / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE,
             decimal.Decimal('0.01'), onq.net_volume_flow_from_oil_bbl_per_min(96.06)),
            (0.80 * (om.registry.m ** 3) / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE,
             decimal.Decimal('0.01'), onq.net_volume_flow_from_cu_m_per_min(0.80)),
            (om.registry.Quantity(157.9, om.registry.degF), opq.PhysicalQuantity.TEMPERATURE,
             decimal.Decimal('0.1'), onq.net_temperature_from_deg_F(157.9)),
            (om.registry.Quantity(68.99, om.registry.degC), opq.PhysicalQuantity.TEMPERATURE,
             decimal.Decimal('0.01'), onq.net_temperature_from_deg_C(68.99)),
            (7217 * om.registry.oil_bbl, opq.PhysicalQuantity.VOLUME,
             decimal.Decimal('1'), onq.net_volume_from_oil_bbl(7217)),
            (1017 * (om.registry.m ** 3), opq.PhysicalQuantity.VOLUME,
             decimal.Decimal('1'), onq.net_volume_from_cu_m(1017.09)),
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

    # noinspection PyUnresolvedReferences
    def test_as_net_quantity_in_same_unit(self):
        for to_convert_measurement, to_unit, tolerance, expected_net_quantity in [
            (14.14 * om.registry.deg, units.Common.ANGLE,
             decimal.Decimal('0.01'), onq.net_angle_from_deg(14.14)),
            (27.18 * om.registry.min, units.Common.DURATION,
             decimal.Decimal('0.01'), onq.net_duration_from_min(27.18)),
            (217.7 * om.registry.lb / om.registry.cu_ft, units.UsOilfield.DENSITY,
             decimal.Decimal('0.1'), onq.net_density_from_lbs_per_cu_ft(217.7)),
            (217.7 * om.registry.lb / om.registry.ft ** 3, units.UsOilfield.DENSITY,
             decimal.Decimal('0.1'), onq.net_density_from_lbs_per_cu_ft(217.7)),
            (3487 * om.registry.kg / om.registry.m ** 3, units.Metric.DENSITY,
             decimal.Decimal('1'), onq.net_density_from_kg_per_cu_m(3487)),
            (31.20e9 * om.registry.ft_lb, units.UsOilfield.ENERGY,
             decimal.Decimal('0.01e9'), onq.net_energy_from_ft_lbs(31.20e9)),
            (42.30e9 * om.registry.J, units.Metric.ENERGY,
             decimal.Decimal('0.01e9'), onq.net_energy_from_J(42.30e9)),
            (106.8e3 * om.registry.lbf, units.UsOilfield.FORCE,
             decimal.Decimal('0.1e3'), onq.net_force_from_lbf(106.8e3)),
            (475.1e3 * om.registry.N, units.Metric.FORCE,
             decimal.Decimal('0.1e3'), onq.net_force_from_N(475.1e3)),
            (44.49 * om.registry.ft, units.UsOilfield.LENGTH,
             decimal.Decimal('0.01'), onq.net_length_from_ft(44.49)),
            (25.93 * om.registry.m, units.Metric.LENGTH,
             decimal.Decimal('0.01'), onq.net_length_from_m(25.93)),
            (5334 * om.registry.lb, units.UsOilfield.MASS,
             decimal.Decimal('1'), onq.net_mass_from_lbs(5334)),
            (145.5e3 * om.registry.kg, units.Metric.MASS,
             decimal.Decimal('0.1e3'), onq.net_mass_from_kg(145.5e3)),
            (24.18 * om.registry.hp, units.UsOilfield.POWER,
             decimal.Decimal('0.01'), onq.net_power_from_hp(24.18)),
            (18.03e3 * om.registry.W, units.Metric.POWER,
             decimal.Decimal('0.01e3'), onq.net_power_from_W(18.03e3)),
            (8303 * om.registry.psi, units.UsOilfield.PRESSURE,
             decimal.Decimal('1'), onq.net_pressure_from_psi(8303)),
            (64.32 * om.registry.kPa, units.Metric.PRESSURE,
             decimal.Decimal('0.01'), onq.net_pressure_from_kPa(64.32)),
            (5.367 * om.registry.lb / om.registry.gal, units.UsOilfield.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.001'), onq.net_mass_concentration_from_lbs_per_gal(5.367)),
            (643.1 * om.registry.kg / (om.registry.m ** 3), units.Metric.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.1'), onq.net_mass_concentration_from_kg_per_cu_m(643.1)),
            (97.93 * (om.registry.oil_bbl / om.registry.min), units.UsOilfield.SLURRY_RATE,
             decimal.Decimal('0.01'), onq.net_volume_flow_from_oil_bbl_per_min(97.93)),
            (15.57 * (om.registry.m ** 3) / om.registry.min, units.Metric.SLURRY_RATE,
             decimal.Decimal('0.01'), onq.net_volume_flow_from_cu_m_per_min(15.57)),
            (om.Quantity(154.3, om.registry.degF), units.UsOilfield.TEMPERATURE,
             decimal.Decimal('0.1'), onq.net_temperature_from_deg_F(154.3)),
            (om.Quantity(67.94, om.registry.degC), units.Metric.TEMPERATURE,
             decimal.Decimal('0.01'), onq.net_temperature_from_deg_C(67.94)),
            (6944 * om.registry.oil_bbl, units.UsOilfield.VOLUME,
             decimal.Decimal('1'), onq.net_volume_from_oil_bbl(6944)),
            (880.9 * om.registry.m ** 3, units.Metric.VOLUME,
             decimal.Decimal('0.1'), onq.net_volume_from_cu_m(880.9)),
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

    # noinspection PyUnresolvedReferences
    def test_as_net_quantity_in_different_unit(self):
        for to_convert_measurement, target_unit, tolerance, expected_net_quantity in [
            (2638 * om.registry.kg / (om.registry.m ** 3), units.UsOilfield.DENSITY,
             decimal.Decimal('0.06'), onq.net_density_from_lbs_per_cu_ft(164.7)),
            (164.7 * om.registry.lb / om.registry.cu_ft, units.Metric.DENSITY,
             decimal.Decimal('2'), onq.net_density_from_kg_per_cu_m(2638)),
            (164.7 * om.registry.lb / om.registry.ft ** 3, units.Metric.DENSITY,
             decimal.Decimal('2'), onq.net_density_from_kg_per_cu_m(2638)),
            (53.58e9 * om.registry.ft_lb, units.Metric.ENERGY,
             decimal.Decimal('0.01e9'), onq.net_energy_from_J(72.65e9)),
            (72.65e9 * om.registry.J, units.UsOilfield.ENERGY,
             decimal.Decimal('0.01e9'), onq.net_energy_from_ft_lbs(53.58e9)),
            (507.4e3 * om.registry.N, units.UsOilfield.FORCE,
             decimal.Decimal('0.1e3'), onq.net_force_from_lbf(114.1e3)),
            (114.1e3 * om.registry.lbf, units.Metric.FORCE,
             decimal.Decimal('0.4e3'), onq.net_force_from_N(507.4e3)),
            (43.13 * om.registry.m, units.UsOilfield.LENGTH,
             decimal.Decimal('0.03'), onq.net_length_from_ft(141.51)),
            (141.5 * om.registry.ft, units.Metric.LENGTH,
             decimal.Decimal('0.01'), onq.net_length_from_m(43.13)),
            (4108 * om.registry.lb, units.Metric.MASS,
             decimal.Decimal('1'), onq.net_mass_from_kg(1863)),
            (1863 * om.registry.kg, units.UsOilfield.MASS,
             decimal.Decimal('2'), onq.net_mass_from_lbs(4108)),
            (13.66 * om.registry.hp, units.Metric.POWER,
             decimal.Decimal('0.01e3'), onq.net_power_from_W(10.18e3)),
            (10.18e3 * om.registry.W, units.UsOilfield.POWER,
             decimal.Decimal('0.02'), onq.net_power_from_hp(13.66)),
            (6984 * om.registry.psi, units.Metric.PRESSURE,
             decimal.Decimal('0.01e3'), onq.net_pressure_from_kPa(48.15e3)),
            (48.15e3 * om.registry.kPa, units.UsOilfield.PRESSURE,
             decimal.Decimal('2'), onq.net_pressure_from_psi(6984)),
            (486.4 * om.registry.kg / om.registry.m ** 3, units.UsOilfield.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.001'), onq.net_mass_concentration_from_lbs_per_gal(4.060)),
            (4.060 * om.registry.lb / om.registry.gal, units.Metric.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.2'), onq.net_mass_concentration_from_kg_per_cu_m(486.4)),
            (11.14 * (om.registry.m ** 3) / om.registry.min, units.UsOilfield.SLURRY_RATE,
             decimal.Decimal('0.06'), onq.net_volume_flow_from_oil_bbl_per_min(70.08)),
            (70.08 * om.registry.oil_bbl / om.registry.min, units.Metric.SLURRY_RATE,
             decimal.Decimal('0.01'), onq.net_volume_flow_from_cu_m_per_min(11.14)),
            (om.Quantity(2.004, om.registry.degC), units.UsOilfield.TEMPERATURE,
             decimal.Decimal('0.02'), onq.net_temperature_from_deg_F(35.61)),
            (om.Quantity(35.61, om.registry.degF), units.Metric.TEMPERATURE,
             decimal.Decimal('0.002'), onq.net_temperature_from_deg_C(2.004)),
            (1387 * om.registry.m ** 3, units.UsOilfield.VOLUME,
             decimal.Decimal('7'), onq.net_volume_from_oil_bbl(8722)),
            (8722 * om.registry.oil_bbl, units.Metric.VOLUME,
             decimal.Decimal('1'), onq.net_volume_from_cu_m(1387),),
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

    def test_as_net_quantity_measurement_has_nan_magnitude_returns_none(self):
        for to_convert, convert_to in [
            (math.nan * om.registry.J, units.Metric.ENERGY),
            (math.nan * om.registry.hp, opq.PhysicalQuantity.POWER),
            (math.nan * om.registry.m, units.UsOilfield.LENGTH)
        ]:
            with self.subTest(f'as_net_measurement({convert_to}, {to_convert})'):
                optional_net_quantity = onq.as_net_quantity(convert_to, to_convert)
                assert_that(optional_net_quantity, is_(none()))


if __name__ == '__main__':
    unittest.main()
