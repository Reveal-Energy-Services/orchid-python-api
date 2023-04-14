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

import re
import unittest
import unittest.mock
import warnings

from hamcrest import assert_that, equal_to, is_, not_none
import toolz.curried as toolz

from orchid import (
    project as onp,
    project_store as loader,
)
from tests import stub_net as tsn

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import Guid


class TestSearchableDataFrames(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_searchable_data_frames_with_duplicate_object_ids_raises_one_warning(self):
        stub_net_project = create_net_project_with_data_frames_with_duplicate_ids()
        sut = create_sut(stub_net_project)

        def assert_single_warning(the_warnings):
            assert_that(len(the_warnings), equal_to(1))

        assert_warning_func(sut, assert_single_warning)

    def test_searchable_data_frames_with_duplicate_object_ids_raises_user_warning(self):
        stub_net_project = create_net_project_with_data_frames_with_duplicate_ids()
        sut = create_sut(stub_net_project)

        def assert_is_user_warning(the_warnings):
            assert_that(the_warnings[-1].category, equal_to(UserWarning))

        assert_warning_func(sut, assert_is_user_warning)

    def test_searchable_data_frames_with_duplicate_object_ids_warning_has_message(self):
        stub_net_project = create_net_project_with_data_frames_with_duplicate_ids()
        sut = create_sut(stub_net_project)

        assert_warning_func(sut, assert_message_contains_patterns_warning(['duplicate object IDs']))

    def test_searchable_data_frames_with_duplicate_object_ids_warning_contains_find_by_alternative(self):
        stub_net_project = create_net_project_with_data_frames_with_duplicate_ids()
        sut = create_sut(stub_net_project)

        assert_warning_func(sut, assert_message_contains_patterns_warning(['find_by_name',
                                                                           'find_by_display_name']))

    def test_searchable_data_frames_with_duplicate_object_ids_warning_has_recreate_alternative(self):
        stub_net_project = create_net_project_with_data_frames_with_duplicate_ids()
        sut = create_sut(stub_net_project)

        assert_warning_func(sut, assert_message_contains_patterns_warning(['recreate all data frames']))


def create_net_project_with_data_frames_with_duplicate_ids():
    data_frame_dtos = [
        {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'querela'},
        {'object_id': tsn.DONT_CARE_ID_A, 'name': 'cado'},
        {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'loco'},
    ]
    stub_net_project = tsn.create_stub_net_project(data_frame_dtos=data_frame_dtos)
    return stub_net_project


def create_sut(stub_net_project):
    patched_loader = loader.ProjectStore('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = onp.Project(patched_loader)
    return sut


def assert_warning_func(sut, assert_single_warning):
    with warnings.catch_warnings(record=True) as actual_warnings:
        # Cause all warnings to be triggered
        warnings.simplefilter("always")
        # Execute the function that I expect to raise a warning
        sut.data_frames()

        assert_single_warning(actual_warnings)


@toolz.curry
def assert_message_contains_patterns_warning(patterns, the_warnings):
    actual_warning_text = the_warnings[-1].message.args[0]
    for pattern in patterns:
        assert_that(re.search(pattern, actual_warning_text, re.MULTILINE), is_(not_none()))


if __name__ == '__main__':
    unittest.main()
