#  Copyright (c) 2017-2023 Reveal Energy Services, Inc
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

import decimal
import unittest.mock
import uuid

from hamcrest import (
    assert_that,
    equal_to,
    instance_of,
    is_,
    empty,
    contains_exactly,
)
import toolz.curried as toolz
import pendulum as pdt

from orchid import (
    measurement as om,
    native_stage_adapter as nsa,
    native_trajectory_adapter as nta,
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
                stub_native_well = tsn.WellDto(ground_level_elevation_above_sea_level=orchid_actual).create_net_stub()
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
                stub_native_well = tsn.WellDto(kelly_bushing_height_above_ground_level=orchid_actual).create_net_stub()
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
                stub_native_well = tsn.WellDto(stage_dtos=stage_dtos).create_net_stub()
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
        stub_native_well = tsn.WellDto().create_net_stub()
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
                stub_native_well = tsn.WellDto(
                    locations_for_md_kb_values={((md_kb_dto,), frame, datum): [orchid_actual]}).create_net_stub()
                sut = nwa.NativeWellAdapter(stub_native_well)

                # noinspection PyTypeChecker
                actual = list(sut.locations_for_md_kb_values([tsn.make_measurement(md_kb_dto)], frame, datum))

                assert_that(len(actual), equal_to(1))
                tcm.assert_that_measurements_close_to(actual[0].x, expected.x, tolerance.x)
                tcm.assert_that_measurements_close_to(actual[0].y, expected.y, tolerance.y)
                tcm.assert_that_measurements_close_to(actual[0].depth, expected.depth, tolerance.depth)

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_many_locations_for_md_kb_values_if_many_md_kb_values(self, mock_as_unit_system):
        for orchid_actual, expected, md_kb_value_dtos, project_units, frame, datum, tolerance in [
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
                              f' at values, {md_kb_value_dtos[0]}...'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.WellDto(
                    locations_for_md_kb_values={(md_kb_value_dtos, frame, datum): orchid_actual}).create_net_stub()
                sut = nwa.NativeWellAdapter(stub_native_well)

                # noinspection PyTypeChecker
                md_kb_values = toolz.map(tsn.make_measurement, md_kb_value_dtos)
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
        stub_native_well = tsn.WellDto(formation=expected_formation).create_net_stub()
        sut = nwa.NativeWellAdapter(stub_native_well)
        assert_that(sut.formation, equal_to(expected_formation))

    def test_formation_returns_empty_string_when_net_formation_uninitialized(self):
        stub_native_well = tsn.WellDto().create_net_stub()
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
            stub_native_well = tsn.WellDto(wellhead_location=whl_input).create_net_stub()
            sut = nwa.NativeWellAdapter(stub_native_well)
            whl_actual = sut.wellhead_location
            with self.subTest(f'Testing Wellhead Location'):
                tcm.assert_that_measurements_close_to(whl_actual.easting, expected_location.easting,
                                                      tolerances.easting)
                tcm.assert_that_measurements_close_to(whl_actual.northing, expected_location.northing,
                                                      tolerances.northing)
                tcm.assert_that_measurements_close_to(whl_actual.depth, expected_location.depth,
                                                      tolerances.depth)


# Test ideas
# - Call add_stages with one stage DTO calls `CreateStage` once
# - Call add_stages with many stage DTOs calls `CreateStage` many times
# - Call add_stages with one stage DTO calls `CreateStage` with correct arguments
class TestNativeWellAdapterAddStages(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_stage')
    def test_add_stages_with_no_items_calls_neither_create_stage_nor_well_add_stages(self, stub_create_stage):
        stub_net_well = tsn.WellDto().create_net_stub()
        stub_net_mutable_well = tsn.MutableWellDto().create_net_stub()
        stub_net_well.ToMutable.return_value = stub_net_mutable_well
        sut = nwa.NativeWellAdapter(stub_net_well)
        sut.add_stages([])

        stub_create_stage.assert_not_called()
        stub_net_mutable_well.Add.assert_not_called()

    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_stage')
    @unittest.mock.patch('orchid.native_well_adapter.NativeWellAdapter._create_net_stages')
    def test_add_stages_with_one_item_calls_both_create_stage_add_well_add_stages_once(self,
                                                                                       stub_create_net_stages,
                                                                                       stub_create_stage,
                                                                                       ):
        created_stage = nsa.NativeStageAdapter(tsn.StageDto().create_net_stub())
        stub_create_stage.return_value = created_stage

        created_net_stages = unittest.mock.MagicMock('created_net_stages')
        stub_create_net_stages.return_value = created_net_stages

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_net_mutable_well = tsn.MutableWellDto().create_net_stub()
        stub_net_well.ToMutable.return_value = stub_net_mutable_well
        sut = nwa.NativeWellAdapter(stub_net_well)

        # noinspection PyTypeChecker
        dont_care_stage_dto = nsa.CreateStageDto(25, nsa.ConnectionType.PLUG_AND_PERF,
                                                 15147.3 * om.registry.ft, 15283.3 * om.registry.ft,
                                                 5, 2.29883 * om.registry.psi,
                                                 pdt.parse('2021-07-12T05:29:34/2021-07-12T07:13:09', tz='UTC'),
                                                 34718.7 * om.registry.kPa)
        sut.add_stages([dont_care_stage_dto])

        # noinspection PyUnresolvedReferences
        sut._create_net_stages.assert_called_once_with([created_stage])
        stub_net_mutable_well.AddStages.assert_called_once_with(created_net_stages)

    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_stage')
    @unittest.mock.patch('orchid.native_well_adapter.NativeWellAdapter._create_net_stages')
    def test_add_stages_with_many_items_calls_both_create_stage_add_well_add_stages_many(self,
                                                                                         stub_create_net_stages,
                                                                                         stub_create_stage,
                                                                                         ):
        created_net_stages = [tsn.StageDto().create_net_stub() for _ in range(3)]
        created_stages = [nsa.NativeStageAdapter(created_net_stage)
                          for created_net_stage in created_net_stages]
        # Use `side_effect` because `nsa.CreateStageDto.create_stage` call **multiple** times
        # each with a single argument.
        stub_create_stage.side_effect = created_stages

        # Use `return_value` because `nwa._create_net_stages` called **once** with a **single** argument
        # that is an `Iterable`.
        stub_create_net_stages.return_value = created_net_stages

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_net_mutable_well = tsn.MutableWellDto().create_net_stub()
        stub_net_well.ToMutable.return_value = stub_net_mutable_well
        sut = nwa.NativeWellAdapter(stub_net_well)

        dont_care_stage_dtos_details = [
            {'stage_no': 9,
             'connection_type': nsa.ConnectionType.PLUG_AND_PERF,
             'md_top': 15762.9 * om.registry.ft,
             'md_bottom': 15898.8 * om.registry.ft,
             'cluster_count': 5,
             'maybe_shmin': 16.24 * om.registry.kPa,
             'maybe_time_range': pdt.parse('2019-01-08T10:57:31/2019-01-08T12:39:14', tz='UTC'),
             'maybe_isip': 5109.66 * om.registry.psi},
            {'stage_no': 27,
             'connection_type': nsa.ConnectionType.SLIDING_SLEEVE,
             'md_top': 12658.8 * om.registry.ft,
             'md_bottom': 12795.8 * om.registry.ft,
             'cluster_count': 3,
             'maybe_shmin': 2.275 * om.registry.psi,
             'maybe_time_range': pdt.parse('2020-04-21T08:29:33/2020-04-21T10:20:29', tz='UTC'),
             'maybe_isip': 34566.8 * om.registry.kPa},
            {'stage_no': 47,
             'connection_type': nsa.ConnectionType.PLUG_AND_PERF,
             'md_top': 3553.9 * om.registry.m,
             'md_bottom': 3591.8 * om.registry.m,
             'cluster_count': 7,
             'maybe_shmin': 2.307 * om.registry.psi,
             'maybe_time_range': pdt.parse('2025-11-19T12:14:52/2025-11-19T13:42:49', tz='UTC'),
             'maybe_isip': 33949.6 * om.registry.kPa},
        ]

        dont_care_stage_dtos = [nsa.CreateStageDto(**details) for details in dont_care_stage_dtos_details]
        sut.add_stages(dont_care_stage_dtos)

        # noinspection PyUnresolvedReferences
        sut._create_net_stages.assert_called_once_with(created_stages)
        stub_net_mutable_well.AddStages.assert_called_once_with(created_net_stages)


if __name__ == '__main__':
    unittest.main()
