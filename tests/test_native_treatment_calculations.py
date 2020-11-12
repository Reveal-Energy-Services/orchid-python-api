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
import tests.stub_net as tsn

# noinspection PyUnresolvedReferences,PyPackageRequirements
import UnitsNet


DONT_CARE_MEASUREMENT_MAGNITUDE = float('NaN')


class TestNativeTreatmentCalculationsAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_median_treating_pressure_returns_get_median_treating_pressure_result(self):
        stub_stage = create_stub_stage_adapter()
        start_time = datetime.datetime(2023, 7, 2, 3, 57, 19)
        stop_time = datetime.datetime(2023, 7, 2, 5, 30, 2)
        for pressure_magnitude, unit in [(7396.93, units.UsOilfield.PRESSURE), (74.19, units.Metric.PRESSURE)]:
            expected_measurement = om.make_measurement(pressure_magnitude, unit.abbreviation)
            stub_native_calculations_factory = tsn.create_stub_net_calculations_factory(
                calculation_unit=unit, pressure_magnitude=pressure_magnitude)
            with self.subTest(expected_measurement=expected_measurement):
                actual_result = ntc.median_treating_pressure(stub_stage, start_time, stop_time,
                                                             calculations_factory=stub_native_calculations_factory)
                tcm.assert_that_scalar_quantities_close_to(actual_result.measurement, expected_measurement,
                                                           tolerance=6e-3)

    def test_median_treating_pressure_returns_get_median_treating_pressure_warnings(self):
        stub_stage = create_stub_stage_adapter()
        start_time = datetime.datetime(2023, 7, 2, 3, 57, 19)
        stop_time = datetime.datetime(2023, 7, 2, 5, 30, 2)
        for expected_warnings in [[], ['lente vetustas lupam vicit'], ['clunis', 'nobile', 'complacuit']]:
            stub_native_calculations_factory = tsn.create_stub_net_calculations_factory(
                warnings=expected_warnings, calculation_unit=units.Metric.PRESSURE,
                pressure_magnitude=DONT_CARE_MEASUREMENT_MAGNITUDE)
            with self.subTest(expected_warnings=expected_warnings):
                actual_result = ntc.median_treating_pressure(stub_stage, start_time, stop_time,
                                                             calculations_factory=stub_native_calculations_factory)
                assert_that(expected_warnings, equal_to(actual_result.warnings))

    def test_pumped_fluid_volume_returns_get_pumped_volume_result(self):
        stub_stage = create_stub_stage_adapter()
        start_time = datetime.datetime(2023, 8, 6, 3, 52, 4)
        stop_time = datetime.datetime(2023, 8, 6, 5, 8, 20)
        for volume_magnitude, unit in [(6269.20, units.UsOilfield.VOLUME), (707.82, units.Metric.VOLUME)]:
            expected_measurement = om.make_measurement(volume_magnitude, unit.abbreviation)
            stub_native_calculations_factory = tsn.create_stub_net_calculations_factory(
                calculation_unit=unit, volume_magnitude=volume_magnitude)
            with self.subTest(expected_measurement=expected_measurement):
                actual_result = ntc.pumped_fluid_volume(stub_stage, start_time, stop_time,
                                                        calculations_factory=stub_native_calculations_factory)
                tcm.assert_that_scalar_quantities_close_to(actual_result.measurement, expected_measurement,
                                                           tolerance=6e-3)

    def test_pumped_fluid_volume_returns_get_pumped_volume_warnings(self):
        stub_stage = create_stub_stage_adapter()
        start_time = datetime.datetime(2023, 8, 6, 3, 52, 4)
        stop_time = datetime.datetime(2023, 8, 6, 5, 8, 20)
        for expected_warnings in [['urinator egregrius'], ['nomenclatura', 'gestus', 'tertia'], []]:
            stub_native_calculations_factory = tsn.create_stub_net_calculations_factory(
                warnings=expected_warnings, calculation_unit=units.UsOilfield.VOLUME,
                volume_magnitude=DONT_CARE_MEASUREMENT_MAGNITUDE)
            with self.subTest(expected_warnings=expected_warnings):
                actual_result = ntc.pumped_fluid_volume(stub_stage, start_time, stop_time,
                                                        calculations_factory=stub_native_calculations_factory)
                assert_that(expected_warnings, equal_to(actual_result.warnings))

    def test_total_proppant_mass_returns_get_total_proppant_mass_result(self):
        stub_stage = create_stub_stage_adapter()
        start_time = datetime.datetime(2020, 1, 29, 7, 35, 2)
        stop_time = datetime.datetime(2020, 1, 29, 9, 13, 30)
        for mass_magnitude, unit in [(5414.58, units.UsOilfield.MASS), (138262.86, units.Metric.MASS)]:
            expected_measurement = om.make_measurement(mass_magnitude, unit.abbreviation)
            stub_native_calculations_factory = tsn.create_stub_net_calculations_factory(
                calculation_unit=unit, mass_magnitude=mass_magnitude)
            with self.subTest(expected_measurement=expected_measurement):
                actual_result = ntc.total_proppant_mass(stub_stage, start_time, stop_time,
                                                        calculations_factory=stub_native_calculations_factory)
                tcm.assert_that_scalar_quantities_close_to(actual_result.measurement, expected_measurement,
                                                           tolerance=6e-3)

    def test_total_proppant_mass_returns_get_total_proppant_mass_warnings(self):
        stub_stage = create_stub_stage_adapter()
        start_time = datetime.datetime(2020, 1, 29, 7, 35, 2)
        stop_time = datetime.datetime(2020, 1, 29, 9, 13, 30)
        for expected_warnings in [[],  ['igitur', 'pantinam', 'incidi'], ['violentia venio']]:
            stub_native_calculations_factory = tsn.create_stub_net_calculations_factory(
                warnings=expected_warnings, calculation_unit=units.UsOilfield.MASS,
                mass_magnitude=DONT_CARE_MEASUREMENT_MAGNITUDE)
            with self.subTest(expected_warnings=expected_warnings):
                actual_result = ntc.total_proppant_mass(stub_stage, start_time, stop_time,
                                                        calculations_factory=stub_native_calculations_factory)
                assert_that(expected_warnings, equal_to(actual_result.warnings))


def create_stub_stage_adapter():
    result = unittest.mock.Mock('stub_stage_adapter', autospec=nsa.NativeStageAdapter)
    result.dom_object = unittest.mock.Mock('mock_dom_object')
    return result


if __name__ == '__main__':
    unittest.main()