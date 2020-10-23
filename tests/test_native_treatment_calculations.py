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

import datetime
import unittest.mock

from hamcrest import assert_that, equal_to

import orchid.measurement as om
import orchid.native_stage_adapter as nsa
import orchid.native_treatment_calculations as ntc
import orchid.unit_system as units

import tests.custom_matchers as tcm

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import ITreatmentCalculations, IFractureDiagnosticsCalculationsFactory
# noinspection PyUnresolvedReferences,PyPackageRequirements
import UnitsNet


class TestNativeTreatmentCalculationsAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_median_treating_pressure_returns_get_median_treating_pressure_result(self):
        stub_native_treatment_calculations = unittest.mock.MagicMock(name='stub_calculations',
                                                                     autospec=ITreatmentCalculations)
        stub_native_calculations_factory = unittest.mock.MagicMock(name='stub_calculations_factory',
                                                                   autospec=IFractureDiagnosticsCalculationsFactory)
        stub_native_calculations_factory.TreatmentCalculations = unittest.mock.MagicMock(
            return_value=stub_native_treatment_calculations)

        stub_stage = unittest.mock.Mock('stub_stage_adapter', autospec=nsa.NativeStageAdapter)
        start_time = datetime.datetime(2023, 7, 2, 3, 57, 19)
        stop_time = datetime.datetime(2023, 7, 2, 5, 30, 2)
        for expected_magnitude, unit in \
                [(7396.93, units.UsOilfield.PRESSURE),
                 (74.19, units.Metric.PRESSURE)]:
            expected_measurement = om.make_measurement(expected_magnitude, unit.abbreviation)
            net_pressure = UnitsNet.Pressure.From(UnitsNet.QuantityValue.op_Implicit(expected_magnitude),
                                                  unit.net_unit)
            stub_native_calculation_result = unittest.mock.MagicMock(name='stub_calculation_result')
            stub_native_calculation_result.Result = net_pressure
            stub_native_treatment_calculations.GetMedianTreatmentPressure = unittest.mock.MagicMock(
                return_value=stub_native_calculation_result)
            with self.subTest(expected_measurement=expected_measurement):
                actual_result = ntc.median_treating_pressure(stub_stage, start_time, stop_time,
                                                             calculations_factory=stub_native_calculations_factory)
                tcm.assert_that_scalar_quantities_close_to(actual_result.measurement, expected_measurement,
                                                           tolerance=6e-3)

    def test_median_treating_pressure_returns_get_median_treating_pressure_warnings(self):
        stub_native_treatment_calculations = unittest.mock.MagicMock(name='stub_calculations',
                                                                     autospec=ITreatmentCalculations)
        stub_native_calculations_factory = unittest.mock.MagicMock(name='stub_calculations_factory',
                                                                   autospec=IFractureDiagnosticsCalculationsFactory)
        stub_native_calculations_factory.TreatmentCalculations = unittest.mock.MagicMock(
            return_value=stub_native_treatment_calculations)

        stub_stage = unittest.mock.Mock('stub_stage_adapter', autospec=nsa.NativeStageAdapter)
        start_time = datetime.datetime(2023, 7, 2, 3, 57, 19)
        stop_time = datetime.datetime(2023, 7, 2, 5, 30, 2)
        for expected_warnings in [[], ['lente vetustas lupam vicit'], ['clunis', 'nobile', 'complacuit']]:
            stub_native_calculation_result = unittest.mock.MagicMock(name='stub_calculation_result')
            stub_native_calculation_result.Result = UnitsNet.Pressure.From(
                UnitsNet.QuantityValue.op_Implicit(61.95835749857516), units.Metric.PRESSURE.net_unit)
            stub_native_calculation_result.Warnings = expected_warnings
            stub_native_treatment_calculations.GetMedianTreatmentPressure = unittest.mock.MagicMock(
                return_value=stub_native_calculation_result)
            with self.subTest(expected_warnings=expected_warnings):
                actual_result = ntc.median_treating_pressure(stub_stage, start_time, stop_time,
                                                             calculations_factory=stub_native_calculations_factory)
                assert_that(expected_warnings, equal_to(actual_result.warnings))


if __name__ == '__main__':
    unittest.main()
