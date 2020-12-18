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
import datetime
import unittest.mock

from hamcrest import assert_that, equal_to

from orchid import (measurement as om,
                    project_loader as loader,
                    native_stage_adapter as nsa,
                    native_treatment_calculations as ntc,
                    net_quantity as onq,
                    unit_system as units)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import ITreatmentCalculations
# noinspection PyUnresolvedReferences,PyPackageRequirements
import UnitsNet

from tests import custom_matchers as tcm


DONT_CARE_MEASUREMENT_MAGNITUDE = float('NaN')
DONT_CARE_WARNINGS = []


# A stub concrete class implementing the same methods as .NET `ICalculationsResult`
NetCalculationResult = namedtuple('NetCalculationResult', ['Result', 'Warnings'])


class TestNativeTreatmentCalculationsAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_median_treating_pressure_returns_get_median_treating_pressure_result(self):
        for expected_magnitude, unit in [(7396.93, units.UsOilfield.PRESSURE), (74.19, units.Metric.PRESSURE)]:
            expected_measurement = om.make_measurement(expected_magnitude, unit)
            warnings = []
            net_pressure_calc_result = NetCalculationResult(onq.as_net_quantity(expected_measurement), warnings)
            stub_get_treatment_pressure = unittest.mock.MagicMock(name='get_treatment_pressure',
                                                                  return_value=net_pressure_calc_result)
            stub_treatment_calculations = unittest.mock.MagicMock(name='treatment_calculations',
                                                                  spec=ITreatmentCalculations)
            stub_treatment_calculations.GetMedianTreatmentPressure = stub_get_treatment_pressure
            with unittest.mock.patch('orchid.native_treatment_calculations.loader.native_treatment_calculations',
                                     spec=loader.native_treatment_calculations,
                                     return_value=stub_treatment_calculations):
                with self.subTest(expected_measurement=expected_measurement):
                    assert_expected_result(ntc.median_treating_pressure,
                                           datetime.datetime(2023, 7, 2, 3, 57, 19),
                                           datetime.datetime(2023, 7, 2, 5, 30, 2),
                                           expected_measurement=expected_measurement)

    def test_median_treating_pressure_returns_get_median_treating_pressure_warnings(self):
        for expected_warnings in [[], ['lente vetustas lupam vicit'], ['clunis', 'nobile', 'complacuit']]:
            net_pressure_calculation_result = NetCalculationResult(
                onq.as_net_quantity(om.make_measurement(DONT_CARE_MEASUREMENT_MAGNITUDE,
                                                        units.UsOilfield.PRESSURE)), expected_warnings)
            stub_get_treatment_pressure = unittest.mock.MagicMock(name='get_pumped_volume',
                                                                  return_value=net_pressure_calculation_result)
            stub_treatment_calculations = unittest.mock.MagicMock(name='treatment_calculations',
                                                                  spec=ITreatmentCalculations)
            stub_treatment_calculations.GetMedianTreatmentPressure = stub_get_treatment_pressure
            with unittest.mock.patch('orchid.native_treatment_calculations.loader.native_treatment_calculations',
                                     spec=loader.native_treatment_calculations,
                                     return_value=stub_treatment_calculations):
                with self.subTest(expected_warnings=expected_warnings):
                    assert_expected_result(ntc.median_treating_pressure,
                                           datetime.datetime(2023, 7, 2, 3, 57, 19),
                                           datetime.datetime(2023, 7, 2, 5, 30, 2),
                                           expected_warnings=expected_warnings)

    def test_pumped_fluid_volume_returns_get_pumped_volume_result(self):
        for volume_magnitude, unit in [(6269.20, units.UsOilfield.VOLUME), (707.82, units.Metric.VOLUME)]:
            expected_measurement = om.make_measurement(volume_magnitude, unit)
            net_volume_calculation_result = NetCalculationResult(onq.as_net_quantity(expected_measurement), [])
            stub_get_pumped_volume = unittest.mock.MagicMock(name='get_pumped_volume',
                                                             return_value=net_volume_calculation_result)
            stub_treatment_calculations = unittest.mock.MagicMock(name='treatment_calculations',
                                                                  spec=ITreatmentCalculations)
            stub_treatment_calculations.GetPumpedVolume = stub_get_pumped_volume
            with unittest.mock.patch('orchid.native_treatment_calculations.loader.native_treatment_calculations',
                                     spec=loader.native_treatment_calculations,
                                     return_value=stub_treatment_calculations):
                with self.subTest(expected_measurement=expected_measurement):
                    assert_expected_result(ntc.pumped_fluid_volume,
                                           datetime.datetime(2023, 8, 6, 3, 52, 4),
                                           datetime.datetime(2023, 8, 6, 5, 8, 20),
                                           expected_measurement=expected_measurement)

    def test_pumped_fluid_volume_returns_get_pumped_volume_warnings(self):
        for expected_warnings in [['urinator egregrius'], ['nomenclatura', 'gestus', 'tertia'], []]:
            net_volume_calculation_result = NetCalculationResult(
                onq.as_net_quantity(om.make_measurement(DONT_CARE_MEASUREMENT_MAGNITUDE,
                                                        units.UsOilfield.VOLUME)), expected_warnings)
            stub_get_pumped_volume = unittest.mock.MagicMock(name='get_pumped_volume',
                                                             return_value=net_volume_calculation_result)
            stub_treatment_calculations = unittest.mock.MagicMock(name='treatment_calculations',
                                                                  spec=ITreatmentCalculations)
            stub_treatment_calculations.GetPumpedVolume = stub_get_pumped_volume
            with unittest.mock.patch('orchid.native_treatment_calculations.loader.native_treatment_calculations',
                                     spec=loader.native_treatment_calculations,
                                     return_value=stub_treatment_calculations):
                with self.subTest(expected_warnings=expected_warnings):
                    assert_expected_result(ntc.pumped_fluid_volume,
                                           datetime.datetime(2023, 8, 6, 3, 52, 4),
                                           datetime.datetime(2023, 8, 6, 5, 8, 20),
                                           expected_warnings=expected_warnings)

    def test_total_proppant_mass_returns_get_total_proppant_mass_result(self):
        for mass_magnitude, unit in [(5414.58, units.UsOilfield.MASS), (138262.86, units.Metric.MASS)]:
            expected_measurement = om.make_measurement(mass_magnitude, unit)
            net_mass_calculation_result = NetCalculationResult(onq.as_net_quantity(expected_measurement), [])
            stub_get_proppant_mass = unittest.mock.MagicMock(name='get_proppant_mass',
                                                             return_value=net_mass_calculation_result)
            stub_treatment_calculations = unittest.mock.MagicMock(name='treatment_calculations',
                                                                  spec=ITreatmentCalculations)
            stub_treatment_calculations.GetTotalProppantMass = stub_get_proppant_mass
            with unittest.mock.patch('orchid.native_treatment_calculations.loader.native_treatment_calculations',
                                     spec=loader.native_treatment_calculations,
                                     return_value=stub_treatment_calculations):
                with self.subTest(expected_measurement=expected_measurement):
                    assert_expected_result(ntc.total_proppant_mass,
                                           datetime.datetime(2020, 1, 29, 7, 35, 2),
                                           datetime.datetime(2020, 1, 29, 9, 13, 30),
                                           expected_measurement=expected_measurement)

    def test_total_proppant_mass_returns_get_total_proppant_mass_warnings(self):
        for expected_warnings in [[],  ['igitur', 'pantinam', 'incidi'], ['violentia venio']]:
            net_mass_calculation_result = NetCalculationResult(
                onq.as_net_quantity(om.make_measurement(DONT_CARE_MEASUREMENT_MAGNITUDE,
                                                        units.UsOilfield.MASS)), expected_warnings)
            stub_get_proppant_mass = unittest.mock.MagicMock(name='get_proppant_mass',
                                                             return_value=net_mass_calculation_result)
            stub_treatment_calculations = unittest.mock.MagicMock(name='treatment_calculations',
                                                                  spec=ITreatmentCalculations)
            stub_treatment_calculations.GetTotalProppantMass = stub_get_proppant_mass
            with unittest.mock.patch('orchid.native_treatment_calculations.loader.native_treatment_calculations',
                                     spec=loader.native_treatment_calculations,
                                     return_value=stub_treatment_calculations):
                with self.subTest(expected_warnings=expected_warnings):
                    assert_expected_result(ntc.total_proppant_mass,
                                           datetime.datetime(2020, 1, 29, 7, 35, 2),
                                           datetime.datetime(2020, 1, 29, 9, 13, 30),
                                           expected_warnings=expected_warnings)


def create_stub_stage_adapter():
    result = unittest.mock.Mock('stub_stage_adapter', autospec=nsa.NativeStageAdapter)
    result.dom_object = unittest.mock.Mock('mock_dom_object')
    return result


def create_stub_calculation(expected_measurement, warnings):
    net_calculation_result = NetCalculationResult(onq.as_net_quantity(expected_measurement), warnings)
    stub_calculation = unittest.mock.MagicMock(name='stub_calculation', return_value=net_calculation_result)
    return stub_calculation


def assert_expected_result(sut, start_time, stop_time, expected_measurement=None, expected_warnings=None):
    actual_result = sut(create_stub_stage_adapter(), start_time, stop_time)
    if expected_measurement is not None:
        tcm.assert_that_scalar_quantities_close_to(actual_result.measurement, expected_measurement,
                                                   tolerance=6e-3)
    if expected_warnings is not None:
        assert_that(expected_warnings, equal_to(actual_result.warnings))


if __name__ == '__main__':
    unittest.main()
