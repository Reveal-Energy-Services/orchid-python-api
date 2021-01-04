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

import decimal
import unittest

from hamcrest import assert_that, equal_to
import toolz.curried as toolz

from orchid import (convert as oc,
                    measurement as om,
                    unit_system as units)

from tests.custom_matchers import assert_that_measurements_close_to


DONT_CARE_MAGNITUDE = 3.14159265


# Test ideas
# - source and target not same physical quantity
class TestConvert(unittest.TestCase):
    """Implements the unit tests for the orchid.convert module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_to_unit_correctly_performs_no_op_conversion(self):
        for source_unit in toolz.concatv(units.UsOilfield, units.Metric):

            source_measurement = om.make_measurement(source_unit, DONT_CARE_MAGNITUDE)

            assert_that(oc.to_unit(source_unit, source_measurement), equal_to(source_measurement))

    def test_to_unit_correctly_converts_to_same_physical_quantity_units(self):
        for source_magnitude, source_unit, target_magnitude, target_unit, tolerance in [
            (2.982e-2, units.Metric.DENSITY, 1.862e-3, units.UsOilfield.DENSITY, decimal.Decimal('0.001e-3')),
            (15280, units.Metric.ENERGY, 11270, units.UsOilfield.ENERGY, decimal.Decimal('8')),
            (94580, units.UsOilfield.FORCE, 420700, units.Metric.FORCE, decimal.Decimal('45')),
            (178.7, units.UsOilfield.LENGTH, 54.48, units.Metric.LENGTH, decimal.Decimal('0.03')),
            (113900, units.Metric.MASS, 251200, units.UsOilfield.MASS, decimal.Decimal('220')),
            (11950, units.Metric.POWER, 16.02, units.UsOilfield.POWER, decimal.Decimal('0.02')),
            (56.44, units.Metric.PRESSURE, 8.18, units.UsOilfield.PRESSURE, decimal.Decimal('0.01')),
            (5.987, units.UsOilfield.PROPPANT_CONCENTRATION,
             717.4, units.Metric.PROPPANT_CONCENTRATION, decimal.Decimal('0.12')),
            (13.66, units.Metric.SLURRY_RATE, 85.91, units.UsOilfield.SLURRY_RATE, decimal.Decimal('0.07')),
            (156.6, units.UsOilfield.TEMPERATURE, 69.24, units.Metric.TEMPERATURE, decimal.Decimal('0.04')),
            (634.1, units.Metric.VOLUME, 3989, units.UsOilfield.VOLUME, decimal.Decimal('0.7')),
        ]:
            with self.subTest(f'Converting {source_unit} to {target_unit}'):
                source_measurement = om.make_measurement(source_unit, source_magnitude)
                actual = oc.to_unit(target_unit, source_measurement)

                expected = om.make_measurement(target_unit, target_magnitude)
                assert_that_measurements_close_to(actual, expected, tolerance)


if __name__ == '__main__':
    unittest.main()
