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

import unittest

import deal
from hamcrest import assert_that, equal_to, calling, raises, close_to

from orchid import (obs_measurement as om,
                    unit_system as units)


DONT_CARE_MAGNITUDE = float('NaN')


class TestMeasurement(unittest.TestCase):
    """Implements the unit tests for the orchid.measurement module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_constructed_instance_has_magnitude_supplied_to_ctor(self):
        sut = om.Measurement(704.3, units.Metric.PROPPANT_CONCENTRATION)

        assert_that(sut.magnitude, equal_to(704.3))

    def test_constructed_instance_has_unit_supplied_to_ctor(self):
        sut = om.Measurement(DONT_CARE_MAGNITUDE, units.UsOilfield.PRESSURE)

        assert_that(sut.unit, equal_to(units.UsOilfield.PRESSURE))

    def test_measurement_repr_returns_appropriate_details(self):
        sut = om.Measurement(147100, units.Metric.MASS)

        actual = repr(sut)
        assert_that(actual, equal_to("Measurement(147100, <Metric.MASS: AboutUnit(unit=<Unit('kilogram')>,"
                                     " physical_quantity=<PhysicalQuantity.MASS: 'mass'>)>)"))

    def test_measurement_str_returns_expected_value(self):
        for magnitude, unit, expected in [
            (64.18, units.Common.ANGLE, '64.18 \u00b0'),
            (4, units.Common.DURATION, '4 min'),
            (1027, units.Metric.DENSITY, '1027 kg/m\u00b3'),
            (64.13, units.UsOilfield.DENSITY, '64.13 lb/ft\u00b3'),
            (4.786, units.UsOilfield.ENERGY, '4.786 ft-lb'),
            (6.489, units.Metric.ENERGY, '6.489 J'),
            (110100, units.UsOilfield.FORCE, '110100 lbf'),
            (489700, units.Metric.FORCE, '489700 N'),
            (48.22, units.Metric.LENGTH, '48.22 m'),
            (158.2, units.UsOilfield.LENGTH, '158.2 ft'),
            (121800, units.Metric.MASS, '121800 kg'),
            (268500, units.UsOilfield.MASS, '268500 lb'),
            (19.27, units.UsOilfield.POWER, '19.27 hp'),
            (14370, units.Metric.POWER, '14370 W'),
            (4.664, units.UsOilfield.PROPPANT_CONCENTRATION, '4.664 lb/gal'),
            (558.9, units.Metric.PROPPANT_CONCENTRATION, '558.9 kg/m\u00b3'),
            (74.29, units.UsOilfield.SLURRY_RATE, '74.29 bpm'),
            (11.81, units.Metric.SLURRY_RATE, '11.81 m\u00b3/min'),
            (68.84, units.Metric.TEMPERATURE, '68.84 \u00b0C'),
            (155.9, units.UsOilfield.TEMPERATURE, '155.9 \u00b0F'),
            (9453, units.UsOilfield.VOLUME, '9453 bbl'),
            (1503, units.Metric.VOLUME, '1503 m\u00b3'),
        ]:
            with self.subTest(f'Testing str for measurement with magnitude, {magnitude}, and unit, "{unit}"'):
                sut = om.Measurement(magnitude, unit)

                actual = str(sut)
                assert_that(actual, equal_to(expected))

    def test_magnitude_is_supplied_magnitude_to_make_measurement(self):
        for magnitude, unit in [(877.26, units.Metric.LENGTH),
                                (3, units.UsOilfield.VOLUME)  # Testing an integral magnitude against contract
                                ]:
            with self.subTest(f'Test returns magnitude, {magnitude}, supplied to make_measurement.'):
                sut = om.make_measurement(unit, magnitude)

                assert_that(sut.magnitude, equal_to(magnitude))

    def test_unit_is_supplied_unit_to_make_measurement(self):
        sut = om.make_measurement(units.UsOilfield.LENGTH, 138.44)

        assert_that(sut.unit, equal_to(units.UsOilfield.LENGTH))

    def test_make_measurement_raises_exception_if_invalid_magnitude(self):
        assert_that(calling(om.make_measurement).with_args(complex(3.14, 2.72), units.UsOilfield.VOLUME),
                    raises(deal.PreContractError))

    def test_make_measurement_raises_exception_if_invalid_unit(self):
        assert_that(calling(om.make_measurement).with_args(1.717, 'm^3'),
                    raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
