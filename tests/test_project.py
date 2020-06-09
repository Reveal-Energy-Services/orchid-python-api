#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
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
import unittest.mock

from hamcrest import assert_that, equal_to

from orchid.project import Project
from orchid.project_loader import ProjectLoader
from tests.stub_net import create_stub_net_project


class TestProject(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_project_name(self):
        stub_native_project = create_stub_net_project(name='commodorum')
        sut = create_sut(stub_native_project)
        assert_that(sut.name(), equal_to('commodorum'))

    def test_project_wells_if_no_wells(self):
        stub_native_project = create_stub_net_project(name='exsistet')
        sut = create_sut(stub_native_project)
        assert_that(len(sut.wells()), equal_to(0))

    def test_project_wells_if_one_well(self):
        stub_native_project = create_stub_net_project(name='exsistet', well_names=['clunibus'])
        sut = create_sut(stub_native_project)
        assert_that(len(sut.wells()), equal_to(1))

    def test_project_wells_if_many_wells(self):
        stub_native_project = create_stub_net_project(name='exsistet', well_names=['cordam', 'turbibus', 'collaris'])
        sut = create_sut(stub_native_project)
        assert_that(len(sut.wells()), equal_to(3))


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = Project(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
