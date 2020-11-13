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

from hamcrest import assert_that, equal_to, close_to, empty, contains_exactly, has_items, instance_of
import toolz.curried as toolz

from orchid.measurement import make_measurement
from orchid.net_quantity import as_net_quantity
import orchid.native_stage_adapter as nsa
import orchid.native_treatment_curve_facade as ntc
import orchid.reference_origins as origins
import orchid.unit_system as units

import tests.custom_matchers as tcm
import tests.stub_net as tsn


AboutLocation = namedtuple('AboutLocation', ['x', 'y', 'depth', 'unit'])
AboutOrigin = namedtuple('AboutOrigin', ['xy', 'depth'])
StubCalculateResult = namedtuple('CalculateResults', ['measurement', 'warnings'])


def make_subsurface_coordinate(coord, unit):
    return as_net_quantity(make_measurement(coord, unit.abbreviation))


@toolz.curry
def mock_subsurface_point_func(expected_location, xy_origin, depth_origin):
    result = tsn.create_stub_net_subsurface_point()
    if (xy_origin == origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE and
            depth_origin == origins.DepthDatum.GROUND_LEVEL):
        result.X = make_subsurface_coordinate(expected_location.x, expected_location.unit)
        result.Y = make_subsurface_coordinate(expected_location.y, expected_location.unit)
        result.Depth = make_subsurface_coordinate(expected_location.depth, expected_location.unit)
    elif (xy_origin == origins.WellReferenceFrameXy.PROJECT and
          depth_origin == origins.DepthDatum.KELLY_BUSHING):
        result.X = make_subsurface_coordinate(expected_location.x, expected_location.unit)
        result.Y = make_subsurface_coordinate(expected_location.y, expected_location.unit)
        result.Depth = make_subsurface_coordinate(expected_location.depth, expected_location.unit)
    elif (xy_origin == origins.WellReferenceFrameXy.WELL_HEAD and
          depth_origin == origins.DepthDatum.SEA_LEVEL):
        result.X = make_subsurface_coordinate(expected_location.x, expected_location.unit)
        result.Y = make_subsurface_coordinate(expected_location.y, expected_location.unit)
        result.Depth = make_subsurface_coordinate(expected_location.depth, expected_location.unit)
    return result


# Test ideas
# - Treatment curves
class TestNativeStageAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_bottom_location_returns_stage_location_center_in_requested_unit(self):
        actual_bottoms = [AboutLocation(200469.40, 549527.27, 2297.12, units.Metric.LENGTH),
                          AboutLocation(198747.28, 2142202.68, 2771.32, units.Metric.LENGTH),
                          AboutLocation(423829, 6976698, 9604.67, units.UsOilfield.LENGTH)]
        expected_bottoms = [AboutLocation(657708.00, 1802910.99, 7536.48, units.UsOilfield.LENGTH),
                            AboutLocation(198747.28, 2142202.68, 2771.32, units.Metric.LENGTH),
                            AboutLocation(129183.08, 2126497.55, 2927.50, units.Metric.LENGTH)]
        origin_references = [AboutOrigin(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                         origins.DepthDatum.GROUND_LEVEL),
                             AboutOrigin(origins.WellReferenceFrameXy.PROJECT,
                                         origins.DepthDatum.KELLY_BUSHING),
                             AboutOrigin(origins.WellReferenceFrameXy.WELL_HEAD,
                                         origins.DepthDatum.SEA_LEVEL)]

        for (actual_bottom, expected_bottom, origin_reference) in \
                zip(actual_bottoms, expected_bottoms, origin_references):
            with self.subTest(actual_bottom=actual_bottom, expected_bottom=expected_bottom,
                              origin_reference=origin_reference):
                bottom_mock_func = mock_subsurface_point_func(actual_bottom)

                stub_net_stage = tsn.create_stub_net_stage(stage_location_bottom=bottom_mock_func)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual = sut.bottom_location(expected_bottom.unit, origin_reference.xy, origin_reference.depth)

                expected = toolz.pipe(expected_bottom[:-1],
                                      toolz.map(toolz.flip(make_measurement, expected_bottom[-1].abbreviation)),
                                      lambda coords: tcm.SubsurfaceLocation(*coords))
                tcm.assert_that_scalar_quantities_close_to(actual.x, expected.x, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.y, expected.y, 7e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.depth, expected.depth, 6e-2)

    def test_center_location_returns_stage_location_center_in_requested_unit(self):
        actual_centers = [AboutLocation(200469.40, 549527.27, 2297.12, units.Metric.LENGTH),
                          AboutLocation(198747.28, 2142202.68, 2771.32, units.Metric.LENGTH),
                          AboutLocation(423829, 6976698, 9604.67, units.UsOilfield.LENGTH)]
        expected_centers = [AboutLocation(657708.00, 1802910.99, 7536.48, units.UsOilfield.LENGTH),
                            AboutLocation(198747.28, 2142202.68, 2771.32, units.Metric.LENGTH),
                            AboutLocation(129183.08, 2126497.55, 2927.50, units.Metric.LENGTH)]
        origin_references = [AboutOrigin(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                         origins.DepthDatum.GROUND_LEVEL),
                             AboutOrigin(origins.WellReferenceFrameXy.PROJECT,
                                         origins.DepthDatum.KELLY_BUSHING),
                             AboutOrigin(origins.WellReferenceFrameXy.WELL_HEAD,
                                         origins.DepthDatum.SEA_LEVEL)]

        for (actual_center, expected_center, origin_reference) in\
                zip(actual_centers, expected_centers, origin_references):
            with self.subTest(actual_center=actual_center, expected_center=expected_center,
                              origin_reference=origin_reference):
                center_mock_func = mock_subsurface_point_func(actual_center)

                stub_net_stage = tsn.create_stub_net_stage(stage_location_center=center_mock_func)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual = sut.center_location(expected_center.unit, origin_reference.xy, origin_reference.depth)

                expected = toolz.pipe(expected_center[:-1],
                                      toolz.map(toolz.flip(make_measurement, expected_center[-1].abbreviation)),
                                      lambda coords: tcm.SubsurfaceLocation(*coords))
                tcm.assert_that_scalar_quantities_close_to(actual.x, expected.x, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.y, expected.y, 7e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.depth, expected.depth, 6e-2)

    def test_display_stage_number(self):
        expected_display_stage_number = 11
        stub_net_stage = tsn.create_stub_net_stage(display_stage_no=expected_display_stage_number)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.display_stage_number, equal_to(expected_display_stage_number))

    def test_md_top(self):
        for actual_top, expected_top in [(make_measurement(13467.8, 'ft'), make_measurement(13467.8, 'ft')),
                                         (make_measurement(3702.48, 'm'), make_measurement(3702.48, 'm')),
                                         (make_measurement(13467.8, 'ft'), make_measurement(4104.98, 'm')),
                                         (make_measurement(3702.48, 'm'), make_measurement(12147.2, 'ft'))]:
            with self.subTest(expected_top=actual_top):
                stub_net_stage = tsn.create_stub_net_stage(md_top=tsn.MeasurementAsUnit(actual_top, expected_top.unit))
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_top(expected_top.unit)
                assert_that(actual_top.magnitude, close_to(expected_top.magnitude, 0.05))
                assert_that(actual_top.unit, equal_to(expected_top.unit))

    def test_md_bottom(self):
        for actual_bottom, expected_bottom in [(make_measurement(13806.7, 'ft'), make_measurement(13806.7, 'ft')),
                                               (make_measurement(4608.73, 'm'), make_measurement(4608.73, 'm')),
                                               (make_measurement(12147.2, 'ft'), make_measurement(3702.47, 'm')),
                                               (make_measurement(4608.73, 'm'), make_measurement(15120.5, 'ft'))]:
            with self.subTest(expected_bottom=actual_bottom):
                stub_net_stage = tsn.create_stub_net_stage(
                    md_bottom=tsn.MeasurementAsUnit(actual_bottom, actual_bottom.unit))
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_bottom = sut.md_bottom(expected_bottom.unit)
                assert_that(actual_bottom.magnitude, close_to(expected_bottom.magnitude, 0.05))
                assert_that(actual_bottom.unit, equal_to(expected_bottom.unit))

    def test_start_time(self):
        expected_start_time = datetime(2024, 10, 31, 7, 31, 27, 357000)
        stub_net_stage = tsn.create_stub_net_stage(start_time=expected_start_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_start_time = sut.start_time
        assert_that(actual_start_time, equal_to(expected_start_time))

    def test_stop_time(self):
        expected_stop_time = datetime(2016, 3, 31, 3, 31, 30, 947000)
        stub_net_stage = tsn.create_stub_net_stage(stop_time=expected_stop_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_stop_time = sut.stop_time
        assert_that(actual_stop_time, equal_to(expected_stop_time))

    def test_treatment_curves_no_curves(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curve = sut.treatment_curves()
        assert_that(actual_curve, empty())

    def test_treatment_curves_one_curve(self):
        expected_sampled_quantity_name = 'Slurry Rate'
        stub_net_stage = tsn.create_stub_net_stage(treatment_curve_names=[expected_sampled_quantity_name])
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), contains_exactly(expected_sampled_quantity_name))
        toolz.valmap(assert_is_native_treatment_curve_facade, actual_curves)

    def test_treatment_curves_many_curves(self):
        expected_sampled_quantity_names = ['Pressure', 'Slurry Rate', 'Proppant Concentration']
        stub_net_stage = tsn.create_stub_net_stage(treatment_curve_names=expected_sampled_quantity_names)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), has_items(ntc.TREATING_PRESSURE, ntc.SLURRY_RATE, ntc.TREATING_PRESSURE))
        toolz.valmap(assert_is_native_treatment_curve_facade, actual_curves)


def assert_is_native_treatment_curve_facade(curve):
    assert_that(curve, instance_of(ntc.NativeTreatmentCurveFacade))


if __name__ == '__main__':
    unittest.main()
