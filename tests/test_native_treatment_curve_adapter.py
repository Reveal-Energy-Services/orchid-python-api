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


from datetime import datetime, timedelta
import unittest.mock

import numpy as np
import pandas as pd
import pandas.testing as pdt
import dateutil.tz as duz
from hamcrest import assert_that, equal_to, has_entries

import orchid.native_treatment_curve_adapter as tca
import orchid.unit_system as units

import tests.stub_net as tsn


class TestTreatmentCurveAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name_from_treatment_curve(self):
        sut = create_sut(display_name='boni')

        assert_that(sut.display_name, equal_to('boni'))

    def test_get_net_project_units_returns_well_project_units(self):
        expected = unittest.mock.MagicMock('expected_project_units')
        stub_project = tsn.create_stub_net_project(project_units=expected)
        sut = create_sut(project=stub_project)

        assert_that(sut.get_net_project_units(), equal_to(expected))

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
                    tca.TreatmentCurveTypes.SURFACE_PROPPANT_CONCENTRATION.value:
                    project_units.PROPPANT_CONCENTRATION,
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
        sut = create_sut(name='palmis', values_starting_at=(values, start_time_point))

        expected = pd.Series(data=[], index=[], name='palmis', dtype=np.float64)
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_single_sample_time_series_from_curve_with_single_samples(self):
        values = [671.09]
        start_time_point = datetime(2016, 2, 9, 4, 50, 39, 340000, tzinfo=duz.UTC)
        sut = create_sut(name='palmis', values_starting_at=(values, start_time_point))

        expected_time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(values))]
        expected = pd.Series(data=values, index=expected_time_points, name='palmis')
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_many_samples_time_series_from_curve_with_many_samples(self):
        values = [331.10, 207.70, 272.08]
        start_time_point = datetime(2018, 12, 8, 18, 18, 35, 264000, tzinfo=duz.UTC)
        sut = create_sut(name='clavis', values_starting_at=(values, start_time_point))

        expected_time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(values))]
        expected = pd.Series(data=values, index=expected_time_points, name='clavis')
        pdt.assert_series_equal(sut.time_series(), expected)


def create_sut(name='', display_name='', sampled_quantity_name='', suffix='', values_starting_at=None, project=None):
    stub_net_treatment_curve = tsn.create_stub_net_treatment_curve(
        name, display_name, sampled_quantity_name, suffix, values_starting_at=values_starting_at, project=project)

    sut = tca.NativeTreatmentCurveAdapter(stub_net_treatment_curve)
    return sut


if __name__ == '__main__':
    unittest.main()
