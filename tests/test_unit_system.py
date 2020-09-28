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

from hamcrest import assert_that, equal_to, raises, calling

import orchid.unit_system as units


class TestUnitSystem(unittest.TestCase):
    """Defines the unit tests for the unit_system module."""

    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_abbreviation_to_unit_returns_us_oilfield_length_member_if_supplied_ft(self):
        actual_unit = units.abbreviation_to_unit('ft')

        assert_that(actual_unit, equal_to(units.UsOilfield.LENGTH))

    def test_abbreviation_to_unit_returns_metric_length_member_if_supplied_m(self):
        actual_unit = units.abbreviation_to_unit('m')

        assert_that(actual_unit, equal_to(units.Metric.LENGTH))

    def test_abbreviation_to_unit_raises_exception_if_unknown_abbreviation(self):
        assert_that(calling(units.abbreviation_to_unit).with_args('fr'),
                    raises(ValueError, pattern=r'Unrecognized unit abbreviation, "fr"'))


if __name__ == '__main__':
    unittest.main()
