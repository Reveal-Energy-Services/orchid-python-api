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

from hamcrest import assert_that, equal_to, is_, none

from orchid import (
    native_stage_part_adapter as spa,
    searchable_stage_parts as ssp,
)

from tests import stub_net as tsn


# Test ideas
#
# I have chosen *not* to test neither the method `find_by_display_name_with_well` nor the method
# `find_by_display_name_without_well` because the implementation of these methods simply delegate to
# `SearchableProjectObject.find()` with no additional logic.
class TestSearchableStageParts(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_find_by_part_number_returns_part_with_part_number_if_part_with_part_number_present(self):
        part_dtos = [tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_A, part_no=2),
                     tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_B, part_no=7),
                     tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_C, part_no=1)]

        sut = ssp.SearchableStageParts(spa.NativeStagePartAdapter,
                                       [part_dto.create_net_stub() for part_dto in part_dtos])

        actual = sut.find_by_part_number(7)
        assert_that(actual.part_no, equal_to(7))

    def test_find_by_part_number_returns_none_if_part_with_part_number_not_present(self):
        part_dtos = [tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_A, part_no=2),
                     tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_B, part_no=7),
                     tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_C, part_no=1)]

        sut = ssp.SearchableStageParts(spa.NativeStagePartAdapter,
                                       [part_dto.create_net_stub() for part_dto in part_dtos])

        actual = sut.find_by_part_number(3)
        assert_that(actual, is_(none()))


if __name__ == '__main__':
    unittest.main()
