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

import unittest.mock

import deal
from hamcrest import assert_that, equal_to, empty, contains_exactly, calling, raises

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
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_get_easting_array_if_empty_easting_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        expected_easting_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              easting_magnitudes=expected_easting_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array(origins.WellReferenceFrameXy.WELL_HEAD), empty())

    def test_get_northing_array_if_empty_northing_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        expected_northing_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              northing_magnitudes=expected_northing_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE), empty())

    def test_get_tvd_ss_array_if_empty_tvd_ss_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        expected_tvd_ss_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              tvd_ss_magnitudes=expected_tvd_ss_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_tvd_array(origins.DepthDatum.SEA_LEVEL), empty())

    def test_get_inclination_array_if_empty_inclination_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Common)
        expected_inclination_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              inclination_magnitudes=expected_inclination_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_inclination_array(), empty())

    def test_get_azimuth_array_if_empty_azimuth_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Common)
        expected_azimuth_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              azimuth_magnitudes=expected_azimuth_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_azimuth_array(), empty())


    def test_get_easting_array_if_one_item_easting_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        expected_easting_magnitudes = [789921]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              easting_magnitudes=expected_easting_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE),
                    contains_exactly(*expected_easting_magnitudes))

    def test_get_northing_array_if_one_item_northing_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        expected_northing_magnitudes = [6936068]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              northing_magnitudes=expected_northing_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array(origins.WellReferenceFrameXy.PROJECT),
                    contains_exactly(*expected_northing_magnitudes))

    def test_get_tvd_array_if_one_item_tvd_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        expected_tvd_ss_magnitudes = [2673.8]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              tvd_ss_magnitudes=expected_tvd_ss_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        np.testing.assert_allclose(sut.get_tvd_array(origins.DepthDatum.SEA_LEVEL), expected_tvd_ss_magnitudes)
        assert_that(stub_trajectory.GetTvdArray.called_once_with(origins.DepthDatum.SEA_LEVEL))

    def test_get_inclination_array_if_one_item_inclination_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Common)
        expected_inclination_magnitudes = [93.857]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              inclination_magnitudes=expected_inclination_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        np.testing.assert_allclose(sut.get_inclination_array(), expected_inclination_magnitudes)

    def test_get_azimuth_array_if_one_item_azimuth_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Common)
        expected_azimuth_magnitudes = [324.63]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              azimuth_magnitudes=expected_azimuth_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        np.testing.assert_allclose(sut.get_azimuth_array(), expected_azimuth_magnitudes)

    def test_get_easting_array_if_many_items_easting_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        expected_easting_magnitudes = [501040, 281770, 289780]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              easting_magnitudes=expected_easting_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE),
                    contains_exactly(*expected_easting_magnitudes))

    def test_get_northing_array_if_many_items_northing_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        expected_northing_magnitudes = [8332810, 2537900, 9876464]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              northing_magnitudes=expected_northing_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array(origins.WellReferenceFrameXy.WELL_HEAD),
                    contains_exactly(*expected_northing_magnitudes))

    def test_get_tvd_ss_array_if_many_items_tvd_ss_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        expected_tvd_ss_magnitudes = [8192.7, 7415.2, 9615.7]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              tvd_ss_magnitudes=expected_tvd_ss_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        np.testing.assert_allclose(sut.get_tvd_array(origins.DepthDatum.SEA_LEVEL), expected_tvd_ss_magnitudes)
        assert_that(stub_trajectory.GetTvdArray.called_once_with(origins.DepthDatum.SEA_LEVEL))

    def test_get_inclination_array_if_many_items_inclination_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Common)
        expected_inclination_magnitudes = [86.049, 89.042, 92.203]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              inclination_magnitudes=expected_inclination_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        np.testing.assert_allclose(sut.get_inclination_array(), expected_inclination_magnitudes)

    def test_get_azimuth_array_if_many_items_azimuth_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Common)
        expected_azimuth_magnitudes = [90.588, 92.327, 92.351]
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              azimuth_magnitudes=expected_azimuth_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        np.testing.assert_allclose(sut.get_azimuth_array(), expected_azimuth_magnitudes)

    def test_get_easting_array_raises_error_if_no_reference_frame(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        expected_easting_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              easting_magnitudes=expected_easting_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)
        assert_that(calling(sut.get_easting_array).with_args(None), raises(deal.PreContractError))

    def test_get_northing_array_raises_error_if_no_reference_frame(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        expected_northing_magnitudes = []
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project,
                                                              northing_magnitudes=expected_northing_magnitudes)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)
        assert_that(calling(sut.get_northing_array).with_args(None), raises(deal.PreContractError))

    def test_send_correct_reference_frame_to_get_easting_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        for (reference_frame, net_reference_frame) in [
            (origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, WellReferenceFrameXy.AbsoluteStatePlane),
            (origins.WellReferenceFrameXy.PROJECT, WellReferenceFrameXy.Project),
            (origins.WellReferenceFrameXy.WELL_HEAD, WellReferenceFrameXy.WellHead),
        ]:
            with self.subTest(f'Test send correct reference frame {reference_frame.name} to get_easting_array'):
                mock_get_easting_array = unittest.mock.MagicMock(name='stub_eastings', return_value=[])
                stub_trajectory.GetEastingArray = mock_get_easting_array
                sut.get_easting_array(reference_frame)
                mock_get_easting_array.assert_called_once_with(net_reference_frame)

    def test_send_correct_reference_frame_to_get_northing_array(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project)
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)

        for (reference_frame, net_reference_frame) in [
            (origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, WellReferenceFrameXy.AbsoluteStatePlane),
            (origins.WellReferenceFrameXy.PROJECT, WellReferenceFrameXy.Project),
            (origins.WellReferenceFrameXy.WELL_HEAD, WellReferenceFrameXy.WellHead),
        ]:
            with self.subTest(f'Test send correct reference frame {reference_frame.name} to get_northing_array'):
                mock_get_northing_array = unittest.mock.MagicMock(name='stub_northings', return_value=[])
                stub_trajectory.GetNorthingArray = mock_get_northing_array
                sut.get_northing_array(reference_frame)
                mock_get_northing_array.assert_called_once_with(net_reference_frame)

    def test_send_correct_length_unit_to_get_easting_array_if_no_length_unit_specified(self):
        stub_project = tsn.create_stub_net_project(project_units=units.UsOilfield)
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project, easting_magnitudes=[])
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)
        sut.get_easting_array(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE)

        mock_get_easting_array = tsn.get_mock_easting_array(stub_trajectory)
        mock_get_easting_array.assert_called_once_with(WellReferenceFrameXy.AbsoluteStatePlane)

    def test_send_correct_length_unit_to_get_northing_array_if_no_length_unit_specified(self):
        stub_project = tsn.create_stub_net_project(project_units=units.Metric)
        stub_trajectory = tsn.create_stub_net_well_trajectory(project=stub_project, northing_magnitudes=[])
        sut = nta.NativeTrajectoryAdapter(stub_trajectory)
        sut.get_northing_array(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE)

        mock_get_northing_array = tsn.get_mock_northing_array(stub_trajectory)
        mock_get_northing_array.assert_called_once_with(WellReferenceFrameXy.AbsoluteStatePlane)


if __name__ == '__main__':
    unittest.main()
