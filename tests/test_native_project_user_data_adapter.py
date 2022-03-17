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


import re
import unittest
import uuid

from hamcrest import assert_that, equal_to, calling, raises

from orchid import (
    native_project_user_data_adapter as uda,
    net_stage_qc as nqc,
)

from tests import stub_net as tsn


# Test ideas
# - Set QC notes for stage ID calls `SetValue` with correct values
# - Set start stop confirmation for stage ID calls `SetValue` with correct values
class TestNativeProjectUserDataAdapter(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_stage_qc_notes_if_qc_notes_available_for_stage(self):
        stage_id = 'b64521bf-56a2-4e9c-abca-d466670c75a1'
        expected_qc_notes = 'lucrum nugatorium provenivit'
        stub_project_user_data = tsn.ProjectUserDataDto(stages_qc={
            uuid.UUID(stage_id): {'stage_qc_notes': expected_qc_notes},
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_qc_notes(uuid.UUID(stage_id)), equal_to(expected_qc_notes))

    def test_stage_qc_notes_empty_if_qc_notes_not_available_for_stage(self):
        stage_id = '412e5a99-7040-4972-8b27-3ff0d1ab4d94'
        stub_project_user_data = tsn.ProjectUserDataDto().create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_qc_notes(uuid.UUID(stage_id)), equal_to(''))

    def test_stage_qc_notes_raises_error_if_value_has_unexpected_net_type(self):
        stage_id = tsn.DONT_CARE_ID_A
        stub_project_user_data = tsn.ProjectUserDataDto(to_json={
            nqc.make_qc_notes_key(stage_id): {'Type': 'System.Int32',
                                              'Value': -84},
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(calling(sut.stage_qc_notes).with_args(uuid.UUID(stage_id)),
                    raises(AssertionError,
                           pattern=re.compile('Expected, "System.String", but found ".*".')))

    def test_stage_start_stop_confirmation_if_start_stop_confirmation_available_for_stage(self):
        stage_id = '15fd59d7-da16-40bd-809b-56f9680a0773'
        expected_start_stop_confirmation = nqc.StageCorrectionStatus.UNCONFIRMED
        stub_project_user_data = tsn.ProjectUserDataDto(stages_qc={
            uuid.UUID(stage_id): {'stage_start_stop_confirmation': expected_start_stop_confirmation},
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_start_stop_confirmation(uuid.UUID(stage_id)),
                    equal_to(expected_start_stop_confirmation))

    def test_stage_start_stop_confirmation_empty_if_start_stop_confirmation_not_available_for_stage(self):
        stage_id = 'f4511635-b0c1-488e-b978-e55a82c40109'
        stub_project_user_data = tsn.ProjectUserDataDto().create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_start_stop_confirmation(uuid.UUID(stage_id)),
                    equal_to(nqc.StageCorrectionStatus.NEW))

    def test_stage_start_stop_confirmation_raises_error_if_value_has_unexpected_net_type(self):
        stage_id = tsn.DONT_CARE_ID_B
        stub_project_user_data = tsn.ProjectUserDataDto(to_json={
            nqc.make_start_stop_confirmation_key(stage_id): {
                'Type': 'System.Double',
                'Value': 129.847},
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(calling(sut.stage_start_stop_confirmation).with_args(uuid.UUID(stage_id)),
                    raises(AssertionError,
                           pattern=re.compile('Expected, "System.String", but found ".*".')))

    def test_stage_start_stop_confirmation_raises_error_if_value_not_stage_correction_status(self):
        stage_id = tsn.DONT_CARE_ID_C
        stub_project_user_data = tsn.ProjectUserDataDto(to_json={
            nqc.make_start_stop_confirmation_key(stage_id): {
                'Type': 'System.String',
                'Value': 'Newt'},
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(calling(sut.stage_start_stop_confirmation).with_args(uuid.UUID(stage_id)),
                    raises(ValueError))


if __name__ == '__main__':
    unittest.main()
