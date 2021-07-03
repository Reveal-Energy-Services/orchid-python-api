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
import uuid

from hamcrest import assert_that, equal_to, contains_exactly, is_, none
import toolz.curried as toolz

from orchid import (
    dom_project_object as dpo,
    dom_searchable_project_objects as spo,
)

from tests import stub_net as tsn


# Test ideas
class TestDomSearchableProjectObjects(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_length_of_constructed_collection_is_correct(self):
        for net_project_object_dtos in (
                (),
                ({'object_id': 'acc01ade-acc0-1ade-acc0-1adeacc01ade'},),
                # Don't care about the object IDs - but the **must** be different
                ({'object_id': 'ba5eba11-ba5e-ba11-ba5e-ba11ba5eba11'},
                 {'object_id': 'ca11ab1e-ca11-ab1e-ca11-ab1eca11ab1e'},
                 {'object_id': 'de7ec7ed-de7e-c7ed-de7e-c7edde7ec7ed'}),
        ):
            with self.subTest(f'Test length {len(net_project_object_dtos)} of constructed collection'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                assert_that(len(sut), equal_to(len(net_project_object_dtos)))

    def test_query_object_ids_from_collection(self):
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

    def test_query_all_display_names_from_collection(self):
        for net_project_object_dtos in (
                (),
                ({'display_name': 'assidui', 'object_id': 'acc01ade-acc0-1ade-acc0-1adeacc01ade'},),
                (
                    # Don't care about the object IDs - but the **must** be different
                    {'object_id': 'ba5eba11-ba5e-ba11-ba5e-ba11ba5eba11', 'display_name': 'mutabilibus'},
                    {'object_id': 'ca11ab1e-ca11-ab1e-ca11-ab1eca11ab1e', 'display_name': 'anno'},
                    {'object_id': 'de7ec7ed-de7e-c7ed-de7e-c7edde7ec7ed', 'display_name': 'vestustas'}
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
                ({'name': 'per', 'object_id': 'acc01ade-acc0-1ade-acc0-1adeacc01ade'},),
                (
                        # Don't care about the object IDs - but the **must** be different
                        {'object_id': 'ba5eba11-ba5e-ba11-ba5e-ba11ba5eba11', 'name': 'caponis'},
                        {'object_id': 'ca11ab1e-ca11-ab1e-ca11-ab1eca11ab1e', 'name': 'probis'},
                        {'object_id': 'de7ec7ed-de7e-c7ed-de7e-c7edde7ec7ed', 'name': 'aversis'}
                ),
        ):
            expected = [dto['name'] for dto in net_project_object_dtos]
            with self.subTest(f'Test all_object_ids, {expected} of constructed collection'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                # noinspection PyTypeChecker
                assert_that(list(sut.all_names()), contains_exactly(*expected))

    def test_find_by_display_name_returns_matching_project_objects_with_sought_name(self):
        for net_project_object_dtos, display_name_to_match, match_count in (
                (({'object_id': 'acc01ade-acc0-1ade-acc0-1adeacc01ade', 'display_name': 'restaurat'},),
                 'restauras', 0),
                (({'object_id': 'ba5eba11-ba5e-ba11-ba5e-ba11ba5eba11', 'display_name': 'insuperabile'},),
                 'insuperabile', 1),
                # Don't care about the object IDs - but the **must** be different
                (({'object_id': 'ca11ab1e-ca11-ab1e-ca11-ab1eca11ab1e', 'display_name': 'diluit'},
                  {'object_id': 'de7ec7ed-de7e-c7ed-de7e-c7edde7ec7ed', 'display_name': 'diluit'},
                  {'object_id': 'e5ca1ade-e5ca-1ade-e5ca-1adee5ca1ade', 'display_name': 'amavit'}),
                 'diluit', 2),
        ):
            with self.subTest(f'Find by display name returns {match_count}'
                              f' matches of "{display_name_to_match}"'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                matching_data_frame_display_names = list(toolz.map(
                    lambda df: df.display_name, sut.find_by_display_name(display_name_to_match)))
                assert_that(matching_data_frame_display_names, equal_to([display_name_to_match] * match_count))

    def test_find_by_name_returns_matching_project_objects_with_sought_name(self):
        for net_project_object_dtos, name_to_match, match_count in (
                (({'object_id': 'acc01ade-acc0-1ade-acc0-1adeacc01ade', 'name': 'vicis'},),
                 'vici', 0),
                (({'object_id': 'ba5eba11-ba5e-ba11-ba5e-ba11ba5eba11', 'name': 'rosae'},),
                 'rosae', 1),
                # Don't care about the object IDs - but the **must** be different
                (({'object_id': 'ca11ab1e-ca11-ab1e-ca11-ab1eca11ab1e', 'name': 'viva'},
                  {'object_id': 'de7ec7ed-de7e-c7ed-de7e-c7edde7ec7ed', 'name': 'cryptico'},
                  {'object_id': 'e5ca1ade-e5ca-1ade-e5ca-1adee5ca1ade', 'name': 'cryptico'}),
                 'cryptico', 2),
        ):
            with self.subTest(f'Find by name returns {match_count}'
                              f' matches of "{name_to_match}"'):
                sut = create_sut([tsn.create_stub_net_project_object(**dto) for dto in net_project_object_dtos])

                matching_data_frame_names = list(toolz.map(
                    lambda df: df.name, sut.find_by_name(name_to_match)))
                assert_that(matching_data_frame_names, equal_to([name_to_match] * match_count))

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
    return spo.DomSearchableProjectObjects(dpo.DomProjectObject, net_project_object_dtos)


if __name__ == '__main__':
    unittest.main()
