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


class TestConvert(unittest.TestCase):
    """Implements the unit tests for the orchid.convert module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_to_unit_correctly_performs_no_op_conversion(self):
        for source_unit in toolz.concatv(units.UsOilfield, units.Metric):

            source_measurement = om.make_measurement(DONT_CARE_MAGNITUDE, source_unit)

            assert_that(oc.to_unit(source_measurement, source_unit), equal_to(source_measurement))

    def test_to_unit_correctly_converts_to_same_physical_quantity_units(self):
        for source_magnitude, source_unit, target_magnitude, target_unit in [
            (178.74, units.UsOilfield.LENGTH, 54.48, units.Metric.LENGTH),
            (113938.75, units.Metric.MASS, 251191.94, units.UsOilfield.MASS),
            (56.44, units.Metric.PRESSURE, 8.18, units.UsOilfield.PRESSURE),
            (684.56, units.Metric.PROPPANT_CONCENTRATION, 5.71, units.UsOilfield.PROPPANT_CONCENTRATION),
        ]:
            source_measurement = om.make_measurement(source_magnitude, source_unit)
            actual = oc.to_unit(source_measurement, target_unit )

            expected = om.make_measurement(target_magnitude, target_unit)
            assert_that_measurements_close_to(actual, expected, decimal.Decimal('0.01'))


if __name__ == '__main__':
    unittest.main()
