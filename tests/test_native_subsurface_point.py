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

from collections import namedtuple
import unittest
import unittest.mock

from hamcrest import assert_that, equal_to, close_to

import orchid.measurement as om
import orchid.native_subsurface_point as nsp
import orchid.reference_origin as oro
import orchid.unit_system as units

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import ISubsurfacePoint
# noinspection PyUnresolvedReferences
import UnitsNet


ScalarQuantity = namedtuple('ScalarQuantity', ['magnitude', 'unit'])


def create_sut(x=None, y=None, depth=None, md_kelly_bushing=None, xy_origin=None, depth_origin=None):
    stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
    if x:
        actual_x = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(x.magnitude),
                                        x.unit.net_unit)
        stub_subsurface_point.X = actual_x
    if y:
        actual_y = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(y.magnitude),
                                        y.unit.net_unit)
        stub_subsurface_point.Y = actual_y
    if depth:
        actual_depth = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(depth.magnitude),
                                            depth.unit.net_unit)
        stub_subsurface_point.Depth = actual_depth
    if md_kelly_bushing:
        actual_md_kelly_bushing = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(md_kelly_bushing.magnitude),
                                                       md_kelly_bushing.unit.net_unit)
        stub_subsurface_point.MdKellyBushing = actual_md_kelly_bushing
    if xy_origin:
        stub_subsurface_point.WellReferenceFrameXy = xy_origin
    if depth_origin:
        stub_subsurface_point.DepthDatum = depth_origin

    sut = nsp.SubsurfacePoint(stub_subsurface_point)
    return sut


# Test ideas
class TestNativeSubsurfacePoint(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_x(self):
        scalar_x = ScalarQuantity(-2725.83, units.Metric.LENGTH)
        sut = create_sut(x=scalar_x)

        expected_x = om.make_measurement(scalar_x.magnitude, scalar_x.unit.abbreviation)
        assert_that(sut.x.unit, equal_to(expected_x.unit))
        assert_that(sut.x.magnitude, close_to(expected_x.magnitude, 6e-2))

    def test_y(self):
        scalar_y = ScalarQuantity(1656448.10, units.Metric.LENGTH)
        sut = create_sut(y=scalar_y)

        expected_y = om.make_measurement(scalar_y.magnitude, scalar_y.unit.abbreviation)
        assert_that(sut.y.unit, equal_to(expected_y.unit))
        assert_that(sut.y.magnitude, close_to(expected_y.magnitude, 6e-2))

    def test_depth(self):
        scalar_depth = ScalarQuantity(8945.60, units.UsOilfield.LENGTH)
        sut = create_sut(depth=scalar_depth)

        expected_depth = om.make_measurement(scalar_depth.magnitude, scalar_depth.unit.abbreviation)
        assert_that(sut.depth.unit, equal_to(expected_depth.unit))
        assert_that(sut.depth.magnitude, close_to(expected_depth.magnitude, 6e-2))

    def test_md_kelly_bushing(self):
        scalar_md_kelly_bushing = ScalarQuantity(3131.45, units.Metric.LENGTH)
        sut = create_sut(md_kelly_bushing=scalar_md_kelly_bushing)

        expected_md_kelly_bushing = om.make_measurement(scalar_md_kelly_bushing.magnitude,
                                                        units.Metric.LENGTH.abbreviation)
        assert_that(sut.md_kelly_bushing.unit, equal_to(expected_md_kelly_bushing.unit))
        assert_that(sut.md_kelly_bushing.magnitude, close_to(expected_md_kelly_bushing.magnitude, 6e-2))

    def test_xy_origin(self):
        expected_xy_origin = oro.WellReferenceFrameXy.PROJECT
        sut = create_sut(xy_origin=expected_xy_origin)

        # The expected Python Enum equals the .NET Enum because the expected value of the Python Enum **is**
        # the .NET Enum.
        assert_that(sut.xy_origin, equal_to(expected_xy_origin))

    def test_depth_origin(self):
        expected_depth_origin = oro.DepthDatum.GROUND_LEVEL
        sut = create_sut(depth_origin=expected_depth_origin)

        # The expected Python Enum equals the .NET Enum because the expected value of the Python Enum **is**
        # the .NET Enum.
        assert_that(sut.depth_origin, equal_to(expected_depth_origin))


if __name__ == '__main__':
    unittest.main()
