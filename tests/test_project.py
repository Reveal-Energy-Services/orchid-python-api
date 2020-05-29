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

from orchid.project_pressure_curves import ProjectPressureCurves
from orchid.project import ProjectAdapter
from orchid.project_loader import ProjectLoader
from orchid.project_wells import ProjectWells

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

    def test_ctor_return_all_pressures(self):
        stub_net_project = create_stub_net_project_abbreviation(well_names=['dont-care-well'],
                                                                project_pressure_unit_abbreviation='psi')
        sut = create_sut(stub_net_project)

        assert_that(sut.monitor_pressure_curves(), instance_of(ProjectPressureCurves))

    def test_ctor_return_all_wells(self):
        stub_net_project = create_stub_net_project_abbreviation(well_names=['dont-care-well'],
                                                                project_length_unit_abbreviation='m')
        sut = create_sut(stub_net_project)

        assert_that(sut.all_wells(), instance_of(ProjectWells))

    def test_returns_meter_project_unit_from_net_project_length_units(self):
        stub_net_project = create_stub_net_project_abbreviation(well_names=['dont-care-well'],
                                                                project_length_unit_abbreviation='m')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('length'), equal_to('m'))

    def test_returns_feet_project_unit_from_net_project_length_units(self):
        stub_net_project = create_stub_net_project_abbreviation(well_names=['dont-care-well'],
                                                                project_length_unit_abbreviation='ft')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('length'), equal_to('ft'))

    def test_returns_kPa_project_unit_from_net_project_pressure_units(self):
        stub_net_project = create_stub_net_project_abbreviation(well_names=['dont-care-well'],
                                                                project_pressure_unit_abbreviation='kPa')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('pressure'), equal_to('kPa'))

    def test_returns_psi_project_unit_from_net_project_pressure_units(self):
        stub_net_project = create_stub_net_project_abbreviation(well_names=['dont-care-well'],
                                                                project_pressure_unit_abbreviation='psi')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('pressure'), equal_to('psi'))

    def test_returns_bpm_project_unit_from_net_slurry_rate_units(self):
        stub_net_project = create_stub_net_project_abbreviation(slurry_rate_unit_abbreviation='bbl/min',
                                                                well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('slurry rate'), equal_to('bbl/min'))

    def test_returns_lb_per_gal_project_unit_from_net_proppant_concentration_units(self):
        stub_net_project = create_stub_net_project_abbreviation(
            proppant_concentration_unit_abbreviation='lb/gal (U.S.)', well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('proppant concentration'), equal_to('lb/gal (U.S.)'))


def set_project_unit(stub_net_project, abbreviation):
    def set_foot_length_unit():
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Foot

    def set_meter_length_unit():
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Meter

    def set_pressure_psi_length_unit():
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.PoundForcePerSquareInch

    def set_pressure_kpa_length_unit():
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.Kilopascal

    def set_slurry_rate_bpm_unit():
        stub_net_project.ProjectUnits.SlurryRateUnit.Item1 = UnitsNet.Units.VolumeUnit.OilBarrel
        stub_net_project.ProjectUnits.SlurryRateUnit.Item2 = UnitsNet.Units.DurationUnit.Minute

    def set_proppant_concentration_lb_gal_unit():
        stub_net_project.ProjectUnits.ProppantConcentrationUnit.Item1 = UnitsNet.Units.MassUnit.Pound
        stub_net_project.ProjectUnits.ProppantConcentrationUnit.Item2 = UnitsNet.Units.VolumeUnit.UsGallon

    abbreviation_unit_map = {'ft': set_foot_length_unit,
                             'm': set_meter_length_unit,
                             'psi': set_pressure_psi_length_unit,
                             'kPa': set_pressure_kpa_length_unit,
                             'bbl/min': set_slurry_rate_bpm_unit,
                             'lb/gal (U.S.)': set_proppant_concentration_lb_gal_unit}

    if abbreviation in abbreviation_unit_map.keys():
        abbreviation_unit_map[abbreviation]()


def create_stub_net_project_abbreviation(well_names=None, well_display_names=None, well_uwis=None, eastings=None,
                                         northings=None, tvds=None, project_length_unit_abbreviation='',
                                         project_pressure_unit_abbreviation='', slurry_rate_unit_abbreviation='',
                                         proppant_concentration_unit_abbreviation=''):
    well_names = well_names if well_names else []
    well_display_names = well_display_names if well_display_names else []
    well_uwis = well_uwis if well_uwis else []
    eastings = eastings if eastings else []
    northings = northings if northings else []
    tvds = tvds if tvds else []

    stub_net_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
    set_project_unit(stub_net_project, project_length_unit_abbreviation)
    set_project_unit(stub_net_project, project_pressure_unit_abbreviation)
    set_project_unit(stub_net_project, slurry_rate_unit_abbreviation)
    set_project_unit(stub_net_project, proppant_concentration_unit_abbreviation)

    stub_net_project.Wells.Items = [unittest.mock.MagicMock(name=well_name, spec=IWell) for well_name in well_names]

    for i in range(len(well_names)):
        stub_well = stub_net_project.Wells.Items[i]
        stub_well.Uwi = well_uwis[i] if well_uwis else None
        stub_well.DisplayName = well_display_names[i] if well_display_names else None
        stub_well.Name = well_names[i]

        # The Pythonnet package has an open issue that the "Implicit Operator does not work from python"
        # (https://github.com/pythonnet/pythonnet/issues/253).
        #
        # One of the comments identifies a work-around from StackOverflow
        # (https://stackoverflow.com/questions/11544056/how-to-cast-implicitly-on-a-reflected-method-call/11563904).
        # This post states that "the trick is to realize that the compiler creates a special static method
        # called `op_Implicit` for your implicit conversion operator."
        stub_well.Trajectory.GetEastingArray.return_value = quantity_coordinate(eastings, i, stub_net_project)
        stub_well.Trajectory.GetNorthingArray.return_value = quantity_coordinate(northings, i, stub_net_project)
        stub_well.Trajectory.GetTvdArray.return_value = quantity_coordinate(tvds, i, stub_net_project)

    return stub_net_project


def quantity_coordinate(raw_coordinates, i, stub_net_project):
    result = [UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(c), stub_net_project.ProjectUnits.LengthUnit)
              for c in raw_coordinates[i]] if raw_coordinates else []
    return result


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = ProjectAdapter(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
