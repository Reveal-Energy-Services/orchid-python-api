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
from typing import Optional

from hamcrest import assert_that, equal_to, close_to
from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description

import orchid.version as ov


def assert_that_scalar_quantities_close_to(actual, expected, tolerance=None, reason=''):
    assert_that(actual.unit, equal_to(expected.unit))
    _assert_magnitudes_close_to(actual.magnitude, expected.magnitude, tolerance, reason)


def _assert_magnitudes_close_to(actual, expected, tolerance, reason):
    to_test_actual = decimal.Decimal(actual)
    to_test_expected = decimal.Decimal(expected)
    last_digit_adjustment = -1
    to_test_tolerance = _calculate_to_test_tolerance(to_test_expected, last_digit_adjustment, tolerance)
    assert_that(to_test_actual, close_to(to_test_expected, to_test_tolerance), reason)


def _calculate_to_test_tolerance(expected: decimal.Decimal, last_digit_adjustment: int,
                                 original_tolerance: Optional[float]):
    """
    Optionally calculate the absolute error tolerance based on the precision of `to_test_expected` and an
    adjustment to the last digit in `to_test_expected`.

    Args:
        expected: The expected value for the test.
        last_digit_adjustment: An adjustment to the precision of the last digit in `expected`. A negative
        value "moves" the error from the last digit of the `expected` value to digit to the right of the
        last digit. A positive value moves the error from the last digit of the `expected` value to the
        digit to the left of the last digit.
        original_tolerance: The original tolerance supplied by the caller. If not `None`, this value is
        returned unchanged.

    Returns:
        The absolute error tolerance to be used in determining equality.
    """
    return (decimal.Decimal((0, (1,), expected.as_tuple()[-1] + last_digit_adjustment))
            if original_tolerance is None
            else decimal.Decimal(original_tolerance))


def assert_that_measurements_close_to(actual, expected, tolerance=None, reason=''):
    assert_that(actual.units, equal_to(expected.units), reason)
    _assert_magnitudes_close_to(actual.magnitude, expected.magnitude, tolerance, reason)


def assert_that_net_quantities_close_to(actual, expected, tolerance=None, reason=''):
    assert_that(get_net_unit(actual), equal_to(get_net_unit(expected)))
    _assert_magnitudes_close_to(actual.Value, expected.Value, tolerance, reason)


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


class IsEqualVersion(BaseMatcher):
    def __init__(self, expected):
        """
        Construct an instance for matching a packaging.version.Version instance against a `tuple` containing
        either 3 (major, minor, patch) or 4 (major, minor, patch, pre) elements.

        Args:
            expected: A tuple containing 3 or 4 elements.
        """
        if len(expected) == 3:
            self._major, self._minor, self._micro = expected
        elif len(expected) == 4:
            self._major, self._minor, self._micro, self._pre = expected
        else:
            raise ValueError(f'Unexpected version tuple {expected}')

    def describe_mismatch(self, item, mismatch_description: Description) -> None:
        """
        Describes the mismatch using the actual item.
        Args:
            item: The actual value in the test.
            mismatch_description: The incoming mismatch_description.
        """
        mismatch_description.append_text(item)

    def describe_to(self, description: Description) -> None:
        """
        Describe the match failure using the expected value.

        Args:
            description: The previous failure description(s).
        """
        if hasattr(self, 'pre'):
            description.append_text(f'Version(major={self._major}, minor={self._minor}, patch={self._micro}, '
                                    f'pre={self._pre})')
        else:
            description.append_text(f'Version(major={self._major}, minor={self._minor}, patch={self._micro})')

    def _matches(self, item: T) -> bool:
        if not isinstance(item, ov.Version):
            return False

        if self._major != item.major:
            return False

        if self._minor != item.minor:
            return False

        if self._micro != item.patch:
            return False

        if item.is_prerelease:
            if self._pre != item.pre:
                return False

        return True


def equal_to_version(expected):
    """
    Create a matcher verifying that a `packaging.version.Version` instance equals `expected`, a `tuple` of
    either 3 (major, minor, micro) or 4 (major, minor, micro, pre) elements.

    Args:
        expected: A `tuple` of 3 or 4 elements.

    Returns:
`       A matcher against `expected`.
    """

    return IsEqualVersion(expected)
