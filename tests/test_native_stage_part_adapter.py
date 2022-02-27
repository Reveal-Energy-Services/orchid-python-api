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


import unittest

from hamcrest import assert_that, equal_to
import pendulum as pdt

from orchid import (
    native_stage_part_adapter as spa,
    unit_system as units,
)

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)


# Test ideas
# - isip returns non-null native stage part property converted to `Pint` `Quantity`
# - isip returns `null` native stage part property converted to `NaN` with correct units
class TestNativeStagePartAdapter(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_display_name_with_well_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.create_stub_net_stage_part(display_name_with_well='calcar')
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.display_name_with_well, equal_to('calcar'))

    def test_display_name_without_well_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.create_stub_net_stage_part(display_name_without_well='edo')
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.display_name_without_well, equal_to('edo'))

    def test_part_no_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.create_stub_net_stage_part(part_no=3)
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.part_no, equal_to(3))

    def test_start_time_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.create_stub_net_stage_part(start_time=pdt.parse('2026-05-31T04:52:20.857'))
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.start_time, equal_to(pdt.parse('2026-05-31T04:52:20.857')))

    def test_stop_time_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.create_stub_net_stage_part(stop_time=pdt.parse('2021-08-22T23:33:36.329'))
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.stop_time, equal_to(pdt.parse('2021-08-22T23:33:36.329')))

    @unittest.mock.patch('orchid.unit_system.as_unit_system')
    def test_isip_returns_native_stage_part_property(self, mock_as_unit_system):

        for isip_dto, project_units in [
            (tsn.make_measurement_dto(units.Metric.PRESSURE, 18780.7), units.Metric)
        ]:
            expected_isip = tsn.make_measurement(isip_dto)
            with self.subTest(f'Testing ISIP of {expected_isip:~P}'):
                mock_as_unit_system.return_value = project_units
                stub_net_stage_part = tsn.create_stub_net_stage_part(isip=isip_dto)
                sut = spa.NativeStagePartAdapter(stub_net_stage_part)

                tcm.assert_that_measurements_close_to(sut.isip, expected_isip, tolerance=0.01)


if __name__ == '__main__':
    unittest.main()
