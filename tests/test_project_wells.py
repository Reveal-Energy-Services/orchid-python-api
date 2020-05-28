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
import numpy.testing as npt
import vectormath as vmath

from orchid.project_wells import ProjectWells
from orchid.project_loader import ProjectLoader

# TODO: Replace some of this code with configuration and/or a method to use `clr.AddReference`
import sys
import clr
IMAGE_FRAC_ASSEMBLIES_DIR = r'c:/src/OrchidApp/ImageFrac/ImageFrac.Application/bin/Debug'
if IMAGE_FRAC_ASSEMBLIES_DIR not in sys.path:
    sys.path.append(IMAGE_FRAC_ASSEMBLIES_DIR)

clr.AddReference('ImageFrac.FractureDiagnostics')
# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics import IProject, IWell, IStage

clr.AddReference('UnitsNet')
# noinspection PyUnresolvedReferences
import UnitsNet


class TestProjectWells(unittest.TestCase):
    # Test ideas:
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

    def test_no_trajectory_points_for_project_with_one_well_but_empty_trajectory(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'], eastings=[], northings=[], tvds=[])
        sut = create_sut(stub_net_project)

        assert_that(sut.trajectory_points('dont-care-well'), is_(empty()))

    def test_one_trajectory_point_for_well_with_one_trajectory_point(self):
        stub_net_project = create_stub_net_project(project_length_unit_abbreviation='m', well_names=['dont-care-well'],
                                                   eastings=[[185939]], northings=[[280875]], tvds=[[2250]])
        sut = create_sut(stub_net_project)

        npt.assert_allclose(sut.trajectory_points('dont-care-well'),
                            vmath.Vector3Array(vmath.Vector3(185939, 280875, 2250)))

    def test_many_trajectory_points_for_well_with_many_trajectory_points(self):
        stub_net_project = create_stub_net_project(project_length_unit_abbreviation='ft', well_names=['dont-care-well'],
                                                   eastings=[[768385, 768359, 768331]],
                                                   northings=[[8320613, 8320703, 8320792]], tvds=[[7515, 7516, 7517]])
        sut = create_sut(stub_net_project)

        npt.assert_allclose(sut.trajectory_points('dont-care-well'),
                            vmath.Vector3Array([[768385, 8320613, 7515], [768359, 8320703, 7516],
                                                [768331, 8320792, 7517]]))

    def test_trajectory_points_invalid_well_id_raises_exception(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'], eastings=[], northings=[], tvds=[])
        sut = create_sut(stub_net_project)

        for invalid_well_id in [None, '', '\t']:
            with self.subTest(invalid_well_id=invalid_well_id):
                self.assertRaises(deal.PreContractError, sut.trajectory_points, invalid_well_id)

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

    def test_treatment_curves_invalid_well_name_raises_exception(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        for invalid_well_name in [None, '', '\t']:
            with self.subTest(invalid_well_name=invalid_well_name):
                self.assertRaises(deal.PreContractError, sut.treatment_curves, invalid_well_name, 40)

    def test_treatment_curves_stage_no_zero_raises_exception(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        assert_that(calling(sut.treatment_curves).with_args('clavis', 0), raises(deal.PreContractError))

    def test_treatment_curves_well_name_not_found(self):
        stub_net_project = create_stub_net_project(well_names=['perditus'])
        sut = create_sut(stub_net_project)

        assert_that(calling(sut.treatment_curves).with_args('perditum', 40), raises(ValueError, 'perditum'))

    def test_treatment_curves_many_well_names_not_found(self):
        stub_net_project = create_stub_net_project(well_names=['perditus', 'perditus'],
                                                   uwis=['13-747-7053-70-64', '10-815-48659-44-52'])
        sut = create_sut(stub_net_project)

        assert_that(calling(sut.treatment_curves).with_args('perditus', 40), raises(ValueError, 'perditus'))

    def test_treatment_curves_stage_number_greater_than_number_of_stages(self):
        stub_net_project = create_stub_net_project(well_names=['perditus'], about_stages=[('corem', [])])
        sut = create_sut(stub_net_project)

        assert_that(calling(sut.treatment_curves).with_args('perditus', 40), raises(ValueError, '40'))

    def test_treatment_curves_returns_empty_when_stage_has_no_treatment_curves(self):
        stub_net_project = create_stub_net_project(well_names=['perditus'], about_stages=[('corem', [])])
        sut = create_sut(stub_net_project)

        assert_that(calling(sut.treatment_curves).with_args('perditus', 40), raises(ValueError, '40'))

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


def create_stub_stage(stage_name, treatment_curves):
    result = unittest.mock.MagicMock(name=stage_name, spec=IStage)
    result.get_DisplayStageNumber.return_value = stage_name
    result.TreatmentCurves = treatment_curves

    return result


def create_stub_net_project(project_length_unit_abbreviation='', well_names=None, well_display_names=None, uwis=None,
                            eastings=None, northings=None, tvds=None, about_stages=None):
    well_names = well_names if well_names else []
    well_display_names = well_display_names if well_display_names else []
    uwis = uwis if uwis else []
    eastings = eastings if eastings else []
    northings = northings if northings else []
    tvds = tvds if tvds else []
    about_stages = about_stages if about_stages else []

    stub_net_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
    if project_length_unit_abbreviation == 'ft':
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Foot
    elif project_length_unit_abbreviation == 'm':
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Meter

    stub_net_project.Wells.Items = [unittest.mock.MagicMock(name=well_name, spec=IWell) for well_name in well_names]

    for i in range(len(well_names)):
        stub_well = stub_net_project.Wells.Items[i]
        stub_well.Uwi = uwis[i] if uwis else None
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

        stub_well.Stages.get_Items.return_value = [create_stub_stage(stage_name, treatment_curve)
                                                   for (stage_name, treatment_curve) in about_stages]

    return stub_net_project


def quantity_coordinate(raw_coordinates, i, stub_net_project):
    result = [UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(c), stub_net_project.ProjectUnits.LengthUnit)
              for c in raw_coordinates[i]] if raw_coordinates else []
    return result


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = ProjectWells(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
