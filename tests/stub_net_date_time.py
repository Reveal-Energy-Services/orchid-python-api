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
from datetime import datetime, timedelta


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
