#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import datetime
import unittest.mock

from hamcrest import assert_that, equal_to, close_to

from orchid.measurement import make_measurement
from orchid.net_quantity import as_net_date_time
import orchid.native_stage_adapter as nsa
from orchid.net_quantity import as_net_quantity_in_different_unit

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IStage
# noinspection PyUnresolvedReferences
import UnitsNet


# Test ideas
# - MD of the stage top/bottom in feet if project length unit is also feet
# - MD of the stage bottom in meters if project length unit is also meters
# - MD of the stage bottom in feet if project length unit is meters
# - MD of the stage bottom in meters if project length unit is feet
class TestNativeStageAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_stage_number(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_display_stage_number = 11
        stub_net_stage.DisplayStageNumber = expected_display_stage_number
        sut = nsa.NativeStageAdapter(stub_net_stage)

        assert_that(sut.display_stage_number(), equal_to(expected_display_stage_number))

    def test_md_top(self):
        for actual_top, expected_top in [(make_measurement(13467.8, 'ft'), make_measurement(13467.8, 'ft')),
                                         (make_measurement(3702.48, 'm'), make_measurement(3702.48, 'm')),
                                         (make_measurement(13467.8, 'ft'), make_measurement(4104.98, 'm')),
                                         (make_measurement(3702.48, 'm'), make_measurement(12147.2, 'ft'))]:
            with self.subTest(expected_top=actual_top):
                stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
                stub_net_stage.MdTop = as_net_quantity_in_different_unit(actual_top, actual_top.unit)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_top(expected_top.unit)
                assert_that(actual_top.magnitude, close_to(expected_top.magnitude, 0.05))
                assert_that(actual_top.unit, equal_to(expected_top.unit))

    def test_md_bottom(self):
        for actual_top, expected_top in [(make_measurement(13806.7, 'ft'), make_measurement(13806.7, 'ft')),
                                         (make_measurement(4608.73, 'm'), make_measurement(4608.73, 'm')),
                                         (make_measurement(12147.2, 'ft'), make_measurement(3702.47, 'm')),
                                         (make_measurement(4608.73, 'm'), make_measurement(15120.5, 'ft'))]:
            with self.subTest(expected_top=actual_top):
                stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
                stub_net_stage.MdBottom = as_net_quantity_in_different_unit(actual_top, actual_top.unit)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                actual_top = sut.md_bottom(expected_top.unit)
                assert_that(actual_top.magnitude, close_to(expected_top.magnitude, 0.05))
                assert_that(actual_top.unit, equal_to(expected_top.unit))

    def test_start_time(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_start_time = datetime.datetime(2024, 10, 31, 7, 31, 27, 357000)
        stub_net_stage.StartTime = as_net_date_time(expected_start_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_start_time = sut.start_time()
        assert_that(actual_start_time, equal_to(expected_start_time))

    def test_stop_time(self):
        stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
        expected_stop_time = datetime.datetime(2016, 3, 31, 3, 31, 30, 947000)
        stub_net_stage.StopTime = as_net_date_time(expected_stop_time)
        sut = nsa.NativeStageAdapter(stub_net_stage)

        actual_stop_time = sut.stop_time()
        assert_that(actual_stop_time, equal_to(expected_stop_time))


if __name__ == '__main__':
    unittest.main()
