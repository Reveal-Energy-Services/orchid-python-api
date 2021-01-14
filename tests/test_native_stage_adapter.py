#  Copyright 2017-2021 Reveal Energy Services, Inc 
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
import decimal
from datetime import datetime
import unittest.mock

import dateutil.tz as duz
import deal
from hamcrest import assert_that, equal_to, empty, contains_exactly, has_items, instance_of, calling, raises
import toolz.curried as toolz

from orchid import (
    measurement as om,
    net_quantity as onq,
    native_stage_adapter as nsa,
    native_treatment_curve_adapter as ntc,
    reference_origins as origins,
    unit_system as units,
)

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)

AboutLocation = namedtuple('AboutLocation', ['x', 'y', 'depth', 'unit'])
AboutOrigin = namedtuple('AboutOrigin', ['xy', 'depth'])
AboutTolerance = namedtuple('AboutTolerance', ['x', 'y', 'depth'])
StubCalculateResult = namedtuple('CalculateResults', ['measurement', 'warnings'])

# Location values needed for tests but not tested in tests
DONT_CARE_METRIC_LOCATION = AboutLocation(314200, 1414000, 1717, units.Metric.LENGTH)
DONT_CARE_US_OILFIELD_LOCATION = AboutLocation(271800, 3142000, 14140, units.UsOilfield.LENGTH)


def _make_subsurface_coordinate(coord, unit):
    return onq.as_net_quantity(om.make_measurement(unit, coord))


@toolz.curry
def mock_subsurface_point_func(expected_location,
                               expected_xy_origin, expected_depth_origin,
                               actual_xy_origin, actual_depth_origin):
    result = tsn.create_stub_net_subsurface_point()
    if expected_xy_origin == actual_xy_origin and expected_depth_origin == actual_depth_origin:
        result.X = _make_subsurface_coordinate(expected_location.x, expected_location.unit)
        result.Y = _make_subsurface_coordinate(expected_location.y, expected_location.unit)
        result.Depth = _make_subsurface_coordinate(expected_location.depth, expected_location.unit)
    return result


def create_expected(expected_location):
    make_measurement_with_unit = om.make_measurement(expected_location[-1])
    expected = toolz.pipe(expected_location[:-1],
                          toolz.map(make_measurement_with_unit),
                          lambda coords: tsn.StubSubsurfaceLocation(*coords))
    return expected


# Test ideas
class TestNativeStageAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_bottom_location_invokes_get_stage_location_bottom_correctly(self):
        bottom_mock_func = mock_subsurface_point_func(DONT_CARE_METRIC_LOCATION,
                                                      origins.WellReferenceFrameXy.WELL_HEAD,
                                                      origins.DepthDatum.KELLY_BUSHING)
        stub_net_stage = tsn.create_stub_net_stage(stage_location_bottom=bottom_mock_func)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.bottom_location(units.Metric.LENGTH, origins.WellReferenceFrameXy.WELL_HEAD,
                            origins.DepthDatum.KELLY_BUSHING)

        stub_net_stage.GetStageLocationBottom.assert_called_with(origins.WellReferenceFrameXy.WELL_HEAD.value,
                                                                 origins.DepthDatum.KELLY_BUSHING.value)

    def test_center_location_invokes_get_stage_location_center_correctly(self):
        center_mock_func = mock_subsurface_point_func(DONT_CARE_US_OILFIELD_LOCATION,
                                                      origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                      origins.DepthDatum.GROUND_LEVEL)
        stub_net_stage = tsn.create_stub_net_stage(stage_location_center=center_mock_func)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.center_location(units.UsOilfield.LENGTH, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                            origins.DepthDatum.GROUND_LEVEL)

        stub_net_stage.GetStageLocationCenter.assert_called_with(
            origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE.value, origins.DepthDatum.GROUND_LEVEL.value)

    def test_cluster_count(self):
        expected_cluster_count = 3
        stub_net_stage = tsn.create_stub_net_stage(cluster_count=expected_cluster_count)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.cluster_count, equal_to(expected_cluster_count))

    def test_cluster_location_invokes_get_stage_location_cluster_correctly(self):
        @toolz.curry
        def mock_cluster_subsurface_point_func(expected_location,
                                               expected_cluster_no, expected_xy_origin, expected_depth_origin,
                                               actual_cluster_no, actual_xy_origin, actual_depth_origin):
            result = tsn.create_stub_net_subsurface_point()
            if expected_cluster_no == actual_cluster_no and expected_xy_origin == actual_xy_origin and \
                    expected_depth_origin == actual_depth_origin:
                result.X = _make_subsurface_coordinate(expected_location.x, expected_location.unit)
                result.Y = _make_subsurface_coordinate(expected_location.y, expected_location.unit)
                result.Depth = _make_subsurface_coordinate(expected_location.depth, expected_location.unit)
            return result

        dont_care_cluster_no = 3
        cluster_mock_func = mock_cluster_subsurface_point_func(DONT_CARE_US_OILFIELD_LOCATION,
                                                               dont_care_cluster_no,
                                                               origins.WellReferenceFrameXy.PROJECT,
                                                               origins.DepthDatum.KELLY_BUSHING)
        stub_net_stage = tsn.create_stub_net_stage(stage_location_cluster=cluster_mock_func)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.cluster_location(units.UsOilfield.LENGTH,
                             dont_care_cluster_no,
                             origins.WellReferenceFrameXy.PROJECT,
                             origins.DepthDatum.KELLY_BUSHING)

        stub_net_stage.GetStageLocationCluster.assert_called_with(
            dont_care_cluster_no, origins.WellReferenceFrameXy.PROJECT.value,
            origins.DepthDatum.KELLY_BUSHING.value)

    def test_cluster_location_invalid_cluster_no_raises_contract_error(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(calling(sut.cluster_location).with_args(units.UsOilfield.LENGTH, -1,
                                                            origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                            origins.DepthDatum.GROUND_LEVEL),
                    raises(deal.PreContractError))

    def test_display_stage_number(self):
        expected_display_stage_number = 11
        stub_net_stage = tsn.create_stub_net_stage(display_stage_no=expected_display_stage_number)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.display_stage_number, equal_to(expected_display_stage_number))

    def test_md_top(self):
        for actual_top, expected_top in [(om.make_measurement(units.UsOilfield.LENGTH, 13467.8),
                                          om.make_measurement(units.UsOilfield.LENGTH, 13467.8)),
                                         (om.make_measurement(units.Metric.LENGTH, 3702.48),
                                          om.make_measurement(units.Metric.LENGTH, 3702.48)),
                                         (om.make_measurement(units.UsOilfield.LENGTH, 13467.8),
                                          om.make_measurement(units.Metric.LENGTH, 4104.98)),
                                         (om.make_measurement(units.Metric.LENGTH, 3702.48),
                                          om.make_measurement(units.UsOilfield.LENGTH, 12147.2))]:
            with self.subTest(f'Test MD top {expected_top}'):
                stub_net_stage = tsn.create_stub_net_stage(md_top=tsn.MeasurementAsUnit(actual_top, expected_top.unit))
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_top(expected_top.unit)
                tcm.assert_that_measurements_close_to(actual_top, expected_top, 5e-2)

    def test_md_bottom(self):
        for actual_bottom, expected_bottom in [
            (om.make_measurement(units.UsOilfield.LENGTH, 13806.7),
             om.make_measurement(units.UsOilfield.LENGTH, 13806.7)),
            (om.make_measurement(units.Metric.LENGTH, 4608.73),
             om.make_measurement(units.Metric.LENGTH, 4608.73)),
            (om.make_measurement(units.UsOilfield.LENGTH, 12147.2),
             om.make_measurement(units.Metric.LENGTH, 3702.47)),
            (om.make_measurement(units.Metric.LENGTH, 4608.73),
             om.make_measurement(units.UsOilfield.LENGTH, 15120.5)),
        ]:
            with self.subTest(f'Test MD bottom {expected_bottom}'):
                stub_net_stage = tsn.create_stub_net_stage(
                    md_bottom=tsn.MeasurementAsUnit(actual_bottom, actual_bottom.unit))
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_bottom = sut.md_bottom(expected_bottom.unit)
                tcm.assert_that_measurements_close_to(actual_bottom, expected_bottom, 5e-2)

    def test_subsurface_point_in_length_units(self):
        net_points = [
            AboutLocation(1.214e5, 6.226e5, 2336, units.Metric.LENGTH),
            AboutLocation(1.840e5, 8.994e6, 8281, units.UsOilfield.LENGTH),
            AboutLocation(5.094e5, 1.489e6, 1833, units.Metric.LENGTH),
            AboutLocation(3.126e5, 6.812e6, 9453, units.UsOilfield.LENGTH),
        ]
        expected_points = [
            AboutLocation(3.984e5, 2.042e6, 7666, units.UsOilfield.LENGTH),
            AboutLocation(5.608e4, 2.741e6, 2524, units.Metric.LENGTH),
            AboutLocation(5.094e5, 1.489e6, 1833, units.Metric.LENGTH),
            AboutLocation(3.126e5, 6.812e6, 9453, units.UsOilfield.LENGTH),
        ]
        origin_references = [
            AboutOrigin(origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.GROUND_LEVEL),
            AboutOrigin(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, origins.DepthDatum.SEA_LEVEL),
            AboutOrigin(origins.WellReferenceFrameXy.PROJECT, origins.DepthDatum.KELLY_BUSHING),
            AboutOrigin(origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.KELLY_BUSHING),
        ]
        tolerances = [
            AboutTolerance(decimal.Decimal('300'), decimal.Decimal('3000'), decimal.Decimal('3')),
            AboutTolerance(decimal.Decimal('30'), decimal.Decimal('3000'), decimal.Decimal('0.3')),
            AboutTolerance(decimal.Decimal('100'), decimal.Decimal('1000'), decimal.Decimal('1')),
            AboutTolerance(decimal.Decimal('100'), decimal.Decimal('1000'), decimal.Decimal('1')),
        ]
        for net_point, expected_point, origin_reference, tolerance in zip(net_points, expected_points,
                                                                          origin_references, tolerances):
            with self.subTest(f'Test subsurface point ({net_point[0]} {net_point[-1].value.unit:~P},...)'
                              f' in length unit {expected_point[-1].value.unit:~P}.'):
                subsurface_point_mock_func = mock_subsurface_point_func(net_point, origin_reference.xy,
                                                                        origin_reference.depth)
                actual = nsa.subsurface_point_in_length_units(origin_reference.depth, origin_reference.xy,
                                                              expected_point[-1], subsurface_point_mock_func)

                expected = create_expected(expected_point)
                tcm.assert_that_measurements_close_to(actual.x, expected.x, tolerance.x)
                tcm.assert_that_measurements_close_to(actual.y, expected.y, tolerance.y)
                tcm.assert_that_measurements_close_to(actual.depth, expected.depth, tolerance.depth)

    def test_start_time(self):
        expected_start_time = datetime(2024, 10, 31, 7, 31, 27, 357000, duz.UTC)
        stub_net_stage = tsn.create_stub_net_stage(start_time=expected_start_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_start_time = sut.start_time
        assert_that(actual_start_time, equal_to(expected_start_time))

    def test_stop_time(self):
        expected_stop_time = datetime(2016, 3, 31, 3, 31, 30, 947000, duz.UTC)
        stub_net_stage = tsn.create_stub_net_stage(stop_time=expected_stop_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_stop_time = sut.stop_time
        assert_that(actual_stop_time, equal_to(expected_stop_time))

    def test_top_location_invokes_get_stage_location_top_correctly(self):
        top_mock_func = mock_subsurface_point_func(DONT_CARE_US_OILFIELD_LOCATION,
                                                   origins.WellReferenceFrameXy.PROJECT,
                                                   origins.DepthDatum.SEA_LEVEL)
        stub_net_stage = tsn.create_stub_net_stage(stage_location_top=top_mock_func)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.top_location(units.UsOilfield.LENGTH, origins.WellReferenceFrameXy.PROJECT,
                         origins.DepthDatum.SEA_LEVEL)

        stub_net_stage.GetStageLocationTop.assert_called_with(
            origins.WellReferenceFrameXy.PROJECT.value, origins.DepthDatum.SEA_LEVEL.value)

    def test_treatment_curves_no_curves(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curve = sut.treatment_curves()
        assert_that(actual_curve, empty())

    def test_treatment_curves_one_curve(self):
        expected_sampled_quantity_name = ntc.TreatmentCurveTypes.SLURRY_RATE
        stub_net_stage = tsn.create_stub_net_stage(treatment_curve_names=[expected_sampled_quantity_name])
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), contains_exactly(expected_sampled_quantity_name))
        toolz.valmap(assert_is_native_treatment_curve_facade, actual_curves)

    def test_treatment_curves_many_curves(self):
        expected_sampled_quantity_names = [ntc.TreatmentCurveTypes.TREATING_PRESSURE,
                                           ntc.TreatmentCurveTypes.SLURRY_RATE,
                                           ntc.TreatmentCurveTypes.SURFACE_PROPPANT_CONCENTRATION]
        stub_net_stage = tsn.create_stub_net_stage(treatment_curve_names=expected_sampled_quantity_names)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), has_items(ntc.TreatmentCurveTypes.TREATING_PRESSURE,
                                                    ntc.TreatmentCurveTypes.SLURRY_RATE,
                                                    ntc.TreatmentCurveTypes.SURFACE_PROPPANT_CONCENTRATION))
        toolz.valmap(assert_is_native_treatment_curve_facade, actual_curves)


def assert_is_native_treatment_curve_facade(curve):
    assert_that(curve, instance_of(ntc.NativeTreatmentCurveAdapter))


if __name__ == '__main__':
    unittest.main()
