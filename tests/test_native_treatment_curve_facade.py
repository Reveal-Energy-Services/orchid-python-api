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
from hamcrest import assert_that, equal_to, is_, contains_exactly

from orchid.native_treatment_curve_facade import NativeTreatmentCurveFacade
from orchid.net_quantity import as_net_date_time
from tests.stub_net import create_stub_net_project

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IProject, IStageSampledQuantityTimeSeries
# noinspection PyUnresolvedReferences
import UnitsNet


StubSample = namedtuple('StubSample', ['Timestamp', 'Value'], module=__name__)


class TestTreatmentCurveFacade(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name_from_treatment_curve(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.DisplayName = 'boni'
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

    def test_name_from_treatment_curve(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.Name = 'magnitudina'
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

        assert_that(sut.name(), equal_to('magnitudina'))

    def test_sampled_quantity_name_from_treatment_curve(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.SampledQuantityName = 'proponeam'
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

        assert_that(sut.sampled_quantity_name(), equal_to('proponeam'))

    def test_sampled_quantity_unit_returns_pressure_if_pressure_samples(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.SampledQuantityName = 'Pressure'
        stub_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
        stub_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.Kilopascal
        stub_net_treatment_curve.Stage.Well.Project = stub_project
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

        assert_that(sut.sampled_quantity_unit(), equal_to('kPa'))

    def test_sampled_quantity_unit_returns_slurry_rate_if_slurry_rate_samples(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.SampledQuantityName = 'Slurry Rate'
        for (unit, expected) in zip(('bbl/min', 'm^3/min'), ('bbl/min', 'm\u00b3/min')):
            stub_project = create_stub_net_project(slurry_rate_unit_abbreviation=unit)
            with self.subTest(expected=expected):
                stub_net_treatment_curve.Stage.Well.Project = stub_project
                sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

                assert_that(sut.sampled_quantity_unit(), equal_to(expected))

    def test_sampled_quantity_unit_returns_proppant_concentration_if_proppant_concentration_samples(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.SampledQuantityName = 'Proppant Concentration'
        for (unit, expected) in zip(('lb/gal (U.S.)', 'kg/m^3'), ('lb/gal (U.S.)', 'kg/m\u00b3')):
            stub_project = create_stub_net_project(proppant_concentration_unit_abbreviation=unit)
            with self.subTest(expected=expected):
                stub_net_treatment_curve.Stage.Well.Project = stub_project
                sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

                assert_that(sut.sampled_quantity_unit(), equal_to(expected))

    def test_suffix_from_treatment_curve(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.Suffix = 'hominibus'
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

        assert_that(sut.suffix(), equal_to('hominibus'))

    def test_empty_time_series_from_curve_with_no_samples(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.Name = 'palmis'
        stub_net_treatment_curve.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(name='stub_time_series',
                                                                                       return_value=[])
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

        expected = pd.Series(data=[], index=[], name='palmis', dtype=np.float64)
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_single_sample_time_series_from_curve_with_single_samples(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.Name = 'palmis'
        values = [671.09]
        start_time_point = datetime(2016, 2, 9, 4, 50, 39, 340000)
        time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(values))]
        samples = [StubSample(t, v) for (t, v) in zip(map(as_net_date_time, time_points), values)]
        stub_net_treatment_curve.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(name='stub_time_series',
                                                                                       return_value=samples)
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

        expected = pd.Series(data=values, index=time_points, name='palmis')
        pdt.assert_series_equal(sut.time_series(), expected)

    def test_many_samples_time_series_from_curve_with_many_sampless(self):
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
        stub_net_treatment_curve.Name = 'palmis'
        values = [331.10, 207.70, 272.08]
        start_time_point = datetime(2018, 12, 8, 18, 18, 35, 264000)
        time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(values))]
        samples = [StubSample(t, v) for (t, v) in zip(map(as_net_date_time, time_points), values)]
        stub_net_treatment_curve.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(name='stub_time_series',
                                                                                       return_value=samples)
        sut = NativeTreatmentCurveFacade(stub_net_treatment_curve)

        expected = pd.Series(data=values, index=time_points, name='palmis')
        pdt.assert_series_equal(sut.time_series(), expected)


if __name__ == '__main__':
    unittest.main()
