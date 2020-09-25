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
import toolz.curried as toolz

import orchid.measurement as om
import orchid.native_subsurface_point as nsp
import orchid.reference_origin as oro
import orchid.unit_system as units

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import ISubsurfacePoint
# noinspection PyUnresolvedReferences
import UnitsNet


ScalarQuantity = namedtuple('ScalarQuantity', ['magnitude', 'unit'])


def create_sut(x=None, y=None, depth=None, md_kelly_bushing=None, xy_origin=None, depth_origin=None):
    def make_length_unit(scalar_quantity):
        return UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(scalar_quantity.magnitude),
                                    scalar_quantity.unit.net_unit)

    stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
    if x:
        stub_subsurface_point.X = make_length_unit(x)
    if y:
        stub_subsurface_point.Y = make_length_unit(y)
    if depth:
        stub_subsurface_point.Depth = make_length_unit(depth)
    if md_kelly_bushing:
        stub_subsurface_point.MdKellyBushing = make_length_unit(md_kelly_bushing)
    if xy_origin:
        stub_subsurface_point.WellReferenceFrameXy = xy_origin
    if depth_origin:
        stub_subsurface_point.DepthDatum = depth_origin

    sut = nsp.SubsurfacePoint(stub_subsurface_point)
    return sut


def assert_that_scalar_quantities_close_to(actual_x, expected_x, tolerance):
    assert_that(actual_x.unit, equal_to(expected_x.unit))
    assert_that(actual_x.magnitude, close_to(expected_x.magnitude, tolerance))


# Test ideas
class TestNativeSubsurfacePoint(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_x(self):
        scalar_x = ScalarQuantity(-2725.83, units.Metric.LENGTH)
        sut = create_sut(x=scalar_x)

        expected_x = om.make_measurement(scalar_x.magnitude, scalar_x.unit.abbreviation)
        assert_that_scalar_quantities_close_to(sut.x, expected_x, 6e-2)

    def test_y(self):
        scalar_y = ScalarQuantity(1656448.10, units.Metric.LENGTH)
        sut = create_sut(y=scalar_y)

        expected_y = om.make_measurement(scalar_y.magnitude, scalar_y.unit.abbreviation)
        assert_that_scalar_quantities_close_to(sut.y, expected_y, 6e-2)

    def test_depth(self):
        scalar_depth = ScalarQuantity(8945.60, units.UsOilfield.LENGTH)
        sut = create_sut(depth=scalar_depth)

        expected_depth = om.make_measurement(scalar_depth.magnitude, scalar_depth.unit.abbreviation)
        assert_that_scalar_quantities_close_to(sut.depth, expected_depth, 6e-2)

    def test_md_kelly_bushing(self):
        scalar_md_kelly_bushing = ScalarQuantity(3131.45, units.Metric.LENGTH)
        sut = create_sut(md_kelly_bushing=scalar_md_kelly_bushing)

        expected_md_kelly_bushing = om.make_measurement(scalar_md_kelly_bushing.magnitude,
                                                        units.Metric.LENGTH.abbreviation)
        assert_that_scalar_quantities_close_to(sut.md_kelly_bushing, expected_md_kelly_bushing, 6e-2)

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

    def test_as_length_unit(self):
        @toolz.curry
        def make_scalar_quantity(magnitude, unit):
            return ScalarQuantity(magnitude=magnitude, unit=unit)

        all_test_data = [((126834.6, 321614.0, 1836.6, 3136.3), units.Metric.LENGTH,
                          (416124, 1055164, 6025.56, 10289.7), units.UsOilfield.LENGTH),
                         ((444401, 9009999, 7799.91, 6722.57), units.UsOilfield.LENGTH,
                          (135453.42, 2746247.70, 2377.41, 2049.04), units.Metric.LENGTH)]
        for length_magnitudes, length_unit, as_length_magnitudes, as_length_unit in all_test_data:
            with self.subTest(length_magnitudes=length_magnitudes, length_unit=length_unit,
                              as_length_magnitudes=as_length_magnitudes,
                              as_length_unit=as_length_unit):
                from_lengths = list(toolz.map(toolz.flip(ScalarQuantity, length_unit), length_magnitudes))
                sut = create_sut(x=from_lengths[0], y=from_lengths[1], depth=from_lengths[2],
                                 md_kelly_bushing=from_lengths[3])
                actual_as_length_unit = sut.as_length_unit(as_length_unit)

                expected_lengths = list(toolz.map(toolz.flip(om.make_measurement, as_length_unit.abbreviation),
                                                  as_length_magnitudes))
                assert_that_scalar_quantities_close_to(actual_as_length_unit.x,
                                                       expected_lengths[0], 6e-2)
                assert_that_scalar_quantities_close_to(actual_as_length_unit.y,
                                                       expected_lengths[1], 6e-2)
                assert_that_scalar_quantities_close_to(actual_as_length_unit.depth,
                                                       expected_lengths[2], 6e-2)
                assert_that_scalar_quantities_close_to(actual_as_length_unit.md_kelly_bushing,
                                                       expected_lengths[3], 6e-2)


if __name__ == '__main__':
    unittest.main()
