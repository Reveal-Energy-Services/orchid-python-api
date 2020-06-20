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

from hamcrest import assert_that, equal_to

from orchid.native_treatment_curve_facade import NativeTreatmentCurveFacade
from tests.stub_net import create_stub_net_project

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IProject, IStageSampledQuantityTimeSeries
# noinspection PyUnresolvedReferences
import UnitsNet


class TestTreatmentCurveFacade(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name_from_treatment_curve(self):
        stub_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                       spec=IStageSampledQuantityTimeSeries)
        stub_treatment_curve.DisplayName = 'boni'
        sut = NativeTreatmentCurveFacade(stub_treatment_curve)

        assert_that(sut.display_name(), equal_to('boni'))

    def test_sampled_quantity_name_from_treatment_curve(self):
        stub_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                       spec=IStageSampledQuantityTimeSeries)
        stub_treatment_curve.SampledQuantityName = 'proponeam'
        sut = NativeTreatmentCurveFacade(stub_treatment_curve)

        assert_that(sut.sampled_quantity_name(), equal_to('proponeam'))

    def test_sampled_quantity_unit_returns_pressure_if_pressure_samples(self):
        stub_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                       spec=IStageSampledQuantityTimeSeries)
        stub_treatment_curve.SampledQuantityName = 'Pressure'
        stub_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
        stub_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.Kilopascal
        stub_treatment_curve.Stage.Well.Project = stub_project
        sut = NativeTreatmentCurveFacade(stub_treatment_curve)

        assert_that(sut.sampled_quantity_unit(), equal_to('kPa'))

    def test_sampled_quantity_unit_returns_slurry_rate_if_slurry_rate_samples(self):
        stub_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                       spec=IStageSampledQuantityTimeSeries)
        stub_treatment_curve.SampledQuantityName = 'Slurry Rate'
        for (unit, expected) in zip(('bbl/min', 'm^3/min'), ('bbl/min', 'm\u00b3/min')):
            stub_project = create_stub_net_project(slurry_rate_unit_abbreviation=unit)
            with self.subTest(expected=expected):
                stub_treatment_curve.Stage.Well.Project = stub_project
                sut = NativeTreatmentCurveFacade(stub_treatment_curve)

                assert_that(sut.sampled_quantity_unit(), equal_to(expected))

    def test_sampled_quantity_unit_returns_proppant_concentration_if_proppant_concentration_samples(self):
        stub_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                       spec=IStageSampledQuantityTimeSeries)
        stub_treatment_curve.SampledQuantityName = 'Proppant Concentration'
        for (unit, expected) in zip(('lb/gal (U.S.)', 'kg/m^3'), ('lb/gal (U.S.)', 'kg/m\u00b3')):
            stub_project = create_stub_net_project(proppant_concentration_unit_abbreviation=unit)
            with self.subTest(expected=expected):
                stub_treatment_curve.Stage.Well.Project = stub_project
                sut = NativeTreatmentCurveFacade(stub_treatment_curve)

                assert_that(sut.sampled_quantity_unit(), equal_to(expected))


if __name__ == '__main__':
    unittest.main()
