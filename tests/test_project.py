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

import deal
from hamcrest import assert_that, equal_to, instance_of, calling, raises

import orchid.dot_net
from orchid.project import ProjectAdapter
from orchid.project_loader import ProjectLoader
from orchid.project_monitor_pressure_curves import ProjectMonitorPressureCurves
from orchid.project_wells import ProjectWells
from tests.stub_net import create_stub_net_project

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
orchid.dot_net.append_orchid_assemblies_directory_path()
# This function call must occur *after* the call to `append_orchid_assemblies_directory_path`
orchid.dot_net.add_orchid_assemblies()

# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics import IProject, IWell
# noinspection PyUnresolvedReferences
import UnitsNet


class TestProject(unittest.TestCase):
    # Test ideas:
    # Return correct abbreviation for the project's length units
    # - Trajectory points
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_ctor_no_loader_raises_exception(self):
        assert_that(calling(ProjectAdapter).with_args(None), raises(deal.PreContractError))

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
    patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = ProjectAdapter(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
