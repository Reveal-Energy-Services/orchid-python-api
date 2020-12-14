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

import deal
from hamcrest import assert_that, equal_to, close_to, empty, contains_exactly, has_items, instance_of, calling, raises
import toolz.curried as toolz

from orchid.measurement import make_measurement
from orchid.net_quantity import as_net_quantity
import orchid.native_stage_adapter as nsa
import orchid.native_treatment_curve_facade as ntc
import orchid.reference_origins as origins
import orchid.unit_system as units

import tests.custom_matchers as tcm
from tests import stub_net as tsn

AboutLocation = namedtuple('AboutLocation', ['x', 'y', 'depth', 'unit'])
AboutOrigin = namedtuple('AboutOrigin', ['xy', 'depth'])
StubCalculateResult = namedtuple('CalculateResults', ['measurement', 'warnings'])


def _make_subsurface_coordinate(coord, unit):
    return as_net_quantity(make_measurement(coord, unit))


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
    expected = toolz.pipe(expected_location[:-1],
                          toolz.map(toolz.flip(make_measurement, expected_location[-1])),
                          lambda coords: tcm.SubsurfaceLocation(*coords))
    return expected


# Test ideas
class TestNativeStageAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_bottom_location_returns_stage_location_center_in_requested_unit(self):
        actual_bottoms = [AboutLocation(396924, -3247781, 6423.56, units.UsOilfield.LENGTH),
                          AboutLocation(791628, 3859627, 7773.03, units.UsOilfield.LENGTH),
                          AboutLocation(251799.84, 186541.56, 2263.19, units.Metric.LENGTH)]
        expected_bottoms = [AboutLocation(396924, -3247781, 6423.56, units.UsOilfield.LENGTH),
                            AboutLocation(241288.21, 1176414.27, 2369.22, units.Metric.LENGTH),
                            AboutLocation(826115, 612013, 7425.16, units.UsOilfield.LENGTH)]
        origin_references = [AboutOrigin(origins.WellReferenceFrameXy.PROJECT,
                                         origins.DepthDatum.GROUND_LEVEL),
                             AboutOrigin(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                         origins.DepthDatum.SEA_LEVEL),
                             AboutOrigin(origins.WellReferenceFrameXy.WELL_HEAD,
                                         origins.DepthDatum.KELLY_BUSHING)]

        for (actual_bottom, expected_bottom, origin_reference) in \
                zip(actual_bottoms, expected_bottoms, origin_references):
            with self.subTest(actual_bottom=actual_bottom, expected_bottom=expected_bottom,
                              origin_reference=origin_reference):
                bottom_mock_func = mock_subsurface_point_func(actual_bottom, origin_reference.xy,
                                                              origin_reference.depth)
                stub_net_stage = tsn.create_stub_net_stage(stage_location_bottom=bottom_mock_func)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual = sut.bottom_location(expected_bottom.unit, origin_reference.xy, origin_reference.depth)

                expected = create_expected(expected_bottom)
                tcm.assert_that_scalar_quantities_close_to(actual.x, expected.x, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.y, expected.y, 6e-2)
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
                center_mock_func = mock_subsurface_point_func(actual_center, origin_reference.xy,
                                                              origin_reference.depth)
                stub_net_stage = tsn.create_stub_net_stage(stage_location_center=center_mock_func)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual = sut.center_location(expected_center.unit, origin_reference.xy, origin_reference.depth)

                expected = create_expected(expected_center)
                tcm.assert_that_scalar_quantities_close_to(actual.x, expected.x, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.y, expected.y, 7e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.depth, expected.depth, 6e-2)

    def test_cluster_count(self):
        expected_cluster_count = 3
        stub_net_stage = tsn.create_stub_net_stage(cluster_count=expected_cluster_count)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.cluster_count, equal_to(expected_cluster_count))

    def test_cluster_location_returns_stage_location_cluster_in_requested_unit(self):
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

        cluster_numbers = [2, 4, 7]
        actual_clusters = [AboutLocation(93859.19, 187991.49, 2619.49, units.Metric.LENGTH),
                           AboutLocation(413364, 684896, 8974.38, units.UsOilfield.LENGTH),
                           AboutLocation(92837, -17316.01, 9275.89, units.UsOilfield.LENGTH)]
        expected_clusters = [AboutLocation(307936.98, 616770.00, 8594.13, units.UsOilfield.LENGTH),
                             AboutLocation(413364, 684896, 8974.38, units.UsOilfield.LENGTH),
                             AboutLocation(28296.72, -5277.92, 2827.29, units.Metric.LENGTH)]
        origin_references = [AboutOrigin(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                         origins.DepthDatum.SEA_LEVEL),
                             AboutOrigin(origins.WellReferenceFrameXy.WELL_HEAD,
                                         origins.DepthDatum.KELLY_BUSHING),
                             AboutOrigin(origins.WellReferenceFrameXy.PROJECT,
                                         origins.DepthDatum.GROUND_LEVEL)]

        for (cluster_no, actual_cluster, expected_cluster, origin_reference) in \
                zip(cluster_numbers, actual_clusters, expected_clusters, origin_references):
            with self.subTest(cluster_no=cluster_no, actual_cluster=actual_cluster, expected_cluster=expected_cluster,
                              origin_reference=origin_reference):
                cluster_mock_func = mock_cluster_subsurface_point_func(actual_cluster, cluster_no,
                                                                       origin_reference.xy, origin_reference.depth)
                stub_net_stage = tsn.create_stub_net_stage(stage_location_cluster=cluster_mock_func)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual = sut.cluster_location(expected_cluster.unit, cluster_no, origin_reference.xy,
                                              origin_reference.depth)

                expected = create_expected(expected_cluster)
                tcm.assert_that_scalar_quantities_close_to(actual.x, expected.x, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.y, expected.y, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.depth, expected.depth, 6e-2)

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
        for actual_top, expected_top in [(make_measurement(13467.8, units.UsOilfield.LENGTH),
                                          make_measurement(13467.8, units.UsOilfield.LENGTH)),
                                         (make_measurement(3702.48, units.Metric.LENGTH),
                                          make_measurement(3702.48, units.Metric.LENGTH)),
                                         (make_measurement(13467.8, units.UsOilfield.LENGTH),
                                          make_measurement(4104.98, units.Metric.LENGTH)),
                                         (make_measurement(3702.48, units.Metric.LENGTH),
                                          make_measurement(12147.2, units.UsOilfield.LENGTH))]:
            with self.subTest(expected_top=actual_top):
                stub_net_stage = tsn.create_stub_net_stage(md_top=tsn.MeasurementAsUnit(actual_top, expected_top.unit))
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_top(expected_top.unit)
                assert_that(actual_top.magnitude, close_to(expected_top.magnitude, 0.05))
                assert_that(actual_top.unit, equal_to(expected_top.unit))

    def test_md_bottom(self):
        for actual_bottom, expected_bottom in [(make_measurement(13806.7, units.UsOilfield.LENGTH),
                                                make_measurement(13806.7, units.UsOilfield.LENGTH)),
                                               (make_measurement(4608.73, units.Metric.LENGTH),
                                                make_measurement(4608.73, units.Metric.LENGTH)),
                                               (make_measurement(12147.2, units.UsOilfield.LENGTH),
                                                make_measurement(3702.47, units.Metric.LENGTH)),
                                               (make_measurement(4608.73, units.Metric.LENGTH),
                                                make_measurement(15120.5, units.UsOilfield.LENGTH))]:
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

    def test_top_location_returns_stage_location_center_in_requested_unit(self):
        actual_tops = [AboutLocation(73080.67, -2189943.43, 2679.41, units.Metric.LENGTH),
                       AboutLocation(520513, 398950, 9447.48, units.UsOilfield.LENGTH),
                       AboutLocation(20437, -4844216, 5663.84, units.UsOilfield.LENGTH)]
        expected_tops = [AboutLocation(239766, -7184854, 8790.70, units.UsOilfield.LENGTH),
                         AboutLocation(520513, 398950, 9447.48, units.UsOilfield.LENGTH),
                         AboutLocation(6229.20, -1476516.99, 1726.34, units.Metric.LENGTH)]
        origin_references = [AboutOrigin(origins.WellReferenceFrameXy.WELL_HEAD,
                                         origins.DepthDatum.SEA_LEVEL),
                             AboutOrigin(origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                         origins.DepthDatum.GROUND_LEVEL),
                             AboutOrigin(origins.WellReferenceFrameXy.PROJECT,
                                         origins.DepthDatum.KELLY_BUSHING)]

        for (actual_top, expected_top, origin_reference) in \
                zip(actual_tops, expected_tops, origin_references):
            with self.subTest(actual_top=actual_top, expected_top=expected_top,
                              origin_reference=origin_reference):
                top_mock_func = mock_subsurface_point_func(actual_top, origin_reference.xy,
                                                           origin_reference.depth)
                stub_net_stage = tsn.create_stub_net_stage(stage_location_top=top_mock_func)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual = sut.top_location(expected_top.unit, origin_reference.xy, origin_reference.depth)

                expected = create_expected(expected_top)
                tcm.assert_that_scalar_quantities_close_to(actual.x, expected.x, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.y, expected.y, 6e-2)
                tcm.assert_that_scalar_quantities_close_to(actual.depth, expected.depth, 6e-2)

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
        expected_sampled_quantity_names = ['Pressure', 'Slurry Rate', 'Surface Proppant Concentration']
        stub_net_stage = tsn.create_stub_net_stage(treatment_curve_names=expected_sampled_quantity_names)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), has_items(ntc.TREATING_PRESSURE, ntc.SLURRY_RATE, ntc.TREATING_PRESSURE))
        toolz.valmap(assert_is_native_treatment_curve_facade, actual_curves)


def assert_is_native_treatment_curve_facade(curve):
    assert_that(curve, instance_of(ntc.NativeTreatmentCurveFacade))


if __name__ == '__main__':
    unittest.main()
