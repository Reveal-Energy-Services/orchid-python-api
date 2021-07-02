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
    dom_project_objects as poc,
)

from tests import stub_net as tsn


# Test ideas
class TestProjectObjects(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_constructed_collection_has_correct_number_of_elements(self):
        # All the tests use a stub object returned by `tsn.create_stub_project_object`. The `mock.MagicMock`
        # returned by this method only supports `object_id`, `name` and `display_name`. This approach assumes that
        # the unit tests for the `Native...Adapter` ensure that these properties work for the actual wrapper objects.
        for net_items, item_callable in [
            ([], tsn.create_stub_project_object),
            ([{}], tsn.create_stub_project_object),
            ([{}, {}, {}], tsn.create_stub_project_object),
        ]:
            with self.subTest(f'Verify {len(net_items)} in collection'):
                sut = create_sut(net_items, item_callable)

                assert_that(len(sut), equal_to(len(net_items)))

    def test_query_object_ids_from_collection(self):
        for net_items, item_callable in [
            ([], tsn.create_stub_project_object()),
            ([{'object_id': 'fbb6edad-2379-4bde-8eac-e42bf472c8f8'}], tsn.create_stub_project_object),
            ([{'object_id': 'a5f8ebd1-d6f2-49c2-aeb5-a8646857f1b7'},
              {'object_id': '83462051-6fb0-4810-92b2-3802fbd55e19'},
              {'object_id': '154af216-6e13-4a10-85ab-24085a674550'}], tsn.create_stub_project_object),
        ]:
            expected = toolz.pipe(net_items,
                                  toolz.map(toolz.get('object_id')),
                                  toolz.map(uuid.UUID),
                                  list)
            with self.subTest(f'Verify object ids, {expected}, in collection'):
                sut = create_sut(net_items, item_callable)

                # noinspection PyTypeChecker
                assert_that(list(sut.all_object_ids()), contains_exactly(*expected))

    def test_query_all_display_names_from_collection(self):
        for net_items, item_callable in [
            ([], tsn.create_stub_project_object()),
            ([{'display_name': 'assidui'}], tsn.create_stub_project_object),
            ([{'display_name': 'mutabilibus'},
              {'display_name': 'anno'},
              {'display_name': 'vestustas'}], tsn.create_stub_project_object),
        ]:
            expected = toolz.pipe(net_items,
                                  toolz.map(toolz.get('display_name')),
                                  list)
            with self.subTest(f'Verify {expected} in collection'):
                sut = create_sut(net_items, item_callable)

                # noinspection PyTypeChecker
                assert_that(list(sut.all_display_names()), contains_exactly(*expected))

    def test_query_all_names_from_collection(self):
        for net_items, item_callable in [
            ([], tsn.create_stub_project_object()),
            ([{'name': 'per'}], tsn.create_stub_project_object),
            ([{'name': 'caponis'},
              {'name': 'probis'},
              {'name': 'aversis'}], tsn.create_stub_project_object),
        ]:
            expected = toolz.pipe(net_items,
                                  toolz.map(toolz.get('name')),
                                  list)
            with self.subTest(f'Verify {expected} in collection'):
                sut = create_sut(net_items, item_callable)

                # noinspection PyTypeChecker
                assert_that(list(sut.all_names()), contains_exactly(*expected))

    def test_find_by_display_name_returns_matching_project_objects_with_sought_name(self):
        for net_items, display_name_to_match, match_count in [
            ([{'display_name': 'restaurat'}], 'restauras', 0),
            ([{'display_name': 'insuperabile'}], 'insuperabile', 1),
            ([{'display_name': 'diluit'}, {'display_name': 'diluit'}, {'display_name': 'amavit'}], 'diluit', 2),
        ]:
            with self.subTest(f'Find by display name returns {match_count}'
                              f' matches of "{display_name_to_match}"'):
                sut = create_sut(net_items, tsn.create_stub_project_object)

                matching_data_frame_display_names = list(toolz.map(
                    lambda df: df.display_name, sut.find_by_display_name(display_name_to_match)))
                assert_that(matching_data_frame_display_names, equal_to([display_name_to_match] * match_count))

    def test_find_with_name_returns_matches_with_requested_name(self):
        for net_items, name_to_match, match_count in [
            ([{'name': 'vicis'}], 'vici', 0),
            ([{'name': 'rosae'}], 'rosae', 1),
            ([{'name': 'viva'}, {'name': 'cryptico'}, {'name': 'cryptico'}], 'cryptico', 2),
        ]:
            with self.subTest(f'Find by name returns {match_count} matches of "{name_to_match}"'):
                sut = create_sut(net_items, tsn.create_stub_project_object)

                matching_data_frame_names = list(toolz.map(lambda df: df.name,
                                                           sut.find_by_name(name_to_match)))
                assert_that(matching_data_frame_names, equal_to([name_to_match] * match_count))

    def test_find_by_object_id_with_match_returns_project_object_with_object_id(self):
        net_ids = [{'object_id': '78999fda-2998-42cb-98df-13a064b3c16f'},
                   {'object_id': '1185f8ed-2dbb-4cb9-8614-95d2eda6f02b'},
                   {'object_id': '38a1414a-c526-48b8-b069-862fcd6668bb'}]
        sought_id = uuid.UUID('38a1414a-c526-48b8-b069-862fcd6668bb')
        sut = create_sut(net_ids, tsn.create_stub_project_object)

        actual_project_object = sut.find_by_object_id(sought_id)
        assert_that(actual_project_object.object_id, equal_to(sought_id))

    def test_find_by_object_id_with_no_match_returns_project_object_with_object_id(self):
        net_id = [{'object_id': '736b6850-6b13-4657-aca2-3efa9629da42'},
                  {'object_id': '15843a09-4de6-45f0-b20c-b61671e9ea41'},
                  {'object_id': 'b40ef09b-fe59-414f-bc00-4bd8a82b0990'}]
        sought_id = uuid.UUID('15843a09-4de6-45f0-b20c-b61671e9ea42')
        sut = create_sut(net_id, tsn.create_stub_project_object)

        actual_project_object = sut.find_by_object_id(sought_id)
        assert_that(actual_project_object, is_(none()))


def create_sut(net_items, create_func):
    return poc.ProjectObjects(create_func, net_items)


if __name__ == '__main__':
    unittest.main()
