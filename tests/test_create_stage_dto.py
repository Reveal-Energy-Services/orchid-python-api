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

from hamcrest import assert_that, equal_to, calling, raises
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
import System
# noinspection PyUnresolvedReferences
import UnitsNet


# Test ideas
# - create_stage calls object factory CreateStage with correct arguments all specified
# - create_stage calls object factory CreateStage with correct arguments without cluster_count
# - create_stage calls object factory CreateStage with correct arguments without shmin
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
    def test_dto_create_stage_calls_factory_create_stage_once(self, stub_object_factory, stub_as_unit_system):
        stub_as_unit_system.return_value = units.Metric
        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        create_stage_details = self.DONT_CARE_STAGE_DETAILS
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        stub_object_factory.CreateStage.assert_called_once()

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_stage_no(self, stub_object_factory,
                                                                                   stub_as_unit_system):
        stub_as_unit_system.return_value = units.UsOilfield
        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'stage_no': 23})
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        actual_call_args = stub_object_factory.CreateStage.call_args
        actual_transformed_stage_number = actual_call_args.args[0]  # transformed stage_no
        assert_that(actual_transformed_stage_number, equal_to(System.UInt32(22)))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    def test_dto_create_stage_calls_factory_create_stage_with_well_dom_object(self, stub_object_factory,
                                                                              stub_as_unit_system):
        stub_as_unit_system.return_value = units.UsOilfield
        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        create_stage_details = self.DONT_CARE_STAGE_DETAILS
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        actual_call_args = stub_object_factory.CreateStage.call_args
        actual_transformed_well = actual_call_args.args[1]  # well_object
        assert_that(actual_transformed_well, equal_to(stub_net_well))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_connection_type(self, stub_object_factory,
                                                                                          stub_as_unit_system):
        stub_as_unit_system.return_value = units.UsOilfield
        stub_net_well = tsn.WellDto().create_net_stub()
        stub_well = nwa.NativeWellAdapter(stub_net_well)
        create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS,
                                           {'connection_type': nsa.ConnectionType.PLUG_AND_PERF})
        nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

        actual_call_args = stub_object_factory.CreateStage.call_args
        actual_transformed_connection_type = actual_call_args.args[2]  # transformed connection_type
        assert_that(actual_transformed_connection_type, equal_to(nsa.ConnectionType.PLUG_AND_PERF))

    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_md_top(self, stub_object_factory,
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
                stub_as_unit_system.return_value = project_unit_system
                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'md_top': source})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                actual_call_args = stub_object_factory.CreateStage.call_args
                actual_transformed_md_top = actual_call_args.args[3]  # transformed md_top
                tcm.assert_that_net_quantities_close_to(actual_transformed_md_top, expected,
                                                        tolerance=decimal.Decimal('0.01'))

    # create_stage_details = {
    #     'stage_no': 23,
    #     'connection_type': nsa.ConnectionType.PLUG_AND_PERF,
    #     'md_top': 3714.60 * om.registry.m,
    #     'md_bottom': 3761.62 * om.registry.m,
    #     'maybe_shmin': 2.27576 * om.registry.psi,
    #     'cluster_count': 4,
    # }
    # noinspection PyUnresolvedReferences
    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    @unittest.mock.patch('orchid.native_stage_adapter._object_factory')
    def test_dto_create_stage_calls_factory_create_stage_with_transformed_md_bottom(self, stub_object_factory,
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
                stub_as_unit_system.return_value = project_unit_system
                stub_net_well = tsn.WellDto().create_net_stub()
                stub_well = nwa.NativeWellAdapter(stub_net_well)
                create_stage_details = toolz.merge(self.DONT_CARE_STAGE_DETAILS, {'md_bottom': source})
                nsa.CreateStageDto(**create_stage_details).create_stage(stub_well)

                actual_call_args = stub_object_factory.CreateStage.call_args
                actual_transformed_md_bottom = actual_call_args.args[4]  # transformed md_bottom
                tcm.assert_that_net_quantities_close_to(actual_transformed_md_bottom, expected,
                                                        tolerance=decimal.Decimal('0.01'))


if __name__ == '__main__':
    unittest.main()
