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

from dateutil import tz as duz

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind


class TimePointTimeZoneKind(enum.Enum):
    """Models the kind of time point.

    This class eases conversions to the .NET `DateTime` class by providing Python with similar capabilities as
    the .NET `Enum`. (See
    [DateTimeKind](https://docs.microsoft.com/en-us/dotnet/api/system.datetimekind?view=net-5.0) for details).
    """
    UTC = DateTimeKind.Utc,  # Time zone is UTC
    LOCAL = DateTimeKind.Local,  # Time zone is specified to be local
    UNSPECIFIED = DateTimeKind.Unspecified,  # Time zone is unspecified


class NetQuantityTimeZoneError(ValueError):
    """
    Raised when an error occurs accessing the `TimeZoneInfo` of a .NET `DateTime` instance.
    """
    pass


class NetQuantityLocalDateTimeKindError(NetQuantityTimeZoneError):
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


class NetQuantityUnspecifiedDateTimeKindError(NetQuantityTimeZoneError):
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
        super().__init__(self, NetQuantityUnspecifiedDateTimeKindError.ERROR_PREFACE,
                         net_time_point.ToString("O"), NetQuantityUnspecifiedDateTimeKindError.ERROR_SUFFIX)


class NetQuantityNoTzInfoError(NetQuantityTimeZoneError):
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


def as_datetime(net_time_point: DateTime) -> dt.datetime:
    """
    Convert a .NET `DateTime` instance to a `dt.datetime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTime`.

    Returns:
        The `dt.datetime` equivalent to the `net_time_point`.
    """
    if net_time_point.Kind == DateTimeKind.Utc:
        return dt.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                           net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                           net_time_point.Millisecond * 1000, duz.UTC)

    if net_time_point.Kind == DateTimeKind.Unspecified:
        raise NetQuantityUnspecifiedDateTimeKindError(net_time_point)

    if net_time_point.Kind == DateTimeKind.Local:
        raise NetQuantityLocalDateTimeKindError(net_time_point)

    raise ValueError(f'Unknown .NET DateTime.Kind, {net_time_point.Kind}.')


def as_net_date_time(time_point: dt.datetime) -> DateTime:
    """
    Convert a `dt.datetime` instance to a .NET `DateTime` instance.

    Args:
        time_point: The `dt.datetime` instance to covert.

    Returns:
        The equivalent .NET `DateTime` instance.
    """
    # TODO: Consider using the zulu package
    # Research using the [zulu package](https://zulu.readthedocs.io/en/latest/). This package is "a drop-in
    # replacement for native datetimes that embraces UTC."
    #
    # Much to my surprise, the `dateutil` and standard Python libraries have two **different** values for a
    # `tzinfo` instance identifying a UTC time. The `dateutil` library uses the value `dateutil.tz.tzutc()`
    # and its synonym: `dateutil.tz.UTC`. The standard library uses `timezone.utc`.
    if time_point.tzinfo != duz.UTC and time_point.tzinfo != dt.timezone.utc:
        raise NetQuantityNoTzInfoError(time_point)

    return DateTime(time_point.year, time_point.month, time_point.day, time_point.hour, time_point.minute,
                    time_point.second, microseconds_to_integral_milliseconds(time_point.microsecond),
                    DateTimeKind.Utc)


def microseconds_to_integral_milliseconds(to_convert: int) -> int:
    """
    Convert microseconds to an integral number of milliseconds.

    Args:
        to_convert: The milliseconds to convert.

    Returns:
        An integral number of milliseconds equivalent to `to_convert` microseconds.

    """
    return int(round(to_convert / 1000))
