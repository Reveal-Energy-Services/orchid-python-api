#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import decimal

from hamcrest import assert_that, equal_to, close_to
from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description


def assert_that_scalar_quantities_close_to(actual, expected, tolerance=None):
    assert_that(actual.unit, equal_to(expected.unit))
    _assert_magnitudes_close_to(actual.magnitude, expected.magnitude, tolerance)


def _assert_magnitudes_close_to(actual, expected, tolerance):
    to_test_actual = decimal.Decimal(actual)
    to_test_expected = decimal.Decimal(expected)
    to_test_tolerance = decimal.Decimal((0, (1,), to_test_expected.as_tuple()[-1] - 1)) if tolerance is None \
        else decimal.Decimal(tolerance)
    assert_that(to_test_actual, close_to(to_test_expected, to_test_tolerance))


def assert_that_measurements_close_to(actual, expected, tolerance=None):
    assert_that(actual.unit, equal_to(expected.unit))
    _assert_magnitudes_close_to(actual.magnitude, expected.magnitude, tolerance)


def assert_that_net_quantities_close_to(actual, expected, tolerance=None):
    assert_that(get_net_unit(actual), equal_to(get_net_unit(expected)))
    _assert_magnitudes_close_to(actual.Value, expected.Value, tolerance)


def get_net_unit(net_quantity):
    try:
        return net_quantity.Unit
    except AttributeError:
        return net_quantity.NumeratorUnit, net_quantity.DenominatorUnit


class IsEqualNetDateTime(BaseMatcher):
    def __init__(self, expected):
        """
        Construct an instance for matching another .NET DateTime instance against
        Args:
            expected: The expected .NET DateTime instance.
        """
        self._expected = expected

    def describe_mismatch(self, item, mismatch_description: Description) -> None:
        """
        Describes the mismatch of the actual item.
        Args:
            item: The actual value in the test.
            mismatch_description: The incoming mismatch_description.
        """
        mismatch_description.append_text(item.ToString("O"))

    def describe_to(self, description: Description) -> None:
        """
        Describe the match failure.

        Args:
            description: The previous failure description(s).
        """
        description.append_text(self._expected.ToString("O"))

    def _matches(self, item) -> bool:
        """
        Determines of one instance with the .NET DateTime "interface" equals another instance.

        Args:
            item: An instance with the .NET DateTime "interface":
                  - Year
                  - Month
                  - Day
                  - Hour
                  - Minute
                  - Second
                  - Millisecond
                  - Kind
        """
        if self._expected.Year != item.Year:
            return False

        if self._expected.Month != item.Month:
            return False

        if self._expected.Day != item.Day:
            return False

        if self._expected.Hour != item.Hour:
            return False

        if self._expected.Minute != item.Minute:
            return False

        if self._expected.Second != item.Second:
            return False

        if self._expected.Millisecond != item.Millisecond:
            return False

        if self._expected.Kind != item.Kind:
            return False

        return True


def equal_to_net_date_time(expected):
    """
    Create a matcher verifying another .NET DateTime equal to `expected`.

    Args:
        expected: An instance implementing the .NET DateTime "interface":
                  - Year
                  - Month
                  - Day
                  - Hour
                  - Minute
                  - Second
                  - Millisecond
                  - Kind
                  - ToString

    Returns:
        A matcher against `expected`.

    """
    return IsEqualNetDateTime(expected)
