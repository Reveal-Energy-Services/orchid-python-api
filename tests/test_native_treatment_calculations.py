#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
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

import dateutil.tz as duz
from hamcrest import assert_that, equal_to

from orchid import (
    project_loader as loader,
    native_stage_adapter as nsa,
    native_treatment_calculations as ntc,
    unit_system as units,
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import ITreatmentCalculations
# noinspection PyUnresolvedReferences,PyPackageRequirements
import UnitsNet

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)


DONT_CARE_MEASUREMENT_MAGNITUDE = float('NaN')
DONT_CARE_WARNINGS = []


# A stub concrete class implementing the same methods as .NET `ICalculationsResult`
NetCalculationResult = namedtuple('NetCalculationResult', ['Result', 'Warnings'])


class TestNativeTreatmentCalculationsAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_median_treating_pressure_returns_get_median_treating_pressure_result(self):
        for expected_measurement_dto in [
            tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 7396.93),
            tsn.make_measurement_dto(units.Metric.PRESSURE, 74.19),
        ]:
            stub_calculation_result = create_stub_calculation_result(expected_measurement_dto, DONT_CARE_WARNINGS)
            stub_treatment_calculations = create_stub_treatment_pressure_calculation(stub_calculation_result)

            expected_measurement = tsn.make_measurement(expected_measurement_dto)
            self.assert_expected_calculation_result(ntc.median_treating_pressure,
                                                    stub_treatment_calculations,
                                                    datetime.datetime(2023, 7, 2, 3, 57, 19, tzinfo=duz.UTC),
                                                    datetime.datetime(2023, 7, 2, 5, 30, 2, tzinfo=duz.UTC),
                                                    expected_measurement=expected_measurement)

    def assert_expected_calculation_result(self, sut, stub_treatment_calculations, start_time, stop_time,
                                           expected_measurement=None, expected_warnings=None):
        with unittest.mock.patch('orchid.native_treatment_calculations.loader.native_treatment_calculations',
                                 spec=loader.native_treatment_calculations,
                                 return_value=stub_treatment_calculations):
            with self.subTest(f'Test calculation result {expected_measurement if expected_measurement else ""}'
                              f'{"with warnings," if expected_warnings is not None else ""}'
                              f' {expected_warnings if expected_warnings is not None else ""}'):
                actual_result = sut(create_stub_stage_adapter(), start_time, stop_time)
                if expected_measurement is not None:
                    tcm.assert_that_measurements_close_to(actual_result.measurement, expected_measurement,
                                                          tolerance=6e-2)
                if expected_warnings is not None:
                    assert_that(expected_warnings, equal_to(actual_result.warnings))

    def test_median_treating_pressure_returns_get_median_treating_pressure_warnings(self):
        for expected_warnings in [[], ['lente vetustas lupam vicit'], ['clunis', 'nobile', 'complacuit']]:
            dont_care_measurement = tsn.make_measurement_dto(units.UsOilfield.PRESSURE,
                                                             DONT_CARE_MEASUREMENT_MAGNITUDE)

            stub_calculation_result = create_stub_calculation_result(dont_care_measurement, expected_warnings)
            stub_treatment_calculations = create_stub_treatment_pressure_calculation(stub_calculation_result)
            self.assert_expected_calculation_result(ntc.median_treating_pressure,
                                                    stub_treatment_calculations,
                                                    datetime.datetime(2023, 7, 2, 3, 57, 19, tzinfo=duz.UTC),
                                                    datetime.datetime(2023, 7, 2, 5, 30, 2, tzinfo=duz.UTC),
                                                    expected_warnings=expected_warnings)

    def test_pumped_fluid_volume_returns_get_pumped_volume_result(self):
        for expected_measurement_dto in [
            tsn.make_measurement_dto(units.UsOilfield.VOLUME, 6969.20),
            tsn.make_measurement_dto(units.Metric.VOLUME, 707.82),
        ]:
            stub_calculation_result = create_stub_calculation_result(expected_measurement_dto, DONT_CARE_WARNINGS)
            stub_treatment_calculations = create_stub_pumped_volume_calculation(stub_calculation_result)

            expected_measurement = tsn.make_measurement(expected_measurement_dto)
            self.assert_expected_calculation_result(ntc.pumped_fluid_volume,
                                                    stub_treatment_calculations,
                                                    datetime.datetime(2023, 8, 6, 3, 52, 4, tzinfo=duz.UTC),
                                                    datetime.datetime(2023, 8, 6, 5, 8, 20, tzinfo=duz.UTC),
                                                    expected_measurement=expected_measurement)

    def test_pumped_fluid_volume_returns_get_pumped_volume_warnings(self):
        for expected_warnings in [['urinator egregrius'], ['nomenclatura', 'gestus', 'tertia'], []]:
            dont_care_measurement = tsn.make_measurement_dto(units.UsOilfield.VOLUME, DONT_CARE_MEASUREMENT_MAGNITUDE)

            stub_calculation_result = create_stub_calculation_result(dont_care_measurement, expected_warnings)
            stub_treatment_calculations = create_stub_pumped_volume_calculation(stub_calculation_result)
            self.assert_expected_calculation_result(ntc.pumped_fluid_volume,
                                                    stub_treatment_calculations,
                                                    datetime.datetime(2023, 8, 6, 3, 52, 4, tzinfo=duz.UTC),
                                                    datetime.datetime(2023, 8, 6, 5, 8, 20, tzinfo=duz.UTC),
                                                    expected_warnings=expected_warnings)

    def test_total_proppant_mass_returns_get_total_proppant_mass_result(self):
        for expected_measurement_dto in [
            tsn.make_measurement_dto(units.UsOilfield.MASS, 5414.58),
            tsn.make_measurement_dto(units.Metric.MASS, 138262.86),
        ]:
            stub_calculation_result = create_stub_calculation_result(expected_measurement_dto, DONT_CARE_WARNINGS)
            stub_treatment_calculations = create_stub_proppant_mass_calculation(stub_calculation_result)

            expected_measurement = tsn.make_measurement(expected_measurement_dto)
            self.assert_expected_calculation_result(ntc.total_proppant_mass,
                                                    stub_treatment_calculations,
                                                    datetime.datetime(2020, 1, 29, 7, 35, 2, tzinfo=duz.UTC),
                                                    datetime.datetime(2020, 1, 29, 9, 13, 30, tzinfo=duz.UTC),
                                                    expected_measurement=expected_measurement)

    def test_total_proppant_mass_returns_get_total_proppant_mass_warnings(self):
        for expected_warnings in [[],  ['igitur', 'pantinam', 'incidi'], ['violentia venio']]:
            dont_care_measurement = tsn.make_measurement_dto(units.UsOilfield.MASS, DONT_CARE_MEASUREMENT_MAGNITUDE)

            stub_calculation_result = create_stub_calculation_result(dont_care_measurement, expected_warnings)
            stub_treatment_calculations = create_stub_proppant_mass_calculation(stub_calculation_result)
            self.assert_expected_calculation_result(ntc.total_proppant_mass,
                                                    stub_treatment_calculations,
                                                    datetime.datetime(2020, 1, 29, 7, 35, 2, tzinfo=duz.UTC),
                                                    datetime.datetime(2020, 1, 29, 9, 13, 30, tzinfo=duz.UTC),
                                                    expected_warnings=expected_warnings)


def create_stub_stage_adapter():
    result = unittest.mock.Mock('stub_stage_adapter', autospec=nsa.NativeStageAdapter)
    result.dom_object = unittest.mock.Mock('mock_dom_object')
    return result


def create_stub_calculation_result(expected_measurement_dto, warnings):
    calculation_result = NetCalculationResult(tsn.make_net_measurement(expected_measurement_dto), warnings)
    result = unittest.mock.MagicMock(name='calculation_result', return_value=calculation_result)
    return result


def create_stub_treatment_pressure_calculation(stub_calculation_result):
    result = unittest.mock.MagicMock(name='treatment_calculations', spec=ITreatmentCalculations)
    result.GetMedianTreatmentPressure = stub_calculation_result
    return result


def create_stub_pumped_volume_calculation(stub_calculation_result):
    result = unittest.mock.MagicMock(name='treatment_calculations', spec=ITreatmentCalculations)
    result.GetPumpedVolume = stub_calculation_result
    return result


def create_stub_proppant_mass_calculation(stub_calculation_result):
    result = unittest.mock.MagicMock(name='treatment_calculations', spec=ITreatmentCalculations)
    result.GetTotalProppantMass = stub_calculation_result
    return result


def assert_expected_result(sut, start_time, stop_time, expected_measurement=None, expected_warnings=None):
    actual_result = sut(create_stub_stage_adapter(), start_time, stop_time)
    if expected_measurement is not None:
        tcm.assert_that_scalar_quantities_close_to(actual_result.measurement, expected_measurement,
                                                   tolerance=6e-3)
    if expected_warnings is not None:
        assert_that(expected_warnings, equal_to(actual_result.warnings))


if __name__ == '__main__':
    unittest.main()
