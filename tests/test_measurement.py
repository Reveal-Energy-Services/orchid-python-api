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

import unittest

import deal
from hamcrest import assert_that, equal_to, calling, raises, close_to

from orchid import (measurement as om,
                    unit_system as units)


DONT_CARE_MAGNITUDE = float('NaN')


class TestMeasurement(unittest.TestCase):
    """Implements the unit tests for the orchid.measurement module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_magnitude_is_supplied_magnitude_to_make_measurement(self):
        for magnitude, unit in [(877.26, units.Metric.LENGTH),
                                (3, units.UsOilfield.VOLUME)  # Testing an integral magnitude against contract
                                ]:
            with self.subTest(magnitude=magnitude, unit=unit):
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
