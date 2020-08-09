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

import unittest.mock

from hamcrest import assert_that, equal_to, instance_of

import orchid.native_stage_adapter as nsa
import orchid.native_trajectory_adapter as nta
import orchid.native_well_adapter as nwa

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IProject, IWell
# noinspection PyUnresolvedReferences
import UnitsNet


class TestNativeWellAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_name(self):
        expected_well_name = 'sapientiarum'
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_native_well.Name = expected_well_name
        sut = nwa.NativeWellAdapter(stub_native_well)

        assert_that(sut.name, equal_to(expected_well_name))

    def test_display_name(self):
        expected_well_display_name = 'agiles'
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_native_well.DisplayName = expected_well_display_name
        sut = nwa.NativeWellAdapter(stub_native_well)

        assert_that(sut.display_name, equal_to(expected_well_display_name))

    def test_stages_length_if_different_net_stages_length(self):
        for expected_stages in [[], ['one'], ['one', 'two', 'three']]:
            with self.subTest(expected_stages=expected_stages):
                stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
                expected_stages = []
                sut = nwa.NativeWellAdapter(stub_native_well)

                assert_that(len(list(sut.stages)), equal_to(len(expected_stages)))

    def test_stages_returns_correct_wrapper(self):
        for expected_stages in [['one'], ['one', 'two', 'three']]:
            with self.subTest(expected_stages=expected_stages):
                stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
                expected_stages = []
                stub_native_well.Stages.Items = expected_stages
                sut = nwa.NativeWellAdapter(stub_native_well)

                for actual in list(sut.stages):
                    assert_that(actual, instance_of(nsa.NativeStageAdapter))

    def test_trajectory(self):
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_trajectory = unittest.mock.MagicMock(name='stub_native_trajectory')
        stub_native_well.Trajectory = stub_trajectory
        sut = nwa.NativeWellAdapter(stub_native_well)

        # noinspection PyTypeChecker
        assert_that(sut.trajectory, instance_of(nta.NativeTrajectoryAdapter))

    def test_uwi(self):
        for uwi in ['01-325-88264-47-65', None]:
            with self.subTest(uwi=uwi):
                expected_uwi = uwi
                stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
                stub_native_well.Uwi = expected_uwi
                sut = nwa.NativeWellAdapter(stub_native_well)

                assert_that(sut.uwi, equal_to(expected_uwi if expected_uwi else 'No UWI'))


if __name__ == '__main__':
    unittest.main()
