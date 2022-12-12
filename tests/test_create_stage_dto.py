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


def assert_transformed_argument_equals_expected_obs(stub_object_factory, actual_argument_index, expected):
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


def make_created_net_stage():
    stub_net_stage = tsn.StageDto().create_net_stub()
    stub_net_mutable_stage = tsn.MutableStageDto().create_net_stub()
    stub_net_stage.ToMutable.return_value = stub_net_mutable_stage
    return stub_net_stage


def make_net_date_time(year, month, day, hour, minute, second):
    result = DateTime(year, month, day, hour, minute, second, DateTimeKind.Utc)
    return result


# Test ideas
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
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_create_net_stage_once(self,
                                                          stub_add_stage_part_to_stage,
                                                          stub_create_net_stage_part,
                                                          stub_create_net_stage,
                                                          stub_as_unit_system):
        stub_create_net_stage.return_value = make_created_net_stage()
        stub_as_unit_system.return_value = units.Metric

        builder = CreateStageDtoBuilder()
        sut = builder.build()

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        sut.create_stage(stub_well)

        stub_create_net_stage.assert_called_once()

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_create_net_stage_with_net_well(self,
                                                                   stub_add_stage_part_to_stage,
                                                                   stub_create_net_stage_part,
                                                                   stub_create_net_stage,
                                                                   stub_as_unit_system):
        stub_create_net_stage.return_value = make_created_net_stage()
        stub_as_unit_system.return_value = units.Metric

        builder = CreateStageDtoBuilder()
        sut = builder.build()

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        sut.create_stage(stub_well)

        # well_object
        actual_net_well = stub_create_net_stage.call_args.args[0]
        assert_that(actual_net_well, equal_to(stub_net_well))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_create_net_stage_with_transformed_stage_no(self,
                                                                               stub_add_stage_part_to_stage,
                                                                               stub_create_net_stage_part,
                                                                               stub_create_net_stage,
                                                                               stub_as_unit_system):
        stub_create_net_stage.return_value = make_created_net_stage()
        stub_as_unit_system.return_value = units.Metric

        builder = CreateStageDtoBuilder().with_stage_no(21)
        sut = builder.build()

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        sut.create_stage(stub_well)

        # transformed stage_no
        actual_transformed_stage_number = stub_create_net_stage.call_args.args[1]
        assert_that(actual_transformed_stage_number,
                    equal_to(UInt32(builder.order_of_completion_on_well)))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_connection_type(self,
                                                                                          stub_add_stage_part_to_stage,
                                                                                          stub_create_net_stage_part,
                                                                                          stub_create_net_stage,
                                                                                          stub_as_unit_system):
        stub_create_net_stage.return_value = make_created_net_stage()
        stub_as_unit_system.return_value = units.UsOilfield

        builder = CreateStageDtoBuilder().with_connection_type(nsa.ConnectionType.SINGLE_POINT_ENTRY)
        sut = builder.build()

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        sut.create_stage(stub_well)

        # transformed connection_type
        actual_transformed_connection_type = stub_create_net_stage.call_args.args[2]
        assert_that(actual_transformed_connection_type, equal_to(nsa.ConnectionType.SINGLE_POINT_ENTRY.value))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_md_top(self,
                                                                                 stub_add_stage_part_to_stage,
                                                                                 stub_create_net_stage_part,
                                                                                 stub_create_net_stage,
                                                                                 stub_as_unit_system):
        for md_top, project_unit_system, expected, tolerance in [
            (3714.60 * om.registry.m, units.Metric,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(3714.60)),
             decimal.Decimal('0.01')),
            (3714.60 * om.registry.m,
             units.UsOilfield, UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(12187.0)),
             decimal.Decimal('0.1')),
            (math.nan * om.registry.ft, units.Metric, None, None),
            (math.nan * om.registry.ft, units.UsOilfield, None, None),
        ]:
            expected_text = f'{expected.ToString()}' if expected is not None else 'None'
            with self.subTest(f'Create stage {md_top=} in {project_unit_system.LENGTH}'
                              f' expected={expected_text}'):
                stub_create_net_stage.return_value = make_created_net_stage()
                stub_as_unit_system.return_value = project_unit_system

                builder = CreateStageDtoBuilder().with_md_top(md_top)
                sut = builder.build()

                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                sut.create_stage(stub_well)

                # transformed md_top
                actual_transformed_md_top = stub_create_net_stage.call_args.args[3]
                if expected is not None:
                    tcm.assert_that_net_quantities_close_to(actual_transformed_md_top, expected, tolerance=tolerance)
                else:
                    assert_that(actual_transformed_md_top, is_(none()))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_md_bottom(self,
                                                                                    stub_add_stage_part_to_stage,
                                                                                    stub_create_net_stage_part,
                                                                                    stub_create_net_stage,
                                                                                    stub_as_unit_system):
        for md_bottom, project_unit_system, expected, tolerance in [
            (16329.7 * om.registry.ft, units.Metric,
             UnitsNet.Length.FromMeters(UnitsNet.QuantityValue.op_Implicit(4977.29)),
             decimal.Decimal('0.01')),
            (16329.7 * om.registry.ft,
             units.UsOilfield, UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(16329.7)),
             decimal.Decimal('0.1')),
            (math.nan * om.registry.ft, units.Metric, None, None),
            (math.nan * om.registry.ft, units.UsOilfield, None, None),
        ]:
            expected_text = f'{expected.ToString()}' if expected is not None else 'None'
            with self.subTest(f'Create stage {md_bottom=} in {project_unit_system.LENGTH}'
                              f' expected={expected_text}'):
                stub_create_net_stage.return_value = make_created_net_stage()
                stub_as_unit_system.return_value = project_unit_system

                builder = CreateStageDtoBuilder().with_md_bottom(md_bottom)
                sut = builder.build()

                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                sut.create_stage(stub_well)

                # transformed md_top
                actual_transformed_md_bottom = stub_create_net_stage.call_args.args[4]
                if expected is not None:
                    tcm.assert_that_net_quantities_close_to(actual_transformed_md_bottom,
                                                            expected, tolerance=tolerance)
                else:
                    assert_that(actual_transformed_md_bottom, is_(none()))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_supplied_cluster_count(self,
                                                                                     stub_add_stage_part_to_stage,
                                                                                     stub_create_net_stage_part,
                                                                                     stub_create_net_stage,
                                                                                     stub_as_unit_system):
        stub_create_net_stage.return_value = make_created_net_stage()
        stub_as_unit_system.return_value = units.UsOilfield

        builder = CreateStageDtoBuilder().with_cluster_count(7)
        sut = builder.build()

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        sut.create_stage(stub_well)

        # transformed stage_no
        actual_transformed_cluster_count = stub_create_net_stage.call_args.args[6]
        assert_that(actual_transformed_cluster_count, equal_to(UInt32(7)))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_shmin(self,
                                                                                stub_add_stage_part_to_stage,
                                                                                stub_create_net_stage_part,
                                                                                stub_create_net_stage,
                                                                                stub_as_unit_system):
        for maybe_shmin, project_unit_system, expected, tolerance in [
            (2.27576 * om.registry.psi, units.UsOilfield,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(2.27576)),
             decimal.Decimal('0.00001')),
            (2.27576 * om.registry.psi,
             units.Metric, UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(15.6908)),
             decimal.Decimal('0.0001')),
        ]:
            with self.subTest(f'Create stage transformed shmin={maybe_shmin}'
                              f' in {project_unit_system.PRESSURE}'):
                stub_create_net_stage.return_value = make_created_net_stage()
                stub_as_unit_system.return_value = project_unit_system

                builder = CreateStageDtoBuilder().with_maybe_shmin(maybe_shmin)
                sut = builder.build()

                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                sut.create_stage(stub_well)

                def assert_actual_close_to(actual):
                    tcm.assert_that_net_quantities_close_to(actual, expected,
                                                            tolerance=tolerance)

                def assert_actual_not_none():
                    self.fail('Expected some shmin but found none.')

                # transformed shmin
                actual_transformed_shmin = stub_create_net_stage.call_args.args[5]
                actual_transformed_shmin.Match(
                    Action[UnitsNet.Pressure](assert_actual_close_to),
                    Action(assert_actual_not_none))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_no_shmin(self,
                                                                                   stub_add_stage_part_to_stage,
                                                                                   stub_create_net_stage_part,
                                                                                   stub_create_net_stage,
                                                                                   stub_as_unit_system):
        for maybe_shmin, project_unit_system in [
            (math.nan * om.registry.kPa, units.Metric),
            (math.nan * om.registry.kPa, units.UsOilfield),
            (None, units.Metric),
            (None, units.UsOilfield),
        ]:
            with self.subTest(f'Create stage transformed nan shmin={maybe_shmin}'
                              f' in {project_unit_system.PRESSURE}'):
                stub_create_net_stage.return_value = make_created_net_stage()
                stub_as_unit_system.return_value = project_unit_system

                builder = CreateStageDtoBuilder().with_maybe_shmin(maybe_shmin)
                sut = builder.build()

                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                sut.create_stage(stub_well)

                # transformed shmin
                actual_transformed_shmin = stub_create_net_stage.call_args.args[5]
                assert_that(actual_transformed_shmin.HasValue, equal_to(False))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_part_with_transformed_start_time(self,
                                                                                          stub_add_stage_part_to_stage,
                                                                                          stub_create_net_stage_part,
                                                                                          stub_create_net_stage,
                                                                                          stub_as_unit_system):
        for actual_time_range, expected_start_time in [
            (pdt.parse('2019-12-29T12:35:15/2019-12-29T14:38:55', tz='UTC'),
             make_net_date_time(2019, 12, 29, 12, 35, 15)),
        ]:
            with self.subTest(f'Actual time range={actual_time_range}, expected start time={expected_start_time}'):
                stub_create_net_stage.return_value = make_created_net_stage()
                stub_as_unit_system.return_value = units.UsOilfield

                builder = CreateStageDtoBuilder().with_maybe_time_range(actual_time_range)
                sut = builder.build()

                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                sut.create_stage(stub_well)

                # transformed time range of stage part
                actual_transformed_maybe_time_range_start = stub_create_net_stage_part.call_args.args[1]
                assert_that(actual_transformed_maybe_time_range_start,
                            tcm.equal_to_net_date_time(expected_start_time))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_part_with_transformed_stop_time(self,
                                                                                         stub_add_stage_part_to_stage,
                                                                                         stub_create_net_stage_part,
                                                                                         stub_create_net_stage,
                                                                                         stub_as_unit_system):
        for actual_time_range, expected_stop_time in [
            (pdt.parse('2019-12-29T12:35:15/2019-12-29T14:38:55', tz='UTC'),
             make_net_date_time(2019, 12, 29, 14, 38, 55)),
        ]:
            with self.subTest(f'Actual time range={actual_time_range}, expected stop time={expected_stop_time}'):
                stub_create_net_stage.return_value = make_created_net_stage()
                stub_as_unit_system.return_value = units.UsOilfield

                builder = CreateStageDtoBuilder().with_maybe_time_range(actual_time_range)
                sut = builder.build()

                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                sut.create_stage(stub_well)

                # transformed time range of stage part
                actual_transformed_maybe_time_range_stop = stub_create_net_stage_part.call_args.args[2]
                assert_that(actual_transformed_maybe_time_range_stop,
                            tcm.equal_to_net_date_time(expected_stop_time))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_calls_factory_create_stage_part_with_transformed_isip(self,
                                                                                    stub_add_stage_part_to_stage,
                                                                                    stub_create_net_stage_part,
                                                                                    stub_create_net_stage,
                                                                                    stub_as_unit_system):
        for actual, project_unit_system, expected, tolerance in [
            (5082.46 * om.registry.psi, units.UsOilfield,
             UnitsNet.Pressure.FromPoundsForcePerSquareInch(UnitsNet.QuantityValue.op_Implicit(5082.46)),
             decimal.Decimal('0.01')),
            (5082.46 * om.registry.psi, units.Metric,
             UnitsNet.Pressure.FromKilopascals(UnitsNet.QuantityValue.op_Implicit(35042.4)),
             decimal.Decimal('0.1')),
            (None, units.UsOilfield, None, None),
            (None, units.Metric, None, None),
            (math.nan * om.registry.kPa, units.UsOilfield, None, None),
            (math.nan * om.registry.kPa, units.Metric, None, None),
        ]:
            actual_text = f'{actual:~P}' if actual is not None else 'None'
            expected_text = f'{expected.ToString()}' if expected is not None else 'None'
            with self.subTest(f'{actual_text}, {project_unit_system=}, {expected_text}'):
                stub_create_net_stage.return_value = make_created_net_stage()
                stub_as_unit_system.return_value = project_unit_system

                builder = CreateStageDtoBuilder().with_maybe_isip(actual)
                sut = builder.build()

                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                sut.create_stage(stub_well)

                # transformed time range of stage part
                actual_transformed_maybe_isip_start = stub_create_net_stage_part.call_args.args[3]
                if expected is not None:
                    assert_that(actual_transformed_maybe_isip_start,
                                tcm.assert_that_net_quantities_close_to(actual_transformed_maybe_isip_start,
                                                                        expected,
                                                                        tolerance))
                else:
                    assert_that(actual_transformed_maybe_isip_start, is_(none()))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.create_net_stage_part')
    @unittest.mock.patch('orchid.native_stage_adapter.CreateStageDto.add_stage_part_to_stage')
    def test_dto_create_stage_adds_created_stage_part_to_created_stage_parts_list(self,
                                                                                  stub_add_stage_part_to_stage,
                                                                                  stub_create_net_stage_part,
                                                                                  stub_create_net_stage,
                                                                                  stub_as_unit_system):
        stub_net_stage_part = tsn.StagePartDto().create_net_stub()
        stub_create_net_stage_part.return_value = stub_net_stage_part

        stub_net_stage = make_created_net_stage()
        stub_create_net_stage.return_value = stub_net_stage
        stub_net_mutable_stage = tsn.MutableStagePartDto().create_net_stub()
        stub_net_stage.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_stage)

        stub_as_unit_system.return_value = units.UsOilfield

        dont_care_time_range = pdt.parse('2028-12-20T05:35:51/2028-12-20T08:59:38', tz='UTC')
        dont_care_isip = 5164.78 * om.registry.psi
        builder = (CreateStageDtoBuilder()
                   .with_maybe_time_range(dont_care_time_range)
                   .with_maybe_isip(dont_care_isip))
        sut = builder.build()

        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        sut.create_stage(stub_well)

        stub_add_stage_part_to_stage.assert_called_once_with(stub_net_mutable_stage,
                                                             stub_net_stage_part)


class CreateStageDtoBuilder:
    """
    This class builds instances of `CreateStageDto` instances for testing.

    Because my tests query the "side effects" of the `CreateStageDto.create_stage()`, this builder constructs mock
    instances for both the created .NET objects and the Python wrappers where needed.
    """

    def __init__(self, stage_no=22, connection_type=nsa.ConnectionType.PLUG_AND_PERF,
                 md_top=14582.1 * om.registry.ft, md_bottom=14720.1 * om.registry.ft):
        self._stage_no = stage_no
        self._connection_type = connection_type
        self._md_top = md_top
        self._md_bottom = md_bottom

        self._options = {}

    @property
    def order_of_completion_on_well(self):
        return self._stage_no - 1

    def build(self) -> nsa.CreateStageDto:
        return nsa.CreateStageDto(stage_no=self._stage_no,
                                  connection_type=self._connection_type,
                                  md_top=self._md_top,
                                  md_bottom=self._md_bottom,
                                  **self._options)

    def with_stage_no(self, stage_no):
        self._stage_no = stage_no
        return self

    def with_connection_type(self, connection_type):
        self._connection_type = connection_type
        return self

    def with_md_top(self, md_top):
        self._md_top = md_top
        return self

    def with_md_bottom(self, md_bottom):
        self._md_bottom = md_bottom
        return self

    def with_cluster_count(self, cluster_count):
        self._options = toolz.assoc(self._options, 'cluster_count', cluster_count)
        return self

    def with_maybe_shmin(self, shmin):
        self._options = toolz.assoc(self._options, 'maybe_shmin', shmin)
        return self

    def with_maybe_time_range(self, maybe_time_range):
        self._options = toolz.assoc(self._options, 'maybe_time_range', maybe_time_range)
        return self

    def with_maybe_isip(self, maybe_isip):
        self._options = toolz.assoc(self._options, 'maybe_isip', maybe_isip)
        return self


if __name__ == '__main__':
    unittest.main()
