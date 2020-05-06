#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

import unittest.mock
import uuid

from hamcrest import assert_that, equal_to, has_length, contains_exactly

import image_frac


class StubWells:
    def __init__(self, items):
        self.Items = items


class TestProjectLoader(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_no_well_ids_for_project_with_no_wells(self):
        stub_project_loader = unittest.mock.MagicMock(name='stub_project_loader', spec=image_frac.ProjectLoader)
        sut = image_frac.ProjectAdapter(stub_project_loader)
        # noinspection PyTypeChecker
        assert_that(sut.well_ids(), has_length(0))

    @unittest.mock.patch('image_frac.project_adapter.uuid', name='stub_uuid_module', autospec=True)
    def test_one_well_ids_for_project_with_one_well(self, stub_uuid_module):
        patched_loader = image_frac.ProjectLoader('dont_care')
        patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project')
        # We do not need an actual item, only an array with the correct number of items: 1
        stub_wells = StubWells(['dont_care_item'])
        patched_loader.loaded_project.return_value.Wells = stub_wells
        expected_well_id = uuid.UUID('cbc82ce5-f8f4-400e-94fc-03a95635f18b')
        stub_uuid_module.uuid4.return_value = expected_well_id
        sut = image_frac.ProjectAdapter(patched_loader)
        # noinspection PyTypeChecker
        assert_that(sut.well_ids(), contains_exactly(expected_well_id))

    @unittest.mock.patch('image_frac.project_adapter.uuid', name='stub_uuid_module', autospec=True)
    def test_many_wells_ids_for_project_with_many_wells(self, stub_uuid_module):
        patched_loader = image_frac.ProjectLoader('dont_care')
        patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project')
        # We do not need an actual item, only an array with the correct number of items: 1
        stub_wells = StubWells(['dont_care_1', 'dont_care_2', 'dont_care_3'])
        patched_loader.loaded_project.return_value.Wells = stub_wells
        uuid_strings = ['0b09aae5-8355-4968-815c-5622dfc7aac6',
                        'a1ba308d-c3d9-4314-bc21-d6bbb80ebcf8', 'cbde9d6f-2c95-4d8b-a1b8-5235194d0fa6']
        expected_well_ids = [uuid.UUID(s) for s in uuid_strings]
        stub_uuid_module.uuid4.side_effect = expected_well_ids
        sut = image_frac.ProjectAdapter(patched_loader)
        # noinspection PyTypeChecker
        # Unpack `expected_well_ids` because `contains_exactly` expects multiple items
        assert_that(sut.well_ids(), contains_exactly(*expected_well_ids))


if __name__ == '__main__':
    unittest.main()
