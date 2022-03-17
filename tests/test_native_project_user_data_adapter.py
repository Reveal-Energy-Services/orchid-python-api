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

from hamcrest import assert_that, equal_to

from orchid import (
    native_project_user_data_adapter as uda,
)

from tests import stub_net as tsn


# Test ideas
# - Return start stop confirmation if start stop confirmation for stage ID available
# - Return new start stop confirmation if start stop confirmation for stage ID not available
# - Set QC notes for stage ID calls `SetValue` with correct values
# - Set start stop confirmation for stage ID calls `SetValue` with correct values
class TestNativeProjectUserDataAdapter(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_stage_qc_notes_if_qc_notes_available_for_stage(self):
        stage_id = 'b64521bf-56a2-4e9c-abca-d466670c75a1'
        expected_qc_notes = 'lucrum nugatorium provenivit'
        stub_project_user_data = tsn.ProjectUserDataDto(stage_qcs={
            uuid.UUID(stage_id): {'stage_qc_notes': expected_qc_notes},
        }).create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_qc_notes(uuid.UUID(stage_id)), equal_to(expected_qc_notes))

    def test_stage_qc_notes_empty_if_qc_notes_not_available_for_stage(self):
        stage_id = '412e5a99-7040-4972-8b27-3ff0d1ab4d94'
        stub_project_user_data = tsn.ProjectUserDataDto().create_net_stub()
        sut = uda.NativeProjectUserData(stub_project_user_data)

        assert_that(sut.stage_qc_notes(uuid.UUID(stage_id)), equal_to(''))


if __name__ == '__main__':
    unittest.main()
