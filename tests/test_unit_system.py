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
import toolz.curried as toolz

from orchid import (measurement as om,
                    physical_quantity as opq,
                    unit_system as units)


DONT_CARE_MAGNITUDE = float('NaN')


class TestUnitSystem(unittest.TestCase):
    """Implements the unit tests for the orchid.measurement module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_find_by_abbreviation_returns_matching_unit_if_match_found(self):
        physical_quantity_unit_map = toolz.merge(units.common, units.us_oilfield, units.metric)
        physical_quantity_unit_abbreviation_map = toolz.valmap(units.abbreviation, physical_quantity_unit_map)
        for physical_quantity in physical_quantity_unit_map.keys():
            expected = physical_quantity_unit_map[physical_quantity]
            to_find = physical_quantity_unit_abbreviation_map[physical_quantity]
            with self.subTest(msg=f'Expected {expected} for abbreviation, "{to_find}".'):
                actual = units.find_by_abbreviation(to_find)
                assert_that(actual, equal_to(expected))

    def test_find_by_abbreviation_raises_error_if_no_match_found(self):
        to_search = units.metric[opq.PRESSURE]
        not_found = units.abbreviation(to_search) + 'w'
        assert_that(calling(units.find_by_abbreviation).with_args(not_found), raises(ValueError))



if __name__ == '__main__':
    unittest.main()
