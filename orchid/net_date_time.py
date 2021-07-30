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

"""
Functions to convert between .NET `DateTime` instances and Python `pendulum.datetime` instances.
"""


import datetime as dt
import enum
from typing import Tuple

import dateutil.tz as duz
import pendulum
import pendulum.tz as ptz

from orchid import base

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, DateTimeOffset, TimeSpan


UTC = pendulum.UTC
"""Encapsulate the use of pendulum."""


class TimePointTimeZoneKind(enum.Enum):
    """Models the kind of time point.

    This class eases conversions to the .NET `DateTime` class by providing Python with similar capabilities as
    the .NET `Enum`. (See
    [DateTimeKind](https://docs.microsoft.com/en-us/dotnet/api/system.datetimekind?view=net-5.0) for details).
    """
    UTC = DateTimeKind.Utc  # Time zone is UTC
    LOCAL = DateTimeKind.Local  # Time zone is specified to be local
    UNSPECIFIED = DateTimeKind.Unspecified  # Time zone is unspecified


class NetDateTimeError(ValueError):
    """
    Raised when an error occurs accessing the `TimeZoneInfo` of a .NET `DateTime` instance.
    """
    pass


class NetDateTimeLocalDateTimeKindError(NetDateTimeError):
    """
    Raised when the `DateTime.Kind` property of a .NET `DateTime` instance is `DateTimeKind.Local`.
    """
    def __init__(self, net_time_point):
        """
        Construct an instance from a .NET DateTime point in time.

        Args:
            net_time_point: A .NET DateTime representing a specific point in time.
        """
        super().__init__(self, '.NET DateTime.Kind cannot be Local.', net_time_point.ToString("O"))


class NetDateTimeUnspecifiedDateTimeKindError(NetDateTimeError):
    """
    Raised when the `DateTime.Kind` property of a .NET `DateTime` instance is not recognized.
    """
    ERROR_PREFACE = '.NET DateTime.Kind is unexpectedly Unspecified.'

    ERROR_SUFFIX = """
    Although .NET DateTime.Kind should not be Unspecified, it may be
    safe to ignore this error by catching the exception.

    However, because it unexpected, **please** report the issue to
    Reveal Energy Services. 
    """

    def __init__(self, net_time_point):
        """
        Construct an instance from a .NET DateTime point in time.

        Args:
            net_time_point: A .NET DateTime representing a specific point in time.
        """
        super().__init__(self, NetDateTimeUnspecifiedDateTimeKindError.ERROR_PREFACE,
                         net_time_point.ToString("O"), NetDateTimeUnspecifiedDateTimeKindError.ERROR_SUFFIX)


class NetDateTimeNoTzInfoError(NetDateTimeError):
    """
    Raised when the `DateTime.Kind` property of a .NET `DateTime` instance is `DateTimeKind.Unspecified`.
    """
    def __init__(self, time_point):
        """
        Construct an instance from a Python point in time.

        Args:
            time_point: A `pendulum.datetime` representing a specific point in time.
        """
        super().__init__(self, f'The Python time point must specify the time zone.', time_point.isoformat())


class NetDateTimeOffsetNonZeroOffsetError(NetDateTimeError):
    """
    Raised when the `Offset` property of a .NET `DateTimeOffset` is non-zero.
    """
    def __init__(self, net_date_time_offset):
        """
        Construct an instance from a .NET `DateTimeOffset`.

        Args:
            net_date_time_offset: A .NET `DateTimeOffset` representing a specific point in time.
        """
        super().__init__(self, f'The `Offset` of the .NET `DateTimeOffset`, {net_date_time_offset.ToString("o")},'
                               ' cannot be non-zero.')


# TODO: Consider changing this implementation to single dispatch
# Note that this change might require more work than is obvious. Two .NET types: `DateTime` and `DateTimeOffset`
def as_date_time(net_time_point: DateTime) -> pendulum.DateTime:
    """
    Convert a .NET `DateTime` instance to a `pendulum.DateTime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTime`.

    Returns:
        The `pendulum.DateTime` equivalent to the `to_test`.

        If `net_time_point` is `DateTime.MaxValue`, returns `pendulum.DateTime.max`. If `net_time_point` is
        `DateTime.MinValue`, returns `pendulum.DateTime.min`.
    """
    if net_time_point == DateTime.MaxValue:
        return pendulum.DateTime.max

    if net_time_point == DateTime.MinValue:
        return pendulum.DateTime.min

    if net_time_point.Kind == DateTimeKind.Utc:
        return _net_time_point_to_datetime(base.constantly(ptz.UTC), net_time_point)

    if net_time_point.Kind == DateTimeKind.Unspecified:
        raise NetDateTimeUnspecifiedDateTimeKindError(net_time_point)

    if net_time_point.Kind == DateTimeKind.Local:
        raise NetDateTimeLocalDateTimeKindError(net_time_point)

    raise ValueError(f'Unknown .NET DateTime.Kind, {net_time_point.Kind}.')


def as_net_date_time(time_point: pendulum.DateTime) -> DateTime:
    """
    Convert a `pendulum.DateTime` instance to a .NET `DateTime` instance.

    Args:
        time_point: The `pendulum.DateTime` instance to covert.

    Returns:
        The equivalent .NET `DateTime` instance.

        If `time_point` is `pendulum.DateTime.max`, return `DateTime.MaxValue`. If `time_point` is
        `pendulum.DateTime.min`, return `DateTime.MinValue`.
    """
    if time_point == pendulum.DateTime.max:
        return DateTime.MaxValue

    if time_point == pendulum.DateTime.min:
        return DateTime.MinValue

    if not time_point.tzinfo == ptz.UTC:
        raise NetDateTimeNoTzInfoError(time_point)

    carry_seconds, milliseconds = microseconds_to_milliseconds_with_carry(time_point.microsecond)
    result = DateTime(time_point.year, time_point.month, time_point.day,
                      time_point.hour, time_point.minute, time_point.second + carry_seconds,
                      milliseconds, DateTimeKind.Utc)
    return result


def as_net_date_time_offset(time_point: pendulum.DateTime) -> DateTimeOffset:
    """
    Convert a `pendulum.DateTime` instance to a .NET `DateTimeOffset` instance.

    Args:
        time_point: The `pendulum.DateTime` instance to covert.

    Returns:
        The equivalent .NET `DateTimeOffset` instance.

        If `time_point` is `pendulum.DateTime.max`, return `DateTime.MaxValue`. If `time_point` is
        `pendulum.DateTime.min`, return `DateTime.MinValue`.
    """
    if time_point == pendulum.DateTime.max:
        return DateTimeOffset.MaxValue

    if time_point == pendulum.DateTime.min:
        return DateTimeOffset.MinValue

    date_time = as_net_date_time(time_point)
    result = DateTimeOffset(date_time)
    return result


def as_net_time_span(to_convert: pendulum.Duration):
    """
    Convert a `pendulum.Duration` instance to a .NET `TimeSpan`.

    Args:
        to_convert: The `pendulum.Duration` instance to convert.

    Returns:
        The .NET `TimeSpan` equivalent to `to_convert`.
    """
    return TimeSpan(round(to_convert.total_seconds() * TimeSpan.TicksPerSecond))


def as_duration(to_convert: TimeSpan) -> pendulum.Duration:
    """
    Convert a .NET `TimeSpan` to a python `pendulum.Duration`

    Args:
        to_convert: The .NET `TimeSpan` to convert.

    Returns:
        The `pendulum.Duration` equivalent to `to_convert`.

    """
    return pendulum.duration(seconds=to_convert.TotalSeconds)


def as_time_delta(net_time_span: TimeSpan):
    """
    Convert a .NET `TimeSpan` to a Python `dt.timedelta`.

    Args:
        net_time_span: The .NET `TimeSpan` to convert.

    Returns:
        The equivalent dt.time_delta value.

    """
    return dt.timedelta(seconds=net_time_span.TotalSeconds)


def microseconds_to_milliseconds_with_carry(to_convert: int) -> Tuple[int, int]:
    """
    Convert microseconds to an integral number of milliseconds with a number of seconds to carry.

    Args:
        to_convert: The microseconds to convert.

    Returns:
        A tuple of the form, (number of seconds to "carry",  number of the integral milliseconds).
    """

    raw_milliseconds = round(to_convert / 1000)
    return divmod(raw_milliseconds, 1000)


def net_date_time_offset_as_date_time(net_time_point: DateTimeOffset) -> pendulum.DateTime:
    """
    Convert a .NET `DateTimeOffset` instance to a `pendulum.DateTime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTimeOffset`.

    Returns:
        The `pendulum.DateTime` equivalent to the `net_time_point`.
    """
    if net_time_point == DateTimeOffset.MaxValue:
        return pendulum.DateTime.max

    if net_time_point == DateTimeOffset.MinValue:
        return pendulum.DateTime.min

    return _net_time_point_to_datetime(lambda ntp: as_time_delta(ntp.Offset), net_time_point)


def is_utc(time_point):
    return (time_point.tzinfo == pendulum.UTC or
            time_point.tzinfo == dt.timezone.utc or
            time_point.tzinfo == duz.UTC)


def _net_time_point_to_datetime(time_zone_func, net_time_point):
    return pendulum.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                             net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                             net_time_point.Millisecond * 1000, time_zone_func(net_time_point))
