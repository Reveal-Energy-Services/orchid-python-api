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

import decimal
import unittest.mock

from hamcrest import assert_that, equal_to, instance_of, is_, empty
import toolz.curried as toolz

from orchid import (
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
            (tsn.StubMeasurement(4537, units.UsOilfield.LENGTH),
             tsn.StubMeasurement(4537, units.UsOilfield.LENGTH),
             units.UsOilfield, decimal.Decimal('1')),
            (tsn.StubMeasurement(1383, units.Metric.LENGTH),
             tsn.StubMeasurement(1383, units.Metric.LENGTH),
             units.Metric, decimal.Decimal('1')),
            (tsn.StubMeasurement(4537, units.UsOilfield.LENGTH),
             tsn.StubMeasurement(1383, units.Metric.LENGTH),
             units.Metric, decimal.Decimal('0.4')),
            (tsn.StubMeasurement(1383, units.Metric.LENGTH),
             tsn.StubMeasurement(4537, units.UsOilfield.LENGTH),
             units.UsOilfield, decimal.Decimal('4')),
        ]:
            with self.subTest(f'Test ground level elevation, {expected}, in units, {project_units.LENGTH}'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(
                    ground_level_elevation_above_sea_level=orchid_actual)
                sut = nwa.NativeWellAdapter(stub_native_well)
                tcm.assert_that_measurements_close_to(
                    sut.ground_level_elevation_above_sea_level, expected, tolerance)

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_kelly_bushing_height_above_ground_level(self, mock_as_unit_system):
        for orchid_actual, expected, project_units, tolerance in [
            (tsn.StubMeasurement(30.86, units.UsOilfield.LENGTH),
             tsn.StubMeasurement(30.86, units.UsOilfield.LENGTH),
             units.UsOilfield, decimal.Decimal('0.01')),
            (tsn.StubMeasurement(9.406, units.Metric.LENGTH),
             tsn.StubMeasurement(9.406, units.Metric.LENGTH),
             units.Metric, decimal.Decimal('0.01')),
            (tsn.StubMeasurement(30.86, units.UsOilfield.LENGTH),
             tsn.StubMeasurement(9.406, units.Metric.LENGTH),
             units.Metric, decimal.Decimal('0.004')),
            (tsn.StubMeasurement(9.406, units.Metric.LENGTH),
             tsn.StubMeasurement(30.86, units.UsOilfield.LENGTH),
             units.UsOilfield, decimal.Decimal('0.004')),
        ]:
            with self.subTest(f'Test kelly bushing height, {expected}, in units, {project_units.LENGTH}'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(
                    kelly_bushing_height_above_ground_level=orchid_actual)
                sut = nwa.NativeWellAdapter(stub_native_well)
                tcm.assert_that_measurements_close_to(
                    sut.kelly_bushing_height_above_ground_level, expected, tolerance)

    def test_name(self):
        expected_well_name = 'sapientiarum'
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_native_well.Name = expected_well_name
        sut = nwa.NativeWellAdapter(stub_native_well)

        assert_that(sut.name, equal_to(expected_well_name))

    def test_stages_count_equals_net_stages_count(self):
        for stub_net_stages in [[], [tsn.create_stub_net_stage()], [tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage()]]:
            with self.subTest(f'Test length of stages for each of {len(stub_net_stages)} .NET stage(s)'):
                stub_net_well = unittest.mock.MagicMock(name='stub_net_well')
                stub_net_well.Stages.Items = stub_net_stages
                sut = nwa.NativeWellAdapter(stub_net_well)

                assert_that(toolz.count(sut.stages), equal_to(len(stub_net_stages)))

    def test_stages_wrap_all_net_stages(self):
        for stub_net_stages in [[], [tsn.create_stub_net_stage()], [tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage(),
                                                                    tsn.create_stub_net_stage()]]:
            with self.subTest(f'Test stage adapter for each of {len(stub_net_stages)} .NET stage(s)'):
                stub_net_well = unittest.mock.MagicMock(name='stub_net_well')
                stub_net_well.Stages.Items = stub_net_stages
                sut = nwa.NativeWellAdapter(stub_net_well)

                for actual_stage in sut.stages:
                    assert_that(actual_stage, instance_of(nsa.NativeStageAdapter))

    def test_trajectory(self):
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_trajectory = unittest.mock.MagicMock(name='stub_native_trajectory')
        stub_native_well.Trajectory = stub_trajectory
        sut = nwa.NativeWellAdapter(stub_native_well)

        # noinspection PyTypeChecker
        assert_that(sut.trajectory, instance_of(nta.NativeTrajectoryAdapter))

    def test_uwi(self):
        for uwi in ['01-325-88264-47-65', None]:
            with self.subTest(uwi=uwi):
                expected_uwi = uwi
                stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
                stub_native_well.Uwi = expected_uwi
                sut = nwa.NativeWellAdapter(stub_native_well)

                assert_that(sut.uwi, equal_to(expected_uwi if expected_uwi else 'No UWI'))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_empty_locations_for_mdkb_values_if_empty_mdkb_values(self, mock_as_unit_system):
        mock_as_unit_system.return_value = units.Metric
        stub_native_well = tsn.create_stub_net_well()
        sut = nwa.NativeWellAdapter(stub_native_well)

        actual = sut.locations_for_mdkb_values([], origins.WellReferenceFrameXy.PROJECT, origins.DepthDatum.SEA_LEVEL)
        # noinspection PyTypeChecker
        assert_that(list(actual), is_(empty()))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_single_location_for_mdkb_values_if_single_mdkb_values(self, mock_as_unit_system):
        for orchid_actual, expected, mdkb, project_units, frame, datum, tolerance in [
            (tsn.StubSubsurfaceLocation(tsn.StubMeasurement(508.0e3, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(4.633e6, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(6850, units.UsOilfield.LENGTH)),
             tsn.StubSubsurfaceLocation(tsn.StubMeasurement(508.0e3, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(4.633e6, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(6850, units.UsOilfield.LENGTH)),
             tsn.StubMeasurement(13.17e3, units.UsOilfield.LENGTH),
             units.UsOilfield, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, origins.DepthDatum.SEA_LEVEL,
             tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'),
                                        decimal.Decimal('0.001e6'),
                                        decimal.Decimal('1'))),
            (tsn.StubSubsurfaceLocation(tsn.StubMeasurement(154.8e3, units.Metric.LENGTH),
                                        tsn.StubMeasurement(1.412e6, units.Metric.LENGTH),
                                        tsn.StubMeasurement(2088, units.Metric.LENGTH)),
             tsn.StubSubsurfaceLocation(tsn.StubMeasurement(154.8e3, units.Metric.LENGTH),
                                        tsn.StubMeasurement(1.412e6, units.Metric.LENGTH),
                                        tsn.StubMeasurement(2088, units.Metric.LENGTH)),
             tsn.StubMeasurement(4015, units.Metric.LENGTH),
             units.Metric, origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.KELLY_BUSHING,
             tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'),
                                        decimal.Decimal('0.001e6'),
                                        decimal.Decimal('1'))),
            (tsn.StubSubsurfaceLocation(tsn.StubMeasurement(508.0e3, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(4.633e6, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(6850, units.UsOilfield.LENGTH)),
             tsn.StubSubsurfaceLocation(tsn.StubMeasurement(154.8e3, units.Metric.LENGTH),
                                        tsn.StubMeasurement(1.412e6, units.Metric.LENGTH),
                                        tsn.StubMeasurement(2088, units.Metric.LENGTH)),
             tsn.StubMeasurement(13.17e3, units.UsOilfield.LENGTH),
             units.Metric, origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.GROUND_LEVEL,
             tsn.StubSubsurfaceLocation(decimal.Decimal('40'),
                                        decimal.Decimal('0.04e6'),
                                        decimal.Decimal('0.4'))),
            (tsn.StubSubsurfaceLocation(tsn.StubMeasurement(154.8e3, units.Metric.LENGTH),
                                        tsn.StubMeasurement(1.412e6, units.Metric.LENGTH),
                                        tsn.StubMeasurement(2088, units.Metric.LENGTH)),
             tsn.StubSubsurfaceLocation(tsn.StubMeasurement(508.0e3, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(4.633e6, units.UsOilfield.LENGTH),
                                        tsn.StubMeasurement(6850, units.UsOilfield.LENGTH)),
             tsn.StubMeasurement(4015, units.Metric.LENGTH),
             units.UsOilfield, origins.WellReferenceFrameXy.WELL_HEAD, origins.DepthDatum.KELLY_BUSHING,
             tsn.StubSubsurfaceLocation(decimal.Decimal('0.4e3'),
                                        decimal.Decimal('0.004e6'),
                                        decimal.Decimal('4'))),
        ]:
            with self.subTest(f'Test single location, {expected}, in project_units {project_units}'
                              f' at value, {mdkb}'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(
                    locations_for_mdkb_values={((mdkb,), frame, datum): [orchid_actual]})
                sut = nwa.NativeWellAdapter(stub_native_well)

                # noinspection PyTypeChecker
                actual = list(sut.locations_for_mdkb_values([mdkb], frame, datum))

                assert_that(len(actual), equal_to(1))
                tcm.assert_that_measurements_close_to(actual[0].x, expected.x, tolerance.x)
                tcm.assert_that_measurements_close_to(actual[0].y, expected.y, tolerance.y)
                tcm.assert_that_measurements_close_to(actual[0].depth, expected.depth, tolerance.depth)

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_many_locations_for_mdkb_values_if_many_mdkb_values(self, mock_as_unit_system):
        for orchid_actual, expected, mdkb_values, project_units, frame, datum, tolerance in [
            ((tsn.StubSubsurfaceLocation(tsn.StubMeasurement(374.3e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(1.365e6, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(8288, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(384.1e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(8.740e6, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(7572, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(182.4e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(541.2e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(7783, units.UsOilfield.LENGTH))),
             (tsn.StubSubsurfaceLocation(tsn.StubMeasurement(374.3e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(1.365e6, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(8288, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(384.1e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(8.740e6, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(7572, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(182.4e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(541.2e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(7783, units.UsOilfield.LENGTH))),
             (tsn.StubMeasurement(10.89e3, units.UsOilfield.LENGTH),
              tsn.StubMeasurement(12.55e3, units.UsOilfield.LENGTH),
              tsn.StubMeasurement(12.16e3, units.UsOilfield.LENGTH)),
             units.UsOilfield, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE, origins.DepthDatum.SEA_LEVEL,
             (tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'), decimal.Decimal('0.001e6'), decimal.Decimal('1')),
              tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'), decimal.Decimal('0.001e6'), decimal.Decimal('1')),
              tsn.StubSubsurfaceLocation(decimal.Decimal('0.1e3'), decimal.Decimal('0.1e3'), decimal.Decimal('1')))),
            ((tsn.StubSubsurfaceLocation(tsn.StubMeasurement(374.3e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(1.365e6, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(8288, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(384.1e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(8.740e6, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(7572, units.UsOilfield.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(182.4e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(541.2e3, units.UsOilfield.LENGTH),
                                         tsn.StubMeasurement(7783, units.UsOilfield.LENGTH))),
             (tsn.StubSubsurfaceLocation(tsn.StubMeasurement(114.1e3, units.Metric.LENGTH),
                                         tsn.StubMeasurement(416.2e3, units.Metric.LENGTH),
                                         tsn.StubMeasurement(2526, units.Metric.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(117.1e3, units.Metric.LENGTH),
                                         tsn.StubMeasurement(2.664e6, units.Metric.LENGTH),
                                         tsn.StubMeasurement(2308, units.Metric.LENGTH)),
              tsn.StubSubsurfaceLocation(tsn.StubMeasurement(55.61e3, units.Metric.LENGTH),
                                         tsn.StubMeasurement(165.0e3, units.Metric.LENGTH),
                                         tsn.StubMeasurement(2372, units.Metric.LENGTH))),
             (tsn.StubMeasurement(10.89e3, units.UsOilfield.LENGTH),
              tsn.StubMeasurement(12.55e3, units.UsOilfield.LENGTH),
              tsn.StubMeasurement(12.16e3, units.UsOilfield.LENGTH)),
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
                              f' at values, {mdkb_values[0]}...'):
                mock_as_unit_system.return_value = project_units
                stub_native_well = tsn.create_stub_net_well(
                    locations_for_mdkb_values={(mdkb_values, frame, datum): orchid_actual})
                sut = nwa.NativeWellAdapter(stub_native_well)

                # noinspection PyTypeChecker
                actual = list(sut.locations_for_mdkb_values(mdkb_values, frame, datum))

                assert_that(len(actual), equal_to(len(expected)))
                for actual_point, expected_point, tolerance_point in zip(actual, expected, tolerance):
                    tcm.assert_that_measurements_close_to(actual_point.x, expected_point.x, tolerance_point.x)
                    tcm.assert_that_measurements_close_to(actual_point.y, expected_point.y, tolerance_point.y)
                    tcm.assert_that_measurements_close_to(actual_point.depth, expected_point.depth,
                                                          tolerance_point.depth)


if __name__ == '__main__':
    unittest.main()
