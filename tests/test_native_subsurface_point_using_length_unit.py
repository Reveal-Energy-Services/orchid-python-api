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

from orchid import (
    measurement as om,
    native_subsurface_point as nsp,
    reference_origins as origins,
    unit_system as units,
)

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)


def create_sut(length_unit, x=None, y=None, depth=None, xy_origin=None, depth_origin=None):
    stub_subsurface_point = tsn.create_stub_net_subsurface_point(x, y, depth, xy_origin, depth_origin)

    sut = nsp.SubsurfacePointUsingLengthUnit(stub_subsurface_point, length_unit)
    return sut


# Test ideas
class TestNativeSubsurfacePointUsingLength(unittest.TestCase):
    DONT_CARE_LENGTH_UNIT = units.UsOilfield.LENGTH

    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_x(self):
        scalar_x = tsn.StubMeasurement(-2725.83, units.Metric.LENGTH)
        sut = create_sut(units.UsOilfield.LENGTH, x=scalar_x)

        expected_x = om.make_measurement(-8943.01, units.UsOilfield.LENGTH)
        tcm.assert_that_scalar_quantities_close_to(sut.x, expected_x, 6e-2)

    def test_y(self):
        scalar_y = tsn.StubMeasurement(1656448.10, units.Metric.LENGTH)
        sut = create_sut(units.UsOilfield.LENGTH, y=scalar_y)

        expected_y = om.make_measurement(5434541.01, units.UsOilfield.LENGTH)
        tcm.assert_that_scalar_quantities_close_to(sut.y, expected_y, 9e-2)

    def test_depth(self):
        scalar_depth = tsn.StubMeasurement(8945.60, units.UsOilfield.LENGTH)
        sut = create_sut(units.Metric.LENGTH, depth=scalar_depth)

        expected_depth = om.make_measurement(2726.62, units.Metric.LENGTH)
        tcm.assert_that_scalar_quantities_close_to(sut.depth, expected_depth, 6e-2)

    def test_xy_origin(self):
        expected_xy_origin = origins.WellReferenceFrameXy.PROJECT
        sut = create_sut(self.DONT_CARE_LENGTH_UNIT, xy_origin=expected_xy_origin)

        # The expected Python Enum equals the .NET Enum because the expected value of the Python Enum **is**
        # the .NET Enum.
        assert_that(sut.xy_origin, equal_to(expected_xy_origin))

    def test_depth_origin(self):
        expected_depth_origin = origins.DepthDatum.GROUND_LEVEL
        sut = create_sut(self.DONT_CARE_LENGTH_UNIT, depth_origin=expected_depth_origin)

        # The expected Python Enum equals the .NET Enum because the expected value of the Python Enum **is**
        # the .NET Enum.
        assert_that(sut.depth_origin, equal_to(expected_depth_origin))


if __name__ == '__main__':
    unittest.main()
