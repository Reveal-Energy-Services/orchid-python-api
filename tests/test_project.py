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

import unittest
import unittest.mock

from hamcrest import assert_that, equal_to, contains_exactly

from orchid.project import Project
from orchid.project_loader import ProjectLoader
from tests.stub_net import create_stub_net_project


class TestProject(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_name(self):
        stub_native_project = create_stub_net_project(name='commodorum')
        sut = create_sut(stub_native_project)
        assert_that(sut.name, equal_to('commodorum'))

    def test_wells_if_no_wells(self):
        stub_native_project = create_stub_net_project(name='exsistet')
        sut = create_sut(stub_native_project)
        assert_that(sut.wells, contains_exactly())

    def test_wells_if_one_well(self):
        expected_well_names = ['clunibus']
        stub_native_project = create_stub_net_project(name='exsistet', well_names=expected_well_names)
        sut = create_sut(stub_native_project)
        assert_that(map(lambda w: w.name, sut.wells), contains_exactly(*expected_well_names))

    def test_wells_if_many_wells(self):
        expected_well_names = ['cordam', 'turbibus', 'collaris']
        stub_native_project = create_stub_net_project(name='exsistet', well_names=expected_well_names)
        sut = create_sut(stub_native_project)
        assert_that(map(lambda w: w.name, sut.wells), contains_exactly(*expected_well_names))

    def test_wells_by_name_if_no_wells(self):
        stub_native_project = create_stub_net_project(name='exsistet')
        sut = create_sut(stub_native_project)
        assert_that(sut.wells_by_name('clunibus'), contains_exactly())

    def test_wells_by_name_if_no_well_with_name_found(self):
        expected_well_names = ['clunibus']
        stub_native_project = create_stub_net_project(name='exsistet', well_names=expected_well_names)
        sut = create_sut(stub_native_project)
        assert_that(map(lambda w: w.name, sut.wells_by_name('clunibus')), contains_exactly(*expected_well_names))

    def test_wells_by_name_if_one_well_with_name_found(self):
        expected_well_names = ['clunibus']
        stub_native_project = create_stub_net_project(name='exsistet', well_names=['clunibus'])
        sut = create_sut(stub_native_project)
        assert_that(map(lambda w: w.name, sut.wells_by_name('clunibus')), contains_exactly(*expected_well_names))

    def test_wells_by_name_if_many_wells_with_name_found(self):
        stub_native_project = create_stub_net_project(name='exsistet',
                                                      well_names=['cordam', 'turbibus',
                                                                  'cordam', 'collaris',
                                                                  'cordam'],
                                                      uwis=["93-167-64050-25-81", "54-107-49537-17-76",
                                                            "80-693-58647-57-44", "66-101-46368-44-99",
                                                            "06-390-40886-62-60"])
        sut = create_sut(stub_native_project)
        assert_that(map(lambda w: w.name, sut.wells_by_name('cordam')), contains_exactly(*(['cordam'] * 3)))

    def test_default_well_colors_if_no_default_well_colors(self):
        stub_native_project = create_stub_net_project(name='exsistet')
        sut = create_sut(stub_native_project)
        assert_that(sut.default_well_colors(), equal_to([tuple([])]))

    def test_default_well_colors_if_one_default_well_color(self):
        stub_native_project = create_stub_net_project(name='exsistet', default_well_colors=[[0.142, 0.868, 0.220]])
        sut = create_sut(stub_native_project)
        # noinspection PyTypeChecker
        assert_that(sut.default_well_colors(), contains_exactly((0.142, 0.868, 0.220)))

    def test_default_well_colors_if_many_default_well_colors(self):
        expected_default_well_colors = [(0.610, 0.779, 0.675), (0.758, 0.982, 0.720), (0.297, 0.763, 0.388)]
        stub_native_project = create_stub_net_project(name='exsistet',
                                                      default_well_colors=[list(t) for t
                                                                           in expected_default_well_colors])
        sut = create_sut(stub_native_project)
        # noinspection PyTypeChecker
        assert_that(sut.default_well_colors(), contains_exactly(*expected_default_well_colors))


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = Project(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
