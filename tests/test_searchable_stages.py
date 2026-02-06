#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2025 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest

from hamcrest import assert_that, equal_to, is_, none, calling, raises, has_property
import toolz.curried as toolz


from orchid import (
    native_stage_adapter as nsa,
    searchable_stages as oss,
    searchable_project_objects as spo,
)

from tests import stub_net as tsn


# Test ideas
class TestSearchableStages(unittest.TestCase):

    def test_find_by_display_stage_number_finds_match_one_if_one_matching_stage(self):
        stage_dtos = toolz.pipe(
            zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C], range(7, 10)),
            toolz.map(lambda e: {'object_id': e[0], 'display_stage_no': e[1]}),
        )
        to_find_stage_display_number = 9
        stub_net_stages = [tsn.StageDto(**stage_dto).create_net_stub() for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        actual = sut.find_by_display_stage_number(to_find_stage_display_number)

        assert_that(actual.display_stage_number, equal_to(to_find_stage_display_number))

    def test_find_by_display_stage_number_returns_none_if_no_stages(self):
        stage_dtos = ()
        to_find_stage_display_number = 4
        stub_net_stages = [tsn.StageDto(**stage_dto).create_net_stub() for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        actual = sut.find_by_display_stage_number(to_find_stage_display_number)

        assert_that(actual, is_(none()))

    def test_find_by_display_stage_number_returns_none_if_no_matching_stages(self):
        stage_dtos = toolz.pipe(
            zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C], range(5, 8)),
            toolz.map(lambda e: {'object_id': e[0], 'display_stage_no': e[1]}),
        )
        to_find_stage_display_number = 8
        stub_net_stages = [tsn.StageDto(**stage_dto).create_net_stub() for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        actual = sut.find_by_display_stage_number(to_find_stage_display_number)

        assert_that(actual, is_(none()))

    def test_find_by_display_stage_number_raises_error_if_multiple_matching_stages(self):
        stage_dtos = toolz.pipe(
            zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C], [6, 7, 6]),
            toolz.map(lambda e: {'object_id': e[0], 'display_stage_no': e[1]}),
        )
        to_find_stage_display_number = 6
        stub_net_stages = [tsn.StageDto(**stage_dto).create_net_stub() for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        assert_that(calling(sut.find_by_display_stage_number).with_args(to_find_stage_display_number),
                    raises(spo.SearchableProjectMultipleMatchError, pattern=str(to_find_stage_display_number)))

    def test_find_by_display_name_returns_all_matches(self):
        for stage_dtos, to_find in [
            # no stages
            ((), 'vacat'),
            # many stages, one match
            (
                toolz.pipe(
                    zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C],
                        ['capus', 'defero', 'deportas']),
                    toolz.map(lambda e: {'object_id': e[0], 'display_name_with_well': e[1]}),
                    tuple),
                'deportas'
            ),
            # many stages, no match
            (
                    toolz.pipe(
                        zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C],
                            ['extirpamus', 'cenae', 'histronis']),
                        toolz.map(lambda e: {'object_id': e[0], 'display_name_with_well': e[1]}),
                        tuple),
                    'histrio'
            ),
            # many stages, two matches
            (
                    toolz.pipe(
                        zip([tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C],
                            ['hominis', 'pons', 'hominis']),
                        toolz.map(lambda e: {'object_id': e[0], 'display_name_with_well': e[1]}),
                        tuple),
                    'hominis'
            ),
        ]:
            with self.subTest(f'Test find_by_display_name_with_well({to_find}) against {stage_dtos}'):
                stub_net_stages = [tsn.StageDto(**stage_dto).create_net_stub() for stage_dto in stage_dtos]
                sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

                all_found = tuple(sut.find_by_display_name_with_well(to_find))
                for actual in all_found:
                    assert_that(actual, has_property('display_name_with_well', to_find))


if __name__ == '__main__':
    unittest.main()
