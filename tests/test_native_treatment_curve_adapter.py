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


from datetime import datetime
import unittest.mock

from hamcrest import assert_that, equal_to, has_entries
import toolz.curried as toolz

import numpy as np
import pandas as pd
import pandas.testing as pdt

from orchid import (
    native_treatment_curve_adapter as tca,
    project_store as loader,
    unit_system as units,
)
from tests import (
    stub_net_date_time as tdt,
    stub_net as tsn,
    test_time_series_equal as tse,
)


# Test ideas
# - Transform datetime.max to `NaT` in Time Series
# - Transform datetime.min to `NaT` in Time Series
class TestTreatmentCurveAdapter(unittest.TestCase):
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

    def test_display_name_from_treatment_curve(self):
        sut = create_sut(display_name='boni')

        assert_that(sut.display_name, equal_to('boni'))

    def test_name_from_treatment_curve(self):
        sut = create_sut(name='magnitudina')

        assert_that(sut.name, equal_to('magnitudina'))

    def test_quantity_unit_map(self):
        for project_units in (units.UsOilfield, units.Metric):
            with self.subTest(f'Quantity unit map for {project_units}'):
                stub_project = tsn.create_stub_net_project(project_units=project_units)
                sut = create_sut(project=stub_project)

                actual = sut.quantity_name_unit_map(project_units)
                assert_that(actual, has_entries({
                    tca.TreatmentCurveTypes.TREATING_PRESSURE.value: project_units.PRESSURE,
                    tca.TreatmentCurveTypes.DOWNHOLE_PROPPANT_CONCENTRATION.value: project_units.PROPPANT_CONCENTRATION,
                    tca.TreatmentCurveTypes.SURFACE_PROPPANT_CONCENTRATION.value: project_units.PROPPANT_CONCENTRATION,
                    tca.TreatmentCurveTypes.SLURRY_RATE.value: project_units.SLURRY_RATE}))

    def test_sampled_quantity_name_from_treatment_curve(self):
        sut = create_sut(sampled_quantity_name='proponeam')

        assert_that(sut.sampled_quantity_name, equal_to('proponeam'))

    def test_suffix_from_treatment_curve(self):
        sut = create_sut(suffix='hominibus')

        assert_that(sut.suffix, equal_to('hominibus'))

    def test_empty_time_series_from_curve_with_no_samples(self):
        values = []
        start_time_point = datetime(2017, 7, 2, 3, 29, 10, 510000)
        expected_name = 'palmis'
        tse.assert_time_series_equal(expected_name, start_time_point, values, create_sut)

    def test_single_sample_time_series_from_curve_with_single_samples(self):
        values = [671.09]
        start_time_point = datetime(2016, 2, 9, 4, 50, 39, 340000, tzinfo=tdt.utc_time_zone())
        expected_name = 'palmis'
        tse.assert_time_series_equal(expected_name, start_time_point, values, create_sut)

    def test_many_samples_time_series_from_curve_with_many_samples(self):
        values = [331.10, 207.70, 272.08]
        start_time_point = datetime(2018, 12, 8, 18, 18, 35, 264000, tzinfo=tdt.utc_time_zone())
        expected_name = 'clavis'
        tse.assert_time_series_equal(expected_name, start_time_point, values, create_sut)


def create_sut(name='', display_name='', sampled_quantity_name='', suffix='', project=None):
    stub_net_treatment_curve = tsn.create_stub_net_treatment_curve(name, display_name, sampled_quantity_name,
                                                                   suffix, project=project)

    sut = tca.NativeTreatmentCurveAdapter(stub_net_treatment_curve)
    return sut


if __name__ == '__main__':
    unittest.main()
