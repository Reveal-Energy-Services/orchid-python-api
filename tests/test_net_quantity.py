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

from hamcrest import assert_that, equal_to, calling, raises
import dateutil.tz as duz


from orchid import (
    measurement as om,
    net_quantity as onq,
    physical_quantity as opq,
    unit_system as units,
)

from tests import (custom_matchers as tcm,
                   stub_net as tsn)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import (ProppantConcentration, SlurryRate)
# noinspection PyUnresolvedReferences
from System import (DateTime, DateTimeKind, Decimal)
# noinspection PyUnresolvedReferences
import UnitsNet


# Test ideas
# - well.frac_gradient (property - appears to return "ratio unit", `FracGradient`)
#   (Consider not exposing this property because we expect it to change.)
# - well.shmin (property - returns `Nullable<Pressure?>`)
#   (Consider not exposing this property because of `Nullable<T>`.)
# - stage.md_top, md_bottom (adjust existing)
# - stage.get_stage_location_center and similar (adjust existing)
# - stage_port.isip (property)
class TestNetQuantity(unittest.TestCase):
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
        for net_quantity, expected, physical_quantity, tolerance in [
            (UnitsNet.Angle.FromDegrees(UnitsNet.QuantityValue.op_Implicit(306.1)),
             306.1 * om.registry.deg, opq.PhysicalQuantity.ANGLE, decimal.Decimal('0.1')),
            (UnitsNet.Duration.FromMinutes(UnitsNet.QuantityValue.op_Implicit(1.414)),
             1.414 * om.registry.min, opq.PhysicalQuantity.DURATION, decimal.Decimal('0.1')),
            (UnitsNet.Density.FromPoundsPerCubicFoot(UnitsNet.QuantityValue.op_Implicit(70.13e-3)),
             70.13e-3 * om.registry.lb / om.registry.cu_ft,
             opq.PhysicalQuantity.DENSITY, decimal.Decimal('0.01e-3')),
            (UnitsNet.Density.FromKilogramsPerCubicMeter(UnitsNet.QuantityValue.op_Implicit(1.123)),
             1.123 * om.registry.kg / (om.registry.m ** 3),
             opq.PhysicalQuantity.DENSITY, decimal.Decimal('0.001')),
            (UnitsNet.Energy.FromFootPounds(UnitsNet.QuantityValue.op_Implicit(43.12e9)),
             43.12e9 * om.registry.ft_lb, opq.PhysicalQuantity.ENERGY, decimal.Decimal('0.01e9')),
            (UnitsNet.Energy.FromJoules(UnitsNet.QuantityValue.op_Implicit(14.22e3)),
             14.22e3 * om.registry.J, opq.PhysicalQuantity.ENERGY, decimal.Decimal('0.01e3')),
            (UnitsNet.Force.FromPoundsForce(UnitsNet.QuantityValue.op_Implicit(101.0e3)),
             101.0e3 * om.registry.lbf, opq.PhysicalQuantity.FORCE, decimal.Decimal('0.1e3')),
            (UnitsNet.Force.FromNewtons(UnitsNet.QuantityValue.op_Implicit(441.2e3)),
             441.2e3 * om.registry.N, opq.PhysicalQuantity.FORCE,  decimal.Decimal('0.1e3')),
            (UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(44.49)),
             44.49 * om.registry.ft, opq.PhysicalQuantity.LENGTH, decimal.Decimal('0.01')),
            (UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(13.56)),
             13.56 * om.registry.m, opq.PhysicalQuantity.LENGTH, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromPounds(UnitsNet.QuantityValue.op_Implicit(30.94)),
             30.94 * om.registry.lb, opq    .PhysicalQuantity.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Mass.FromKilograms(UnitsNet.QuantityValue.op_Implicit(68.21)),
             68.21 * om.registry.kg, opq.PhysicalQuantity.MASS, decimal.Decimal('0.01')),
            (UnitsNet.Power.FromMechanicalHorsepower(UnitsNet.QuantityValue.op_Implicit(23.28e3)),
             23.28e3 * om.registry.hp, opq.PhysicalQuantity.POWER, decimal.Decimal('0.01e3')),
            (UnitsNet.Power.FromWatts(UnitsNet.QuantityValue.op_Implicit(21.05)),
             21.05 * om.registry.W, opq.PhysicalQuantity.POWER, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(49.70)),
             49.70 * om.registry.psi, opq.PhysicalQuantity.PRESSURE, decimal.Decimal('0.01')),
            (UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(342.7)),
             342.7 * om.registry.kPa, opq.PhysicalQuantity.PRESSURE, decimal.Decimal('0.01')),
            (ProppantConcentration(3.82, UnitsNet.Units.MassUnit.Pound, UnitsNet.Units.VolumeUnit.UsGallon),
             3.82 * om.registry.lb / om.registry.gal, opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.01')),
            (ProppantConcentration(457.4, UnitsNet.Units.MassUnit.Kilogram, UnitsNet.Units.VolumeUnit.CubicMeter),
             457.4 * om.registry.kg / (om.registry.m ** 3), opq.PhysicalQuantity.PROPPANT_CONCENTRATION,
             decimal.Decimal('0.01')),
            (SlurryRate(114.6, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
             114.6 * om.registry.oil_bbl / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE, decimal.Decimal('0.1')),
            (SlurryRate(18.22, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
             18.22 * (om.registry.m ** 3) / om.registry.min, opq.PhysicalQuantity.SLURRY_RATE, decimal.Decimal('0.01')),
            (UnitsNet.Temperature.FromDegreesFahrenheit(UnitsNet.QuantityValue.op_Implicit(153.6)),
             om.Quantity(153.6, om.registry.degF), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.1')),
            (UnitsNet.Temperature.FromDegreesCelsius(UnitsNet.QuantityValue.op_Implicit(4.618)),
             om.Quantity(4.618, om.registry.degC), opq.PhysicalQuantity.TEMPERATURE, decimal.Decimal('0.001')),
            (UnitsNet.Volume.FromOilBarrels(UnitsNet.QuantityValue.op_Implicit(83.48)),
             83.48 * om.registry.oil_bbl, opq.PhysicalQuantity.VOLUME, decimal.Decimal('0.01')),
            (UnitsNet.Volume.FromCubicMeters(UnitsNet.QuantityValue.op_Implicit(13.27)),
             13.27 * om.registry.m ** 3, opq.PhysicalQuantity.VOLUME, decimal.Decimal('0.01')),
        ]:
            with self.subTest(f'Test as_measurement for {expected.magnitude} {expected.units:~P}'):
                actual = onq.as_measurement(physical_quantity, net_quantity)
                tcm.assert_that_measurements_close_to(actual, expected, tolerance)

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


if __name__ == '__main__':
    unittest.main()
