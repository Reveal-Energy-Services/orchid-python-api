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
    native_variant_adapter as nva,
    net_stage_qc as nqc,
)

from tests import stub_net as tsn


# Test ideas
# - start_stop_confirmation returns status if set in project user data
# - start_stop_confirmation returns NEW if status not set in project user data
# - qc_notes returns notes if set in project user data
# - qc_notes returns empty string if not set in project user data
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

    @unittest.skip('Awaiting lower-level code')
    def test_start_stop_confirmation_returns_available_value_from_project_user_data(self):
        dont_care_stage_id = tsn.DONT_CARE_ID_B
        expected_start_stop_confirmation = 'animus meus aedificio repudiat'
        stub_project_user_data = tsn.ProjectUserDataDto({
            dont_care_stage_id: {
                nqc.StageQCTags.START_STOP_CONFIRMATION:
                    tsn.StageQCValueDto(tsn.VariantDto(expected_start_stop_confirmation,
                                                       nva.PythonVariantTypes.INT32),
                                        tsn.VariantDto('non applicabitis',
                                                       nva.PythonVariantTypes.STRING)),
            }
        }).create_net_stub()

        sut = qca.NativeStageQCAdapter(uuid.UUID(dont_care_stage_id), stub_project_user_data)

        assert_that(sut.start_stop_confirmation, equal_to(expected_start_stop_confirmation))

    @unittest.skip('Awaiting lower-level code')
    def test_start_stop_confirmation_returns_default_variant_value_from_project_user_data(self):
        dont_care_stage_id = tsn.DONT_CARE_ID_C
        stub_project_user_data = tsn.ProjectUserDataDto({
            dont_care_stage_id: {
                nqc.StageQCTags.START_STOP_CONFIRMATION:
                    tsn.StageQCValueDto(None, tsn.VariantDto('non applicabitis',
                                                             nva.PythonVariantTypes.STRING)),
            }
        }).create_net_stub()

        sut = qca.NativeStageQCAdapter(uuid.UUID(dont_care_stage_id), stub_project_user_data)

        assert_that(sut.start_stop_confirmation, equal_to('non applicabitis'))

    def test_qc_notes_returns_available_value_from_project_user_data(self):
        dont_care_stage_id = tsn.DONT_CARE_ID_D
        expected_qc_notes = 'lucrum nugatorium provenivit'
        stub_project_user_data = tsn.ProjectUserDataDto({
            dont_care_stage_id: {
                nqc.StageQCTags.QC_NOTES: tsn.StageQCValueDto(tsn.VariantDto(expected_qc_notes,
                                                                             nva.PythonVariantTypes.STRING),
                                                              tsn.VariantDto('non applicabitis',
                                                                             nva.PythonVariantTypes.STRING)),
            }
        }).create_net_stub()

        sut = qca.NativeStageQCAdapter(uuid.UUID(dont_care_stage_id), stub_project_user_data)

        assert_that(sut.qc_notes, equal_to(expected_qc_notes))

    def test_qc_notes_returns_default_variant_value_from_project_user_data(self):
        dont_care_stage_id = tsn.DONT_CARE_ID_E
        stub_project_user_data = tsn.ProjectUserDataDto({
            dont_care_stage_id: {
                nqc.StageQCTags.QC_NOTES: tsn.StageQCValueDto(None, tsn.VariantDto('non applicabitis',
                                                                                   nva.PythonVariantTypes.STRING)),
            }
        }).create_net_stub()

        sut = qca.NativeStageQCAdapter(uuid.UUID(dont_care_stage_id), stub_project_user_data)

        assert_that(sut.qc_notes, equal_to('non applicabitis'))


if __name__ == '__main__':
    unittest.main()
