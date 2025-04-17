#  Copyright (c) 2017-2025 KAPPA
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

import deal
from hamcrest import assert_that, equal_to, calling, raises

import numpy as np

from orchid import (
    native_trajectory_adapter as nta,
    reference_origins as origins,
    unit_system as units,
)
from tests import (stub_net as tsn)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import Convert

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import WellReferenceFrameXy

# noinspection PyUnresolvedReferences
import UnitsNet


# Test ideas
class TestNativeTrajectoryAdapter(unittest.TestCase):

    def test_get_easting_array(self):
        for expected, project_units, reference_frame in [
            ([], units.UsOilfield, origins.WellReferenceFrameXy.WELL_HEAD),
            ([789921], units.Metric, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE),
            ([501040, 281770, 289780], units.Metric, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE),
        ]:
            with self.subTest(f'eastings: {expected}, project units: {project_units}, '
                              f'relative to: {str(reference_frame)}'):
                stub_project = tsn.create_stub_net_project(project_units=project_units)
                stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                                      easting_magnitudes=expected)
                sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)

                actual = sut.get_easting_array(reference_frame)

                assert_that(stub_trajectory.GetEastingArray.called_once_with(reference_frame))
                np.testing.assert_allclose(actual, expected)

    def test_get_northing_array(self):
        for expected, project_units, reference_frame in [
            ([], units.Metric, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE),
            ([6936068], units.UsOilfield, origins.WellReferenceFrameXy.PROJECT),
            ([8332810, 2537900, 9876464], units.UsOilfield, origins.WellReferenceFrameXy.WELL_HEAD),
        ]:
            with self.subTest(f'northings: {expected}, project units: {project_units}, '
                              f'relative to: {str(reference_frame)}'):
                stub_project = tsn.create_stub_net_project(project_units=project_units)
                stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                                      northing_magnitudes=expected)
                sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)

                assert_that(stub_trajectory.GetNorthingArray.called_once_with(reference_frame))
                np.testing.assert_allclose(sut.get_northing_array(reference_frame), expected)

    def test_get_tvd_ss_array(self):
        for expected, project_units in [
            ([], units.UsOilfield),
            ([2673.8], units.Metric),
            ([8192.7, 7415.2, 9615.7], units.Metric),
        ]:
            with self.subTest(f'tvd_sss: {expected}, project units: {project_units}'):
                stub_project = tsn.create_stub_net_project(project_units=project_units)
                stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                                      tvd_ss_magnitudes=expected)
                sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)

                assert_that(stub_trajectory.GetTvdArray.called_once_with(origins.DepthDatum.SEA_LEVEL))
                np.testing.assert_allclose(sut.get_tvd_ss_array(), expected)

    def test_get_inclination_array(self):
        for expected in [
            ([]),
            ([93.857]),
            ([86.049, 89.042, 92.203]),
        ]:
            with self.subTest(f'inclinations: {expected}'):
                stub_project = tsn.create_stub_net_project(project_units=units.Common)
                stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                                      inclination_magnitudes=expected)
                sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)

                np.testing.assert_allclose(sut.get_inclination_array(), expected)

    def test_get_azimuth_array(self):
        for expected in [
            ([]),
            ([324.63]),
            ([90.588, 92.327, 92.351]),
        ]:
            with self.subTest(f'azimuths: {expected}'):
                stub_project = tsn.create_stub_net_project(project_units=units.Common)
                stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                                      azimuth_magnitudes=expected)
                sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)

                np.testing.assert_allclose(sut.get_azimuth_east_of_north_array(), expected)

    def test_get_md_kb_array(self):
        for expected, project_units in [
            ([], units.UsOilfield),
            ([2588.5], units.Metric),
            ([9669.3, 12206., 13289.], units.UsOilfield),
        ]:
            with self.subTest(f'tvd_sss: {expected}, project units: {project_units}'):
                stub_project = tsn.create_stub_net_project(project_units=project_units)
                stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                                      md_kb_magnitudes=expected)
                sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)

                assert_that(stub_trajectory.GetMdKbArray.called_once_with())
                np.testing.assert_allclose(sut.get_md_kb_array(), expected)

    def test_get_easting_array_raises_error_if_no_reference_frame(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        expected_easting_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              easting_magnitudes=expected_easting_magnitudes)
        sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)
        assert_that(calling(sut.get_easting_array).with_args(None), raises(deal.PreContractError))

    def test_get_northing_array_raises_error_if_no_reference_frame(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        expected_northing_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              northing_magnitudes=expected_northing_magnitudes)
        sut = nta.NativeTrajectoryAdapterIdentified(stub_trajectory)
        assert_that(calling(sut.get_northing_array).with_args(None), raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
