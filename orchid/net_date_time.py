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
Functions to convert between .NET `DateTime` instances and Python `datetime.datetime` instances.
"""


import datetime as dt
import enum
from typing import Tuple

from dateutil import tz as duz
import toolz.curried as toolz

from orchid import base

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, DateTimeOffset, TimeSpan


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
            time_point: A Python `dt.datetime` representing a specific point in time.
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


def as_datetime(net_time_point: DateTime) -> dt.datetime:
    """
    Convert a .NET `DateTime` instance to a `dt.datetime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTime`.

    Returns:
        The `dt.datetime` equivalent to the `to_test`.

        If `net_time_point` is `DateTime.MaxValue`, returns `dt.datetime.max`. If `net_time_point` is
        `DateTime.MinValue`, returns `dt.datetime.min`.
    """
    if net_time_point == DateTime.MaxValue:
        return dt.datetime.max

    if net_time_point == DateTime.MinValue:
        return dt.datetime.min

    if net_time_point.Kind == DateTimeKind.Utc:
        return _net_time_point_to_datetime(base.constantly(duz.UTC), net_time_point)

    if net_time_point.Kind == DateTimeKind.Unspecified:
        raise NetDateTimeUnspecifiedDateTimeKindError(net_time_point)

    if net_time_point.Kind == DateTimeKind.Local:
        raise NetDateTimeLocalDateTimeKindError(net_time_point)

    raise ValueError(f'Unknown .NET DateTime.Kind, {net_time_point.Kind}.')


def as_net_date_time(time_point: dt.datetime) -> DateTime:
    """
    Convert a `dt.datetime` instance to a .NET `DateTime` instance.

    Args:
        time_point: The `dt.datetime` instance to covert.

    Returns:
        The equivalent .NET `DateTime` instance.

        If `time_point` is `dt.datetime.max`, return `DateTime.MaxValue`. If `time_point` is
        `dt.datetime.min`, return `DateTime.MinValue`.
    """
    if time_point == dt.datetime.max:
        return DateTime.MaxValue

    if time_point == dt.datetime.min:
        return DateTime.MinValue

    if (time_point.tzinfo != duz.UTC) and (time_point.tzinfo != dt.timezone.utc):
        raise NetDateTimeNoTzInfoError(time_point)

    carry_seconds, milliseconds = microseconds_to_milliseconds_with_carry(time_point.microsecond)
    result = DateTime(time_point.year, time_point.month, time_point.day,
                      time_point.hour, time_point.minute, time_point.second + carry_seconds,
                      milliseconds, DateTimeKind.Utc)
    return result


def as_net_date_time_offset(time_point: dt.datetime) -> DateTimeOffset:
    """
    Convert a `dt.datetime` instance to a .NET `DateTimeOffset` instance.

    Args:
        time_point: The `dt.datetime` instance to covert.

    Returns:
        The equivalent .NET `DateTimeOffset` instance.

        If `time_point` is `dt.datetime.max`, return `DateTime.MaxValue`. If `time_point` is
        `dt.datetime.min`, return `DateTime.MinValue`.
    """
    if time_point == dt.datetime.max:
        return DateTimeOffset.MaxValue

    if time_point == dt.datetime.min:
        return DateTimeOffset.MinValue

    date_time = as_net_date_time(time_point)
    result = DateTimeOffset(date_time)
    return result


def as_net_time_span(to_convert):
    """
    Convert a `dt.timedelta` instance to a .NET `TimeSpan`
    Args:
        to_convert: The `dt.timedelta` instance to convert.

    Returns:
        The .NET `TimeSpan` equivalent to `to_convert`.
    """
    return TimeSpan(round(to_convert.total_seconds() * TimeSpan.TicksPerSecond))


def as_timedelta(to_convert: TimeSpan) -> dt.timedelta:
    """
    Convert a .NET `TimeSpan` to a python `dt.timedelta`

    Args:
        to_convert: The .NET `TimeSpan` to convert.

    Returns:
        The python `dt.timedelta` equivalent to `to_convert`.

    """
    return dt.timedelta(seconds=to_convert.TotalSeconds)


def dateutil_utc_to_datetime_utc(time_point):
    """
    Convert a UTC timezone from the `dateutil` package to a UTC timezone from the `datetime` package.
    Args:
        time_point: The time point whose timezone may need conversion.

    Returns:
        The converted time point.
    """
    if isinstance(time_point, type(dt.datetime.utcnow())):
        return time_point.replace(tzinfo=dt.timezone.utc)
    return time_point


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


def net_date_time_offset_as_datetime(net_time_point: DateTimeOffset) -> dt.datetime:
    """
    Convert a .NET `DateTimeOffset` instance to a `dt.datetime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTimeOffset`.

    Returns:
        The `dt.datetime` equivalent to the `net_time_point`.
    """
    if net_time_point == DateTimeOffset.MaxValue:
        return dt.datetime.max

    if net_time_point == DateTimeOffset.MinValue:
        return dt.datetime.min

    if net_time_point.Offset.TotalSeconds != 0:
        raise NetDateTimeOffsetNonZeroOffsetError(net_time_point)

    make_timezone = toolz.compose(dt.timezone,
                                  lambda s: dt.timedelta(seconds=s),
                                  round,
                                  lambda ntp: ntp.Offset.TotalSeconds)
    return _net_time_point_to_datetime(make_timezone, net_time_point)


def _net_time_point_to_datetime(time_zone_func, net_time_point):
    return dt.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                       net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                       net_time_point.Millisecond * 1000, time_zone_func(net_time_point))
