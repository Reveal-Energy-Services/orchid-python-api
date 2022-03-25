#  Copyright (c) 2017-2022 Reveal Energy Services, Inc 
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

import dataclasses as dc
import decimal
import unittest.mock
import uuid

from hamcrest import (assert_that, equal_to, instance_of, is_, empty, contains_exactly,
                      calling, raises)

from orchid import (
    measurement as om,
    native_trajectory_adapter as nta,
    native_stage_adapter as nsa,
    native_well_adapter as nwa,
    reference_origins as origins,
    unit_system as units,
)

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)


class TestNativeWellAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name(self):
        expected_well_display_name = 'agiles'
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_native_well.DisplayName = expected_well_display_name
        sut = nwa.NativeWellAdapter(stub_native_well)

        assert_that(sut.display_name, equal_to(expected_well_display_name))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_ground_level_elevation_above_sea_level(self, mock_as_unit_system):
        for orchid_actual, expected, project_units, tolerance in [
            (tsn.MeasurementDto(4537, units.UsOilfield.LENGTH),
             4537 * om.registry.ft, units.UsOilfield, decimal.Decimal('1')),
            (tsn.MeasurementDto(1383, units.Metric.LENGTH),
             1383 * om.registry.m, units.Metric, decimal.Decimal('1')),
            (tsn.MeasurementDto(4537, units.UsOilfield.LENGTH),
             1383 * om.registry.m, units.Metric, decimal.Decimal('0.4')),
            (tsn.MeasurementDto(1383, units.Metric.LENGTH),
             4537 * om.registry.ft, units.UsOilfield, decimal.Decimal('4')),
        ]:
            with self.subTest(f'Test ground level elevation, {expected:~P}'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(ground_level_elevation_above_sea_level=orchid_actual)
                sut = nwa.NativeWellAdapter(stub_native_well)
                tcm.assert_that_measurements_close_to(
                    sut.ground_level_elevation_above_sea_level, expected, tolerance)

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_kelly_bushing_height_above_ground_level(self, mock_as_unit_system):
        for orchid_actual, expected, project_units, tolerance in [
            (tsn.MeasurementDto(30.86, units.UsOilfield.LENGTH),
             30.86 * om.registry.ft, units.UsOilfield, decimal.Decimal('0.01')),
            (tsn.MeasurementDto(9.406, units.Metric.LENGTH),
             9.406 * om.registry.m, units.Metric, decimal.Decimal('0.01')),
            (tsn.MeasurementDto(30.86, units.UsOilfield.LENGTH),
             9.406 * om.registry.m, units.Metric, decimal.Decimal('0.004')),
            (tsn.MeasurementDto(9.406, units.Metric.LENGTH),
             30.86 * om.registry.ft, units.UsOilfield, decimal.Decimal('0.004')),
        ]:
            with self.subTest(f'Test kelly bushing height above ground level, {expected:~P}'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(kelly_bushing_height_above_ground_level=orchid_actual)
                sut = nwa.NativeWellAdapter(stub_native_well)
                tcm.assert_that_measurements_close_to(
                    sut.kelly_bushing_height_above_ground_level, expected, tolerance)

    def test_stages(self):
        for stage_dtos in (
                (),
                ({'object_id': tsn.DONT_CARE_ID_A, 'name': 'romanorm', 'display_name': ''},),
                # Don't care about object IDs but must be unique
                ({'object_id': tsn.DONT_CARE_ID_B, 'name': 'mea', 'display_name': ''},
                 {'object_id': tsn.DONT_CARE_ID_C, 'name': 'monueras', 'display_name': ''},
                 {'object_id': tsn.DONT_CARE_ID_D, 'name': 'animi', 'display_name': ''})
        ):
            get_stage_dtos_property = tsn.get_dtos_property(stage_dtos)
            expected_object_ids = get_stage_dtos_property('object_id', transform=uuid.UUID)
            expected_names = get_stage_dtos_property('name')
            with self.subTest(f'Verify monitors object IDs, {expected_object_ids}'
                              f' and names, {expected_names}'):
                stub_native_well = tsn.create_stub_net_well(stage_dtos=stage_dtos)
                sut = nwa.NativeWellAdapter(stub_native_well)

                assert_that(sut.stages().all_object_ids(), contains_exactly(*expected_object_ids))
                assert_that(sut.stages().all_names(), contains_exactly(*expected_names))

    def test_trajectory(self):
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_trajectory = unittest.mock.MagicMock(name='stub_native_trajectory')
        stub_native_well.Trajectory = stub_trajectory
        sut = nwa.NativeWellAdapter(stub_native_well)

        # noinspection PyTypeChecker
        assert_that(sut.trajectory, instance_of(nta.NativeTrajectoryAdapterIdentified))

    def test_uwi(self):
        for uwi in ['01-325-88264-47-65', None]:
            with self.subTest(uwi=uwi):
                expected_uwi = uwi
                stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
                stub_native_well.Uwi = expected_uwi
                sut = nwa.NativeWellAdapter(stub_native_well)

                assert_that(sut.uwi, equal_to(expected_uwi if expected_uwi else 'No UWI'))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_empty_locations_for_md_kb_values_if_empty_md_kb_values(self, mock_as_unit_system):
        mock_as_unit_system.return_value = units.Metric
        stub_native_well = tsn.create_stub_net_well()
        sut = nwa.NativeWellAdapter(stub_native_well)

        actual = sut.locations_for_md_kb_values([], origins.WellReferenceFrameXy.PROJECT, origins.DepthDatum.SEA_LEVEL)
        # noinspection PyTypeChecker
        assert_that(list(actual), is_(empty()))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_single_location_for_md_kb_values_if_single_md_kb_values(self, mock_as_unit_system):
        for orchid_actual, expected, md_kb_dto, project_units, frame, datum, tolerance in [
            (tsn.StubSubsurfaceLocation(tsn.MeasurementDto(508.0e3, units.UsOilfield.LENGTH),
                                        tsn.MeasurementDto(4.633e6, units.UsOilfield.LENGTH),
                                        tsn.MeasurementDto(6850, units.UsOilfield.LENGTH)),
             tsn.StubSubsurfaceLocation(508.0e3 * om.registry.ft, 4.633e6 * om.registry.ft, 6850 * om.registry.ft),
             tsn.MeasurementDto(13.17e3, units.UsOilfield.LENGTH),
             units.UsOilfield, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, origins.DepthDatum.SEA_LEVEL,
             tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'),
                                        decimal.Decimal('0.001e6'),
                                        decimal.Decimal('1'))),
            (tsn.StubSubsurfaceLocation(tsn.MeasurementDto(154.8e3, units.Metric.LENGTH),
                                        tsn.MeasurementDto(1.412e6, units.Metric.LENGTH),
                                        tsn.MeasurementDto(2088, units.Metric.LENGTH)),
             tsn.StubSubsurfaceLocation(154.8e3 * om.registry.m, 1.412e6 * om.registry.m, 2088 * om.registry.m),
             tsn.MeasurementDto(4015, units.Metric.LENGTH),
             units.Metric, origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.KELLY_BUSHING,
             tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'),
                                        decimal.Decimal('0.001e6'),
                                        decimal.Decimal('1'))),
            (tsn.StubSubsurfaceLocation(tsn.MeasurementDto(508.0e3, units.UsOilfield.LENGTH),
                                        tsn.MeasurementDto(4.633e6, units.UsOilfield.LENGTH),
                                        tsn.MeasurementDto(6850, units.UsOilfield.LENGTH)),
             tsn.StubSubsurfaceLocation(154.8e3 * om.registry.m, 1.412e6 * om.registry.m, 2088 * om.registry.m),
             tsn.MeasurementDto(13.17e3, units.UsOilfield.LENGTH),
             units.Metric, origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.GROUND_LEVEL,
             tsn.StubSubsurfaceLocation(decimal.Decimal('40'),
                                        decimal.Decimal('0.04e6'),
                                        decimal.Decimal('0.4'))),
            (tsn.StubSubsurfaceLocation(tsn.MeasurementDto(154.8e3, units.Metric.LENGTH),
                                        tsn.MeasurementDto(1.412e6, units.Metric.LENGTH),
                                        tsn.MeasurementDto(2088, units.Metric.LENGTH)),
             tsn.StubSubsurfaceLocation(508.0e3 * om.registry.ft,
                                        4.633e6 * om.registry.ft,
                                        6850 * om.registry.ft),
             tsn.MeasurementDto(4015, units.Metric.LENGTH),
             units.UsOilfield, origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.KELLY_BUSHING,
             tsn.StubSubsurfaceLocation(decimal.Decimal('0.4e3'),
                                        decimal.Decimal('0.004e6'),
                                        decimal.Decimal('4'))),
        ]:
            with self.subTest(f'Test single location, {expected.x:~P} at md_kb value, {md_kb_dto.magnitude}'
                              f' {md_kb_dto.unit.value.unit:~P}'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(
                    locations_for_md_kb_values={((md_kb_dto,), frame, datum): [orchid_actual]})
                sut = nwa.NativeWellAdapter(stub_native_well)

                # noinspection PyTypeChecker
                actual = list(sut.locations_for_md_kb_values([tsn.make_measurement(md_kb_dto)], frame, datum))

                assert_that(len(actual), equal_to(1))
                tcm.assert_that_measurements_close_to(actual[0].x, expected.x, tolerance.x)
                tcm.assert_that_measurements_close_to(actual[0].y, expected.y, tolerance.y)
                tcm.assert_that_measurements_close_to(actual[0].depth, expected.depth, tolerance.depth)

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_many_locations_for_md_kb_values_if_many_md_kb_values(self, mock_as_unit_system):
        for orchid_actual, expected, md_kb_values, project_units, frame, datum, tolerance in [
            ((tsn.StubSubsurfaceLocation(tsn.MeasurementDto(374.3e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(1.365e6, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(8288, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.MeasurementDto(384.1e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(8.740e6, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(7572, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.MeasurementDto(182.4e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(541.2e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(7783, units.UsOilfield.LENGTH))),
             (tsn.StubSubsurfaceLocation(374.3e3 * om.registry.ft, 1.365e6 * om.registry.ft, 8288 * om.registry.ft),
              tsn.StubSubsurfaceLocation(384.1e3 * om.registry.ft, 8.740e6 * om.registry.ft, 7572 * om.registry.ft),
              tsn.StubSubsurfaceLocation(182.4e3 * om.registry.ft, 541.2e3 * om.registry.ft, 7783 * om.registry.ft)),
             (tsn.MeasurementDto(10.89e3, units.UsOilfield.LENGTH),
              tsn.MeasurementDto(12.55e3, units.UsOilfield.LENGTH),
              tsn.MeasurementDto(12.16e3, units.UsOilfield.LENGTH)),
             units.UsOilfield, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, origins.DepthDatum.SEA_LEVEL,
             (tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'), decimal.Decimal('0.001e6'), decimal.Decimal('1')),
              tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'), decimal.Decimal('0.001e6'), decimal.Decimal('1')),
              tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'), decimal.Decimal('0.1e3'), decimal.Decimal('1')))),
            ((tsn.StubSubsurfaceLocation(tsn.MeasurementDto(374.3e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(1.365e6, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(8288, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.MeasurementDto(384.1e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(8.740e6, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(7572, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.MeasurementDto(182.4e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(541.2e3, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(7783, units.UsOilfield.LENGTH))),
             (tsn.StubSubsurfaceLocation(114.1e3 * om.registry.m, 416.2e3 * om.registry.m, 2526 * om.registry.m),
              tsn.StubSubsurfaceLocation(117.1e3 * om.registry.m, 2.664e6 * om.registry.m, 2308 * om.registry.m),
              tsn.StubSubsurfaceLocation(55.61e3 * om.registry.m, 165.0e3 * om.registry.m, 2372 * om.registry.m)),
             (tsn.MeasurementDto(10.89e3, units.UsOilfield.LENGTH),
              tsn.MeasurementDto(12.55e3, units.UsOilfield.LENGTH),
              tsn.MeasurementDto(12.16e3, units.UsOilfield.LENGTH)),
             units.Metric, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, origins.DepthDatum.SEA_LEVEL,
             (tsn.StubSubsurfaceLocation(decimal.Decimal('0.04e3'),
                                         decimal.Decimal('0.004e6'),
                                         decimal.Decimal('0.4')),
              tsn.StubSubsurfaceLocation(decimal.Decimal('0.04e3'),
                                         decimal.Decimal('0.001e6'),
                                         decimal.Decimal('0.4')),
              tsn.StubSubsurfaceLocation(decimal.Decimal('0.04e3'),
                                         decimal.Decimal('0.001e6'),
                                         decimal.Decimal('0.4')))),
        ]:
            with self.subTest(f'Test many locations, {expected[0]}..., in project_units {project_units}'
                              f' at values, {md_kb_values[0]}...'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(
                    locations_for_md_kb_values={(md_kb_values, frame, datum): orchid_actual})
                sut = nwa.NativeWellAdapter(stub_native_well)

                # noinspection PyTypeChecker
                actual = list(sut.locations_for_md_kb_values(md_kb_values, frame, datum))

                assert_that(len(actual), equal_to(len(expected)))
                for actual_point, expected_point, tolerance_point in zip(actual, expected, tolerance):
                    tcm.assert_that_measurements_close_to(actual_point.x, expected_point.x, tolerance_point.x)
                    tcm.assert_that_measurements_close_to(actual_point.y, expected_point.y, tolerance_point.y)
                    tcm.assert_that_measurements_close_to(actual_point.depth,
                                                          expected_point.depth,
                                                          tolerance_point.depth)

    def test_formation_returns_expected_formation_when_initialized(self):
        expected_formation = 'Bakken'
        stub_native_well = tsn.create_stub_net_well(formation=expected_formation)
        sut = nwa.NativeWellAdapter(stub_native_well)
        assert_that(sut.formation, equal_to(expected_formation))

    def test_formation_returns_empty_string_when_net_formation_uninitialized(self):
        stub_native_well = tsn.create_stub_net_well()
        sut = nwa.NativeWellAdapter(stub_native_well)
        # TODO Add custom matcher 'empty_string()', test would be "assert_that(sut.formation, equal_to(empty_string())"
        assert_that(sut.formation, equal_to(''))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_wellhead_location_values_are_correct(self, mock_as_unit_system):
        # Since StubSubsurfaceLocation data points are so similar to wellhead location, this testing will
        # use the same testing data in evaluation
        inputs = [tsn.StubWellHeadLocation(tsn.MeasurementDto(374.3e3, units.UsOilfield.LENGTH),
                                           tsn.MeasurementDto(1.365e6, units.UsOilfield.LENGTH),
                                           tsn.MeasurementDto(8288, units.UsOilfield.LENGTH)),
                  tsn.StubWellHeadLocation(tsn.MeasurementDto(384.1e3, units.UsOilfield.LENGTH),
                                           tsn.MeasurementDto(8.740e6, units.UsOilfield.LENGTH),
                                           tsn.MeasurementDto(7572, units.UsOilfield.LENGTH)),
                  tsn.StubWellHeadLocation(tsn.MeasurementDto(182.4e3, units.UsOilfield.LENGTH),
                                           tsn.MeasurementDto(541.2e3, units.UsOilfield.LENGTH),
                                           tsn.MeasurementDto(7783, units.UsOilfield.LENGTH))]

        expected = [tsn.StubWellHeadLocation(374.3e3 * om.registry.ft, 1.365e6 * om.registry.ft, 8288 * om.registry.ft),
                    tsn.StubWellHeadLocation(384.1e3 * om.registry.ft, 8.740e6 * om.registry.ft, 7572 * om.registry.ft),
                    tsn.StubWellHeadLocation(182.4e3 * om.registry.ft, 541.2e3 * om.registry.ft, 7783 * om.registry.ft)]

        comparison_tolerances = [tsn.StubWellHeadLocation(decimal.Decimal('0.04e3'),
                                                          decimal.Decimal('0.004e6'),
                                                          decimal.Decimal('0.4')),
                                 tsn.StubWellHeadLocation(decimal.Decimal('0.04e3'),
                                                          decimal.Decimal('0.001e6'),
                                                          decimal.Decimal('0.4')),
                                 tsn.StubWellHeadLocation(decimal.Decimal('0.04e3'),
                                                          decimal.Decimal('0.001e6'),
                                                          decimal.Decimal('0.4'))]

        for input_location, expected_location, tolerances in zip(inputs, expected, comparison_tolerances):
            whl_input = [input_location.easting, input_location.northing, input_location.depth]
            mock_as_unit_system.return_value = units.UsOilfield
            stub_native_well = tsn.create_stub_net_well(wellhead_location=whl_input)
            sut = nwa.NativeWellAdapter(stub_native_well)
            whl_actual = sut.wellhead_location
            with self.subTest(f'Testing Wellhead Location'):
                tcm.assert_that_measurements_close_to(whl_actual.easting, expected_location.easting,
                                                      tolerances.easting)
                tcm.assert_that_measurements_close_to(whl_actual.northing, expected_location.northing,
                                                      tolerances.northing)
                tcm.assert_that_measurements_close_to(whl_actual.depth, expected_location.depth,
                                                      tolerances.depth)


DONT_CARE_STAGE_NO = 32
DONT_CARE_STAGE_TYPE = nsa.ConnectionType.PLUG_AND_PERF
DONT_CARE_MD_TOP = units.make_us_oilfield_length_measurement(11389.3)
DONT_CARE_MD_BOTTOM = units.make_us_oilfield_length_measurement(11550.0)
DONT_CARE_ISIP = units.make_us_oilfield_pressure_measurement(2.217)


@dc.dataclass
class CreateStageDtoArgs:
    stage_no: int = DONT_CARE_STAGE_NO
    stage_type: nsa.ConnectionType = DONT_CARE_STAGE_TYPE
    md_top: om.Quantity = DONT_CARE_MD_TOP
    md_bottom: om.Quantity = DONT_CARE_MD_BOTTOM
    maybe_isip: om.Quantity = DONT_CARE_ISIP


# Test ideas
# - Added stage has stage_no supplied to constructor
# - Added stage has stage_type supplied to constructor
# - Added stage has md_top supplied to constructor
# - Added stage has md_bottom supplied to constructor
# - Added stage has cluster_count supplied to constructor
# - Added stage has time_range supplied to constructor
# - Added stage has isip supplied to constructor
# - Added stage has shmin supplied to constructor
# - Added stage has .NET "not a time" time range if maybe_time_range has no value
# - Added stage has no shmin if maybe_shmin has no value
class TestNativeWellAdapterAddStages(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    @unittest.skip('Not yet implemented')
    def test_added_stage_has_display_stage_number_from_ctor(self):
        stage_no = 27
        create_dto_args = dc.asdict(CreateStageDtoArgs(stage_no=stage_no))
        stub_well = tsn.create_stub_net_well()
        actual_stage = nwa.CreateStageDto(**create_dto_args).create_stage(stub_well)

        assert_that(actual_stage.display_stage_number, equal_to(stage_no))


# Test ideas
class TestCreateStageDto(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_order_of_completion_on_well_is_one_less_than_stage_no_to_ctor(self):
        create_dto_args = dc.asdict(CreateStageDtoArgs(stage_no=24))
        sut = nwa.CreateStageDto(**create_dto_args)

        assert_that(sut.order_of_completion_on_well, equal_to(24 - 1))

    def test_ctor_raises_error_if_stage_no_less_than_1(self):
        erroneous_stage_no = 0
        create_dto_args = dc.astuple(CreateStageDtoArgs(stage_no=erroneous_stage_no))
        assert_that(calling(nwa.CreateStageDto).with_args(*create_dto_args),
                    raises(ValueError, pattern=f'`stage_no` greater than 0.*Found {erroneous_stage_no}'))

    def test_ctor_raises_error_if_md_top_is_not_a_length_unit(self):
        erroneous_md_top = units.make_us_oilfield_pressure_measurement(5246.7)
        create_dto_args = dc.astuple(CreateStageDtoArgs(md_top=erroneous_md_top))
        assert_that(calling(nwa.CreateStageDto).with_args(*create_dto_args),
                    raises(ValueError, pattern=f'`md_top` to be a length measurement. Found {erroneous_md_top:~P}'))

    def test_ctor_raises_error_if_md_bottom_is_not_a_length_unit(self):
        erroneous_md_bottom = units.make_us_oilfield_pressure_measurement(5246.7)
        create_dto_args = dc.astuple(CreateStageDtoArgs(md_bottom=erroneous_md_bottom))
        assert_that(calling(nwa.CreateStageDto).with_args(*create_dto_args),
                    raises(ValueError, pattern=f'`md_bottom` to be a length measurement.'
                                               f' Found {erroneous_md_bottom:~P}'))

    def test_ctor_raises_error_if_cluster_count_less_than_0(self):
        erroneous_cluster_count = -1
        assert_that(calling(nwa.CreateStageDto).with_args(
            stage_no=DONT_CARE_STAGE_NO,
            stage_type=DONT_CARE_STAGE_TYPE,
            md_top=DONT_CARE_MD_TOP,
            md_bottom=DONT_CARE_MD_BOTTOM,
            cluster_count=erroneous_cluster_count,
        ), raises(ValueError, pattern=f'`cluster_count` to be non-negative.*Found {erroneous_cluster_count}'))

    def test_ctor_raises_error_if_maybe_isip_is_not_a_pressure_unit(self):
        erroneous_isip = units.make_metric_length_measurement(4419.58)
        assert_that(calling(nwa.CreateStageDto).with_args(
            stage_no=DONT_CARE_STAGE_NO,
            stage_type=DONT_CARE_STAGE_TYPE,
            md_top=DONT_CARE_MD_TOP,
            md_bottom=DONT_CARE_MD_BOTTOM,
            maybe_isip=erroneous_isip,
        ), raises(ValueError, pattern=f'`maybe_isip` to be a pressure measurement. Found {erroneous_isip:~P}'))

    def test_ctor_raises_error_if_maybe_isip_is_not_supplied(self):
        assert_that(calling(nwa.CreateStageDto).with_args(
            stage_no=DONT_CARE_STAGE_NO,
            stage_type=DONT_CARE_STAGE_TYPE,
            md_top=DONT_CARE_MD_TOP,
            md_bottom=DONT_CARE_MD_BOTTOM,
        ), raises(TypeError, pattern=f'`maybe_isip` to be supplied. Found `None`'))

    def test_ctor_raises_error_if_maybe_shmin_is_not_a_pressure_unit(self):
        erroneous_shmin = units.make_metric_length_measurement(4473.45)
        assert_that(calling(nwa.CreateStageDto).with_args(
            stage_no=DONT_CARE_STAGE_NO,
            stage_type=DONT_CARE_STAGE_TYPE,
            md_top=DONT_CARE_MD_TOP,
            md_bottom=DONT_CARE_MD_BOTTOM,
            maybe_isip=DONT_CARE_ISIP,
            maybe_shmin=erroneous_shmin,
        ), raises(ValueError, pattern=f'`maybe_shmin` to be a pressure measurement. Found {erroneous_shmin:~P}'))


if __name__ == '__main__':
    unittest.main()
