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

from hamcrest import assert_that, equal_to, close_to

from orchid.measurement import make_measurement
from orchid.net_measurement import as_net_measurement, as_net_measurement_in_different_unit

# noinspection PyUnresolvedReferences
import UnitsNet


class TestNetMeasurement(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_net_length_measurement_in_original_unit(self):
        for measurement in [make_measurement(44.49, 'ft'), make_measurement(25.93, 'm')]:
            with self.subTest(measurement=measurement):
                actual = as_net_measurement(measurement)
                expected_unit = (UnitsNet.Units.LengthUnit.Foot if measurement.unit == 'ft'
                                 else UnitsNet.Units.LengthUnit.Meter)
                assert_that(actual.Unit, equal_to(expected_unit))
                assert_that(actual.As(expected_unit), close_to(measurement.magnitude, 5e-3))

    def test_as_net_length_measurement_in_specified_unit(self):
        for measurement, expected_value, to_unit_abbreviation in [(make_measurement(44.49, 'ft'), 13.56, 'm'),
                                                                  (make_measurement(25.93, 'm'), 85.07, 'ft')]:
            with self.subTest(measurement=measurement, expected_value=expected_value,
                              to_unit_abbreviation_abbreviation=to_unit_abbreviation):
                actual = as_net_measurement_in_different_unit(measurement, to_unit_abbreviation)
                expected_unit = (UnitsNet.Units.LengthUnit.Foot if to_unit_abbreviation == 'ft'
                                 else UnitsNet.Units.LengthUnit.Meter)
                assert_that(actual.Unit, equal_to(expected_unit))
                assert_that(actual.As(expected_unit), close_to(expected_value, 5e-3))


if __name__ == '__main__':
    unittest.main()
