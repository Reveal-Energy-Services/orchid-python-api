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

import deal
from hamcrest import assert_that, equal_to, calling, raises

from orchid import (
    native_stage_qc_adapter as qca,
    net_stage_qc as nqc,
)

from tests import stub_net as tsn


# Test ideas
# - start_stop_confirmation returns NEW if stage exists but status not set in project user data
# - start_stop_confirmation raises error if stage not present in project user data
# - start_stop_confirmation raises error if stage start stop confirmation not of type `System.String`
# - qc_notes raises error if stage not present in project user data
# - qc_notes returns notes if set in project user data
# - qc_notes returns empty string if not set in project user data
# - qc_notes raises error if stage not present in project user data
# - qc_notes raises error if stage QC notes not of type `System.String`
class TestNativeStageQCAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_ctor_raises_exception_if_no_stage_id(self):
        stub_project_user_data = tsn.ProjectUserDataDto().create_net_stub()

        assert_that(calling(qca.NativeStageQCAdapter).with_args(None, stub_project_user_data),
                    raises(deal.PreContractError, pattern='stage_id.*required'))

    def test_ctor_raises_exception_if_stage_id_not_in_project_user_data(self):
        not_found_stage_id = tsn.DONT_CARE_ID_A
        stub_project_user_data = tsn.ProjectUserDataDto({tsn.DONT_CARE_ID_C: {}}).create_net_stub()

        assert_that(calling(qca.NativeStageQCAdapter).with_args(not_found_stage_id, stub_project_user_data),
                    raises(deal.PreContractError, pattern='`stage_id` must be in project user data'))

    def test_stage_id_returns_id_set_at_construction(self):
        expected_stage_id = 'b64521bf-56a2-4e9c-abca-d466670c75a1'
        stub_project_user_data = tsn.ProjectUserDataDto().create_net_stub()
        sut = qca.NativeStageQCAdapter(uuid.UUID(expected_stage_id), stub_project_user_data)

        assert_that(sut.stage_id, equal_to(uuid.UUID(expected_stage_id)))

    def test_stage_start_stop_confirmation_returns_value_if_stage_exists_and_value_set(self):
        for expected_confirmation in [nqc.StageCorrectionStatus.CONFIRMED,
                                      nqc.StageCorrectionStatus.NEW,
                                      nqc.StageCorrectionStatus.UNCONFIRMED]:
            with self.subTest(f'Verify that confirmation status, {expected_confirmation},'
                              f' exists for stage, {tsn.DONT_CARE_ID_B}'):
                stub_project_user_data = tsn.ProjectUserDataDto(to_json={
                    nqc.make_start_stop_confirmation_key(tsn.DONT_CARE_ID_B): {
                        'Type': 'System.String',
                        'Value': expected_confirmation.name.capitalize(),
                    },
                }).create_net_stub()
                sut = qca.NativeStageQCAdapter(tsn.DONT_CARE_ID_B, stub_project_user_data)

                assert_that(sut.start_stop_confirmation, equal_to(nqc.StageCorrectionStatus(expected_confirmation)))


if __name__ == '__main__':
    unittest.main()
