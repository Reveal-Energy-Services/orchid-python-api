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

from hamcrest import assert_that, equal_to

import orchid.measurement as om


class TestMeasurement(unittest.TestCase):
    """Implements the unit tests for the orchid.measurement module."""
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_has_magnitude_set_in_ctor(self):
        sut = om.make_measurement(74.168, 'm')
        assert_that(74.168, sut.magnitude)

    def test_has_unit_set_in_ctor(self):
        sut = om.make_measurement(74.168, 'm')
        assert_that('m', sut.unit)


if __name__ == '__main__':
    unittest.main()
