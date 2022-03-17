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
    native_project_user_data_adapter as uda,
    net_stage_qc as nqc,
)

from tests import stub_net as tsn


# Test ideas
class TestNativeProjectUserDataAdapter(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_stage_qc_has_correct_stage_id_if_stage_id_and_start_stop_confirmation_in_user_data(self):
        stage_id_dto = '78edb717-0528-4710-8b61-15ebc8f283c1'
        key = nqc.make_start_stop_confirmation_key(stage_id_dto)
        value = {'Type': 'System.String', 'Value': 'Confirmed'}
        stub_project_user_data = tsn.ProjectUserDataDto(to_json={key: value}).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_qc(uuid.UUID(stage_id_dto)).stage_id, equal_to(uuid.UUID(stage_id_dto)))

    def test_stage_qc_has_correct_stage_id_if_stage_id_and_qc_notes_in_user_data(self):
        stage_id_dto = 'c93dcd1a-b156-46b6-b7fd-3d0c8205675c'
        key = nqc.make_qc_notes_key(stage_id_dto)
        value = {'Type': 'System.String', 'Value': 'animus meus aedificio repudiat'}
        stub_project_user_data = tsn.ProjectUserDataDto(to_json={key: value}).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_qc(uuid.UUID(stage_id_dto)).stage_id, equal_to(uuid.UUID(stage_id_dto)))

    def test_stage_qc_raises_error_if_supplied_stage_id_is_none(self):
        stub_project_user_data = tsn.ProjectUserDataDto(to_json={tsn.DONT_CARE_ID_B: {}}).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(calling(sut.stage_qc).with_args(None), raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
