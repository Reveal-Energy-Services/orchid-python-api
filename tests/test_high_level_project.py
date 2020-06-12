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

import unittest.mock

import deal
from hamcrest import assert_that, equal_to, instance_of, calling, raises

from orchid.project import Project
from orchid.project_loader import ProjectLoader
from orchid.project_monitor_pressure_curves import ProjectMonitorPressureCurves
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

    def test_ctor_no_loader_raises_exception(self):
        assert_that(calling(Project).with_args(None), raises(deal.PreContractError))

    def test_ctor_return_all_monitor_pressures(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_pressure_unit_abbreviation='psi')
        sut = create_sut(stub_net_project)

        assert_that(sut.monitor_pressure_curves(), instance_of(ProjectMonitorPressureCurves))

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
