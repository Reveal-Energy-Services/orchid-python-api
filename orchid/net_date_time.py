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
import functools
from typing import Tuple, Union

import dateutil.tz as duz
import pendulum
import pendulum.tz as ptz

from orchid import base

# noinspection PyUnresolvedReferences
import System


UTC = pendulum.UTC
"""Encapsulate the use of pendulum."""


class TimePointTimeZoneKind(enum.Enum):
    """Models the kind of time point.

    This class eases conversions to the .NET `System.DateTime` class by providing Python with similar capabilities as
    the .NET `System.Enum`. (See
    [DateTimeKind](https://docs.microsoft.com/en-us/dotnet/api/system.datetimekind?view=net-5.0) for details).
    """
    UTC = System.DateTimeKind.Utc  # Time zone is UTC
    LOCAL = System.DateTimeKind.Local  # Time zone is specified to be local
    UNSPECIFIED = System.DateTimeKind.Unspecified  # Time zone is unspecified


class NetDateTimeError(ValueError):
    """
    Raised when an error occurs accessing the `System.TimeZoneInfo` of a .NET `System.DateTime` instance.
    """
    pass


class NetDateTimeLocalDateTimeKindError(NetDateTimeError):
    """
    Raised when the `System.DateTime.Kind` property of a .NET `System.DateTime` instance is `System.DateTimeKind.Local`.
    """
    def __init__(self, net_time_point: Union[System.DateTime, System.DateTimeOffset]):
        """
        Construct an instance from a .NET System.DateTime point in time.

        Args:
            net_time_point: A .NET System.DateTime representing a specific point in time.
        """
        super().__init__(self, '.NET System.DateTime.Kind cannot be Local.', net_time_point.ToString("O"))


class NetDateTimeUnspecifiedDateTimeKindError(NetDateTimeError):
    """
    Raised when the `System.DateTime.Kind` property of a .NET `System.DateTime` instance is not recognized.
    """
    ERROR_PREFACE = '.NET System.DateTime.Kind is unexpectedly Unspecified.'

    ERROR_SUFFIX = """
    Although .NET System.DateTime.Kind should not be Unspecified, it may be
    safe to ignore this error by catching the exception.

    However, because it unexpected, **please** report the issue to
    Reveal Energy Services. 
    """

    def __init__(self, net_time_point: Union[System.DateTime, System.DateTimeOffset]):
        """
        Construct an instance from a .NET System.DateTime point in time.

        Args:
            net_time_point: A .NET System.DateTime representing a specific point in time.
        """
        super().__init__(self, NetDateTimeUnspecifiedDateTimeKindError.ERROR_PREFACE,
                         net_time_point.ToString("O"), NetDateTimeUnspecifiedDateTimeKindError.ERROR_SUFFIX)


class NetDateTimeNoTzInfoError(NetDateTimeError):
    """
    Raised when the `System.DateTime.Kind` property of a .NET `System.DateTime` instance is
    `System.DateTimeKind.Unspecified`.
    """
    def __init__(self, time_point):
        """
        Construct an instance from a Python point in time.

        Args:
            time_point: A `pendulum.DateTime` representing a specific point in time.
        """
        super().__init__(self, f'The Python time point must specify the time zone.', time_point.isoformat())


class NetDateTimeOffsetNonZeroOffsetError(NetDateTimeError):
    """
    Raised when the `Offset` property of a .NET `System.DateTimeOffset` is non-zero.
    """
    def __init__(self, net_date_time_offset):
        """
        Construct an instance from a .NET `System.DateTimeOffset`.

        Args:
            net_date_time_offset: A .NET `System.DateTimeOffset` representing a specific point in time.
        """
        super().__init__(self,
                         f'The `Offset` of the .NET `System.DateTimeOffset`, {net_date_time_offset.ToString("o")},'
                         ' cannot be non-zero.')


@functools.singledispatch
def as_date_time(net_time_point: object) -> pendulum.DateTime:
    raise NotImplementedError


@as_date_time.register
def _(net_time_point: System.DateTime) -> pendulum.DateTime:
    """
    Convert a .NET `System.DateTime` instance to a `pendulum.DateTime` instance.

    Args:
        net_time_point: A point in time of type .NET `System.DateTime`.

    Returns:
        The `pendulum.DateTime` equivalent to the `to_test`.

        If `net_time_point` is `System.DateTime.MaxValue`, returns `pendulum.DateTime.max`. If `net_time_point` is
        `System.DateTime.MinValue`, returns `pendulum.DateTime.min`.
    """
    if net_time_point == System.DateTime.MaxValue:
        return pendulum.DateTime.max

    if net_time_point == System.DateTime.MinValue:
        return pendulum.DateTime.min

    if net_time_point.Kind == System.DateTimeKind.Utc:
        return _net_time_point_to_datetime(base.constantly(ptz.UTC), net_time_point)

    if net_time_point.Kind == System.DateTimeKind.Unspecified:
        raise NetDateTimeUnspecifiedDateTimeKindError(net_time_point)

    if net_time_point.Kind == System.DateTimeKind.Local:
        raise NetDateTimeLocalDateTimeKindError(net_time_point)

    raise ValueError(f'Unknown .NET System.DateTime.Kind, {net_time_point.Kind}.')


@as_date_time.register
def _(net_time_point: System.DateTimeOffset) -> pendulum.DateTime:
    """
    Convert a .NET `System.DateTimeOffset` instance to a `pendulum.DateTime` instance.

    Args:
        net_time_point: A point in time of type .NET `System.DateTimeOffset`.

    Returns:
        The `pendulum.DateTime` equivalent to the `net_time_point`.
    """
    if net_time_point == System.DateTimeOffset.MaxValue:
        return pendulum.DateTime.max

    if net_time_point == System.DateTimeOffset.MinValue:
        return pendulum.DateTime.min

    def net_date_time_offset_to_timezone(ntp):
        integral_offset = int(ntp.Offset.TotalSeconds)
        if integral_offset == 0:
            return ptz.UTC

        return ptz.timezone(integral_offset)

    return _net_time_point_to_datetime(net_date_time_offset_to_timezone, net_time_point)


def as_net_date_time(time_point: pendulum.DateTime) -> System.DateTime:
    """
    Convert a `pendulum.DateTime` instance to a .NET `System.DateTime` instance.

    Args:
        time_point: The `pendulum.DateTime` instance to covert.

    Returns:
        The equivalent .NET `System.DateTime` instance.

        If `time_point` is `pendulum.DateTime.max`, return `System.DateTime.MaxValue`. If `time_point` is
        `pendulum.DateTime.min`, return `System.DateTime.MinValue`.
    """
    if time_point == pendulum.DateTime.max:
        return System.DateTime.MaxValue

    if time_point == pendulum.DateTime.min:
        return System.DateTime.MinValue

    if not time_point.tzinfo == ptz.UTC:
        raise NetDateTimeNoTzInfoError(time_point)

    carry_seconds, milliseconds = microseconds_to_milliseconds_with_carry(time_point.microsecond)
    result = System.DateTime(time_point.year, time_point.month, time_point.day,
                             time_point.hour, time_point.minute, time_point.second + carry_seconds,
                             milliseconds, System.DateTimeKind.Utc)
    return result


def as_net_date_time_offset(time_point: pendulum.DateTime) -> System.DateTimeOffset:
    """
    Convert a `pendulum.DateTime` instance to a .NET `System.DateTimeOffset` instance.

    Args:
        time_point: The `pendulum.DateTime` instance to covert.

    Returns:
        The equivalent .NET `System.DateTimeOffset` instance.

        If `time_point` is `pendulum.DateTime.max`, return `System.DateTime.MaxValue`. If `time_point` is
        `pendulum.DateTime.min`, return `System.DateTime.MinValue`.
    """
    if time_point == pendulum.DateTime.max:
        return System.DateTimeOffset.MaxValue

    if time_point == pendulum.DateTime.min:
        return System.DateTimeOffset.MinValue

    date_time = as_net_date_time(time_point)
    result = System.DateTimeOffset(date_time)
    return result


def as_net_time_span(to_convert: pendulum.Duration):
    """
    Convert a `pendulum.Duration` instance to a .NET `System.TimeSpan`.

    Args:
        to_convert: The `pendulum.Duration` instance to convert.

    Returns:
        The .NET `System.TimeSpan` equivalent to `to_convert`.
    """
    return System.TimeSpan(round(to_convert.total_seconds() * System.TimeSpan.TicksPerSecond))


def as_duration(to_convert: System.TimeSpan) -> pendulum.Duration:
    """
    Convert a .NET `System.TimeSpan` to a python `pendulum.Duration`

    Args:
        to_convert: The .NET `System.TimeSpan` to convert.

    Returns:
        The `pendulum.Duration` equivalent to `to_convert`.

    """
    return pendulum.duration(seconds=to_convert.TotalSeconds)


def as_time_delta(net_time_span: System.TimeSpan):
    """
    Convert a .NET `System.TimeSpan` to a Python `dt.timedelta`.

    Args:
        net_time_span: The .NET `System.TimeSpan` to convert.

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


def is_utc(time_point):
    return (time_point.tzinfo == pendulum.UTC or
            time_point.tzinfo == dt.timezone.utc or
            time_point.tzinfo == duz.UTC)


def _net_time_point_to_datetime(time_zone_func, net_time_point):
    return pendulum.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                             net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                             net_time_point.Millisecond * 1000, tz=time_zone_func(net_time_point))
