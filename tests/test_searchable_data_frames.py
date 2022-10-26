#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
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
import warnings

from hamcrest import assert_that, equal_to, is_, not_none

from orchid import (
    project as onp,
    project_store as loader,
)
from tests import stub_net as tsn

# noinspection PyUnresolvedReferences
from System import Guid


class TestSearchableDataFrames(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_searchable_data_frames_with_duplicate_object_ids_raises_one_warning(self):
        data_frame_dtos = [
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'querela'},
            {'object_id': tsn.DONT_CARE_ID_A, 'name': 'cado'},
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'loco'},
        ]
        stub_net_project = tsn.create_stub_net_project(data_frame_dtos=data_frame_dtos)
        sut = create_sut(stub_net_project)

        with warnings.catch_warnings(record=True) as actual_warnings:
            # Cause all warnings to be triggered
            warnings.simplefilter("always")
            # Execute the function that I expect to raise a warning
            sut.data_frames()

            # Assert information about the warning(s)
            assert_that(len(actual_warnings), equal_to(1))

    def test_searchable_data_frames_with_duplicate_object_ids_raises_user_warning(self):
        data_frame_dtos = [
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'querela'},
            {'object_id': tsn.DONT_CARE_ID_A, 'name': 'cado'},
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'loco'},
        ]
        stub_net_project = tsn.create_stub_net_project(data_frame_dtos=data_frame_dtos)
        sut = create_sut(stub_net_project)

        with warnings.catch_warnings(record=True) as actual_warnings:
            # Cause all warnings to be triggered
            warnings.simplefilter("always")
            # Execute the function that I expect to raise a warning
            sut.data_frames()

            # Assert information about the warning(s)
            assert_that(actual_warnings[-1].category, equal_to(UserWarning))

    def test_searchable_data_frames_with_duplicate_object_ids_warning_has_message(self):
        data_frame_dtos = [
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'querela'},
            {'object_id': tsn.DONT_CARE_ID_A, 'name': 'cado'},
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'loco'},
        ]
        stub_net_project = tsn.create_stub_net_project(data_frame_dtos=data_frame_dtos)
        sut = create_sut(stub_net_project)

        with warnings.catch_warnings(record=True) as actual_warnings:
            # Cause all warnings to be triggered
            warnings.simplefilter("always")
            # Execute the function that I expect to raise a warning
            sut.data_frames()

            # Assert information about the warning(s)
            actual_warning_text = actual_warnings[-1].message.args[0]
            assert_that(re.search('duplicate object IDs', actual_warning_text, re.MULTILINE))

    def test_searchable_data_frames_with_duplicate_object_ids_warning_contains_find_by_alternative(self):
        data_frame_dtos = [
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'querela'},
            {'object_id': tsn.DONT_CARE_ID_A, 'name': 'cado'},
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'loco'},
        ]
        stub_net_project = tsn.create_stub_net_project(data_frame_dtos=data_frame_dtos)
        sut = create_sut(stub_net_project)

        with warnings.catch_warnings(record=True) as actual_warnings:
            # Cause all warnings to be triggered
            warnings.simplefilter("always")
            # Execute the function that I expect to raise a warning
            sut.data_frames()

            # Assert information about the warning(s)
            actual_warning_text = actual_warnings[-1].message.args[0]
            assert_that(re.search('find_by_name', actual_warning_text, re.MULTILINE) and
                        re.search('find_by_display_name', actual_warning_text, re.MULTILINE))

    def test_searchable_data_frames_with_duplicate_object_ids_warning_has_recreate_alternative(self):
        data_frame_dtos = [
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'querela'},
            {'object_id': tsn.DONT_CARE_ID_A, 'name': 'cado'},
            {'object_id': 'b4a04767-8202-4fd5-a995-bc3531db3f84', 'name': 'loco'},
        ]
        stub_net_project = tsn.create_stub_net_project(data_frame_dtos=data_frame_dtos)
        sut = create_sut(stub_net_project)

        with warnings.catch_warnings(record=True) as actual_warnings:
            # Cause all warnings to be triggered
            warnings.simplefilter("always")
            # Execute the function that I expect to raise a warning
            sut.data_frames()

            # Assert information about the warning(s)
            actual_warning_text = actual_warnings[-1].message.args[0]
            assert_that(re.search('recreate all data frames', actual_warning_text, re.MULTILINE))


def create_sut(stub_net_project):
    patched_loader = loader.ProjectStore('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = onp.Project(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
