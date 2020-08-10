#  Copyright 2017-2020 Reveal Energy Services, Inc 
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

import unittest.mock

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


import deal
from hamcrest import assert_that, equal_to, has_length, contains_exactly, is_, empty, calling, raises

from orchid.project_wells import ProjectWells
from orchid.project_loader import ProjectLoader
from tests.stub_net import create_stub_net_project

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IProject, IWell, IStage
# noinspection PyUnresolvedReferences
import UnitsNet


class TestProjectWells(unittest.TestCase):
    # Test ideas:
    # - Call deprecated_transform_net_treatment correctly with one stage with stage number 1
    # - Call deprecated_transform_net_treatment correctly with one stage with stage number 40
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_ctor_no_loader_raises_exception(self):
        assert_that(calling(ProjectWells).with_args(None), raises(deal.PreContractError))

    def test_no_well_ids_for_project_with_no_wells(self):
        stub_project_loader = unittest.mock.MagicMock(name='stub_project_loader', spec=ProjectLoader)
        sut = ProjectWells(stub_project_loader)
        # noinspection PyTypeChecker
        assert_that(sut.well_ids(), has_length(0))

    def test_one_well_id_for_project_with_one_well(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        # noinspection PyTypeChecker
        assert_that(sut.well_ids(), contains_exactly('dont-care-well'))

    def test_many_wells_ids_for_project_with_many_wells(self):
        well_uwis = ['03-293-91256-93-16', '66-253-17741-53-93', '03-76-97935-41-93']
        stub_net_project = create_stub_net_project(well_names=['dont-care-1', 'dont-car-2', 'dont-care-3'],
                                                   uwis=well_uwis)
        sut = create_sut(stub_net_project)

        # noinspection PyTypeChecker
        # Unpack `expected_well_ids` because `contains_exactly` expects multiple items not a list
        assert_that(sut.well_ids(), contains_exactly(*well_uwis))

    def test_well_name_no_well_id_raises_exception(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'], eastings=[], northings=[], tvds=[])
        sut = create_sut(stub_net_project)

        for invalid_well_id in [None, '', '    ']:
            with self.subTest(invalid_well_id=invalid_well_id):
                self.assertRaises(deal.PreContractError, sut.well_name, invalid_well_id)

    def test_display_well_name_no_well_id_raises_exception(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'], eastings=[], northings=[], tvds=[])
        sut = create_sut(stub_net_project)

        for invalid_well_id in [None, '', '\r']:
            with self.subTest(invalid_well_id=invalid_well_id):
                self.assertRaises(deal.PreContractError, sut.well_display_name, invalid_well_id)

    def test_wells_by_name_empty_if_no_well_with_specified_name_in_project(self):
        stub_net_project = create_stub_net_project(well_names=['perditus'])
        sut = create_sut(stub_net_project)

        assert_that(sut.wells_by_name('perditum'), is_(empty()))

    def test_wells_by_name_returns_one_item_if_one_well_with_specified_name_in_project(self):
        stub_net_project = create_stub_net_project(well_names=['perditus'])
        sut = create_sut(stub_net_project)

        assert_that(sut.wells_by_name('perditus'), has_length(equal_to(1)))

    def test_wells_by_name_returns_one_item_if_one_well_with_specified_name_in_project_but_many_wells(self):
        stub_net_project = create_stub_net_project(well_names=['recidivus', 'trusi', 'perditus'])
        sut = create_sut(stub_net_project)

        assert_that(sut.wells_by_name('perditus'), has_length(equal_to(1)))

    def test_wells_by_name_returns_many_items_if_many_wells_with_specified_name_in_project(self):
        stub_net_project = create_stub_net_project(well_names=['recidivus', 'perditus', 'perditus'],
                                                   uwis=['06-120-72781-16-45', '56-659-26378-28-77',
                                                         '66-814-49035-82-57'])
        sut = create_sut(stub_net_project)

        assert_that(sut.wells_by_name('perditus'), has_length(equal_to(2)))


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = ProjectWells(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
