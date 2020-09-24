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

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IStage, IStageSampledQuantityTimeSeries, ISubsurfacePoint
# noinspection PyUnresolvedReferences
import UnitsNet


SubsurfaceLocation = namedtuple('SubsurfaceLocation', ['x', 'y', 'depth', 'unit'])


# Test ideas
# - Treatment curves
class TestNativeStageAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_center_location_returns_stage_location_center_in_project_units(self):
        def maker(unit_points_pair):
            unit, points = unit_points_pair
            return list(toolz.map(unit, points))

        actual_location_points = [(200469.40, 549527.27, 2297.12),
                                  (198747.28, 2142202.68, 2771.32),
                                  (423829, 6976698, 9604.67)]
        actual_location_units = [units.Metric.LENGTH, units.Metric.LENGTH, units.UsOilfield.LENGTH]
        actual_location_abbrevs = toolz.map(lambda u: u.abbreviation, actual_location_units)
        actual_measurement_maker_funcs = toolz.map(toolz.flip(make_measurement), actual_location_abbrevs)
        actual_locations = toolz.pipe(zip(actual_measurement_maker_funcs, actual_location_points),
                                      toolz.map(maker),
                                      list)

        expected_location_points = [(657708.00, 1802910.99, 7536.48),
                                    (198747.28, 2142202.68, 2771.32),
                                    (129183.08, 2126497.55, 2927.50)]
        expected_location_units = [units.UsOilfield.LENGTH, units.Metric.LENGTH, units.Metric.LENGTH]
        expected_location_abbrevs = toolz.map(lambda u: u.abbreviation, expected_location_units)
        expected_measurement_maker_funcs = toolz.map(toolz.flip(make_measurement), expected_location_abbrevs)
        expected_location = toolz.pipe(zip(expected_measurement_maker_funcs, expected_location_points),
                                       toolz.map(maker),
                                       list)

        test_data = [(oro.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, oro.DepthDatum.GROUND_LEVEL,
                      actual_locations[0], expected_location[0]),
                     (oro.WellReferenceFrameXy.PROJECT, oro.DepthDatum.KELLY_BUSHING,
                      actual_locations[1], expected_location[1]),
                     (oro.WellReferenceFrameXy.WELL_HEAD, oro.DepthDatum.SEA_LEVEL,
                      actual_locations[2], expected_location[2])]
        for xy_origin, depth_origin, actual_location, expected_location in test_data:
            with self.subTest(xy_origin=xy_origin, depth_origin=depth_origin,
                              actual_location=actual_location, expected_location=expected_location):
                stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
                actual_subsurface_point = unittest.mock.MagicMock(name='stub_net_subsurface_point',
                                                                  spec='ISubsurfacePoint')
                actual_subsurface_point.X = as_net_quantity(actual_location[0])
                actual_subsurface_point.Y = as_net_quantity(actual_location[1])
                actual_subsurface_point.Depth = as_net_quantity(actual_location[2])
                stub_net_stage.GetStageLocationCenter = unittest.mock.MagicMock(name='stub_get_stage_location_center',
                                                                                return_value=actual_subsurface_point)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_center_location = sut.center_location(expected_location[0].unit, xy_origin, depth_origin)
                # delta of "7" is a result of half-even rounding and truncation
                assert_that(actual_center_location[0].magnitude, close_to(expected_location[0].magnitude, 7e-2))
                assert_that(actual_center_location[1].magnitude, close_to(expected_location[1].magnitude, 7e-2))
                assert_that(actual_center_location[2].magnitude, close_to(expected_location[2].magnitude, 7e-2))

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
