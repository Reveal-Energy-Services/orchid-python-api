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

from hamcrest import assert_that, equal_to, instance_of
import toolz.curried as toolz

from orchid import (
    native_stage_adapter as nsa,
    native_trajectory_adapter as nta,
    native_well_adapter as nwa,
)

from tests import stub_net as tsn


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

    def test_stages_count_equals_net_stages_count(self):
        for stub_net_stages in [[], [tsn.create_stub_net_stage()], [tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage()]]:
            with self.subTest(f'Test length of stages for each of {len(stub_net_stages)} .NET stage(s)'):
                stub_net_well = unittest.mock.MagicMock(name='stub_net_well')
                stub_net_well.Stages.Items = stub_net_stages
                sut = nwa.NativeWellAdapter(stub_net_well)

                assert_that(toolz.count(sut.stages), equal_to(len(stub_net_stages)))

    def test_stages_wrap_all_net_stages(self):
        for stub_net_stages in [[], [tsn.create_stub_net_stage()], [tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage()]]:
            with self.subTest(f'Test stage adapter for each of {len(stub_net_stages)} .NET stage(s)'):
                stub_net_well = unittest.mock.MagicMock(name='stub_net_well')
                stub_net_well.Stages.Items = stub_net_stages
                sut = nwa.NativeWellAdapter(stub_net_well)

                for actual_stage in sut.stages:
                    assert_that(actual_stage, instance_of(nsa.NativeStageAdapter))

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
