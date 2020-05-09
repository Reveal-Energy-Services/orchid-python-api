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

import sys
import unittest.mock
import uuid

# TODO: Remove the clr dependency and spec's using .NET types if tests too slow
# To mitigate risks of tests continuing to pass if the .NET types change, I have chosen to add arguments like
# `spec=IProject` to a number of `MagicMock` calls. As explained in the documentation, these specs cause the
# mocks to fail if a mocked method *does not* adhere to the interface exposed by the type used for the spec
# (in this case, `IProject`).
#
# A consequence of this choice is a noticeable slowing of the tests (hypothesized to result from loading the
# .NET assemblies and reflecting on the .NET types to determine correct names). Before this change, this
# author noticed that tests were almost instantaneous (11 tests). Afterwards, a slight, but noticeable pause
# occurs before the tests complete.
#
# If these slowdowns become "too expensive," our future selves will need to remove dependencies on the clr
# and the .NET types used for specs.
import clr
from hamcrest import assert_that, equal_to, has_length, contains_exactly

import image_frac

sys.path.append(r'c:/src/ImageFracApp/ImageFrac/ImageFrac.Application/bin/x64/Debug')
clr.AddReference('ImageFrac.FractureDiagnostics')
# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics import IProject


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
        stub_project = unittest.mock.MagicMock(name='stub_project', spec=IProject)
        # We do not need an actual item, only an array with the correct number of items: 1
        stub_project.Wells.Items = ['dont-care-well']
        patched_loader = image_frac.ProjectLoader('dont_care')
        patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_project)
        uuid_strings = ['cbc82ce5-f8f4-400e-94fc-03a95635f18b']
        expected_well_ids = [uuid.UUID(s) for s in uuid_strings]
        stub_uuid_module.uuid4.side_effect = expected_well_ids
        sut = image_frac.ProjectAdapter(patched_loader)
        # noinspection PyTypeChecker
        # Unpack `expected_well_ids` because `contains_exactly` expects multiple items
        assert_that(sut.well_ids(), contains_exactly(*expected_well_ids))

    @unittest.mock.patch('image_frac.project_adapter.uuid', name='stub_uuid_module', autospec=True)
    def test_many_wells_ids_for_project_with_many_wells(self, stub_uuid_module):
        stub_project = unittest.mock.MagicMock(name='stub_project', spec=IProject)
        # We do not need an actual item, only an array with the correct number of items: 3
        stub_project.Wells.Items = ['dont-care-1', 'dont-car-2', 'dont-care-3']
        patched_loader = image_frac.ProjectLoader('dont_care')
        patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_project)
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
