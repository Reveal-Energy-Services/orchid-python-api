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

from collections import namedtuple
from datetime import datetime, timedelta
import unittest.mock

import numpy as np
import pandas as pd
import pandas.testing as pdt
from hamcrest import assert_that, equal_to

import orchid.native_treatment_curve_facade as ontc
from orchid.net_quantity import as_net_date_time
from tests.stub_net import create_stub_net_project

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IProject, IStageSampledQuantityTimeSeries
# noinspection PyUnresolvedReferences
import UnitsNet


class TestTreatmentCurveFacade(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name_from_treatment_curve(self):
        sut = create_sut(display_name='boni')

        assert_that(sut.display_name, equal_to('boni'))

    def test_name_from_treatment_curve(self):
        sut = create_sut(name='magnitudina')

        assert_that(sut.name, equal_to('magnitudina'))

    def test_sampled_quantity_name_from_treatment_curve(self):
        sut = create_sut(sampled_quantity_name='proponeam')

        assert_that(sut.sampled_quantity_name, equal_to('proponeam'))

    def test_sampled_quantity_unit_returns_pressure_if_pressure_samples(self):
        for (unit, expected) in zip(('psi', 'kPa', 'MPa'), ('psi', 'kPa', 'MPa')):
            stub_project = create_stub_net_project(project_pressure_unit_abbreviation=unit)
            sut = create_sut(sampled_quantity_name=ontc.TREATING_PRESSURE, project=stub_project)
            with self.subTest(expected=expected):
                assert_that(sut.sampled_quantity_unit(), equal_to(expected))

    def test_sampled_quantity_unit_returns_slurry_rate_if_slurry_rate_samples(self):
        for (unit, expected) in zip(('bbl/min', 'm^3/min'), ('bbl/min', 'm\u00b3/min')):
            stub_project = create_stub_net_project(slurry_rate_unit_abbreviation=unit)
            sut = create_sut(sampled_quantity_name=ontc.SLURRY_RATE, project=stub_project)
            with self.subTest(expected=expected):
                assert_that(sut.sampled_quantity_unit(), equal_to(expected))

    def test_sampled_quantity_unit_returns_proppant_concentration_if_proppant_concentration_samples(self):
        for (unit, expected) in zip(('lb/gal (U.S.)', 'kg/m^3'), ('lb/gal (U.S.)', 'kg/m\u00b3')):
            stub_project = create_stub_net_project(slurry_rate_unit_abbreviation=unit)
            sut = create_sut(sampled_quantity_name=ontc.PROPPANT_CONCENTRATION, project=stub_project)
            with self.subTest(expected=expected):
                assert_that(sut.sampled_quantity_unit(), equal_to(expected))

    def test_suffix_from_treatment_curve(self):
        sut = create_sut(suffix='hominibus')

        assert_that(sut.suffix, equal_to('hominibus'))

    def test_empty_time_series_from_curve_with_no_samples(self):
        values = []
        start_time_point = datetime(2017, 7, 2, 3, 29, 10, 510000)
        sut = create_sut(name='palmis', values=values, start_time_point=start_time_point)

        expected = pd.Series(data=[], index=[], name='palmis', dtype=np.float64)
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_single_sample_time_series_from_curve_with_single_samples(self):
        values = [671.09]
        start_time_point = datetime(2016, 2, 9, 4, 50, 39, 340000)
        sut = create_sut(name='palmis', values=values, start_time_point=start_time_point)

        expected_time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(values))]
        expected = pd.Series(data=values, index=expected_time_points, name='palmis')
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_many_samples_time_series_from_curve_with_many_samples(self):
        values = [331.10, 207.70, 272.08]
        start_time_point = datetime(2018, 12, 8, 18, 18, 35, 264000)
        sut = create_sut(name='palmis', values=values, start_time_point=start_time_point)

        expected_time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(values))]
        expected = pd.Series(data=values, index=expected_time_points, name='palmis')
        pdt.assert_series_equal(sut.time_series(), expected)


StubSample = namedtuple('StubSample', ['Timestamp', 'Value'], module=__name__)


def create_sut(name='', display_name='', sampled_quantity_name='', suffix='',
               values=None, start_time_point=None,
               project=None):
    stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                       spec=IStageSampledQuantityTimeSeries)
    stub_net_treatment_curve.Name = name
    stub_net_treatment_curve.DisplayName = display_name
    stub_net_treatment_curve.SampledQuantityName = sampled_quantity_name
    stub_net_treatment_curve.Suffix = suffix

    actual_values = values if values else []
    time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(actual_values))]
    samples = [StubSample(t, v) for (t, v) in zip(map(as_net_date_time, time_points), actual_values)]
    stub_net_treatment_curve.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(name='stub_time_series',
                                                                                   return_value=samples)

    stub_net_treatment_curve.Stage.Well.Project = project

    sut = ontc.NativeTreatmentCurveFacade(stub_net_treatment_curve)
    return sut


if __name__ == '__main__':
    unittest.main()
