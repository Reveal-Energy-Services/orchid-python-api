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
import decimal

from hamcrest import assert_that, equal_to, close_to


# The following functions are not custom matchers as defined by the `pyhamcrest` package; however, they
# provide similar functionality by implementing common test code.


ScalarQuantity = namedtuple('ScalarQuantity', ['magnitude', 'unit'])
SubsurfaceLocation = namedtuple('SubsurfaceLocation', ['x', 'y', 'depth'])


def assert_that_scalar_quantities_close_to(actual, expected, tolerance=None):
    assert_that(actual.unit, equal_to(expected.unit))
    to_test_actual_magnitude = decimal.Decimal(actual.magnitude)
    to_test_expected_magnitude = decimal.Decimal(expected.magnitude)
    to_test_tolerance = decimal.Decimal((0, (1,), to_test_expected_magnitude.as_tuple()[-1] - 1)) if tolerance is None \
        else decimal.Decimal(tolerance)
    assert_that(to_test_actual_magnitude, close_to(to_test_expected_magnitude, to_test_tolerance))


def assert_that_net_quantities_close_to(actual, expected, tolerance):
    def get_net_unit(net_quantity):
        return net_quantity.Unit

    assert_that(get_net_unit(actual), equal_to(get_net_unit(expected)))

    to_test_actual_value = decimal.Decimal(actual.Value)
    to_test_expected_value = decimal.Decimal(expected.Value)
    to_test_tolerance = decimal.Decimal((0, (1,), to_test_expected_value.as_tuple()[-1] - 1)) if tolerance is None \
        else decimal.Decimal(tolerance)
    assert_that(to_test_actual_value, close_to(to_test_expected_value, to_test_tolerance))
