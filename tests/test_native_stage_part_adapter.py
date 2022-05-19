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
class TestNativeStagePartAdapter(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_display_name_with_well_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.StagePartDto(display_name_with_well='calcar').create_net_stub()
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.display_name_with_well, equal_to('calcar'))

    def test_display_name_without_well_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.StagePartDto(display_name_without_well='edo').create_net_stub()
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.display_name_without_well, equal_to('edo'))

    def test_part_no_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.StagePartDto(part_no=3).create_net_stub()
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.part_no, equal_to(3))

    def test_start_time_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.StagePartDto(start_time=pdt.parse('2026-05-31T04:52:20.857')).create_net_stub()
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.start_time, equal_to(pdt.parse('2026-05-31T04:52:20.857')))

    def test_stop_time_returns_native_stage_part_property(self):
        stub_net_stage_part = tsn.StagePartDto(stop_time=pdt.parse('2021-08-22T23:33:36.329')).create_net_stub()
        sut = spa.NativeStagePartAdapter(stub_net_stage_part)

        assert_that(sut.stop_time, equal_to(pdt.parse('2021-08-22T23:33:36.329')))

    def test_isip_returns_native_stage_part_property(self):
        for net_isip_dto, project_units, expected_isip_dto in [
            (tsn.make_measurement_dto(units.Metric.PRESSURE, 18780.7),
             units.Metric,
             tsn.make_measurement_dto(units.Metric.PRESSURE, 18780.7)),
            (tsn.make_measurement_dto(units.Metric.PRESSURE, 22142.0),
             units.UsOilfield,
             tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 3211.43)),
            (tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 3891.73),
             units.UsOilfield,
             tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 3891.73)),
            (tsn.make_measurement_dto(units.UsOilfield.PRESSURE, 3348.05),
             units.Metric,
             tsn.make_measurement_dto(units.Metric.PRESSURE, 23084.0)),
        ]:
            with self.subTest(f'Testing ISIP of {expected_isip_dto}'):
                stub_net_project = tsn.create_stub_net_project(project_units=project_units)
                stub_net_stage_part = tsn.StagePartDto(isip=net_isip_dto, project=stub_net_project).create_net_stub()
                sut = spa.NativeStagePartAdapter(stub_net_stage_part)

                tcm.assert_that_measurements_close_to(sut.isip,
                                                      tsn.make_measurement(expected_isip_dto),
                                                      tolerance=decimal.Decimal('0.01'))

    def test_isip_returns_nan_if_native_stage_part_property_is_null(self):
        for isip_dto, project_units in [
            (tsn.make_measurement_dto(units.Metric.PRESSURE, float('NaN')), units.Metric),
            (tsn.make_measurement_dto(units.Metric.PRESSURE, float('NaN')), units.UsOilfield),
            (tsn.make_measurement_dto(units.UsOilfield.PRESSURE, float('NaN')), units.UsOilfield),
            (tsn.make_measurement_dto(units.UsOilfield.PRESSURE, float('NaN')), units.Metric),
        ]:
            with self.subTest(f'Test `null` .NET ISIP produces `NaN` in {project_units} units'):
                stub_net_project = tsn.create_stub_net_project(project_units=project_units)
                stub_net_stage_part = tsn.StagePartDto(isip=isip_dto, project=stub_net_project).create_net_stub()
                sut = spa.NativeStagePartAdapter(stub_net_stage_part)

                actual = sut.isip
                assert_that(math.isnan(actual.magnitude))
                assert_that(actual.units, equal_to(project_units.PRESSURE.value.unit))


if __name__ == '__main__':
    unittest.main()
