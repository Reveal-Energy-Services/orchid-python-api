#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest.mock

import deal
from hamcrest import assert_that, equal_to, empty, contains_exactly

from orchid.native_trajectory_adapter import NativeTrajectoryAdapter
from tests.stub_net import create_stub_net_project, create_stub_net_trajectory_array, unit_abbreviation_to_unit

# noinspection PyUnresolvedReferences
from System import Convert

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWellTrajectory, WellReferenceFrameXy

# noinspection PyUnresolvedReferences
import UnitsNet


# Test ideas
# - No, empty or all whitespace reference frame
# - Unrecognized reference frame
class TestNativeTrajectoryAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_get_easting_array_if_empty_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        expected_eastings = []
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=expected_eastings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array('well_head'), empty())

    def test_get_northing_array_if_empty_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        expected_northings = []
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_northings',
                                                                  return_value=expected_northings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array('absolute'), empty())

    def test_get_easting_array_if_one_item_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='m')
        expected_easting_magnitudes = [789921]
        actual_eastings = create_stub_net_trajectory_array(expected_easting_magnitudes,
                                                           unit_abbreviation_to_unit('m'))
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=actual_eastings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array('absolute'), contains_exactly(*expected_easting_magnitudes))

    def test_get_northing_array_if_one_item_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='ft')
        expected_northing_magnitudes = [6936068]
        actual_northings = create_stub_net_trajectory_array(expected_northing_magnitudes,
                                                            unit_abbreviation_to_unit('ft'))
        stub_trajectory.GetNorthingArray = unittest.mock.MagicMock(name='stub_northings',
                                                                   return_value=actual_northings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array('project'), contains_exactly(*expected_northing_magnitudes))

    def test_get_easting_array_if_many_items_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='ft')
        expected_easting_magnitudes = [501040, 281770, 289780]
        actual_eastings = create_stub_net_trajectory_array(expected_easting_magnitudes, unit_abbreviation_to_unit('ft'))
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=actual_eastings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_easting_array('absolute'), contains_exactly(*expected_easting_magnitudes))

    def test_get_northing_array_if_many_items_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='ft')
        expected_northing_magnitudes = [8332810, 2537900, 9876464]
        actual_northings = create_stub_net_trajectory_array(expected_northing_magnitudes,
                                                            unit_abbreviation_to_unit('ft'))
        stub_trajectory.GetNorthingArray = unittest.mock.MagicMock(name='stub_northings',
                                                                   return_value=actual_northings)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        assert_that(sut.get_northing_array('well_head'), contains_exactly(*expected_northing_magnitudes))

    def test_send_correct_reference_frame_to_get_easting_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        # When debugging
        # - WellReferenceFrameXy.AbsoluteStatePlane = 0
        # - WellReferenceFrameXy.Project = 1
        # - WellReferenceFrameXy.WellHead = 2
        for (text_reference_frame, net_reference_frame) in [('absolute', WellReferenceFrameXy.AbsoluteStatePlane),
                                                            ('project', WellReferenceFrameXy.Project),
                                                            ('well_head', WellReferenceFrameXy.WellHead)]:
            with self.subTest(text_reference_frame=text_reference_frame, net_reference_frame=net_reference_frame):
                mock_get_easting_array = unittest.mock.MagicMock(name='stub_eastings', return_value=[])
                stub_trajectory.GetEastingArray = mock_get_easting_array
                sut.get_easting_array(text_reference_frame)
                mock_get_easting_array.assert_called_once_with(net_reference_frame)

    def test_send_correct_reference_frame_to_get_northing_array(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        # When debugging
        # - WellReferenceFrameXy.AbsoluteStatePlane = 0
        # - WellReferenceFrameXy.Project = 1
        # - WellReferenceFrameXy.WellHead = 2
        for (text_reference_frame, net_reference_frame) in [('absolute', WellReferenceFrameXy.AbsoluteStatePlane),
                                                            ('project', WellReferenceFrameXy.Project),
                                                            ('well_head', WellReferenceFrameXy.WellHead)]:
            with self.subTest(text_reference_frame=text_reference_frame, net_reference_frame=net_reference_frame):
                mock_get_northing_array = unittest.mock.MagicMock(name='stub_northings', return_value=[])
                stub_trajectory.GetNorthingArray = mock_get_northing_array
                sut.get_northing_array(text_reference_frame)
                mock_get_northing_array.assert_called_once_with(net_reference_frame)

    def test_send_correct_length_unit_to_get_easting_array_if_no_length_unit_specified(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='m')
        sut = NativeTrajectoryAdapter(stub_trajectory)
        mock_get_easting_array = unittest.mock.MagicMock(name='stub_eastings', return_value=[])
        stub_trajectory.GetEastingArray = mock_get_easting_array
        sut.get_easting_array('absolute')

        mock_get_easting_array.assert_called_once_with(WellReferenceFrameXy.AbsoluteStatePlane)

    def test_send_correct_length_unit_to_get_northing_array_if_no_length_unit_specified(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        stub_trajectory.Well.Project = create_stub_net_project(project_length_unit_abbreviation='m')
        sut = NativeTrajectoryAdapter(stub_trajectory)
        mock_get_northing_array = unittest.mock.MagicMock(name='stub_northings', return_value=[])
        stub_trajectory.GetNorthingArray = mock_get_northing_array
        sut.get_northing_array('absolute')

        mock_get_northing_array.assert_called_once_with(WellReferenceFrameXy.AbsoluteStatePlane)

    def test_get_xyz_array_invalid_reference_frame_raises_exception(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        for method_to_test in [sut.get_easting_array, sut.get_northing_array]:
            for invalid_reference_frame in [None, '', '\f']:
                with(self.subTest(method_to_test=method_to_test, invalid_well_id=invalid_reference_frame)):
                    self.assertRaises(deal.PreContractError, method_to_test, invalid_reference_frame)

    def test_get_xyz_array_unrecognized_reference_frame_raises_exception(self):
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
        sut = NativeTrajectoryAdapter(stub_trajectory)

        for method_to_test in [sut.get_easting_array, sut.get_northing_array]:
            with(self.subTest(method_to_test=method_to_test)):
                # noinspection SpellCheckingInspection
                self.assertRaises(deal.PreContractError, method_to_test, 'well_heaf')


if __name__ == '__main__':
    unittest.main()
