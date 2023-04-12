#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2023 Reveal Energy Services.  All Rights Reserved.
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
import uuid

from hamcrest import assert_that, equal_to, contains_exactly, is_, none
import toolz.curried as toolz

from orchid import (
    dom_project_object as dpo,
    searchable_project_objects as spo,
)

from tests import stub_net as tsn


# Test ideas
class TestSearchableProjectObjects(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_length_of_constructed_collection_is_correct(self):
        for net_project_object_dtos in (
                (),
                ({'object_id': tsn.DONT_CARE_ID_A},),
                # Don't care about the object IDs - but **must** be different
                ({'object_id': tsn.DONT_CARE_ID_B},
                 {'object_id': tsn.DONT_CARE_ID_C},
                 {'object_id': tsn.DONT_CARE_ID_D}),
        ):
            with self.subTest(f'Test length {len(net_project_object_dtos)} of constructed collection'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                assert_that(len(sut), equal_to(len(net_project_object_dtos)))

    def test_iteration_over_collection_returns_all_items(self):
        for net_project_object_dtos in (
                (),
                ({'object_id': tsn.DONT_CARE_ID_A},),
                ({'object_id': tsn.DONT_CARE_ID_B},
                 {'object_id': tsn.DONT_CARE_ID_C},
                 {'object_id': tsn.DONT_CARE_ID_D}),
        ):
            with self.subTest(f'Test length {len(net_project_object_dtos)} of constructed collection'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])
                actual_object_ids = toolz.pipe(
                    sut,
                    toolz.map(lambda po: po.object_id),
                    set,
                )
                expected_object_ids = toolz.pipe(
                    net_project_object_dtos,
                    toolz.map(toolz.get('object_id')),
                    toolz.map(uuid.UUID),
                    set,
                )
                assert_that(actual_object_ids, equal_to(expected_object_ids))

    def test_query_all_object_ids_from_collection(self):
        for net_project_object_dtos in (
                (),
                ({'object_id': 'fbb6edad-2379-4bde-8eac-e42bf472c8f8'},),
                ({'object_id': 'a5f8ebd1-d6f2-49c2-aeb5-a8646857f1b7'},
                 {'object_id': '83462051-6fb0-4810-92b2-3802fbd55e19'},
                 {'object_id': '154af216-6e13-4a10-85ab-24085a674550'}),
        ):
            expected = [uuid.UUID(dto['object_id']) for dto in net_project_object_dtos]
            with self.subTest(f'Test all_object_ids, {expected} of constructed collection'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                # noinspection PyTypeChecker
                assert_that(list(sut.all_object_ids()), contains_exactly(*expected))

    def test_query_all_objects_from_collection(self):
        for net_project_object_dtos in (
                (),
                ({'object_id': tsn.DONT_CARE_ID_A},),
                ({'object_id': tsn.DONT_CARE_ID_B},
                 {'object_id': tsn.DONT_CARE_ID_C},
                 {'object_id': tsn.DONT_CARE_ID_D}),
        ):
            with self.subTest(f'Test all_objects() returns {len(net_project_object_dtos)} instances'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                actual_object_ids = toolz.pipe(
                    sut.all_objects(),
                    toolz.map(lambda po: po.object_id),
                    set,
                )
                expected_object_ids = toolz.pipe(
                    net_project_object_dtos,
                    toolz.map(toolz.get('object_id')),
                    toolz.map(uuid.UUID),
                    set
                )
                assert_that(actual_object_ids, equal_to(expected_object_ids))

    def test_query_all_display_names_from_collection(self):
        for net_project_object_dtos in (
                (),
                ({'object_id': tsn.DONT_CARE_ID_A, 'display_name': 'assidui'},),
                (
                    # Don't care about the object IDs - but the **must** be different
                    {'object_id': tsn.DONT_CARE_ID_B, 'display_name': 'mutabilibus'},
                    {'object_id': tsn.DONT_CARE_ID_C, 'display_name': 'anno'},
                    {'object_id': tsn.DONT_CARE_ID_D, 'display_name': 'vestustas'}
                ),
        ):
            expected = [dto['display_name'] for dto in net_project_object_dtos]
            with self.subTest(f'Test all_object_ids, {expected} of constructed collection'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                # noinspection PyTypeChecker
                assert_that(list(sut.all_display_names()), contains_exactly(*expected))

    def test_query_all_names_from_collection(self):
        for net_project_object_dtos in (
                (),
                ({'object_id': tsn.DONT_CARE_ID_A, 'name': 'per'},),
                (
                        # Don't care about the object IDs - but the **must** be different
                        {'object_id': tsn.DONT_CARE_ID_B, 'name': 'caponis'},
                        {'object_id': tsn.DONT_CARE_ID_C, 'name': 'probis'},
                        {'object_id': tsn.DONT_CARE_ID_D, 'name': 'aversis'}
                ),
        ):
            expected = [dto['name'] for dto in net_project_object_dtos]
            with self.subTest(f'Test all_object_ids, {expected} of constructed collection'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                # noinspection PyTypeChecker
                assert_that(list(sut.all_names()), contains_exactly(*expected))

    def test_find_by_display_name_returns_matching_project_objects_with_sought_name(self):
        for net_project_object_dtos, display_name_to_match, match_count in (
                (({'object_id': tsn.DONT_CARE_ID_A, 'display_name': 'restaurat'},),
                 'restauras', 0),
                (({'object_id': tsn.DONT_CARE_ID_B, 'display_name': 'insuperabile'},),
                 'insuperabile', 1),
                # Don't care about the object IDs - but the **must** be different
                (({'object_id': tsn.DONT_CARE_ID_C, 'display_name': 'diluit'},
                  {'object_id': tsn.DONT_CARE_ID_D, 'display_name': 'diluit'},
                  {'object_id': tsn.DONT_CARE_ID_E, 'display_name': 'amavit'}),
                 'diluit', 2),
        ):
            with self.subTest(f'Find by display name returns {match_count}'
                              f' matches of "{display_name_to_match}"'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                matching_data_frame_display_names = list(toolz.map(
                    lambda df: df.display_name, sut.find_by_display_name(display_name_to_match)))
                assert_that(matching_data_frame_display_names, equal_to([display_name_to_match] * match_count))

    def test_find_by_display_name_correctly_ignores_surrounding_whitespace(self):
        expected_display_name = 'immutabilis'
        for leading, trailing in [
            (' ', ' '),
            ('', ' '),
            (' ', ''),
            ('', ''),
        ]:
            display_name_to_find = f'{leading}{expected_display_name}{trailing}'
            with self.subTest(f'Find by display name("{display_name_to_find}")'):
                net_project_object_dto = {'object_id': tsn.DONT_CARE_ID_A, 'display_name': expected_display_name}
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in [net_project_object_dto]])

                matching_data_frame_display_names = list(toolz.map(
                    lambda df: df.display_name, sut.find_by_display_name(display_name_to_find)))
                assert_that(matching_data_frame_display_names, equal_to([expected_display_name]))

    def test_find_by_name_returns_matching_project_objects_with_sought_name(self):
        for net_project_object_dtos, name_to_match, match_count in (
                (({'object_id': tsn.DONT_CARE_ID_A, 'name': 'vicis'},),
                 'vici', 0),
                (({'object_id': tsn.DONT_CARE_ID_B, 'name': 'rosae'},),
                 'rosae', 1),
                # Don't care about the object IDs - but the **must** be different
                (({'object_id': tsn.DONT_CARE_ID_C, 'name': 'viva'},
                  {'object_id': tsn.DONT_CARE_ID_D, 'name': 'cryptico'},
                  {'object_id': tsn.DONT_CARE_ID_E, 'name': 'cryptico'}),
                 'cryptico', 2),
        ):
            with self.subTest(f'Find by name returns {match_count}'
                              f' matches of "{name_to_match}"'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                matching_data_frame_names = list(toolz.map(
                    lambda df: df.name, sut.find_by_name(name_to_match)))
                assert_that(matching_data_frame_names, equal_to([name_to_match] * match_count))

    def test_find_by_name_correctly_ignores_surrounding_whitespace(self):
        expected_name = 'deglutio'
        for leading, trailing in [
            (' ', ' '),
            ('', ' '),
            (' ', ''),
            ('', ''),
        ]:
            name_to_find = f'{leading}{expected_name}{trailing}'
            with self.subTest(f'Find by name("{name_to_find}")'):
                net_project_object_dto = {'object_id': tsn.DONT_CARE_ID_C, 'name': expected_name}
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in [net_project_object_dto]])

                matching_data_frame_names = list(toolz.map(
                    lambda df: df.name, sut.find_by_name(name_to_find)))
                assert_that(matching_data_frame_names, equal_to([expected_name]))

    def test_find_by_object_id_with_match_returns_project_object_with_object_id(self):
        net_project_object_dtos = ({'object_id': '78999fda-2998-42cb-98df-13a064b3c16f'},
                                   {'object_id': '1185f8ed-2dbb-4cb9-8614-95d2eda6f02b'},
                                   {'object_id': '38a1414a-c526-48b8-b069-862fcd6668bb'})
        sought_id = uuid.UUID('38a1414a-c526-48b8-b069-862fcd6668bb')
        sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

        actual_project_object = sut.find_by_object_id(sought_id)
        assert_that(actual_project_object.object_id, equal_to(sought_id))

    def test_find_by_object_id_with_no_match_returns_project_object_with_object_id(self):
        net_project_object_dtos = [{'object_id': '736b6850-6b13-4657-aca2-3efa9629da42'},
                                   {'object_id': '15843a09-4de6-45f0-b20c-b61671e9ea41'},
                                   {'object_id': 'b40ef09b-fe59-414f-bc00-4bd8a82b0990'}]
        sought_id = uuid.UUID('15843a09-4de6-45f0-b20c-b61671e9ea42')
        sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

        actual_project_object = sut.find_by_object_id(sought_id)
        assert_that(actual_project_object, is_(none()))


def create_sut(net_project_object_dtos):
    return spo.SearchableProjectObjects(dpo.DomProjectObject, net_project_object_dtos)


if __name__ == '__main__':
    unittest.main()
