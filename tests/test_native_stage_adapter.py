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
    native_stage_adapter as nsa,
    native_treatment_curve_adapter as ntc,
    reference_origins as origins,
    unit_system as units,
)

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)

# noinspection PyUnresolvedReferences
import UnitsNet

AboutLocation = namedtuple('AboutLocation', ['x', 'y', 'depth', 'unit'])
AboutOrigin = namedtuple('AboutOrigin', ['xy', 'depth'])
AboutTolerance = namedtuple('AboutTolerance', ['x', 'y', 'depth'])
StubCalculateResult = namedtuple('CalculateResults', ['measurement', 'warnings'])

# Location values needed for tests but not tested in tests
DONT_CARE_CLUSTER_NO = 3414
DONT_CARE_METRIC_LOCATION = AboutLocation(314200, 1414000, 1717, units.Metric.LENGTH)
DONT_CARE_US_OILFIELD_LOCATION = AboutLocation(271800, 3142000, 14140, units.UsOilfield.LENGTH)


def _make_subsurface_coordinate(coord, unit):
    return tsn.make_net_measurement(tsn.make_measurement_dto(unit, coord))


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
    make_measurement_with_unit = units.make_measurement(expected_location[-1])
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

    def test_bottom_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.Metric.PRESSURE
        assert_that(calling(sut.bottom_location).with_args(invalid_unit, origins.WellReferenceFrameXy.WELL_HEAD,
                                                           origins.DepthDatum.GROUND_LEVEL),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

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

    def test_center_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.UsOilfield.POWER
        assert_that(calling(sut.center_location).with_args(invalid_unit, origins.WellReferenceFrameXy.PROJECT,
                                                           origins.DepthDatum.SEA_LEVEL),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

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

        cluster_mock_func = mock_cluster_subsurface_point_func(DONT_CARE_US_OILFIELD_LOCATION,
                                                               DONT_CARE_CLUSTER_NO,
                                                               origins.WellReferenceFrameXy.PROJECT,
                                                               origins.DepthDatum.KELLY_BUSHING)
        stub_net_stage = tsn.create_stub_net_stage(stage_location_cluster=cluster_mock_func)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.cluster_location(units.UsOilfield.LENGTH,
                             DONT_CARE_CLUSTER_NO,
                             origins.WellReferenceFrameXy.PROJECT,
                             origins.DepthDatum.KELLY_BUSHING)

        stub_net_stage.GetStageLocationCluster.assert_called_with(
            DONT_CARE_CLUSTER_NO, origins.WellReferenceFrameXy.PROJECT.value,
            origins.DepthDatum.KELLY_BUSHING.value)

    def test_cluster_location_invalid_cluster_no_raises_contract_error(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(calling(sut.cluster_location).with_args(units.UsOilfield.LENGTH, -1,
                                                            origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                            origins.DepthDatum.GROUND_LEVEL),
                    raises(deal.PreContractError))

    def test_cluster_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.Metric.DENSITY
        assert_that(calling(sut.cluster_location).with_args(invalid_unit,
                                                            DONT_CARE_CLUSTER_NO,
                                                            origins.WellReferenceFrameXy.PROJECT,
                                                            origins.DepthDatum.KELLY_BUSHING),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

    def test_display_stage_number(self):
        expected_display_stage_number = 11
        stub_net_stage = tsn.create_stub_net_stage(display_stage_no=expected_display_stage_number)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.display_stage_number, equal_to(expected_display_stage_number))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_isip(self, mock_as_unit_system):
        for orchid_actual, expected, project_units, tolerance in [
            (tsn.MeasurementDto(4901, units.UsOilfield.PRESSURE),
             4901 * om.registry.psi, units.UsOilfield, decimal.Decimal('1')),
            (tsn.MeasurementDto(33.79e3, units.Metric.PRESSURE),
             33.79e3 * om.registry.kPa, units.Metric, decimal.Decimal('0.01')),
            (tsn.MeasurementDto(4901, units.UsOilfield.PRESSURE),
             33.79e3 * om.registry.kPa, units.Metric, decimal.Decimal('7')),
            (tsn.MeasurementDto(33.79e3, units.Metric.PRESSURE),
             4901 * om.registry.psi, units.UsOilfield, decimal.Decimal('2')),
        ]:
            with self.subTest(self.in_project_units_test_description('ISIP', orchid_actual, expected, project_units)):
                mock_as_unit_system.return_value = project_units
                stub_net_stage = tsn.create_stub_net_stage(isip=orchid_actual)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                tcm.assert_that_measurements_close_to(sut.isip, expected, tolerance)

    @staticmethod
    def in_project_units_test_description(phenomenon, orchid_actual, expected, project_units):
        return (f'Test actual {phenomenon}, {orchid_actual.magnitude} {orchid_actual.unit.value.unit:~P},'
                f' to expected, {expected:~P}, in project units, {project_units}.')

    def test_isip_all(self):
        net_isips, expected_matrix = self._make_pressure_test_pairs()
        for net_isip, expected_pair in zip(net_isips, expected_matrix):
            expected_dto, tolerance = expected_pair
            with self.subTest(f'Test .NET shmin {net_isip} in US oilfield units, "{expected_dto.unit.value.unit:~P}"'):
                stub_net_stage = tsn.create_stub_net_stage(isip=net_isip)
                sut = nsa.NativeStageAdapter(stub_net_stage)
                expected = tsn.make_measurement(expected_dto)
                tcm.assert_that_measurements_close_to(sut.isip_in_pressure_unit(expected_dto.unit), expected, tolerance)

    def test_isip_all_non_unit_errors(self):
        expected_pressure_dto = tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 1414)
        stub_net_stage = tsn.create_stub_net_stage(isip=expected_pressure_dto)
        sut = nsa.NativeStageAdapter(stub_net_stage)
        assert_that(calling(sut.isip_in_pressure_unit).with_args(units.UsOilfield.LENGTH),
                    raises(deal.PreContractError))

    def test_md_bottom(self):
        for actual_bottom_dto, expected_bottom_dto in [
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 13806.7),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 13806.7)),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 4608.73),
             tsn.make_measurement_dto(units.Metric.LENGTH, 4608.73)),
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12147.2),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3702.47)),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 4608.73),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 15120.5)),
        ]:
            expected_bottom = tsn.make_measurement(expected_bottom_dto)
            with self.subTest(f'Test MD bottom {expected_bottom:~P}'):
                stub_net_stage = tsn.create_stub_net_stage(md_bottom=actual_bottom_dto)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_bottom = sut.md_bottom(expected_bottom_dto.unit)
                tcm.assert_that_measurements_close_to(actual_bottom, expected_bottom, 5e-2)

    def test_md_top(self):
        for actual_top_dto, expected_top_dto in [
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 13467.8),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 13467.8)),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 3702.48),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3702.48)),
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 13467.8),
             tsn.make_measurement_dto(units.Metric.LENGTH, 4104.98)),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 3702.48),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12147.2)),
        ]:
            expected_top = tsn.make_measurement(expected_top_dto)
            with self.subTest(f'Test MD top {expected_top:~P}'):
                stub_net_stage = tsn.create_stub_net_stage(md_top=actual_top_dto)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_top(expected_top_dto.unit)
                tcm.assert_that_measurements_close_to(actual_top, expected_top, 5e-2)

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_pnet(self, mock_as_unit_system):
        for orchid_actual, expected, project_units, tolerance in [
            (tsn.MeasurementDto(46.93e3, units.UsOilfield.PRESSURE),
             46.93e3 * om.registry.psi, units.UsOilfield, decimal.Decimal('1')),
            (tsn.MeasurementDto(323.6e3, units.Metric.PRESSURE),
             323.6e3 * om.registry.kPa, units.Metric, decimal.Decimal('0.01')),
            (tsn.MeasurementDto(46.93e3, units.UsOilfield.PRESSURE),
             323.6e3 * om.registry.kPa, units.Metric, decimal.Decimal('0.1e3')),
            (tsn.MeasurementDto(323.6e3, units.Metric.PRESSURE),
             46.93e3 * om.registry.psi, units.UsOilfield, decimal.Decimal('0.02e3')),
        ]:
            with self.subTest(self.in_project_units_test_description('PNET', orchid_actual, expected, project_units)):
                mock_as_unit_system.return_value = project_units
                stub_net_stage = tsn.create_stub_net_stage(pnet=orchid_actual)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                tcm.assert_that_measurements_close_to(sut.pnet, expected, tolerance)

    def test_pnet_all(self):
        net_pnets, expected_matrix = self._make_pressure_test_pairs()
        for net_pnet, expected_pair in zip(net_pnets, expected_matrix):
            expected_dto, tolerance = expected_pair
            with self.subTest(f'Test .NET shmin {net_pnet} in US oilfield units, "{expected_dto.unit.value.unit:~P}"'):
                stub_net_stage = tsn.create_stub_net_stage(pnet=net_pnet)
                sut = nsa.NativeStageAdapter(stub_net_stage)
                expected = tsn.make_measurement(expected_dto)
                tcm.assert_that_measurements_close_to(sut.pnet_in_pressure_unit(expected_dto.unit), expected, tolerance)

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_shmin(self, mock_as_unit_system):
        for orchid_actual, expected, project_units, tolerance in [
            (tsn.MeasurementDto(2.392, units.UsOilfield.PRESSURE),
             2.392 * om.registry.psi, units.UsOilfield, decimal.Decimal('1')),
            (tsn.MeasurementDto(16.49, units.Metric.PRESSURE),
             16.49 * om.registry.kPa, units.Metric, decimal.Decimal('0.01')),
            (tsn.MeasurementDto(2.392, units.UsOilfield.PRESSURE),
                16.49 * om.registry.kPa, units.Metric, decimal.Decimal('0.01')),
            (tsn.MeasurementDto(16.49, units.Metric.PRESSURE),
             2.392 * om.registry.psi, units.UsOilfield, decimal.Decimal('0.001')),
        ]:
            with self.subTest(self.in_project_units_test_description('shmin', orchid_actual, expected, project_units)):
                mock_as_unit_system.return_value = project_units
                stub_net_stage = tsn.create_stub_net_stage(shmin=orchid_actual)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                tcm.assert_that_measurements_close_to(sut.shmin, expected, tolerance)

    def test_shmin_all(self):
        net_shmins, expected_matrix = self._make_pressure_test_pairs()
        for net_shmin, expected_pair in zip(net_shmins, expected_matrix):
            expected_dto, tolerance = expected_pair
            with self.subTest(f'Test .NET shmin {net_shmin} in US oilfield units, "{expected_dto.unit.value.unit:~P}"'):
                stub_net_stage = tsn.create_stub_net_stage(shmin=net_shmin)
                sut = nsa.NativeStageAdapter(stub_net_stage)
                expected = tsn.make_measurement(expected_dto)
                tcm.assert_that_measurements_close_to(sut.shmin_in_pressure_unit(expected_dto.unit),
                                                      expected, tolerance)

    def test_subsurface_point_in_length_unit(self):
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
                actual = nsa.subsurface_point_in_length_unit(origin_reference.depth, origin_reference.xy,
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

    def test_top_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.create_stub_net_stage()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.UsOilfield.PROPPANT_CONCENTRATION
        assert_that(calling(sut.top_location).with_args(invalid_unit,
                                                        origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                        origins.DepthDatum.KELLY_BUSHING),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

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

    @staticmethod
    def _make_pressure_test_pairs():
        net_pressures = [
            tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 1414),
            tsn.make_measurement_dto(units.Metric.PRESSURE, 3.142),
            UnitsNet.Pressure.FromBars(UnitsNet.QuantityValue.op_Implicit(0.1506)),
        ]
        expected_measurements = [
            (tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 1414), decimal.Decimal('1')),
            (tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 0.4557), decimal.Decimal('0.0001')),
            (tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 2.184), decimal.Decimal('0.001')),
            (tsn.make_measurement_dto(units.Metric.PRESSURE, 9749), decimal.Decimal('1')),
            (tsn.make_measurement_dto(units.Metric.PRESSURE, 3.142), decimal.Decimal('0.001')),
            (tsn.make_measurement_dto(units.Metric.PRESSURE, 15.06), decimal.Decimal('0.01')),
        ]
        return net_pressures * 2, expected_measurements


def assert_is_native_treatment_curve_facade(curve):
    assert_that(curve, instance_of(ntc.NativeTreatmentCurveAdapter))


if __name__ == '__main__':
    unittest.main()
