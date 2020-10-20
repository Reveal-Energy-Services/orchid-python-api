#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

from collections import namedtuple
from datetime import datetime
import unittest.mock

from hamcrest import assert_that, equal_to, close_to, empty, contains_exactly, has_items
import toolz.curried as toolz

from orchid.measurement import make_measurement
from orchid.net_quantity import as_net_date_time, as_net_quantity
import orchid.native_stage_adapter as nsa
import orchid.native_treatment_curve_facade as ntc
from orchid.net_quantity import as_net_quantity_in_different_unit
import orchid.reference_origin as oro
import orchid.unit_system as units

import tests.custom_matchers as tcm


# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import IStage, IStageSampledQuantityTimeSeries, ISubsurfacePoint
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import IFractureDiagnosticsCalculationsFactory, ITreatmentCalculations
# noinspection PyUnresolvedReferences
import UnitsNet


AboutCenter = namedtuple('AboutCenter', ['x', 'y', 'depth', 'unit'])
AboutOrigin = namedtuple('AboutOrigin', ['xy', 'depth'])


# Test ideas
# - Treatment curves
class TestNativeStageAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_center_location_returns_stage_location_center_in_requested_unit(self):
        def make_subsurface_coordinate(center_coord, center_unit):
            return as_net_quantity(make_measurement(center_coord, center_unit.abbreviation))

        actual_centers = [AboutCenter(200469.40, 549527.27, 2297.12, units.Metric.LENGTH),
                          AboutCenter(198747.28, 2142202.68, 2771.32, units.Metric.LENGTH),
                          AboutCenter(423829, 6976698, 9604.67, units.UsOilfield.LENGTH)]
        expected_centers = [AboutCenter(657708.00, 1802910.99, 7536.48, units.UsOilfield.LENGTH),
                            AboutCenter(198747.28, 2142202.68, 2771.32, units.Metric.LENGTH),
                            AboutCenter(129183.08, 2126497.55, 2927.50, units.Metric.LENGTH)]
        origin_references = [AboutOrigin(oro.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, oro.DepthDatum.GROUND_LEVEL),
                             AboutOrigin(oro.WellReferenceFrameXy.PROJECT, oro.DepthDatum.KELLY_BUSHING),
                             AboutOrigin(oro.WellReferenceFrameXy.WELL_HEAD, oro.DepthDatum.SEA_LEVEL)]

        for (actual_center, expected_center, origin_reference) in\
                zip(actual_centers, expected_centers, origin_references):
            def center_mock_func(*args):
                result = unittest.mock.MagicMock(name='stub_net_subsurface_point',
                                                 spec='ISubsurfacePoint')
                if (args[0] == oro.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE and
                        args[1] == oro.DepthDatum.GROUND_LEVEL):
                    result.X = make_subsurface_coordinate(expected_center.x, expected_center.unit)
                    result.Y = make_subsurface_coordinate(expected_center.y, expected_center.unit)
                    result.Depth = make_subsurface_coordinate(expected_center.depth, expected_center.unit)
                elif args[0] == oro.WellReferenceFrameXy.PROJECT and args[1] == oro.DepthDatum.KELLY_BUSHING:
                    result.X = make_subsurface_coordinate(expected_center.x, expected_center.unit)
                    result.Y = make_subsurface_coordinate(expected_center.y, expected_center.unit)
                    result.Depth = make_subsurface_coordinate(expected_center.depth, expected_center.unit)
                elif args[0] == oro.WellReferenceFrameXy.WELL_HEAD and args[1] == oro.DepthDatum.SEA_LEVEL:
                    result.X = make_subsurface_coordinate(expected_center.x, expected_center.unit)
                    result.Y = make_subsurface_coordinate(expected_center.y, expected_center.unit)
                    result.Depth = make_subsurface_coordinate(expected_center.depth, expected_center.unit)
                return result

            stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
            stub_net_stage.GetStageLocationCenter = unittest.mock.MagicMock(name='stub_get_stage_location_center',
                                                                            side_effect=center_mock_func)
            sut = nsa.NativeStageAdapter(stub_net_stage)

            actual = sut.center_location(expected_center.unit, origin_reference.xy, origin_reference.depth)

            expected = toolz.pipe(expected_center[:-1],
                                  toolz.map(toolz.flip(make_measurement, expected_center[-1].abbreviation)),
                                  lambda coords: tcm.SubsurfaceLocation(*coords))
            tcm.assert_that_scalar_quantities_close_to(actual.x, expected.x, 6e-2)
            tcm.assert_that_scalar_quantities_close_to(actual.y, expected.y, 7e-2)
            tcm.assert_that_scalar_quantities_close_to(actual.depth, expected.depth, 6e-2)

    def test_display_stage_number(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_display_stage_number = 11
        stub_net_stage.DisplayStageNumber = expected_display_stage_number
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.display_stage_number, equal_to(expected_display_stage_number))

    def test_md_top(self):
        for actual_top, expected_top in [(make_measurement(13467.8, 'ft'), make_measurement(13467.8, 'ft')),
                                         (make_measurement(3702.48, 'm'), make_measurement(3702.48, 'm')),
                                         (make_measurement(13467.8, 'ft'), make_measurement(4104.98, 'm')),
                                         (make_measurement(3702.48, 'm'), make_measurement(12147.2, 'ft'))]:
            with self.subTest(expected_top=actual_top):
                stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
                stub_net_stage.MdTop = as_net_quantity_in_different_unit(actual_top, actual_top.unit)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_top(expected_top.unit)
                assert_that(actual_top.magnitude, close_to(expected_top.magnitude, 0.05))
                assert_that(actual_top.unit, equal_to(expected_top.unit))

    def test_md_bottom(self):
        for actual_top, expected_top in [(make_measurement(13806.7, 'ft'), make_measurement(13806.7, 'ft')),
                                         (make_measurement(4608.73, 'm'), make_measurement(4608.73, 'm')),
                                         (make_measurement(12147.2, 'ft'), make_measurement(3702.47, 'm')),
                                         (make_measurement(4608.73, 'm'), make_measurement(15120.5, 'ft'))]:
            with self.subTest(expected_top=actual_top):
                stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
                stub_net_stage.MdBottom = as_net_quantity_in_different_unit(actual_top, actual_top.unit)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_bottom(expected_top.unit)
                assert_that(actual_top.magnitude, close_to(expected_top.magnitude, 0.05))
                assert_that(actual_top.unit, equal_to(expected_top.unit))

    def test_median_treating_pressure(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_start_time = datetime(2023, 12, 13, 20, 3, 29, 200000)
        stub_net_stage.StartTime = as_net_date_time(expected_start_time)
        expected_stop_time = datetime(2023, 12, 13, 22, 25, 51, 300000)
        stub_net_stage.StopTime = as_net_date_time(expected_stop_time)
        for expected_median_pressure in [make_measurement(6608.55, units.UsOilfield.PRESSURE.abbreviation),
                                         make_measurement(30281.49, units.Metric.PRESSURE.abbreviation)]:
            with self.subTest(expected_median_pressure=expected_median_pressure):
                stub_net_treatment_calculations = unittest.mock.MagicMock(name='stub_net_treatment_calculations',
                                                                          spec=ITreatmentCalculations)
                stub_net_treatment_calculations.GetMedianTreatmentPressure = unittest.mock.MagicMock(
                    return_value=(as_net_quantity(expected_median_pressure), None))
                stub_net_calculations_factory = unittest.mock.MagicMock(name='stub_net_calculations_factory',
                                                                        spec=IFractureDiagnosticsCalculationsFactory)
                stub_net_calculations_factory.CreateTreatmentCalculations = unittest.mock.MagicMock(
                    return_value=stub_net_treatment_calculations)
                sut = nsa.NativeStageAdapter(stub_net_stage, stub_net_calculations_factory)

                actual_median_treating = sut.median_treating_pressure()
                tcm.assert_that_scalar_quantities_close_to(actual_median_treating, expected_median_pressure, 5e-3)

    def test_pumped_fluid_volume(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_start_time = datetime(2017, 5, 26, 3, 20, 5, 940000)
        stub_net_stage.StartTime = as_net_date_time(expected_start_time)
        expected_stop_time = datetime(2017, 5, 26, 5, 42, 10, 936000)
        stub_net_stage.StopTime = as_net_date_time(expected_stop_time)
        for expected_fluid_volume in [make_measurement(7511.38, units.UsOilfield.VOLUME.abbreviation),
                                      make_measurement(919.83, units.Metric.VOLUME.abbreviation)]:
            with self.subTest(expected_fluid_volume=expected_fluid_volume):
                stub_net_treatment_calculations = unittest.mock.MagicMock(name='stub_net_treatment_calculations',
                                                                          spec=ITreatmentCalculations)
                stub_net_treatment_calculations.GetPumpedVolume = unittest.mock.MagicMock(
                    return_value=(as_net_quantity(expected_fluid_volume), None))
                stub_net_calculations_factory = unittest.mock.MagicMock(name='stub_net_calculations_factory',
                                                                        spec=IFractureDiagnosticsCalculationsFactory)
                stub_net_calculations_factory.CreateTreatmentCalculations = unittest.mock.MagicMock(
                    return_value=stub_net_treatment_calculations)
                sut = nsa.NativeStageAdapter(stub_net_stage, stub_net_calculations_factory)

                actual_fluid_volume = sut.pumped_fluid_volume()
                tcm.assert_that_scalar_quantities_close_to(actual_fluid_volume, expected_fluid_volume, 5e-3)

    def test_start_time(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_start_time = datetime(2024, 10, 31, 7, 31, 27, 357000)
        stub_net_stage.StartTime = as_net_date_time(expected_start_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_start_time = sut.start_time
        assert_that(actual_start_time, equal_to(expected_start_time))

    def test_stop_time(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_stop_time = datetime(2016, 3, 31, 3, 31, 30, 947000)
        stub_net_stage.StopTime = as_net_date_time(expected_stop_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_stop_time = sut.stop_time
        assert_that(actual_stop_time, equal_to(expected_stop_time))

    def test_total_proppant_mass(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_start_time = datetime(2016, 9, 30, 5, 22, 14, 345000)
        stub_net_stage.StartTime = as_net_date_time(expected_start_time)
        expected_stop_time = datetime(2016, 9, 30, 7, 3, 46, 621000)
        stub_net_stage.StopTime = as_net_date_time(expected_stop_time)
        for expected_proppant_mass in [make_measurement(5167.93, units.UsOilfield.MASS.abbreviation),
                                       make_measurement(132537.16, units.Metric.MASS.abbreviation)]:
            with self.subTest(expected_proppant_mass=expected_proppant_mass):
                stub_net_treatment_calculations = unittest.mock.MagicMock(name='stub_net_treatment_calculations',
                                                                          spec=ITreatmentCalculations)
                stub_net_treatment_calculations.GetTotalProppantMass = unittest.mock.MagicMock(
                    return_value=(as_net_quantity(expected_proppant_mass), None))
                stub_net_calculations_factory = unittest.mock.MagicMock(name='stub_net_calculations_factory',
                                                                        spec=IFractureDiagnosticsCalculationsFactory)
                stub_net_calculations_factory.CreateTreatmentCalculations = unittest.mock.MagicMock(
                    return_value=stub_net_treatment_calculations)
                sut = nsa.NativeStageAdapter(stub_net_stage, stub_net_calculations_factory)

                actual_proppant_mass = sut.total_proppant_mass()
                tcm.assert_that_scalar_quantities_close_to(actual_proppant_mass, expected_proppant_mass, 5e-3)

    def test_treatment_curves_no_curves(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        stub_net_stage.TreatmentCurves.Items = []
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curve = sut.treatment_curves()
        assert_that(actual_curve, empty())

    def test_treatment_curves_one_curve(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_sampled_quantity_name = 'Slurry Rate'
        stub_treatment_curve = unittest.mock.MagicMock(name='Treatment Curve', spec=IStageSampledQuantityTimeSeries)
        stub_treatment_curve.SampledQuantityName = expected_sampled_quantity_name
        stub_net_stage.TreatmentCurves.Items = [stub_treatment_curve]
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), contains_exactly(expected_sampled_quantity_name))
        assert_that(toolz.map(lambda c: c.sampled_quantity_name, actual_curves.values()),
                    contains_exactly(expected_sampled_quantity_name))

    def test_treatment_curves_many_curves(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_sampled_quantity_names = ['Pressure', 'Slurry Rate', 'Proppant Concentration']
        expected_curve_names = [ntc.TREATING_PRESSURE, ntc.SLURRY_RATE, ntc.TREATING_PRESSURE]

        def make_stub_treatment_curve(name):
            stub_treatment_curve = unittest.mock.MagicMock(name='Treatment Curve', spec=IStageSampledQuantityTimeSeries)
            stub_treatment_curve.SampledQuantityName = name
            return stub_treatment_curve

        stub_treatment_curves = toolz.map(make_stub_treatment_curve, expected_sampled_quantity_names)
        stub_net_stage.TreatmentCurves.Items = stub_treatment_curves
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), has_items(*expected_curve_names))
        assert_that(toolz.map(lambda c: c.sampled_quantity_name, actual_curves.values()),
                    has_items(*expected_sampled_quantity_names))


if __name__ == '__main__':
    unittest.main()
