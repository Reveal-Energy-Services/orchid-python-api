#  Copyright (c) 2017-2024 KAPPA
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
import unittest.mock

import deal
from hamcrest import (assert_that, equal_to, empty, contains_exactly, has_items,
                      instance_of, calling, raises, same_instance, is_, none)
import pendulum as pdt
import toolz.curried as toolz

from orchid import (
    measurement as om,
    native_stage_adapter as nsa,
    native_treatment_curve_adapter as ntc,
    net_date_time as ndt,
    net_quantity as onq,
    reference_origins as origins,
    unit_system as units,
)

from tests import (
    custom_matchers as tcm,
    stub_net_date_time as tdt,
    stub_net as tsn,
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import IMutableStagePart
# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import (DateTime, DateTimeKind)
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

    def test_bottom_location_invokes_get_stage_location_bottom_correctly(self):
        bottom_mock_func = mock_subsurface_point_func(DONT_CARE_METRIC_LOCATION,
                                                      origins.WellReferenceFrameXy.WELL_HEAD,
                                                      origins.DepthDatum.KELLY_BUSHING)
        stub_net_stage = tsn.StageDto(stage_location_bottom=bottom_mock_func).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.bottom_location(units.Metric.LENGTH, origins.WellReferenceFrameXy.WELL_HEAD,
                            origins.DepthDatum.KELLY_BUSHING)

        stub_net_stage.GetStageLocationBottom.assert_called_with(origins.WellReferenceFrameXy.WELL_HEAD.value,
                                                                 origins.DepthDatum.KELLY_BUSHING.value)

    def test_bottom_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.Metric.PRESSURE
        assert_that(calling(sut.bottom_location).with_args(invalid_unit, origins.WellReferenceFrameXy.WELL_HEAD,
                                                           origins.DepthDatum.GROUND_LEVEL),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

    def test_center_location_invokes_get_stage_location_center_correctly(self):
        center_mock_func = mock_subsurface_point_func(DONT_CARE_US_OILFIELD_LOCATION,
                                                      origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                      origins.DepthDatum.GROUND_LEVEL)
        stub_net_stage = tsn.StageDto(stage_location_center=center_mock_func).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.center_location(units.UsOilfield.LENGTH, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                            origins.DepthDatum.GROUND_LEVEL)

        stub_net_stage.GetStageLocationCenter.assert_called_with(
            origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE.value, origins.DepthDatum.GROUND_LEVEL.value)

    def test_center_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.UsOilfield.POWER
        assert_that(calling(sut.center_location).with_args(invalid_unit, origins.WellReferenceFrameXy.PROJECT,
                                                           origins.DepthDatum.SEA_LEVEL),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

    def test_center_location_mdkb_returns_average_of_md_top_bottom(self):
        for actual_top_dto, actual_bottom_dto, expected_center_mdkb_dto, expected_center_mdkb_unit in [
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12035.8),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12200.0),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12117.9),
             units.UsOilfield.LENGTH),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 3668.52),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3718.55),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3693.53),
             units.Metric.LENGTH),
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12035.8),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12200.0),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3693.53),
             units.Metric.LENGTH),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 3668.52),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3718.55),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 12117.9),
             units.UsOilfield.LENGTH),
        ]:
            expected_center_mdkb = tsn.make_measurement(expected_center_mdkb_dto)
            with self.subTest(f'Stage center MDKB = {expected_center_mdkb:~P})'):
                stub_net_stage = tsn.StageDto(md_top=actual_top_dto,
                                              md_bottom=actual_bottom_dto).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_center_mdkb = sut.center_location_mdkb(expected_center_mdkb_unit)
                tcm.assert_that_measurements_close_to(actual_center_mdkb, expected_center_mdkb, 5e-2)

    def test_cluster_count(self):
        expected_cluster_count = 3
        stub_net_stage = tsn.StageDto(cluster_count=expected_cluster_count).create_net_stub()
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
        stub_net_stage = tsn.StageDto(stage_location_cluster=cluster_mock_func).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.cluster_location(units.UsOilfield.LENGTH,
                             DONT_CARE_CLUSTER_NO,
                             origins.WellReferenceFrameXy.PROJECT,
                             origins.DepthDatum.KELLY_BUSHING)

        stub_net_stage.GetStageLocationCluster.assert_called_with(
            DONT_CARE_CLUSTER_NO, origins.WellReferenceFrameXy.PROJECT.value,
            origins.DepthDatum.KELLY_BUSHING.value)

    def test_cluster_location_invalid_cluster_no_raises_contract_error(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(calling(sut.cluster_location).with_args(units.UsOilfield.LENGTH, -1,
                                                            origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                            origins.DepthDatum.GROUND_LEVEL),
                    raises(deal.PreContractError))

    def test_cluster_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.Metric.DENSITY
        assert_that(calling(sut.cluster_location).with_args(invalid_unit,
                                                            DONT_CARE_CLUSTER_NO,
                                                            origins.WellReferenceFrameXy.PROJECT,
                                                            origins.DepthDatum.KELLY_BUSHING),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

    def test_display_stage_number(self):
        expected_display_stage_number = 11
        stub_net_stage = tsn.StageDto(display_stage_no=expected_display_stage_number).create_net_stub()
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
                stub_net_stage = tsn.StageDto(isip=orchid_actual).create_net_stub()
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
                stub_net_stage = tsn.StageDto(isip=net_isip).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)
                expected = tsn.make_measurement(expected_dto)
                tcm.assert_that_measurements_close_to(sut.isip_in_pressure_unit(expected_dto.unit), expected, tolerance)

    def test_isip_all_non_unit_errors(self):
        expected_pressure_dto = tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 1414)
        stub_net_stage = tsn.StageDto(isip=expected_pressure_dto).create_net_stub()
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
                stub_net_stage = tsn.StageDto(md_bottom=actual_bottom_dto).create_net_stub()
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
                stub_net_stage = tsn.StageDto(md_top=actual_top_dto).create_net_stub()
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
                stub_net_stage = tsn.StageDto(pnet=orchid_actual).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)

                tcm.assert_that_measurements_close_to(sut.pnet, expected, tolerance)

    def test_pnet_all(self):
        net_pnets, expected_matrix = self._make_pressure_test_pairs()
        for net_pnet, expected_pair in zip(net_pnets, expected_matrix):
            expected_dto, tolerance = expected_pair
            with self.subTest(f'Test .NET shmin {net_pnet} in US oilfield units, "{expected_dto.unit.value.unit:~P}"'):
                stub_net_stage = tsn.StageDto(pnet=net_pnet).create_net_stub()
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
                stub_net_stage = tsn.StageDto(shmin=orchid_actual).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)

                tcm.assert_that_measurements_close_to(sut.shmin, expected, tolerance)

    def test_shmin_all(self):
        net_shmins, expected_matrix = self._make_pressure_test_pairs()
        for net_shmin, expected_pair in zip(net_shmins, expected_matrix):
            expected_dto, tolerance = expected_pair
            with self.subTest(f'Test .NET shmin {net_shmin} in US oilfield units, "{expected_dto.unit.value.unit:~P}"'):
                stub_net_stage = tsn.StageDto(shmin=net_shmin).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)
                expected = tsn.make_measurement(expected_dto)
                tcm.assert_that_measurements_close_to(sut.shmin_in_pressure_unit(expected_dto.unit),
                                                      expected, tolerance)

    def test_stage_length(self):
        for actual_top_dto, actual_bottom_dto, expected_stage_length_dto in [
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 11568),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 11725),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 158)),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 3526),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3574),
             tsn.make_measurement_dto(units.Metric.LENGTH, 48)),
            (tsn.make_measurement_dto(units.UsOilfield.LENGTH, 11568),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 11725),
             tsn.make_measurement_dto(units.Metric.LENGTH, 48)),
            (tsn.make_measurement_dto(units.Metric.LENGTH, 3526),
             tsn.make_measurement_dto(units.Metric.LENGTH, 3574),
             tsn.make_measurement_dto(units.UsOilfield.LENGTH, 158)),
        ]:
            expected_stage_length = tsn.make_measurement(expected_stage_length_dto)
            with self.subTest(f'Test stage length with expected stage length {expected_stage_length:~P}'):
                stub_net_stage = tsn.StageDto(md_top=actual_top_dto,
                                              md_bottom=actual_bottom_dto).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_stage_length = sut.stage_length(expected_stage_length_dto.unit)
                tcm.assert_that_measurements_close_to(actual_stage_length, expected_stage_length, decimal.Decimal('1'))

    def test_stage_parts(self):
        for stage_part_dtos in [
            (),
            (tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_A),),
            [tsn.StagePartDto(object_id=oid) for oid in [tsn.DONT_CARE_ID_A, tsn.DONT_CARE_ID_B, tsn.DONT_CARE_ID_C]],
        ]:
            with self.subTest(f'Expecting {len(stage_part_dtos)} stage parts'):
                stub_net_stage = tsn.StageDto(stage_parts=stage_part_dtos).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)

                assert_that(len(sut.stage_parts()), equal_to(len(stage_part_dtos)))

    def test_start_time_if_neither_nat_nor_null(self):
        start_time_dto = tdt.TimePointDto(2024, 10, 31, 7, 31, 27, 357000 * om.registry.microseconds)
        stub_net_stage = tsn.StageDto(start_time=start_time_dto.to_datetime()).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_start_time = sut.start_time
        assert_that(actual_start_time, equal_to(start_time_dto.to_datetime()))

    def test_start_time_if_nat(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        stub_net_stage.StartTime = DateTime.MinValue
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_start_time = sut.start_time
        assert_that(actual_start_time, equal_to(ndt.NAT))

    def test_start_time_if_null(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        stub_net_stage.StartTime = None
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_start_time = sut.start_time
        assert_that(actual_start_time, equal_to(ndt.NAT))

    def test_stop_time_if_neither_nat_nor_null(self):
        stop_time_dto = tdt.TimePointDto(2016, 3, 31, 3, 31, 30, 947000 * om.registry.microseconds)
        stub_net_stage = tsn.StageDto(stop_time=stop_time_dto.to_datetime()).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_stop_time = sut.stop_time
        assert_that(actual_stop_time, equal_to(stop_time_dto.to_datetime()))

    def test_stop_time_if_nat(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        stub_net_stage.StopTime = ndt.NET_NAT
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_stop_time = sut.stop_time
        assert_that(actual_stop_time, equal_to(ndt.NAT))

    def test_stop_time_if_null(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        stub_net_stage.StopTime = None
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_stop_time = sut.stop_time
        assert_that(actual_stop_time, equal_to(ndt.NAT))

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
                subsurface_point_mock_func = mock_subsurface_point_func(net_point, origin_reference.xy.value,
                                                                        origin_reference.depth.value)
                actual = nsa.subsurface_point_in_length_unit(origin_reference.depth, origin_reference.xy,
                                                             expected_point[-1], subsurface_point_mock_func)

                expected = create_expected(expected_point)
                tcm.assert_that_measurements_close_to(actual.x, expected.x, tolerance.x)
                tcm.assert_that_measurements_close_to(actual.y, expected.y, tolerance.y)
                tcm.assert_that_measurements_close_to(actual.depth, expected.depth, tolerance.depth)

    def test_time_range(self):
        start_time_dto = tdt.TimePointDto(2024, 10, 31, 7, 31, 27, 357000 * om.registry.microseconds)
        stop_time_dto = tdt.TimePointDto(2016, 3, 31, 3, 31, 30, 947000 * om.registry.microseconds)
        stub_net_stage = tsn.StageDto(start_time=start_time_dto.to_datetime(),
                                      stop_time=stop_time_dto.to_datetime()).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.time_range, equal_to(pdt.period(start_time_dto.to_datetime(),
                                                        stop_time_dto.to_datetime())))

    def test_top_location_invokes_get_stage_location_top_correctly(self):
        top_mock_func = mock_subsurface_point_func(DONT_CARE_US_OILFIELD_LOCATION,
                                                   origins.WellReferenceFrameXy.PROJECT,
                                                   origins.DepthDatum.SEA_LEVEL)
        stub_net_stage = tsn.StageDto(stage_location_top=top_mock_func).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        sut.top_location(units.UsOilfield.LENGTH, origins.WellReferenceFrameXy.PROJECT,
                         origins.DepthDatum.SEA_LEVEL)

        stub_net_stage.GetStageLocationTop.assert_called_with(
            origins.WellReferenceFrameXy.PROJECT.value, origins.DepthDatum.SEA_LEVEL.value)

    def test_top_location_raises_error_if_not_length_unit(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        invalid_unit = units.UsOilfield.PROPPANT_CONCENTRATION
        assert_that(calling(sut.top_location).with_args(invalid_unit,
                                                        origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                        origins.DepthDatum.KELLY_BUSHING),
                    raises(deal.PreContractError, pattern=f'must be a unit system length'))

    def test_treatment_curves_no_curves(self):
        stub_net_stage = tsn.StageDto().create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curve = sut.treatment_curves()
        assert_that(actual_curve, empty())

    def test_treatment_curves_one_curve(self):
        expected_sampled_quantity_name = ntc.TreatmentCurveTypes.SLURRY_RATE
        stub_net_stage = tsn.StageDto(treatment_curve_names=[expected_sampled_quantity_name]).create_net_stub()
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_curves = sut.treatment_curves()
        assert_that(actual_curves.keys(), contains_exactly(expected_sampled_quantity_name))
        toolz.valmap(assert_is_native_treatment_curve_facade, actual_curves)

    def test_treatment_curves_many_curves(self):
        for proppant_curve_type in [
            ntc.TreatmentCurveTypes.SURFACE_PROPPANT_CONCENTRATION,
            ntc.TreatmentCurveTypes.DOWNHOLE_PROPPANT_CONCENTRATION,
        ]:
            proppant_curve_description = proppant_curve_type.value.lower()
            with self.subTest(f'Pressure, rate and {proppant_curve_description}'):
                expected_sampled_quantity_names = [ntc.TreatmentCurveTypes.TREATING_PRESSURE,
                                                   ntc.TreatmentCurveTypes.SLURRY_RATE,
                                                   proppant_curve_type]
                stub_net_stage = tsn.StageDto(treatment_curve_names=expected_sampled_quantity_names).create_net_stub()
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_curves = sut.treatment_curves()
                assert_that(actual_curves.keys(), has_items(ntc.TreatmentCurveTypes.TREATING_PRESSURE,
                                                            ntc.TreatmentCurveTypes.SLURRY_RATE,
                                                            proppant_curve_type))
                toolz.valmap(assert_is_native_treatment_curve_facade, actual_curves)

    @staticmethod
    def _make_pressure_test_pairs():
        # noinspection PyUnresolvedReferences
        net_pressures = [
            tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 1414),
            tsn.make_measurement_dto(units.Metric.PRESSURE, 3.142),
            # Remember, functions like `onq.net_pressure_from_bars` are created *dynamically* when the
            # module is loaded. See the comments preceding `onq.net_creator_attributes`.
            onq.net_pressure_from_bars(0.1506),
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


# TODO: Handle set start/stop edge cases
# I have seen an error in the integration tests in which Orchid raised an exception because the `StartTime` of an
# `IStage` was *after* the `StopTime`. However, when I tried to duplicate what I though caused this error, I could
# not create a failing test. I am leaving this to-do reminder and these test ideas for further work.
# Test ideas
# - Change start time
#   - Error when many stage parts and start after first stage start
# - Change stop time
#   - Error when many stage parts and stop before last stage start
class TestNativeStageAdapterSetter(unittest.TestCase):

    def test_set_start_time_if_single_part(self):
        ante_start_time_dto = tdt.TimePointDto(2025, 8, 27, 12, 4, 12, 677 * om.registry.milliseconds)
        stop_time_dto = tdt.TimePointDto(2025, 8, 27, 13, 46, 59, 506 * om.registry.milliseconds)
        builder = NativeStageAdapterBuilderForSetter(ante_start_time_dto, stop_time_dto)
        sut = builder.build()

        post_start_time_dto = tdt.TimePointDto(2025, 8, 27, 7, 5, 54, 66 * om.registry.milliseconds)
        sut.time_range = pdt.period(post_start_time_dto.to_datetime(), stop_time_dto.to_datetime())

        assert_correct_net_calls_when_setting_time_range(builder.stub_net_stage_part,
                                                         builder.stub_net_mutable_stage_part,
                                                         post_start_time_dto,
                                                         stop_time_dto)

    def test_set_stop_time_if_single_part(self):
        start_time_dto = tdt.TimePointDto(2022, 11, 25, 4, 21, 53, 846 * om.registry.milliseconds)
        ante_stop_time_dto = tdt.TimePointDto(2022, 11, 25, 7, 7, 46, 31 * om.registry.milliseconds)
        builder = NativeStageAdapterBuilderForSetter(start_time_dto, ante_stop_time_dto)
        sut = builder.build()

        post_stop_time_dto = tdt.TimePointDto(2022, 11, 25, 5, 32, 42, 406 * om.registry.milliseconds)
        sut.time_range = pdt.period(start_time_dto.to_datetime(), post_stop_time_dto.to_datetime())

        assert_correct_net_calls_when_setting_time_range(builder.stub_net_stage_part,
                                                         builder.stub_net_mutable_stage_part,
                                                         start_time_dto, post_stop_time_dto)

    @unittest.mock.patch('orchid.native_stage_adapter.fdf.create')
    def test_set_start_stop_time_if_no_parts(self, stub_factory_create):
        stub_net_stage_part = tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_A).create_net_stub()
        stub_fd_factory = unittest.mock.MagicMock(name='stub_fd_factory')
        stub_fd_factory.CreateStagePart = unittest.mock.MagicMock('stub_create_stage_part',
                                                                  return_value=stub_net_stage_part)
        stub_factory_create.return_value = stub_fd_factory

        stub_net_mutable_stage = tsn.MutableStagePartDto().create_net_stub()
        stub_net_stage = tsn.StageDto().create_net_stub()
        stub_net_stage.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_stage)

        sut = nsa.NativeStageAdapter(stub_net_stage)

        post_start_time_dto = tdt.TimePointDto(2020, 5, 10, 22, 36, 8, 58 * om.registry.milliseconds)
        post_stop_time_dto = tdt.TimePointDto(2020, 5, 11, 0, 55, 11, 61 * om.registry.milliseconds)
        sut.time_range = pdt.period(post_start_time_dto.to_datetime(), post_stop_time_dto.to_datetime())

        # Expect one call to create a stage part with the post start and stop times
        stub_fd_factory.CreateStagePart.assert_called_once()
        stage_arg, start_arg, stop_arg, isip_arg = stub_fd_factory.CreateStagePart.call_args_list[0].args
        assert_that(stage_arg, same_instance(stub_net_stage))
        assert_that(start_arg.ToString('o'), equal_to(post_start_time_dto.to_net_date_time().ToString('o')))
        assert_that(stop_arg.ToString('o'), equal_to(post_stop_time_dto.to_net_date_time().ToString('o')))
        assert_that(isip_arg, is_(none()))

        # Expect calls to add the newly created stage part to the Parts of the mutable stage
        stub_net_stage.ToMutable.assert_called_once_with()
        stub_net_mutable_stage.Parts.Add.assert_called_once_with(stub_net_stage_part)

    def test_set_start_stop_time_if_many_parts(self):
        ante_start_time_dtos = [
            tdt.TimePointDto(2022, 2, 14, 22, 35, 9, 273 * om.registry.milliseconds),
            tdt.TimePointDto(2022, 2, 15, 2, 51, 4, 216 * om.registry.milliseconds),
            tdt.TimePointDto(2022, 2, 15, 7, 17, 2, 360 * om.registry.milliseconds),
        ]
        ante_start_date_times = [start_time_dto.to_datetime() for start_time_dto in ante_start_time_dtos]
        ante_stop_time_dtos = [
            tdt.TimePointDto(2022, 2, 15, 0, 57, 49, 123 * om.registry.milliseconds),
            tdt.TimePointDto(2022, 2, 15, 4, 26, 5, 21 * om.registry.milliseconds),
            tdt.TimePointDto(2022, 2, 15, 9, 30, 57, 983 * om.registry.milliseconds),
        ]
        ante_stop_date_times = [stop_time_dto.to_datetime() for stop_time_dto in ante_stop_time_dtos]
        part_object_ids = [
            tsn.DONT_CARE_ID_A,
            tsn.DONT_CARE_ID_B,
            tsn.DONT_CARE_ID_C,
        ]
        stub_net_mutable_stage_part = [tsn.MutableStagePartDto().create_net_stub()
                                       for _ in range(len(ante_start_time_dtos))]
        stub_net_stage_parts = [tsn.StagePartDto(object_id=args[0],
                                                 start_time=args[1],
                                                 stop_time=args[2]).create_net_stub()
                                for args in zip(part_object_ids, ante_start_date_times,
                                                ante_stop_date_times)]
        for i in range(len(stub_net_mutable_stage_part)):
            # noinspection PyPep8Naming
            stub_net_stage_parts[i].ToMutable = unittest.mock.MagicMock(
                return_value=stub_net_mutable_stage_part[i])

        stub_net_stage = tsn.StageDto(start_time=ante_start_date_times[0],
                                      stage_parts=stub_net_stage_parts,
                                      stop_time=ante_stop_date_times[-1]).create_net_stub()

        sut = nsa.NativeStageAdapter(stub_net_stage)

        post_start_time_dto = tdt.TimePointDto(2022, 2, 14, 22, 12, 12, 650 * om.registry.milliseconds)
        post_stop_time_dto = tdt.TimePointDto(2022, 2, 15, 9, 2, 12, 912 * om.registry.milliseconds)
        sut.time_range = pdt.period(post_start_time_dto.to_datetime(), post_stop_time_dto.to_datetime())

        # Expect one call to first mutable stage part
        stub_net_stage_parts[0].ToMutable.assert_called_once_with()
        # One call to last mutable stage part
        stub_net_stage_parts[-1].ToMutable.assert_called_once_with()
        # And no calls to middle mutable stage part
        stub_net_stage_parts[1].ToMutable.assert_not_called()

        # First call to `SetStartStopTimes` contains new start and old stop
        first_call = stub_net_mutable_stage_part[0].SetStartStopTimes.call_args_list[0]
        assert_that(first_call.args[0].ToString('o'),
                    equal_to(post_start_time_dto.to_net_date_time().ToString('o')))
        assert_that(first_call.args[1].ToString('o'),
                    equal_to(ante_stop_time_dtos[0].to_net_date_time().ToString('o')))

        # Second call to `SetStartStopTimes` contains old start and new stop
        second_call = stub_net_mutable_stage_part[-1].SetStartStopTimes.call_args_list[0]
        assert_that(second_call.args[0].ToString('o'),
                    equal_to(ante_start_time_dtos[-1].to_net_date_time().ToString('o')))
        assert_that(second_call.args[1].ToString('o'),
                    equal_to(post_stop_time_dto.to_net_date_time().ToString('o')))


def assert_correct_net_calls_when_setting_time_range(stub_net_stage_part, stub_net_mutable_stage_part,
                                                     expected_start_time_dto, expected_stop_time_dto):
    # Expect one call with no arguments
    stub_net_stage_part.ToMutable.assert_called_once_with()
    # First call contains new start and old stop
    stub_net_mutable_stage_part.SetStartStopTimes.assert_called_once()
    actual_call = stub_net_mutable_stage_part.SetStartStopTimes.call_args_list[0]
    assert_that(actual_call.args[0].ToString('o'),
                equal_to(expected_start_time_dto.to_net_date_time().ToString('o')))
    assert_that(actual_call.args[1].ToString('o'),
                equal_to(expected_stop_time_dto.to_net_date_time().ToString('o')))


class NativeStageAdapterBuilderForSetter:
    """
    This class builds `NativeStageAdapter` instances for testing.

    However, to support testing the calls made to the underlying .NET `IStage` and
    `IStagePart` instances, this class exposes the `mock` instances for those .NET instances.
    """

    def __init__(self, start_time_dto, stop_time_dto):
        self.start_time_dto = start_time_dto
        self.stop_time_dto = stop_time_dto
        self.stub_net_mutable_stage_part = None
        self.stub_net_stage_part = None

    def build(self) -> nsa.NativeStageAdapter:
        self.stub_net_mutable_stage_part = tsn.MutableStagePartDto().create_net_stub()
        self.stub_net_stage_part = tsn.StagePartDto(object_id=tsn.DONT_CARE_ID_A,
                                                    start_time=self.start_time_dto.to_datetime(),
                                                    stop_time=self.stop_time_dto.to_datetime()).create_net_stub()
        self.stub_net_stage_part.ToMutable = unittest.mock.MagicMock(return_value=self.stub_net_mutable_stage_part)

        stub_net_stage = tsn.StageDto(start_time=self.start_time_dto.to_datetime(),
                                      stage_parts=[self.stub_net_stage_part],
                                      stop_time=self.stop_time_dto.to_datetime()).create_net_stub()

        return nsa.NativeStageAdapter(stub_net_stage)


def assert_is_native_treatment_curve_facade(curve):
    assert_that(curve, instance_of(ntc.NativeTreatmentCurveAdapter))


if __name__ == '__main__':
    unittest.main()
