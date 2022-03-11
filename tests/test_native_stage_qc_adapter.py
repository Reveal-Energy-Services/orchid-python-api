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

from orchid import native_stage_qc_adapter as qca

from tests import stub_net as tsn


# Test ideas
# - Ctor raises exception if supplied stage id not in project user data
# - start_stop_confirmation returns status if set in project user data
# - start_stop_confirmation returns NEW if status not set in project user data
# - qc_notes returns notes if set in project user data
# - qc_notes returns empty string if not set in project user data
class TestNativeStageQCAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_stage_id_returns_id_set_at_construction(self):
        expected_stage_id = 'b64521bf-56a2-4e9c-abca-d466670c75a1'
        stub_project_user_data = tsn.ProjectUserDataDto().create_net_stub()
        sut = qca.NativeStageQCAdapter(uuid.UUID(expected_stage_id), stub_project_user_data)

        assert_that(sut.stage_id, equal_to(uuid.UUID(expected_stage_id)))


if __name__ == '__main__':
    unittest.main()
