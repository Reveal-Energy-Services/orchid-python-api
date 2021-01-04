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
import unittest

import deal
from hamcrest import assert_that, is_, equal_to, calling, raises
import pandas as pd

from orchid.time_series import transform_net_time_series
from tests.stub_net import create_30_second_time_points, create_stub_net_time_series


class TestTimeSeries(unittest.TestCase):
    # Test ideas:
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


if __name__ == '__main__':
    unittest.main()
