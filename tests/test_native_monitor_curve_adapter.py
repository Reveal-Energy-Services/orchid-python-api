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
import unittest.mock

import dateutil.tz
from hamcrest import assert_that, equal_to, has_entries
import numpy as np
import pandas as pd
import pandas.testing as pdt

from orchid import (native_monitor_curve_adapter as mca,
                    unit_system as units)

import tests.stub_net as tsn


class TestNativeMonitorCurveAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_get_net_project_units_returns_well_project_units(self):
        expected = unittest.mock.MagicMock('expected_project_units')
        stub_project = tsn.create_stub_net_project(project_units=expected)
        sut = create_sut(project=stub_project)

        assert_that(sut.get_net_project_units(), equal_to(expected))

    def test_name(self):
        expected_display_name = 'excoriaverunt'
        sut = create_sut(display_name=expected_display_name)

        assert_that(sut.display_name, equal_to(expected_display_name))

    def test_quantity_unit_map(self):
        for project_units in (units.UsOilfield, units.Metric):
            with self.subTest(f'Quantity unit map for {project_units}'):
                stub_project = tsn.create_stub_net_project(project_units=project_units)
                sut = create_sut(project=stub_project)

                actual = sut.quantity_name_unit_map(project_units)
                assert_that(actual, has_entries({
                    mca.MonitorCurveTypes.MONITOR_PRESSURE.value: project_units.PRESSURE,
                    mca.MonitorCurveTypes.MONITOR_TEMPERATURE.value: project_units.TEMPERATURE}))

    def test_sampled_quantity_name(self):
        expected_quantity_name = 'perspici'
        sut = create_sut(sampled_quantity_name=expected_quantity_name)

        assert_that(sut.sampled_quantity_name, equal_to(expected_quantity_name))

    def test_empty_time_series_if_no_samples(self):
        name = 'trucem'
        values = []
        start_time_point = datetime.datetime(2021, 4, 2, 15, 17, 57)
        samples = tsn.create_stub_net_time_series(start_time_point, values)
        sut = create_sut(name=name, samples=samples)

        expected = pd.Series(data=[], index=[], name=name, dtype=np.float64)
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_single_sample_time_series_if_single_sample(self):
        name = 'aquilinum'
        values = [26.3945]
        start_time_point = datetime.datetime(2016, 2, 9, 4, 50, 39, tzinfo=dateutil.tz.UTC)
        self.assert_equal_time_series(name, start_time_point, values)

    @staticmethod
    def assert_equal_time_series(name, start_time_point, values):
        samples = tsn.create_stub_net_time_series(start_time_point, values)
        sut = create_sut(name=name, samples=samples)
        expected_time_points = tsn.create_30_second_time_points(start_time_point, len(values))
        expected = pd.Series(data=values, index=expected_time_points, name=name)
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_many_sample_time_series_if_many_sample(self):
        name = 'vulnerabatis'
        values = [75.75, 62.36, 62.69]
        start_time_point = datetime.datetime(2016, 11, 25, 12, 8, 15, tzinfo=dateutil.tz.UTC)

        self.assert_equal_time_series(name, start_time_point, values)


def create_sut(name='', display_name='', sampled_quantity_name='', sampled_quantity_type=-1, samples=None,
               project=None):
    stub_native_well_time_series = tsn.create_stub_net_monitor_curve(
        name=name, display_name=display_name, sampled_quantity_name=sampled_quantity_name,
        sampled_quantity_type=sampled_quantity_type, samples=samples, project=project
    )

    sut = mca.NativeMonitorCurveAdapter(stub_native_well_time_series)
    return sut


if __name__ == '__main__':
    unittest.main()
