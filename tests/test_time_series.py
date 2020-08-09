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

import deal
from hamcrest import assert_that, is_, equal_to, calling, raises
import pandas as pd

from orchid.time_series import transform_net_time_series, deprecated_transform_net_treatment
from tests.stub_net import create_30_second_time_points, create_stub_net_time_series, create_net_treatment


def assert_equal_treatments(concentration, rate, start_time_point, treating_pressures):
    stub_net_treatment = create_net_treatment(start_time_point, treating_pressures, rate, concentration)
    actual_treatments = deprecated_transform_net_treatment(stub_net_treatment)
    expected_treatments = pd.DataFrame(data={'Treating Pressure': treating_pressures,
                                             'Slurry Rate': rate,
                                             'Proppant Concentration': concentration},
                                       index=create_30_second_time_points(start_time_point,
                                                                          len(treating_pressures)))
    pd.testing.assert_frame_equal(actual_treatments, expected_treatments)


class TestTimeSeries(unittest.TestCase):
    # Test ideas:
    # - deprecated_transform_net_treatment
    #   - no treating pressure generates empty named column
    #   - no rate returns generates empty named column
    #   - no concentration generates empty named column
    def test_canary(self):
        assert_that(2 + 2, is_(equal_to(4)))

    def test_time_series_transform_returns_no_items_when_no_net_samples(self):
        sample_values = []
        actual_time_series = transform_net_time_series(sample_values)

        assert_that(actual_time_series.empty, is_(True))

    def test_time_series_transform_returns_one_item_when_one_net_samples(self):
        start_time_point = datetime.datetime(2021, 7, 30, 15, 44, 22)
        sample_values = [3.684]
        net_time_series = create_stub_net_time_series(start_time_point, sample_values)
        actual_time_series = transform_net_time_series(net_time_series)

        pd.testing.assert_series_equal(actual_time_series,
                                       pd.Series(data=sample_values,
                                                 index=create_30_second_time_points(start_time_point,
                                                                                    len(sample_values))))

    def test_time_series_transform_returns_many_items_when_many_net_samples(self):
        start_time_point = datetime.datetime(2018, 11, 7, 17, 50, 18)
        sample_values = [68.67, 67.08, 78.78]
        net_time_series = create_stub_net_time_series(start_time_point, sample_values)
        actual_time_series = transform_net_time_series(net_time_series)

        pd.testing.assert_series_equal(actual_time_series,
                                       pd.Series(data=sample_values,
                                                 index=create_30_second_time_points(start_time_point,
                                                                                    len(sample_values))))

    def test_transform_net_time_series_raises_exception_when_net_time_series_is_none(self):
        assert_that(calling(transform_net_time_series).with_args(None), raises(deal.PreContractError))

    def test_treatment_net_transform_returns_no_items_when_no_net_treatment(self):
        actual_treatments = deprecated_transform_net_treatment([])

        assert_that(actual_treatments.empty, is_(True))

    def test_treatment_net_transform_returns_treatment_when_one_sample(self):
        start_time_point = datetime.datetime(2023, 8, 19, 14, 5, 47)
        treating_pressures = [5.212e-4]
        rate = [188.7]
        concentration = [6.037]

        assert_equal_treatments(concentration, rate, start_time_point, treating_pressures)

    def test_treatment_net_transform_returns_treatment_when_many_samples(self):
        start_time_point = datetime.datetime(2018, 10, 3, 16, 14, 33)
        treating_pressures = [276.3, 276.3, 278.5]
        rate = [219.2, 207.6, 278.5]
        concentration = [5.386, 5.757, 4.878]

        assert_equal_treatments(concentration, rate, start_time_point, treating_pressures)

    def test_transform_net_treatment_raises_exception_if_net_treatment_curve_none(self):
        assert_that(calling(deprecated_transform_net_treatment).with_args(None), raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
