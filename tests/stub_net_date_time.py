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

import enum
import dataclasses as dc
import datetime as dt
from numbers import Real

import dateutil.tz as duz
import toolz.curried as toolz

from orchid import (
    measurement as om,
    net_date_time as net_dt,
)

# noinspection PyUnresolvedReferences
from System import Int32, DateTime, DateTimeKind, DateTimeOffset


@dc.dataclass
class TimePointDto:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    fractional: om.Quantity = 0 * om.registry.microseconds
    kind: net_dt.TimePointTimeZoneKind = net_dt.TimePointTimeZoneKind.UTC


# noinspection PyPep8Naming
class StubNetDateTime:
    def __init__(self, year, month, day, hour, minute, second, millisecond, kind):
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._millisecond = millisecond
        self._kind = kind

    @property
    def Year(self):
        return self._year

    @property
    def Month(self):
        return self._month

    @property
    def Day(self):
        return self._day

    @property
    def Hour(self):
        return self._hour

    @property
    def Minute(self):
        return self._minute

    @property
    def Second(self):
        return self._second

    @property
    def Millisecond(self):
        return self._millisecond

    @property
    def Kind(self):
        return self._kind

    def ToString(self, _format):
        return f'{self.Year}-{self.Month:02}-{self.Day:02}T{self.Hour:02}:{self.Minute:02}:{self.Second:02}' \
               f'.000{self.Millisecond}K{self.Kind}'


class StubDateTimeKind(enum.IntEnum):
    UNSPECIFIED = 0,
    UTC = 1,
    LOCAL = 2,
    INVALID = -999999999,  # most likely not a match to any DateTimeKind member.


def make_microseconds(magnitude: Real) -> om.Quantity:
    """
    Make a `pint` `Quantity` with the specified magnitude and `microsecond` unit.
    Args:
        magnitude: The magnitude of the measurement

    Returns:
        The `pint` `Quantity`.
    """
    return magnitude * om.registry.microseconds


def make_milliseconds(magnitude: Real) -> om.Quantity:
    """
    Make a `pint` `Quantity` with the specified magnitude and `millisecond` unit.
    Args:
        magnitude: The magnitude of the measurement

    Returns:
        The `pint` `Quantity`.
    """
    return magnitude * om.registry.milliseconds


def make_net_date_time(time_point_dto: TimePointDto) -> DateTime:
    """
    Construct a .NET `DateTime` instance from a `TimePointDto` instance.

    Args:
        time_point_dto: The `TimePointDto` instance used to construct the .NET `DateTime` instance.

    Returns:
        The .NET `DateTime` equivalent to `time_point_dto`.
    """
    result = DateTime(time_point_dto.year, time_point_dto.month, time_point_dto.day,
                      time_point_dto.hour, time_point_dto.minute, time_point_dto.second,
                      int(round(time_point_dto.fractional.to(om.registry.milliseconds).magnitude)),
                      time_point_dto.kind.value)

    return result


def make_net_date_time_offset(time_point_dto: TimePointDto) -> DateTimeOffset:
    """
    Construct a .NET `DateTimeOffset` instance from a `TimePointDto` instance.

    Args:
        time_point_dto: The `TimePointDto` instance used to construct the .NET `DateTimeOffset` instance.

    Returns:
        The .NET `DateTimeOffset` equivalent to `time_point_dto`.
    """
    result = DateTimeOffset(make_net_date_time(time_point_dto))
    return result


def make_datetime(time_point_dto: TimePointDto) -> dt.datetime:
    """
    Constructs a `datetime` instance from a `TimePointDto` instance.

    This method is mostly for convenience.

    Args:
        time_point_dto: The instance from which to construct the `datetime` instance.

    Returns:
        The `datetime` instance equivalent to `time_point_dto`.
    """

    result = dt.datetime(time_point_dto.year, time_point_dto.month, time_point_dto.day,
                         time_point_dto.hour, time_point_dto.minute, time_point_dto.second,
                         int(time_point_dto.fractional.to(om.registry.microseconds).magnitude),
                         _kind_to_tzinfo(time_point_dto.kind.value))
    return result


def utc_time_zone() -> dt.tzinfo:
    """
    Calculate the single instance of the UTC time zone.

    Returns:
        The single instance of the UTC time zone.
    """
    return duz.UTC


_KIND_TO_TZINFO = {
    net_dt.TimePointTimeZoneKind.UTC: dt.timezone.utc,
    net_dt.TimePointTimeZoneKind.LOCAL: duz.tzlocal(),
    net_dt.TimePointTimeZoneKind.UNSPECIFIED: None,
}


def _kind_to_tzinfo(to_convert: int) -> dt.tzinfo:
    return toolz.get(net_dt.TimePointTimeZoneKind(to_convert), _KIND_TO_TZINFO)
