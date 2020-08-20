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

import datetime
import unittest
import unittest.mock as mock

from hamcrest import assert_that, equal_to
import numpy as np
import pandas as pd
import pandas.testing as pdt

import orchid.native_monitor_curve_facade as nmcf
from orchid.physical_quantity import PhysicalQuantity
from tests.stub_net import create_stub_net_time_series, create_30_second_time_points


class TestNativeMonitorCurveFacade(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_name(self):
        expected_display_name = 'excoriaverunt'
        sut = create_sut(display_name=expected_display_name)

        assert_that(sut.display_name, equal_to(expected_display_name))

    def test_sampled_quantity_name(self):
        expected_quantity_name = 'perspici'
        sut = create_sut(sampled_quantity_name=expected_quantity_name)

        assert_that(sut.sampled_quantity_name, equal_to(expected_quantity_name))

    def test_sampled_quantity_type(self):
        native_quantity_types = [68, 83]  # hard-coded UnitsNet.QuantityType.Pressure and Temperature
        physical_quantities = [PhysicalQuantity.PRESSURE, PhysicalQuantity.TEMPERATURE]
        for native_quantity_type, physical_quantity in zip(native_quantity_types, physical_quantities):
            with self.subTest(native_quantity_type=native_quantity_type, physical_quantity=physical_quantity):
                sut = create_sut(sampled_quantity_type=native_quantity_type)
                assert_that(sut.sampled_quantity_type, equal_to(physical_quantity))

    def test_empty_time_series_if_no_samples(self):
        display_name = 'trucem'
        values = []
        start_time_point = datetime.datetime(2021, 4, 2, 15, 17, 57)
        samples = create_stub_net_time_series(start_time_point, values)
        sut = create_sut(display_name=display_name, samples=samples)

        expected = pd.Series(data=[], index=[], name=display_name, dtype=np.float64)
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_single_sample_time_series_if_single_sample(self):
        display_name = 'aquilinum'
        values = [26.3945]
        start_time_point = datetime.datetime(2016, 2, 9, 4, 50, 39)
        self.assert_equal_time_series(display_name, start_time_point, values)

    @staticmethod
    def assert_equal_time_series(display_name, start_time_point, values):
        samples = create_stub_net_time_series(start_time_point, values)
        sut = create_sut(display_name=display_name, samples=samples)
        expected_time_points = create_30_second_time_points(start_time_point, len(values))
        expected = pd.Series(data=values, index=expected_time_points, name=display_name)
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_many_sample_time_series_if_many_sample(self):
        display_name = 'vulnerabatis'
        values = [75.75, 62.36, 62.69]
        start_time_point = datetime.datetime(2016, 11, 25, 12, 8, 15)

        self.assert_equal_time_series(display_name, start_time_point, values)


def create_sut(display_name='', sampled_quantity_name='', sampled_quantity_type=-1, samples=None):
    stub_native_well_time_series = mock.MagicMock(name='stub_native_well_time_series')
    stub_native_well_time_series.DisplayName = display_name
    stub_native_well_time_series.SampledQuantityName = sampled_quantity_name
    stub_native_well_time_series.SampledQuantityType = sampled_quantity_type
    stub_native_well_time_series.GetOrderedTimeSeriesHistory = mock.MagicMock(name='stub_time_series',
                                                                              return_value=samples)

    sut = nmcf.NativeMonitorCurveFacade(stub_native_well_time_series)
    return sut


if __name__ == '__main__':
    unittest.main()
