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


import unittest
import uuid

from hamcrest import assert_that, equal_to, is_, none

from orchid import (
    native_project_user_data_adapter as uda,
    net_stage_qc as nqc,
)

from tests import stub_net as tsn


# Test ideas
# - Return correct stage QC if pair, stage ID and start stop confirmation, are available
# - Return correct stage QC if pair, stage ID and QC notes, are available
# - Return None if no such matching stage ID exists but at least one other pair
# - Return None if no stage ID exists but neither start stop confirmation nor QC notes
class TestNativeProjectUserDataAdapter(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    @unittest.skip('Awaiting lower-level code')
    def test_stage_qc_has_correct_stage_id_if_stage_id_and_start_stop_confirmation_in_user_data(self):
        stage_id_dto = tsn.DONT_CARE_ID_A
        stub_net_project_user_data = tsn.ProjectUserDataDto(stage_qcs={
            uuid.UUID(stage_id_dto): {
                nqc.StageQCTags.START_STOP_CONFIRMATION:
                    tsn.StageQCValueDto(nqc.StageCorrectionStatus.UNCONFIRMED, None),
            },
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_net_project_user_data)

        assert_that(sut.stage_qc(uuid.UUID(stage_id_dto)).stage_id, equal_to(uuid.UUID(stage_id_dto)))

    @unittest.skip('Awaiting lower-level code')
    def test_stage_qc_has_correct_start_stop_confirmation_if_stage_id_and_start_stop_confirmation_in_user_data(self):
        stage_id_dto = tsn.DONT_CARE_ID_B
        expected_start_stop_confirmation = nqc.StageCorrectionStatus.CONFIRMED
        stub_net_project_user_data = tsn.ProjectUserDataDto(stage_qcs={
            uuid.UUID(stage_id_dto): {
                nqc.StageQCTags.START_STOP_CONFIRMATION: tsn.StageQCValueDto(expected_start_stop_confirmation, None),
            },
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_net_project_user_data)

        assert_that(sut.stage_qc(uuid.UUID(stage_id_dto)).start_stop_confirmation,
                    equal_to(expected_start_stop_confirmation))

    @unittest.skip('Awaiting lower-level code')
    def test_stage_qc_has_correct_stage_id_if_stage_id_and_qc_notes_in_user_data(self):
        stage_id_dto = tsn.DONT_CARE_ID_C
        stub_net_project_user_data = tsn.ProjectUserDataDto(stage_qcs={
            uuid.UUID(stage_id_dto): {
                nqc.StageQCTags.QC_NOTES: tsn.StageQCValueDto('soror', None),
            },
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_net_project_user_data)

        assert_that(sut.stage_qc(uuid.UUID(stage_id_dto)).stage_id,
                    equal_to(uuid.UUID(stage_id_dto)))

    @unittest.skip('Awaiting lower-level code')
    def test_stage_qc_has_correct_qc_notes_if_stage_id_and_qc_notes_in_user_data(self):
        stage_id_dto = tsn.DONT_CARE_ID_C
        expected_qc_notes = 'pellet'
        stub_net_project_user_data = tsn.ProjectUserDataDto(stage_qcs={
            uuid.UUID(stage_id_dto): {
                nqc.StageQCTags.QC_NOTES: tsn.StageQCValueDto(expected_qc_notes, None),
            },
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_net_project_user_data)

        assert_that(sut.stage_qc(uuid.UUID(stage_id_dto)).qc_notes,
                    equal_to(expected_qc_notes))

    @unittest.skip('Awaiting lower-level code')
    def test_stage_qc_is_none_if_stage_id_not_in_user_data(self):
        stub_net_project_user_data = tsn.ProjectUserDataDto().create_net_stub()
        sut = uda.NativeProjectUserData(stub_net_project_user_data)

        assert_that(sut.stage_qc(uuid.UUID(tsn.DONT_CARE_ID_E)), is_(none()))


if __name__ == '__main__':
    unittest.main()
