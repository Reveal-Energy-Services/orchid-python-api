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
import unittest.mock as mock

from hamcrest import assert_that, equal_to

import orchid.native_well_time_series_adapter as nwtsa


class TestWellTimeSeries(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_name(self):
        expected_display_name = 'excoriaverunt'
        stub_native_well_time_series = mock.MagicMock(name='stub_native_well_time_series')
        stub_native_well_time_series.DisplayName = expected_display_name
        sut = nwtsa.NativeWellTimeSeriesAdapter(stub_native_well_time_series)

        assert_that(sut.display_name, equal_to(expected_display_name))



if __name__ == '__main__':
    unittest.main()
