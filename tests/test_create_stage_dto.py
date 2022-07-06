#  Copyright 2017-2022 Reveal Energy Services, Inc
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
import math
import unittest
import unittest.mock

from hamcrest import assert_that, equal_to, calling, raises, is_, none
import pendulum as pdt
import toolz.curried as toolz

from orchid import (
    measurement as om,
    native_stage_adapter as nsa,
    native_well_adapter as nwa,
    unit_system as units,
)

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import ScriptAdapter
# noinspection PyUnresolvedReferences
from System import (Action, DateTime, DateTimeKind, Int32, UInt32)
# noinspection PyUnresolvedReferences
import UnitsNet


def assert_transformed_argument_equals_expected(stub_object_factory, actual_argument_index, expected):
    actual_call_args = stub_object_factory.CreateStage.call_args
    actual_transformed_stage_number = actual_call_args.args[actual_argument_index]
    assert_that(actual_transformed_stage_number, equal_to(expected))


def assert_transformed_net_quantities_close_to(stub_object_factory, actual_argument_index, expected,
                                               tolerance):
    actual_call_args = stub_object_factory.CreateStage.call_args
    actual_transformed_md_top = actual_call_args.args[actual_argument_index]
    tcm.assert_that_net_quantities_close_to(actual_transformed_md_top, expected, tolerance=tolerance)


def create_stub_well_obs(stub_as_unit_system, stub_object_factory, stub_unit_system):
    stub_net_stage_part = tsn.StagePartDto().create_net_stub()
    stub_object_factory.CreateStagePart.return_value = stub_net_stage_part

    stub_net_mutable_stage = tsn.MutableStagePartDto().create_net_stub()
    stub_net_stage = tsn.StageDto().create_net_stub()
    stub_net_stage.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_stage)
    stub_object_factory.CreateStage.return_value = stub_net_stage
    stub_as_unit_system.return_value = stub_unit_system
    stub_net_well = tsn.WellDto().create_net_stub()
    stub_well = nwa.NativeWellAdapter(stub_net_well)
    return stub_well


def make_net_date_time(year, month, day, hour, minute, second):
    result = DateTime.Overloads[Int32, Int32, Int32, Int32, Int32, Int32, DateTimeKind](year, month, day,
                                                                                        hour, minute, second,
                                                                                        DateTimeKind.Utc)
    return result


# Test ideas
# - create_stage calls object factory CreateStageParts with correct arguments all specified
#   - Time range (specified)
#   - Time range (not-specified)
#   - Isip (specified)
#   - Isip (non-specified)
class TestCreateStageDto(unittest.TestCase):
    DONT_CARE_STAGE_DETAILS = {
            'stage_no': 22,
            'connection_type': nsa.ConnectionType.PLUG_AND_PERF,
            'md_top': 14582.1 * om.registry.ft,
            'md_bottom': 14720.1 * om.registry.ft,
        }

    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_create_stage_dto_returns_correct_order_of_completion_on_well(self):
        created_stage = nsa.CreateStageDto(**toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                         {'stage_no': 34}))

        assert_that(created_stage.order_of_completion_on_well, equal_to(33))

    def test_create_stage_dto_throws_exception_if_stage_no_not_positive(self):
        assert_that(calling(nsa.CreateStageDto).with_args(**toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                                        {'stage_no': 0})),
                    raises(ValueError,
                           pattern=f'Expected stage_no to be positive. Found 0'))

    def test_create_stage_dto_throws_exception_if_md_top_not_length(self):
        assert_that(calling(nsa.CreateStageDto).with_args(**toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                                        {'md_top': 227.661 * om.registry.deg})),
                    raises(ValueError,
                           pattern=f'Expected md_top to be a length. Found {(227.661 * om.registry.deg):~P}'))

    def test_create_stage_dto_throws_exception_if_md_bottom_not_length(self):
        assert_that(calling(nsa.CreateStageDto).with_args(**toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                                        {'md_bottom': 7260.14 * om.registry.psi})),
                    raises(ValueError,
                           pattern=f'Expected md_bottom to be a length. Found {(7260.14 * om.registry.psi):~P}'))

    def test_create_stage_dto_throws_exception_if_cluster_count_is_negative(self):
        assert_that(calling(nsa.CreateStageDto).with_args(**toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                                        {'cluster_count': -1})),
                    raises(ValueError,
                           pattern=f'Expected cluster_count to be non-negative. Found -1'))

    def test_create_stage_dto_throws_exception_if_maybe_isip_has_value_but_is_not_pressure(self):
        assert_that(calling(nsa.CreateStageDto).with_args(**toolz.merge(
            self.DONT_CARE_STAGE_DETAILS, {'maybe_isip': om.Quantity(5.22410, om.registry.degC)})),
                    raises(ValueError,
                           pattern=f'Expected maybe_isip to be a pressure if not None.'
                                   f' Found {om.Quantity(5.22410, om.registry.degC):~P}'))

    def test_create_stage_dto_throws_exception_if_maybe_shmin_has_value_but_is_not_pressure(self):
        assert_that(calling(nsa.CreateStageDto).with_args(**toolz.merge(
            self.DONT_CARE_STAGE_DETAILS, {'maybe_shmin': 172.8 * om.registry.ft})),
                    raises(ValueError,
                           pattern=f'Expected maybe_shmin to be a pressure if not None.'
                                   f' Found {172.8 * om.registry.ft:~P}'))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_once(self,
                                                              stub_add_stage_part_to_stage,
                                                              stub_object_factory,
                                                              stub_as_unit_system):
        stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, units.Metric)
        create_stage_details = self.DONT_CARE_STAGE_DETAILS
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        stub_object_factory.CreateStage.assert_called_once()

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_stage_no(self,
                                                                                   stub_add_stage_part_to_stage,
                                                                                   stub_object_factory,
                                                                                   stub_as_unit_system):
        stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, units.UsOilfield)
        create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'stage_no': 23})
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        # transformed stage_no
        assert_transformed_argument_equals_expected(stub_object_factory, 0, UInt32(22))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_well_dom_object(self,
                                                                              stub_add_stage_part_to_stage,
                                                                              stub_object_factory,
                                                                              stub_as_unit_system):
        stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, units.Metric)
        create_stage_details = self.DONT_CARE_STAGE_DETAILS
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        # well_object
        # TODO: Uncertain if querying `dom_object` on `stub_well` is best choice
        # But I do not think I want to add a `stub_net_well` argument to `create_stub_well` is
        # a better choice.
        assert_transformed_argument_equals_expected(stub_object_factory, 1, stub_well.dom_object)

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_connection_type(self,
                                                                                          stub_add_stage_part_to_stage,
                                                                                          stub_object_factory,
                                                                                          stub_as_unit_system):
        stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, units.UsOilfield)
        create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                           {'connection_type': nsa.ConnectionType.PLUG_AND_PERF})
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        # transformed connection_type
        assert_transformed_argument_equals_expected(stub_object_factory, 2, nsa.ConnectionType.PLUG_AND_PERF)

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_md_top(self,
                                                                                 stub_add_stage_part_to_stage,
                                                                                 stub_object_factory,
                                                                                 stub_as_unit_system):
        for source, project_unit_system, expected in [
            (3714.60 * om.registry.m, units.Metric,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(3714.60))),
            (3714.60 * om.registry.m,
             units.UsOilfield, UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(12187.00))),
            (math.nan * om.registry.ft, units.Metric, None),
            (math.nan * om.registry.ft, units.UsOilfield, None),
        ]:
            with self.subTest(f'Create stage transformed md_top={source}'
                              f' in {project_unit_system.LENGTH}'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, project_unit_system)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'md_top': source})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                # transformed md_top
                assert_transformed_net_quantities_close_to(stub_object_factory, 3,
                                                           expected, decimal.Decimal('0.01'))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_md_bottom(self,
                                                                                    stub_add_stage_part_to_stage,
                                                                                    stub_object_factory,
                                                                                    stub_as_unit_system):
        for source, project_unit_system, expected in [
            (16329.7 * om.registry.ft, units.Metric,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(4977.29))),
            (16329.7 * om.registry.ft,
             units.UsOilfield, UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(16329.7))),
            (math.nan * om.registry.m, units.Metric, None),
            (math.nan * om.registry.m, units.UsOilfield, None),
        ]:
            with self.subTest(f'Create stage transformed md_bottom={source}'
                              f' in {project_unit_system.LENGTH}'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, project_unit_system)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'md_bottom': source})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                # transformed md_bottom
                assert_transformed_net_quantities_close_to(stub_object_factory, 4,
                                                           expected, decimal.Decimal('0.01'))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_supplied_cluster_count(self,
                                                                                     stub_add_stage_part_to_stage,
                                                                                     stub_object_factory,
                                                                                     stub_as_unit_system):
        stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, units.UsOilfield)
        create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'cluster_count': 4})
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        assert_transformed_argument_equals_expected(stub_object_factory, 6, UInt32(4))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_shmin(self,
                                                                                stub_add_stage_part_to_stage,
                                                                                stub_object_factory,
                                                                                stub_as_unit_system):
        for source, project_unit_system, expected, tolerance in [
            (2.27576 * om.registry.psi, units.UsOilfield,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(2.27576)),
             decimal.Decimal('0.00001')),
            (2.27576 * om.registry.psi,
             units.Metric, UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(15.6908)),
             decimal.Decimal('0.0001')),
        ]:
            with self.subTest(f'Create stage transformed shmin={source}'
                              f' in {project_unit_system.PRESSURE}'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, project_unit_system)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'maybe_shmin': source})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                def assert_actual_close_to(actual):
                    tcm.assert_that_net_quantities_close_to(actual, expected,
                                                            tolerance=tolerance)

                def assert_actual_not_none():
                    self.fail('Expected some pressure but found none.')

                actual_call_args = stub_object_factory.CreateStage.call_args
                actual_transformed_shmin = actual_call_args.args[5]  # transformed shmin
                actual_transformed_shmin.Match(
                    Action[UnitsNet.Pressure](assert_actual_close_to),
                    Action(assert_actual_not_none))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_nan_shmin(self,
                                                                                    stub_add_stage_part_to_stage,
                                                                                    stub_object_factory,
                                                                                    stub_as_unit_system):
        for source, project_unit_system in [
            (math.nan * om.registry.kPa, units.Metric),
            (math.nan * om.registry.kPa, units.UsOilfield),
        ]:
            with self.subTest(f'Create stage transformed nan shmin={source}'
                              f' in {project_unit_system.PRESSURE}'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, project_unit_system)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'maybe_shmin': source})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                actual_call_args = stub_object_factory.CreateStage.call_args
                actual_transformed_shmin = actual_call_args.args[5]  # transformed shmin
                assert_that(actual_transformed_shmin.HasValue, equal_to(False))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_part_with_transformed_start_time(self,
                                                                                          stub_add_stage_part_to_stage,
                                                                                          stub_object_factory,
                                                                                          stub_as_unit_system):
        for actual_time_range, expected_start_time in [
            (pdt.parse('2019-12-29T12:35:15/2019-12-29T14:38:55', tz='UTC'),
             make_net_date_time(2019, 12, 29, 12, 35, 15)),
        ]:
            with self.subTest(f'Actual time range={actual_time_range}, expected start time={expected_start_time}'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, units.UsOilfield)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                   {'maybe_time_range': actual_time_range})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                # transformed time range of stage part
                actual_call_args = stub_object_factory.CreateStagePart.call_args
                actual_transformed_maybe_time_range_start = actual_call_args.args[1]
                assert_that(actual_transformed_maybe_time_range_start,
                            tcm.equal_to_net_date_time(expected_start_time))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_part_with_transformed_stop_time(self,
                                                                                         stub_add_stage_part_to_stage,
                                                                                         stub_object_factory,
                                                                                         stub_as_unit_system):
        for actual_time_range, expected_stop_time in [
            (pdt.parse('2019-12-29T12:35:15/2019-12-29T14:38:55', tz='UTC'),
             make_net_date_time(2019, 12, 29, 14, 38, 55)),
        ]:
            with self.subTest(f'Actual time range={actual_time_range}, expected stop time={expected_stop_time}'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, units.UsOilfield)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                   {'maybe_time_range': actual_time_range})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                # transformed time range of stage part
                actual_call_args = stub_object_factory.CreateStagePart.call_args
                actual_transformed_maybe_time_range_start = actual_call_args.args[2]
                assert_that(actual_transformed_maybe_time_range_start,
                            tcm.equal_to_net_date_time(expected_stop_time))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_part_with_transformed_some_isip(self,
                                                                                         stub_add_stage_part_to_stage,
                                                                                         stub_object_factory,
                                                                                         stub_as_unit_system):
        for actual_isip, project_unit_system, expected_isip, tolerance in [
            (5082.46 * om.registry.psi, units.UsOilfield,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(5082.46)),
             decimal.Decimal('0.01')),
            (5082.46 * om.registry.psi, units.Metric,
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(35042.4)),
             decimal.Decimal('0.1')),
        ]:
            with self.subTest(f'{actual_isip=:~P}, {project_unit_system=}, {expected_isip.ToString()}'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, project_unit_system)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                   {'maybe_isip': actual_isip})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                # transformed time range of stage part
                actual_call_args = stub_object_factory.CreateStagePart.call_args
                actual_transformed_maybe_isip_start = actual_call_args.args[3]
                assert_that(actual_transformed_maybe_isip_start,
                            tcm.assert_that_net_quantities_close_to(actual_transformed_maybe_isip_start,
                                                                    expected_isip,
                                                                    tolerance))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_calls_factory_create_stage_part_with_transformed_none_isip(self,
                                                                                         stub_add_stage_part_to_stage,
                                                                                         stub_object_factory,
                                                                                         stub_as_unit_system):
        for actual_isip, project_unit_system in [
            (None, units.UsOilfield),
            (None, units.Metric),
            (math.nan * om.registry.kPa, units.UsOilfield),
            (math.nan * om.registry.kPa, units.Metric),
        ]:
            with self.subTest(f'actual_isip={actual_isip if actual_isip is not None else "None"},'
                              f' {project_unit_system=}, expected_isip=None'):
                stub_well = create_stub_well_obs(stub_as_unit_system, stub_object_factory, project_unit_system)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                                   {'maybe_isip': actual_isip})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                # transformed time range of stage part
                actual_call_args = stub_object_factory.CreateStagePart.call_args
                actual_transformed_maybe_isip_start = actual_call_args.args[3]
                assert_that(actual_transformed_maybe_isip_start, is_(none()))


    # noinspection PyUnresolvedReferences
    @unittest.skip('Refactoring other tests')
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_created_stage_part_to_created_stage')
    def test_dto_create_stage_adds_created_stage_part_to_created_stage_parts_list(self,
                                                                                  stub_add_stage_part_to_stage,
                                                                                  stub_object_factory,
                                                                                  stub_as_unit_system):
        stub_net_stage_part = tsn.StagePartDto().create_net_stub()
        stub_object_factory.CreateStagePart.return_value = stub_net_stage_part

        stub_net_mutable_stage = tsn.MutableStagePartDto().create_net_stub()
        stub_net_stage = tsn.StageDto().create_net_stub()
        stub_net_stage.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_stage)
        stub_object_factory.CreateStage.return_value = stub_net_stage
        stub_as_unit_system.return_value = units.UsOilfield
        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        dont_care_time_range = pdt.parse('2028-12-20T05:35:51/2028-12-20T08:59:38', tz='UTC')
        dont_care_isip = 5164.78 * om.registry.psi
        create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                           {'maybe_time_range': dont_care_time_range},
                                           {'maybe_isip': dont_care_isip})
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        stub_add_stage_part_to_stage.Add.assert_called_once_with(stub_net_mutable_stage,
                                                                 stub_created_stage_part)


if __name__ == '__main__':
    unittest.main()
