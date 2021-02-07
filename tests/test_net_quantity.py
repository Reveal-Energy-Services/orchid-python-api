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
