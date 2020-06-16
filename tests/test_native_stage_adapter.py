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

import unittest.mock

from hamcrest import assert_that, equal_to

from orchid.measurement import make_measurement
import orchid.native_stage_adapter as nsa
from orchid.net_measurement import as_net_measurement_in_different_unit

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
        # for expected_top, net_stage_top in [((13467.8, 'ft'), (13467.8, 'ft')), ('m', 'm'), ('ft', 'm'), ('m', 'ft')]:
        for actual_top, expected_top in [(make_measurement(13467.8, 'ft'), make_measurement(13467.8, 'ft'))]:
            with self.subTest(expected_top=actual_top):
                stub_net_stage = unittest.mock.MagicMock(name='stub_net_stage', spec=IStage)
                stub_net_stage.MdTop = as_net_measurement_in_different_unit(actual_top, actual_top.unit)
                sut = nsa.NativeStageAdapter(stub_net_stage)

                assert_that(sut.md_top(expected_top.unit), equal_to(expected_top.magnitude))


if __name__ == '__main__':
    unittest.main()
