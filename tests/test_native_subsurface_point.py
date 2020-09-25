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

import math
import unittest
import unittest.mock

from hamcrest import assert_that, equal_to, close_to
from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description

import orchid.measurement as om
import orchid.native_subsurface_point as nsp
import orchid.reference_origin as oro
import orchid.unit_system as units

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import ISubsurfacePoint
# noinspection PyUnresolvedReferences
import UnitsNet


# Test ideas
class TestNativeSubsurfacePoint(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_x(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        x_magnitude = -2725.83
        actual_x = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(x_magnitude),
                                        units.Metric.LENGTH.net_unit)
        stub_subsurface_point.X = actual_x

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        expected_x = om.make_measurement(x_magnitude, units.Metric.LENGTH.abbreviation)
        assert_that(sut.x.unit, equal_to(expected_x.unit))
        assert_that(sut.x.magnitude, close_to(expected_x.magnitude, 6e-2))

    def test_y(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        y_magnitude = 1656448.10
        actual_y = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(y_magnitude),
                                        units.Metric.LENGTH.net_unit)
        stub_subsurface_point.Y = actual_y

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        expected_y = om.make_measurement(y_magnitude, units.Metric.LENGTH.abbreviation)
        assert_that(sut.y.unit, equal_to(expected_y.unit))
        assert_that(sut.y.magnitude, close_to(expected_y.magnitude, 6e-2))

    def test_depth(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        depth_magnitude = 1656448.10
        actual_depth = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(depth_magnitude),
                                            units.Metric.LENGTH.net_unit)
        stub_subsurface_point.Depth = actual_depth

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        expected_depth = om.make_measurement(depth_magnitude, units.Metric.LENGTH.abbreviation)
        assert_that(sut.depth.unit, equal_to(expected_depth.unit))
        assert_that(sut.depth.magnitude, close_to(expected_depth.magnitude, 6e-2))

    def test_md_kelly_bushing(self):
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
        md_kelly_bushing_magnitude = 1656448.10
        actual_md_kelly_bushing = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(md_kelly_bushing_magnitude),
                                                       units.Metric.LENGTH.net_unit)
        stub_subsurface_point.MdKellyBushing = actual_md_kelly_bushing

        sut = nsp.SubsurfacePoint(stub_subsurface_point)

        expected_md_kelly_bushing = om.make_measurement(md_kelly_bushing_magnitude, units.Metric.LENGTH.abbreviation)
        assert_that(sut.md_kelly_bushing.unit, equal_to(expected_md_kelly_bushing.unit))
        assert_that(sut.md_kelly_bushing.magnitude, close_to(expected_md_kelly_bushing.magnitude, 6e-2))

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
