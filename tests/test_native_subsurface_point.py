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

import unittest
import unittest.mock

from hamcrest import assert_that, equal_to

import orchid.native_subsurface_point as nsp
import orchid.reference_origin as oro

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import ISubsurfacePoint


# Test ideas
# - xy_origin
# - depth_origin
class TestNativeSubsurfacePoint(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_x(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        expected_x = -2725.83
        stub_subsurface_point.X = expected_x

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        assert_that(sut.x, equal_to(expected_x))

    def test_y(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        expected_y = 1656448.10
        stub_subsurface_point.Y = expected_y

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        assert_that(sut.y, equal_to(expected_y))

    def test_depth(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        expected_depth = 8945.60
        stub_subsurface_point.Depth = expected_depth

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        assert_that(sut.depth, equal_to(expected_depth))

    def test_md_kelly_bushing(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        expected_md_kelly_bushing = 3131.45
        stub_subsurface_point.MdKellyBushing = expected_md_kelly_bushing

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        assert_that(sut.md_kelly_bushing, equal_to(expected_md_kelly_bushing))

    def test_xy_origin(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        expected_xy_origin = oro.WellReferenceFrameXy.PROJECT
        stub_subsurface_point.WellReferenceFrameXy = expected_xy_origin

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        # The expected Python Enum equals the .NET Enum because the expected value of the Python Enum **is**
        # the .NET Enum.
        assert_that(sut.xy_origin, equal_to(expected_xy_origin))

    def test_depth_origin(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        expected_depth_origin = oro.DepthDatum.GROUND_LEVEL
        stub_subsurface_point.DepthDatum = expected_depth_origin

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        # The expected Python Enum equals the .NET Enum because the expected value of the Python Enum **is**
        # the .NET Enum.
        assert_that(sut.depth_origin, equal_to(expected_depth_origin))


if __name__ == '__main__':
    unittest.main()
