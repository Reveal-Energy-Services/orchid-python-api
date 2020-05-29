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

from orchid.project_monitor_pressure_curves import ProjectMonitorPressureCurves
from orchid.project import ProjectAdapter
from orchid.project_loader import ProjectLoader
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
# TODO: Replace some of this code with configuration and/or a method to use `clr.AddReference`
import sys
import clr
IMAGE_FRAC_ASSEMBLIES_DIR = r'c:/src/OrchidApp/ImageFrac/ImageFrac.Application/bin/Debug'
if IMAGE_FRAC_ASSEMBLIES_DIR not in sys.path:
    sys.path.append(IMAGE_FRAC_ASSEMBLIES_DIR)

clr.AddReference('ImageFrac.FractureDiagnostics')
# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics import IProject, IWell

clr.AddReference('UnitsNet')
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

    def test_returns_meter_project_unit_from_net_project_length_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_length_unit_abbreviation='m')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('length'), equal_to('m'))

    def test_returns_feet_project_unit_from_net_project_length_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_length_unit_abbreviation='ft')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('length'), equal_to('ft'))

    def test_returns_kPa_project_unit_from_net_project_pressure_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_pressure_unit_abbreviation='kPa')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('pressure'), equal_to('kPa'))

    def test_returns_psi_project_unit_from_net_project_pressure_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_pressure_unit_abbreviation='psi')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('pressure'), equal_to('psi'))

    def test_returns_bpm_project_unit_from_net_slurry_rate_units(self):
        stub_net_project = create_stub_net_project(slurry_rate_unit_abbreviation='bbl/min',
                                                   well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('slurry rate'), equal_to('bbl/min'))

    def test_returns_lb_per_gal_project_unit_from_net_proppant_concentration_units(self):
        stub_net_project = create_stub_net_project(
            proppant_concentration_unit_abbreviation='lb/gal (U.S.)', well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('proppant concentration'), equal_to('lb/gal (U.S.)'))


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = ProjectAdapter(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
