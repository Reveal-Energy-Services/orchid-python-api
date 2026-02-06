#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2025 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import enum
import dataclasses as dc
import datetime as dt  # only for UTC time zone
from numbers import Real

import pendulum as pdt
import toolz.curried as toolz

from orchid import (
    measurement as om,
    net_date_time as net_dt,
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import Int32, DateTime, DateTimeKind, DateTimeOffset, TimeSpan


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

    def to_datetime(self) -> pdt.DateTime:
        """
        Constructs a `pdt.DateTime` instance from this instance.

        Returns:
            The `pdt.Datetime` instance equivalent to `time_point_dto`.
        """

        result = pdt.datetime(self.year, self.month, self.day,
                              self.hour, self.minute, self.second,
                              int(self.fractional.to(om.registry.microseconds).magnitude),
                              tz=_kind_to_tzinfo(self.kind.value))
        return result

    def to_net_date_time(self) -> DateTime:
        """
        Construct a .NET `DateTime` instance from this instance.

        Returns:
            The .NET `DateTime` equivalent to this instance.
        """
        result = DateTime(self.year, self.month, self.day,
                          self.hour, self.minute, self.second,
                          int(round(self.fractional.to(om.registry.milliseconds).magnitude)),
                          self.kind.value)
        return result


@dc.dataclass
class TimeSpanDto:
    hour: int
    minute: int
    second: int
    # Setting is negative to `False` makes all components, hour, minute, and second, negative in the resulting
    # .NET `TimeSpan`.
    is_negative: bool = False


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


def make_net_time_span(time_delta_dto: TimeSpanDto):
    if not time_delta_dto.is_negative:
        return TimeSpan(time_delta_dto.hour, time_delta_dto.minute, time_delta_dto.second)
    else:
        return TimeSpan(-time_delta_dto.hour, -time_delta_dto.minute, -time_delta_dto.second)


def utc_time_zone() -> dt.tzinfo:
    """
    Calculate the single instance of the UTC time zone.

    Returns:
        The single instance of the UTC time zone.
    """
    return pdt.UTC


_KIND_TO_TZINFO = {
    net_dt.TimePointTimeZoneKind.UTC: pdt.UTC,
    net_dt.TimePointTimeZoneKind.LOCAL: pdt.local_timezone(),
    net_dt.TimePointTimeZoneKind.UNSPECIFIED: '',
}


def _kind_to_tzinfo(to_convert: int) -> str:
    return toolz.get(net_dt.TimePointTimeZoneKind(to_convert), _KIND_TO_TZINFO)
