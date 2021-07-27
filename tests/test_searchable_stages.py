#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest

from hamcrest import assert_that, equal_to, is_, none, calling, raises
import toolz.curried as toolz


from orchid import (
    native_stage_adapter as nsa,
    searchable_stages as oss,
    searchable_project_objects as spo,
)

from tests import stub_net as tsn


# Test ideas
class TestSearchableStages(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_search_finds_one_matching_display_stage_number_if_one_matching_stage(self):
        stage_dtos = toolz.pipe(
            zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C], range(7, 10)),
            toolz.map(lambda e: {'object_id': e[0], 'display_stage_no': e[1]}),
        )
        to_find_stage_display_number = 9
        stub_net_stages = [tsn.create_stub_net_stage(**stage_dto) for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        actual = sut.find_by_display_stage_number(to_find_stage_display_number)

        assert_that(actual.display_stage_number, equal_to(to_find_stage_display_number))

    def test_search_returns_none_if_no_stages(self):
        stage_dtos = ()
        to_find_stage_display_number = 4
        stub_net_stages = [tsn.create_stub_net_stage(**stage_dto) for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        actual = sut.find_by_display_stage_number(to_find_stage_display_number)

        assert_that(actual, is_(none()))

    def test_search_returns_none_if_no_matching_stages(self):
        stage_dtos = toolz.pipe(
            zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C], range(5, 8)),
            toolz.map(lambda e: {'object_id': e[0], 'display_stage_no': e[1]}),
        )
        to_find_stage_display_number = 8
        stub_net_stages = [tsn.create_stub_net_stage(**stage_dto) for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        actual = sut.find_by_display_stage_number(to_find_stage_display_number)

        assert_that(actual, is_(none()))

    def test_search_raises_error_if_multiple_matching_stages(self):
        stage_dtos = toolz.pipe(
            zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C], [6, 7, 6]),
            toolz.map(lambda e: {'object_id': e[0], 'display_stage_no': e[1]}),
        )
        to_find_stage_display_number = 6
        stub_net_stages = [tsn.create_stub_net_stage(**stage_dto) for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        assert_that(calling(sut.find_by_display_stage_number).with_args(to_find_stage_display_number),
                    raises(spo.SearchableProjectMultipleMatchError, pattern=str(to_find_stage_display_number)))


if __name__ == '__main__':
    unittest.main()
