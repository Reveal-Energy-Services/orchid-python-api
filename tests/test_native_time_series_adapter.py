#  Copyright (c) 2017-2022 Reveal Energy Services, Inc 
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

import unittest.mock

from hamcrest import assert_that, equal_to, has_entries, is_
import pendulum
import toolz.curried as toolz

import numpy as np
import pandas as pd
import pandas.testing as pdt


from orchid import (
    native_time_series_adapter as tsa,
    project_loader as loader,
    unit_system as units,
)
from tests import (
    stub_net as tsn,
    test_time_series_equal as tse,
)


# Test ideas
# - Transform pendulum.DateTime.max to `NaT` in Time Series
# - Transform pendulum.DateTime.min to `NaT` in Time Series
class TestNativeTimeSeriesAdapter(unittest.TestCase):
    # TODO: Think about isolating unit testing of the SUT and its base classes into separate test classes.
    # Currently, we test the SUT by mocking the project and testing the SUT and its base classes together.
    # This approach works, but, in theory, this set up conflates testing the unit, `NativeTimeSeriesAdapter`,
    # and its base classes, `BaseTimeSeriesAdapter` and `DotNetAdapter`.
    #
    # This conflation is not required. (See the unit tests for `BaseTimeSeriesAdapter` for examples of mocking the
    # required base class properties.) However, it uses a set up that is unlike other unit test set up.
    # Because of time pressure, because the unit (and acceptance / integration) tests all work, and because
    # of this dissimilar set up, I have chosen for now to leave these unit tests as is.

    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

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
                    tsa.TimeSeriesCurveTypes.MONITOR_PRESSURE.value: project_units.PRESSURE,
                    tsa.TimeSeriesCurveTypes.MONITOR_TEMPERATURE.value: project_units.TEMPERATURE}))

    def test_sampled_quantity_name(self):
        expected_quantity_name = 'perspici'
        sut = create_sut(sampled_quantity_name=expected_quantity_name)

        assert_that(sut.sampled_quantity_name, equal_to(expected_quantity_name))

    def test_empty_time_series_if_no_samples(self):
        name = 'trucem'
        values = []
        start_time_point = pendulum.datetime(2021, 4, 2, 15, 17, 57)
        tse.assert_time_series_equal(name, start_time_point, values, create_sut)

    def test_single_sample_time_series_if_single_sample(self):
        name = 'aquilinum'
        values = [26.3945]
        start_time_point = pendulum.datetime(2016, 2, 9, 4, 50, 39, tz='UTC')
        tse.assert_time_series_equal(name, start_time_point, values, create_sut)

    def test_many_sample_time_series_if_many_sample(self):
        name = 'vulnerabatis'
        values = [75.75, 62.36, 62.69]
        start_time_point = pendulum.datetime(2016, 11, 25, 12, 8, 15, tz='UTC')
        tse.assert_time_series_equal(name, start_time_point, values, create_sut)


def create_sut(name='', display_name='', sampled_quantity_name='', sampled_quantity_type=-1, project=None):
    stub_native_well_time_series = tsn.create_stub_net_time_series(
        object_id=None, name=name, display_name=display_name,
        sampled_quantity_name=sampled_quantity_name,
        sampled_quantity_type=sampled_quantity_type,
        project=project,
    )

    sut = tsa.NativeTimeSeriesAdapter(stub_native_well_time_series)
    return sut


if __name__ == '__main__':
    unittest.main()
