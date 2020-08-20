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

import deal
from hamcrest import assert_that, equal_to, instance_of, calling, raises

from orchid.project import Project
from orchid.project_loader import ProjectLoader
from orchid.project_wells import ProjectWells
from tests.stub_net import create_stub_net_project

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IProject, IWell
# noinspection PyUnresolvedReferences
import UnitsNet


class TestHighLevelProject(unittest.TestCase):
    # Test ideas:
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_ctor_return_all_wells(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_length_unit_abbreviation='m')
        sut = create_sut(stub_net_project)

        assert_that(sut.all_wells(), instance_of(ProjectWells))


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = Project(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
