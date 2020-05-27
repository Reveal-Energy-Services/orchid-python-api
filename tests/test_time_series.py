#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

import datetime
import unittest

from hamcrest import assert_that, is_, equal_to
import pandas as pd

from orchid.time_series import transform_net_time_series, transform_net_treatment
from tests.stub_net import create_30_second_time_points, create_stub_net_time_series, create_net_treatment


class TestTimeSeries(unittest.TestCase):
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

    def test_treatment_transform_returns_no_items_when_no_net_treatment(self):
        actual_treatments = transform_net_treatment([])

        assert_that(actual_treatments.empty, is_(True))

    def test_treatment_transform_returns_treatment_when_one_sample(self):
        start_time_point = datetime.datetime(2023, 8, 19, 14, 5, 47)
        treating_pressures = [5.212e-4]
        rate = [188.7]
        concentration = [6.037]

        stub_net_treatment = create_net_treatment(start_time_point, treating_pressures, rate, concentration)
        actual_treatments = transform_net_treatment(stub_net_treatment)

        expected_treatments = pd.DataFrame(data={'Treating Pressure': treating_pressures,
                                                 'Slurry Rate': rate,
                                                 'Proppant Concentration': concentration},
                                           index=create_30_second_time_points(start_time_point,
                                                                              len(treating_pressures)))
        pd.testing.assert_frame_equal(actual_treatments, expected_treatments)

    def test_treatment_transform_returns_treatment_when_many_samples(self):
        start_time_point = datetime.datetime(2018, 10, 3, 16, 14, 33)
        treating_pressures = [276.3, 276.3, 278.5]
        rate = [219.2, 207.6, 278.5]
        concentration = [5.386, 5.757, 4.878]

        stub_net_treatment = create_net_treatment(start_time_point, treating_pressures, rate, concentration)
        actual_treatments = transform_net_treatment(stub_net_treatment)

        expected_treatments = pd.DataFrame(data={'Treating Pressure': treating_pressures,
                                                 'Slurry Rate': rate,
                                                 'Proppant Concentration': concentration},
                                           index=create_30_second_time_points(start_time_point,
                                                                              len(treating_pressures)))
        pd.testing.assert_frame_equal(actual_treatments, expected_treatments)


if __name__ == '__main__':
    unittest.main()
