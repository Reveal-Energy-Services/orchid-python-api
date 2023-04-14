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
import unittest
import unittest.mock
import uuid

import deal
from hamcrest import assert_that, equal_to, contains_exactly, calling, raises

from orchid import (
    measurement as om,
    project as onp,
    project_store as loader,
    unit_system as units)
from tests import (
    stub_net as tsn,
    custom_matchers as tcm,
)


# Test ideas
# - User data is empty if .NET user data is empty
# - User data has one item if .NET user data has one item
# - User data has many items if .NET user data has many items
class TestProject(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_ctor_no_loader_raises_exception(self):
        assert_that(calling(onp.Project).with_args(None), raises(deal.PreContractError))

    def test_azimuth_returns_azimuth_in_project_units(self):
        for actual_azimuth, project_units, expected_azimuth, tolerance in (
                (tsn.MeasurementDto(30.32, units.Common.ANGLE), units.UsOilfield,
                 30.32 * om.registry.deg, decimal.Decimal('0.01')),
                (tsn.MeasurementDto(60.35, units.Common.ANGLE), units.Metric,
                 60.35 * om.registry.deg, decimal.Decimal('0.01')),
        ):
            with self.subTest(f'Testing azimuth in same units {expected_azimuth}'):
                stub_native_project = tsn.create_stub_net_project(azimuth=actual_azimuth, project_units=project_units)
                sut = create_sut(stub_native_project)
                tcm.assert_that_measurements_close_to(sut.azimuth, expected_azimuth, tolerance)

    def test_data_frames(self):
        for data_frame_dtos in (
                (),
                # Need trailing comma inside parentheses to retain tuple
                ({'object_id': tsn.DONT_CARE_ID_A, 'display_name': 'ianitore', 'name': 'praescindent'},),
                # Don't care about object IDs but must be unique
                ({'object_id': tsn.DONT_CARE_ID_B, 'display_name': 'adamanti', 'name': 'partes'},
                 {'object_id': tsn.DONT_CARE_ID_C, 'display_name': 'indicium', 'name': 'cunctas'},
                 {'object_id': tsn.DONT_CARE_ID_D, 'display_name': 'aquila', 'name': 'curae'})
        ):
            get_data_frame_dtos_property = tsn.get_dtos_property(data_frame_dtos)
            expected_object_ids = get_data_frame_dtos_property('object_id', transform=uuid.UUID)
            expected_display_names = get_data_frame_dtos_property('display_name')
            expected_names = get_data_frame_dtos_property('name')
            with self.subTest(f'Verify data frame object IDs, {expected_object_ids}'
                              f' display_names, {expected_display_names},'
                              f' and names, {expected_names}'):
                stub_native_project = tsn.create_stub_net_project(data_frame_dtos=data_frame_dtos)
                sut = create_sut(stub_native_project)

                assert_that(sut.data_frames().all_object_ids(), contains_exactly(*expected_object_ids))
                assert_that(sut.data_frames().all_display_names(), contains_exactly(*expected_display_names))
                assert_that(sut.data_frames().all_names(), contains_exactly(*expected_names))

    def test_default_well_colors_if_no_default_well_colors(self):
        stub_native_project = tsn.create_stub_net_project(name='exsistet')
        sut = create_sut(stub_native_project)
        assert_that(sut.default_well_colors(), equal_to([tuple([])]))

    def test_default_well_colors_if_one_default_well_color(self):
        stub_native_project = tsn.create_stub_net_project(name='exsistet', default_well_colors=[[0.142, 0.868, 0.220]])
        sut = create_sut(stub_native_project)
        # noinspection PyTypeChecker
        assert_that(sut.default_well_colors(), contains_exactly((0.142, 0.868, 0.220)))

    def test_default_well_colors_if_many_default_well_colors(self):
        expected_default_well_colors = [(0.610, 0.779, 0.675), (0.758, 0.982, 0.720), (0.297, 0.763, 0.388)]
        stub_native_project = tsn.create_stub_net_project(
            name='exsistet', default_well_colors=[list(t) for t in expected_default_well_colors])
        sut = create_sut(stub_native_project)
        # noinspection PyTypeChecker
        assert_that(sut.default_well_colors(), contains_exactly(*expected_default_well_colors))

    def test_fluid_density_returns_fluid_density_in_project_units(self):
        for actual_density, project_units, expected_density, tolerance in (
                (tsn.MeasurementDto(47.02, units.UsOilfield.DENSITY), units.UsOilfield,
                 47.02 * om.registry.lb / om.registry.ft ** 3, decimal.Decimal('0.01')),
                (tsn.MeasurementDto(1053, units.Metric.DENSITY), units.Metric,
                 1053 * om.registry.kg / om.registry.m ** 3, decimal.Decimal('1')),
                (tsn.MeasurementDto(47.02, units.UsOilfield.DENSITY), units.Metric,
                 753.2 * om.registry.kg / om.registry.m ** 3, decimal.Decimal('0.2')),
                (tsn.MeasurementDto(1053, units.Metric.DENSITY), units.UsOilfield,
                 65.74 * om.registry.lb / om.registry.ft ** 3, decimal.Decimal('0.07')),
        ):
            with self.subTest(f'Testing fluid density in same units {expected_density}'):
                stub_native_project = tsn.create_stub_net_project(fluid_density=actual_density,
                                                                  project_units=project_units)
                sut = create_sut(stub_native_project)
                tcm.assert_that_measurements_close_to(sut.fluid_density, expected_density, tolerance)

    def test_monitors(self):
        for monitor_dtos in (
            (),
            ({'object_id': tsn.DONT_CARE_ID_A, 'display_name': 'congruent'},),  # need trailing comma to retain tuple
            # Don't care about object IDs but must be unique
            ({'object_id': tsn.DONT_CARE_ID_B, 'display_name': 'histrio'},
             {'object_id': tsn.DONT_CARE_ID_C, 'display_name': 'principis'},
             {'object_id': tsn.DONT_CARE_ID_D, 'display_name': 'quaesivuisti'})
        ):
            get_monitor_dtos_property = tsn.get_dtos_property(monitor_dtos)
            expected_object_ids = get_monitor_dtos_property('object_id', transform=uuid.UUID)
            expected_display_names = get_monitor_dtos_property('display_name')
            with self.subTest(f'Verify monitors object IDs, {expected_object_ids}'
                              f' and display names, {expected_display_names}'):
                stub_native_project = tsn.create_stub_net_project(monitor_dtos=monitor_dtos)
                sut = create_sut(stub_native_project)

                assert_that(sut.monitors().all_object_ids(), contains_exactly(*expected_object_ids))
                assert_that(sut.monitors().all_display_names(), contains_exactly(*expected_display_names))

    def test_name(self):
        stub_native_project = tsn.create_stub_net_project(name='commodorum')
        sut = create_sut(stub_native_project)
        assert_that(sut.name, equal_to('commodorum'))

    def test_project_bounds_in_project_units(self):
        def us_oilfield_bounds():
            return tsn.StubProjectBounds(tsn.MeasurementDto(538990, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(668394, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(3439222, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(7227474, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(7491, units.UsOilfield.LENGTH),
                                         tsn.MeasurementDto(7713, units.UsOilfield.LENGTH))

        def metric_bounds():
            return tsn.StubProjectBounds(tsn.MeasurementDto(164284, units.Metric.LENGTH),
                                         tsn.MeasurementDto(203726, units.Metric.LENGTH),
                                         tsn.MeasurementDto(1048275, units.Metric.LENGTH),
                                         tsn.MeasurementDto(2202934, units.Metric.LENGTH),
                                         tsn.MeasurementDto(2283, units.Metric.LENGTH),
                                         tsn.MeasurementDto(2351, units.Metric.LENGTH))

        for orchid_actual, expected, project_units, tolerances in [
            (us_oilfield_bounds(),
             tsn.StubProjectBounds(538990 * om.registry.ft, 668394 * om.registry.ft,
                                   3439222 * om.registry.ft, 7227474 * om.registry.ft,
                                   7491 * om.registry.ft, 7713 * om.registry.ft),
             units.UsOilfield,
             tsn.StubProjectBounds(decimal.Decimal('1'), decimal.Decimal('1'),
                                   decimal.Decimal('1'), decimal.Decimal('1'),
                                   decimal.Decimal('1'), decimal.Decimal('1'))),
            (us_oilfield_bounds(),
             tsn.StubProjectBounds(164284 * om.registry.m, 203726 * om.registry.m,
                                   1048275 * om.registry.m, 2202934 * om.registry.m,
                                   2283 * om.registry.m, 2351 * om.registry.m),
             units.Metric,
             tsn.StubProjectBounds(decimal.Decimal('1'), decimal.Decimal('1'),
                                   decimal.Decimal('1'), decimal.Decimal('1'),
                                   decimal.Decimal('1'), decimal.Decimal('1'))),
            (metric_bounds(),
             tsn.StubProjectBounds(164284 * om.registry.m, 203726 * om.registry.m,
                                   1048275 * om.registry.m, 2202934 * om.registry.m,
                                   2283 * om.registry.m, 2351 * om.registry.m),
             units.Metric,
             tsn.StubProjectBounds(decimal.Decimal('1'), decimal.Decimal('1'),
                                   decimal.Decimal('1'), decimal.Decimal('1'),
                                   decimal.Decimal('1'), decimal.Decimal('1'))),
            (metric_bounds(),
             tsn.StubProjectBounds(538990 * om.registry.ft, 668394 * om.registry.ft,
                                   3439222 * om.registry.ft, 7227474 * om.registry.ft,
                                   7491 * om.registry.ft, 7713 * om.registry.ft),
             units.UsOilfield,
             tsn.StubProjectBounds(decimal.Decimal('1'), decimal.Decimal('3'),
                                   decimal.Decimal('1'), decimal.Decimal('1'),
                                   decimal.Decimal('1'), decimal.Decimal('1'))),
        ]:
            with self.subTest(f'Test project bounds {expected} in project units {project_units}'):
                stub_native_project = tsn.create_stub_net_project(project_bounds=orchid_actual,
                                                                  project_units=project_units)
                sut = create_sut(stub_native_project)
                tcm.assert_that_measurements_close_to(sut.project_bounds().min_x, expected.min_x, tolerances.min_x)
                tcm.assert_that_measurements_close_to(sut.project_bounds().max_x, expected.max_x, tolerances.max_x)
                tcm.assert_that_measurements_close_to(sut.project_bounds().min_y, expected.min_y, tolerances.min_y)
                tcm.assert_that_measurements_close_to(sut.project_bounds().max_y, expected.max_y, tolerances.max_y)
                tcm.assert_that_measurements_close_to(sut.project_bounds().min_y, expected.min_y, tolerances.min_y)
                tcm.assert_that_measurements_close_to(sut.project_bounds().max_y, expected.max_y, tolerances.max_y)

    def test_project_center_relative_to_well_head_in_project_units(self):
        for orchid_actual, expected, project_units, tolerances in [
            (tsn.StubSurfaceLocation(tsn.MeasurementDto(-106505, units.UsOilfield.LENGTH),
                                     tsn.MeasurementDto(-1777697, units.UsOilfield.LENGTH)),
             tsn.StubSurfaceLocation(-106505 * om.registry.ft, -1777697 * om.registry.ft),
             units.UsOilfield, tsn.StubSurfaceLocation(decimal.Decimal('1'), decimal.Decimal('1'))),
            (tsn.StubSurfaceLocation(tsn.MeasurementDto(-106.5e3, units.UsOilfield.LENGTH),
                                     tsn.MeasurementDto(-1.778e6, units.UsOilfield.LENGTH)),
             tsn.StubSurfaceLocation(-32.46e3 * om.registry.m, -541.9e3 * om.registry.m),
             units.Metric, tsn.StubSurfaceLocation(decimal.Decimal('20'), decimal.Decimal('0.4e3'))),
            (tsn.StubSurfaceLocation(tsn.MeasurementDto(106.7e3, units.Metric.LENGTH),
                                     tsn.MeasurementDto(870.0e3, units.Metric.LENGTH)),
             tsn.StubSurfaceLocation(106.7e3 * om.registry.m, 870.0e3 * om.registry.m),
             units.Metric, tsn.StubSurfaceLocation(decimal.Decimal('0.1e3'), decimal.Decimal('0.1e3'))),
            (tsn.StubSurfaceLocation(tsn.MeasurementDto(106.7e3, units.Metric.LENGTH),
                                     tsn.MeasurementDto(870.0e3, units.Metric.LENGTH)),
             tsn.StubSurfaceLocation(350.1e3 * om.registry.ft, 2.854e6 * om.registry.ft),
             units.UsOilfield, tsn.StubSurfaceLocation(decimal.Decimal('0.4e3'), decimal.Decimal('0.4e3'))),
        ]:
            with self.subTest(f'Test project center {expected} in project units {project_units}'):
                stub_native_project = tsn.create_stub_net_project(project_center=orchid_actual,
                                                                  project_units=project_units)
                sut = create_sut(stub_native_project)
                tcm.assert_that_measurements_close_to(sut.project_center().x, expected.x, tolerances.x)
                tcm.assert_that_measurements_close_to(sut.project_center().y, expected.y, tolerances.y)

    def test_project_units_if_known(self):
        for expected_project_units in [units.Metric, units.UsOilfield]:
            with self.subTest(f'Testing if project has known units, "{expected_project_units}"'):
                stub_native_project = tsn.create_stub_net_project(project_units=expected_project_units)
                sut = create_sut(stub_native_project)

                assert_that(sut.project_units, equal_to(expected_project_units))

    def test_project_units_raises_type_error_if_unknown(self):
        stub_native_project = tsn.create_stub_net_project()
        sut = create_sut(stub_native_project)

        # I define this "phony" function because the expression returned by a property **is not** a
        # `callable`. By wrapping this expression in a function, I can than use `calling` and `raises`
        # to test for an expected exception.
        def phony_function():
            print(sut.project_units)

        # noinspection PyTypeChecker
        assert_that(calling(phony_function), raises(ValueError, pattern='^Unrecognized unit system'))

    def test_proppant_concentration_mass_unit(self):
        for expected_unit_system in [units.UsOilfield, units.Metric]:
            with self.subTest(f'Test proppant concentration mass unit: {expected_unit_system.MASS}'):
                stub_native_project = tsn.create_stub_net_project(project_units=expected_unit_system)
                sut = create_sut(stub_native_project)

                assert_that(sut.proppant_concentration_mass_unit(), equal_to(expected_unit_system.MASS))

    def test_proppant_concentration_mass_unit_raises_error_if_unit_system_unknown(self):
        stub_native_project = tsn.create_stub_net_project()
        sut = create_sut(stub_native_project)

        assert_that(calling(onp.Project.proppant_concentration_mass_unit).with_args(sut), raises(ValueError))

    def test_slurry_rate_volume_unit(self):
        for expected_unit_system in [units.UsOilfield, units.Metric]:
            with self.subTest(f'Test slurry rate volume unit: {expected_unit_system.VOLUME}'):
                stub_native_project = tsn.create_stub_net_project(project_units=expected_unit_system)
                sut = create_sut(stub_native_project)

                assert_that(sut.slurry_rate_volume_unit(), equal_to(expected_unit_system.VOLUME))

    def test_slurry_rate_volume_unit_raises_error_if_unit_system_unknown(self):
        stub_native_project = tsn.create_stub_net_project()
        sut = create_sut(stub_native_project)

        assert_that(calling(onp.Project.slurry_rate_volume_unit).with_args(sut), raises(ValueError))

    def test_time_series(self):
        for time_series_dtos in (
                (),
                # Need trailing comma inside parentheses to retain tuple
                ({'object_id': tsn.DONT_CARE_ID_A, 'display_name': 'malae', 'name': 'lustrabit'},),
                # Don't care about object IDs but must be unique
                ({'object_id': tsn.DONT_CARE_ID_B, 'display_name': 'vivis', 'name': 'mulgetis'},
                 {'object_id': tsn.DONT_CARE_ID_C, 'display_name': 'pluvia', 'name': 'aedificabatis'},
                 {'object_id': tsn.DONT_CARE_ID_D, 'display_name': 'lautus', 'name': 'adventicieae'})
        ):
            get_time_series_dtos_property = tsn.get_dtos_property(time_series_dtos)
            expected_object_ids = get_time_series_dtos_property('object_id', transform=uuid.UUID)
            expected_display_names = get_time_series_dtos_property('display_name')
            expected_names = get_time_series_dtos_property('name')
            with self.subTest(f'Verify time series object IDs, {expected_object_ids}'
                              f' display_names, {expected_display_names},'
                              f' and names, {expected_names}'):
                stub_native_project = tsn.create_stub_net_project(time_series_dtos=time_series_dtos)
                sut = create_sut(stub_native_project)

                assert_that(sut.time_series().all_object_ids(), contains_exactly(*expected_object_ids))
                assert_that(sut.time_series().all_display_names(), contains_exactly(*expected_display_names))
                assert_that(sut.time_series().all_names(), contains_exactly(*expected_names))

    def test_wells(self):
        for well_dtos in (
                (),
                ({'object_id': tsn.DONT_CARE_ID_A, 'name': 'congruent'},),  # need trailing comma to retain tuple
                # Don't care about object IDs but must be unique
                ({'object_id': tsn.DONT_CARE_ID_B, 'name': 'histrio'},
                 {'object_id': tsn.DONT_CARE_ID_C, 'name': 'principis'},
                 {'object_id': tsn.DONT_CARE_ID_D, 'name': 'quaesivuisti'})
        ):
            get_well_dtos_property = tsn.get_dtos_property(well_dtos)
            expected_object_ids = get_well_dtos_property('object_id', transform=uuid.UUID)
            expected_names = get_well_dtos_property('name')
            with self.subTest(f'Verify wells object IDs, {expected_object_ids}'
                              f' and names, {expected_names}'):
                stub_native_project = tsn.create_stub_net_project(well_dtos=well_dtos)
                sut = create_sut(stub_native_project)

                assert_that(sut.wells().all_object_ids(), contains_exactly(*expected_object_ids))
                assert_that(sut.wells().all_names(), contains_exactly(*expected_names))


def create_sut(stub_net_project):
    patched_loader = loader.ProjectStore('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = onp.Project(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()
