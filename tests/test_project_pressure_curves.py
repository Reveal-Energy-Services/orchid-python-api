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

import datetime
import itertools
import unittest.mock

import deal
from hamcrest import assert_that, is_, equal_to, calling, raises, has_length, contains_exactly, empty
import pandas as pd

from orchid.project_pressure_curves import ProjectPressureCurves
from orchid.project_loader import ProjectLoader

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
from tests.stub_net import StubNetSample

clr.AddReference('System')
# noinspection PyUnresolvedReferences
from System import DateTime

clr.AddReference('ImageFrac.FractureDiagnostics')
# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics import IProject, IWellSampledQuantityTimeSeries

clr.AddReference('UnitsNet')
# noinspection PyUnresolvedReferences
import UnitsNet


class ProjectPressureCurvesTest(unittest.TestCase):
    @staticmethod
    def test_canary():
        assert_that(2 + 2, is_(equal_to(4)))

    @staticmethod
    def test_ctor_no_project_loader_raises_exception():
        assert_that(calling(ProjectPressureCurves).with_args(None), raises(deal.PreContractError))

    @staticmethod
    def test_all_pressure_curves_returns_empty_if_no_pressure_curves():
        stub_loader = unittest.mock.MagicMock(name='stub_loader', spec=ProjectLoader)
        sut = ProjectPressureCurves(stub_loader)

        # noinspection PyTypeChecker
        assert_that(sut.pressure_curve_ids(), has_length(0))

    @staticmethod
    def test_all_pressure_curves_returns_empty_if_only_temperature_curves():
        stub_net_project = create_stub_net_project(curve_names=['oppugnavi'],
                                                   curves_physical_quantities=['temperature'])
        sut = create_sut(stub_net_project)

        # noinspection PyTypeChecker
        assert_that(sut.pressure_curve_ids(), has_length(0))

    @staticmethod
    def test_all_pressure_curves_returns_one_id_if_one_pressure_curves():
        stub_net_project = create_stub_net_project(curve_names=['oppugnavi'])
        sut = create_sut(stub_net_project)

        assert_that(sut.pressure_curve_ids(), contains_exactly('oppugnavi'))

    @staticmethod
    def test_many_pressure_curves_ids_for_project_with_many_pressure_curves():
        pressure_curve_names = ['iris', 'convenes', 'commune']
        stub_net_project = create_stub_net_project(curve_names=pressure_curve_names)
        sut = create_sut(stub_net_project)

        # noinspection PyTypeChecker
        # Unpack `expected_well_ids` because `contains_exactly` expects multiple items not a list
        assert_that(sut.pressure_curve_ids(), contains_exactly(*pressure_curve_names))

    def test_two_pressure_curves_ids_for_project_with_three_curves_but_only_two_pressure(self):
        pressure_curve_names = ['iris', 'convenes', 'commune']
        curves_physical_quantities = ['pressure', 'temperature', 'pressure']
        stub_net_project = create_stub_net_project(curve_names=pressure_curve_names,
                                                   curves_physical_quantities=curves_physical_quantities)
        sut = create_sut(stub_net_project)

        self.assertEqual(sut.pressure_curve_ids(), ['iris', 'commune'])

    @staticmethod
    def test_no_samples_for_project_with_one_pressure_curve_but_no_samples():
        stub_net_project = create_stub_net_project(curve_names=['oppugnavi'], samples=[[]])
        sut = create_sut(stub_net_project)

        # noinspection PyTypeChecker
        assert_that(sut.pressure_curve_samples('oppugnavi'), is_(empty()))

    @staticmethod
    def test_one_sample_for_project_with_one_sample():
        stub_net_project = create_stub_net_project(curve_names=['oppugnavi'],
                                                   samples=[[StubNetSample(datetime.datetime(2016, 7, 17, 15, 31, 58),
                                                                           0.10456)]],
                                                   project_pressure_unit_abbreviation='MPa')
        sut = create_sut(stub_net_project)

        expected_series = pd.Series(data=[0.10456], index=[datetime.datetime(2016, 7, 17, 15, 31, 58)])
        pd.testing.assert_series_equal(sut.pressure_curve_samples('oppugnavi'), expected_series)

    @staticmethod
    def test_many_samples_for_project_with_many_samples():
        curve_names = ['iris', 'convenes', 'commune']
        start_times = [datetime.datetime(2017, 3, 8, 4, 32, 25), datetime.datetime(2017, 3, 8, 18, 33, 39),
                       datetime.datetime(2017, 3, 9, 13, 23, 47)]
        sample_values = [[14.85, 14.53, 15.32], [27.21, 27.13, 27.05], [26.97, 26.89, 26.80]]
        sample_times = [[start_times[i] + j * datetime.timedelta(seconds=30) for j in range(len(sample_values[i]))] for
                        i in range(len(sample_values))]
        sample_parameters = [zip(sample_times[i], sample_values[i]) for i in range(len(start_times))]
        samples = [[StubNetSample(*sps) for sps in list(sample_parameters[i])] for i in range(len(sample_parameters))]
        stub_net_project = \
            create_stub_net_project(curve_names=curve_names,
                                    samples=samples,
                                    project_pressure_unit_abbreviation='psi')
        sut = create_sut(stub_net_project)

        for i in range(len(curve_names)):
            expected_series = pd.Series(sample_values[i], sample_times[i])
            pd.testing.assert_series_equal(sut.pressure_curve_samples(curve_names[i]), expected_series)

    def test_pressure_curve_samples_with_invalid_curve_name_raises_exception(self):
        stub_net_project = create_stub_net_project(curve_names=['oppugnavi'], samples=[[]])
        sut = create_sut(stub_net_project)

        # Using self.subTest as a context manager to parameterize a unit test. Note that the
        # test count treats this as a single test; however, failures are reported as a
        # "SubTest Error" with detail listing the specific failure(s).
        for invalid_curve_id in [None, '', '\v']:
            with self.subTest(invalid_curve_name=invalid_curve_id):
                self.assertRaises(deal.PreContractError, sut.pressure_curve_samples, invalid_curve_id)

    @staticmethod
    def test_one_curve_display_name_for_project_with_one_pressure_curve():
        stub_net_project = create_stub_net_project(curve_names=['oppugnavi'], samples=[[]])
        sut = create_sut(stub_net_project)

        # noinspection PyTypeChecker
        assert_that(sut.display_name('oppugnavi'), equal_to('oppugnavi'))

    def test_display_name_with_invalid_curve_id_raises_exception(self):
        stub_net_project = create_stub_net_project(curve_names=['oppugnavi'], samples=[[]])
        sut = create_sut(stub_net_project)

        # Using self.subTest as a context manager to parameterize a unit test. Note that the
        # test count treats this as a single test; however, failures are reported as a
        # "SubTest Error" with detail listing the specific failure(s).
        for invalid_curve_id in [None, '', '\v']:
            with self.subTest(invalid_curve_name=invalid_curve_id):
                self.assertRaises(deal.PreContractError, sut.display_name, invalid_curve_id)


def create_stub_net_project(curve_names=None, samples=None, curves_physical_quantities=None,
                            project_pressure_unit_abbreviation=''):
    curve_names = curve_names if curve_names else []
    samples = samples if samples else []
    curves_physical_quantities = (curves_physical_quantities
                                  if curves_physical_quantities
                                  else list(itertools.repeat('pressure', len(curve_names))))

    stub_net_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
    if project_pressure_unit_abbreviation == 'psi':
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.PoundForcePerSquareInch
    elif project_pressure_unit_abbreviation == 'kPa':
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.Kilopascal
    elif project_pressure_unit_abbreviation == 'MPa':
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.Megapascal

    stub_net_project.WellTimeSeriesList.Items = \
        [unittest.mock.MagicMock(name=curve_name, spec=IWellSampledQuantityTimeSeries)
         for curve_name in curve_names]
    quantity_name_type_map = {'pressure': UnitsNet.QuantityType.Pressure,
                              'temperature': UnitsNet.QuantityType.Temperature}
    for i in range(len(curve_names)):
        stub_curve = stub_net_project.WellTimeSeriesList.Items[i]
        stub_curve.DisplayName = curve_names[i] if curve_names else None
        stub_curve.SampledQuantityType = quantity_name_type_map[curves_physical_quantities[i]]
        stub_curve.GetOrderedTimeSeriesHistory.return_value = samples[i] if len(samples) > 0 else []
    return stub_net_project


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.loaded_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = ProjectPressureCurves(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
