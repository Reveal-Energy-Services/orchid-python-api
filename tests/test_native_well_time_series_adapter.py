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
from orchid.physical_quantity import PhysicalQuantity


class TestWellTimeSeries(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_name(self):
        expected_display_name = 'excoriaverunt'
        stub_native_well_time_series = mock.MagicMock(name='stub_native_well_time_series')
        stub_native_well_time_series.DisplayName = expected_display_name
        sut = nwtsa.NativeWellTimeSeriesAdapter(stub_native_well_time_series)

        assert_that(sut.display_name, equal_to(expected_display_name))

    def test_sampled_quantity_name(self):
        expected_quantity_name = 'perspici'
        stub_native_well_time_series = mock.MagicMock(name='stub_native_well_time_series')
        stub_native_well_time_series.SampledQuantityName = expected_quantity_name
        sut = nwtsa.NativeWellTimeSeriesAdapter(stub_native_well_time_series)

        assert_that(sut.sampled_quantity_name, equal_to(expected_quantity_name))

    def test_sampled_quantity_type(self):
        native_quantity_types = [68, 83]  # hard-coded UnitsNet.QuantityType.Pressure and Temperature
        physical_quantities = [PhysicalQuantity.PRESSURE, PhysicalQuantity.TEMPERATURE]
        for native_quantity_type, physical_quantity in zip(native_quantity_types, physical_quantities):
            with self.subTest(native_quantity_type=native_quantity_type, physical_quantity=physical_quantity):
                stub_native_well_time_series = mock.MagicMock(name='stub_native_well_time_series')
                stub_native_well_time_series.SampledQuantityType = native_quantity_type
                sut = nwtsa.NativeWellTimeSeriesAdapter(stub_native_well_time_series)

                assert_that(sut.sampled_quantity_type, equal_to(physical_quantity))


if __name__ == '__main__':
    unittest.main()
