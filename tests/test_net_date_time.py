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

import datetime as dt
import unittest

from dateutil import (
    parser as dup,
)
from hamcrest import assert_that, calling, equal_to, raises

from orchid import (
    measurement as om,
    net_date_time as net_dt,
)

from tests import (
    custom_matchers as tcm,
    stub_net_date_time as stub_dt,
)

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, DateTimeOffset, TimeSpan


# Test ideas
# - Correctly handle `microsecond_to_integral_millisecond()` for 999999 microsecond
#   - 999400 microseconds to 999 milliseconds
#   - 999500 microseconds to 1 **second**
#   - 999999 microseconds to 1 **second**
#   - For both `DateTime` and for `DateTimeOffset`
class TestNetDateTime(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_datetime_net_time_point_kind_utc(self):
        time_point_dto = stub_dt.TimePointDto(2020, 8, 5, 6, 59, 41, stub_dt.make_milliseconds(726),
                                              net_dt.TimePointTimeZoneKind.UTC)
        actual = net_dt.as_datetime(stub_dt.make_net_date_time(time_point_dto))

        assert_that(actual, equal_to(stub_dt.make_datetime(time_point_dto)))

    def test_as_datetime_net_time_point_kind_local(self):
        time_point_dto = stub_dt.TimePointDto(2024, 11, 24, 18, 56, 35, stub_dt.make_milliseconds(45),
                                              net_dt.TimePointTimeZoneKind.LOCAL)
        net_time_point = stub_dt.make_net_date_time(time_point_dto)
        expected_error_message = f'{net_time_point.ToString("O")}.'
        assert_that(calling(net_dt.as_datetime).with_args(net_time_point),
                    raises(net_dt.NetDateTimeLocalDateTimeKindError, pattern=expected_error_message))

    def test_as_datetime_net_time_point_kind_unspecified_throws_exception(self):
        time_point_dto = stub_dt.TimePointDto(2023, 7, 31, 1, 11, 26, stub_dt.make_milliseconds(216),
                                              net_dt.TimePointTimeZoneKind.UNSPECIFIED)
        net_time_point = stub_dt.make_net_date_time(time_point_dto)
        expected_error_message = f'{net_time_point.ToString("O")}'
        assert_that(calling(net_dt.as_datetime).with_args(net_time_point),
                    raises(net_dt.NetDateTimeUnspecifiedDateTimeKindError, pattern=expected_error_message))

    def test_as_datetime_net_time_point_kind_unknown_throws_exception(self):
        net_time_point = stub_dt.StubNetDateTime(2019, 2, 10, 9, 36, 36, 914, stub_dt.StubDateTimeKind.INVALID)
        expected_error_pattern = f'Unknown .NET DateTime.Kind, {stub_dt.StubDateTimeKind.INVALID}.'
        assert_that(calling(net_dt.as_datetime).with_args(net_time_point),
                    raises(ValueError, pattern=expected_error_pattern))

    def test_as_net_date_time(self):
        for time_point in [
            stub_dt.TimePointDto(2017, 3, 22, 3, 0, 37,
                                 stub_dt.make_microseconds(23124), net_dt.TimePointTimeZoneKind.UTC),
            stub_dt.TimePointDto(2020, 9, 20, 22, 11, 51,
                                 stub_dt.make_microseconds(654859), net_dt.TimePointTimeZoneKind.UTC),
            # The Python `round` function employs "half-even" rounding; however, the
            # following test rounds to an *odd* value instead. See the "Note" in the
            # Python documentation of `round` for an explanation of this (unexpected)
            # behavior.
            stub_dt.TimePointDto(2022, 2, 2, 23, 35, 39,
                                 stub_dt.make_microseconds(978531), net_dt.TimePointTimeZoneKind.UTC),
            stub_dt.TimePointDto(2019, 2, 7, 10, 18, 17,
                                 stub_dt.make_microseconds(487500), net_dt.TimePointTimeZoneKind.UTC),
            stub_dt.TimePointDto(2022, 1, 14, 20, 29, 18,
                                 stub_dt.make_microseconds(852500), net_dt.TimePointTimeZoneKind.UTC),
        ]:
            expected = stub_dt.make_net_date_time(time_point)
            with self.subTest(f'Test as_net_date_time for {expected.ToString("o")}'):
                actual = net_dt.as_net_date_time(stub_dt.make_datetime(time_point))
                assert_that(actual, tcm.equal_to_net_date_time(expected))

    def test_as_net_date_time_from_parsed_time_is_correct(self):
        parsed_date_time = dup.parse("2025-12-16T23:19:56.095891Z")
        expected_dto = stub_dt.TimePointDto(2025, 12, 16, 23, 19, 56,
                                            95891 * om.registry.microseconds, net_dt.TimePointTimeZoneKind.UTC)

        expected = stub_dt.make_net_date_time(expected_dto)
        assert_that(net_dt.as_net_date_time(parsed_date_time), tcm.equal_to_net_date_time(expected))

    def test_as_net_date_time_raises_error_if_not_utc(self):
        to_test_datetime = dt.datetime(2025, 12, 21, 9, 15, 7, 896671)
        assert_that(calling(net_dt.as_net_date_time).with_args(to_test_datetime),
                    raises(net_dt.NetDateTimeNoTzInfoError, pattern=to_test_datetime.isoformat()))

    def test_as_net_date_time_offset(self):
        for time_point in [
            stub_dt.TimePointDto(2023, 4, 20, 0, 3, 54,
                                 stub_dt.make_microseconds(500438), net_dt.TimePointTimeZoneKind.UTC),
            stub_dt.TimePointDto(2024, 8, 20, 21, 50, 15,
                                 stub_dt.make_microseconds(590797), net_dt.TimePointTimeZoneKind.UTC),
            stub_dt.TimePointDto(2010, 10, 14, 6, 56, 11,
                                 stub_dt.make_microseconds(348562), net_dt.TimePointTimeZoneKind.UTC),
            stub_dt.TimePointDto(2026, 12, 15, 6, 53, 25,
                                 stub_dt.make_microseconds(301500), net_dt.TimePointTimeZoneKind.UTC),
            stub_dt.TimePointDto(2027, 7, 28, 18, 49, 15,
                                 stub_dt.make_microseconds(348500), net_dt.TimePointTimeZoneKind.UTC),
        ]:
            expected = stub_dt.make_net_date_time_offset(time_point)
            with self.subTest(f'Test as_net_date_time for {expected.ToString("o")}'):
                actual = net_dt.as_net_date_time_offset(stub_dt.make_datetime(time_point))
                assert_that(actual, tcm.equal_to_net_date_time_offset(expected))

    def test_as_net_date_time_offset_from_parsed_time_is_correct(self):
        parsed_date_time = dup.parse('2019-06-18T11:14:29.901487Z')
        expected_dto = stub_dt.TimePointDto(2019, 6, 18, 11, 14, 29,
                                            901487 * om.registry.microseconds,
                                            net_dt.TimePointTimeZoneKind.UTC)

        expected = stub_dt.make_net_date_time_offset(expected_dto)
        assert_that(net_dt.as_net_date_time_offset(parsed_date_time), tcm.equal_to_net_date_time_offset(expected))

    def test_as_net_date_time_offset_raises_error_if_not_utc(self):
        to_test_datetime = dt.datetime(2027, 4, 5, 10, 14, 13, 696066)
        assert_that(calling(net_dt.as_net_date_time_offset).with_args(to_test_datetime),
                    raises(net_dt.NetDateTimeNoTzInfoError, pattern=to_test_datetime.isoformat()))

    def test_convert_datetime_max_returns_net_max_sentinel(self):
        for net_sentinel, to_test_func in [
            (DateTime.MaxValue, net_dt.as_net_date_time),
            (DateTimeOffset.MaxValue, net_dt.as_net_date_time_offset),
        ]:
            with self.subTest(f'{to_test_func.__name__}(datetime.max) == ({net_sentinel.ToString("o")})'):
                actual = to_test_func(dt.datetime.max)
                assert_that(actual, equal_to(net_sentinel))

    def test_convert_datetime_min_returns_net_min_sentinel(self):
        for net_sentinel, to_test_func in [
            (DateTime.MinValue, net_dt.as_net_date_time),
            (DateTimeOffset.MinValue, net_dt.as_net_date_time_offset),
        ]:
            with self.subTest(f'{to_test_func.__name__}(datetime.min) == ({net_sentinel.ToString("o")})'):
                actual = to_test_func(dt.datetime.min)
                assert_that(actual, equal_to(net_sentinel))

    def test_net_date_time_offset_as_datetime(self):
        time_point = stub_dt.TimePointDto(
            2026, 2, 19, 12, 26, 58, 226 * om.registry.milliseconds, net_dt.TimePointTimeZoneKind.UTC
        )
        actual = net_dt.net_date_time_offset_as_datetime(stub_dt.make_net_date_time_offset(time_point))
        expected = stub_dt.make_datetime(time_point)
        assert_that(actual, tcm.equal_to_datetime(expected))

    def test_net_date_time_offset_as_datetime_raises_error_if_non_zero_offset(self):
        net_date_time_offset = DateTimeOffset(2026, 3, 17, 16, 42, 47, 694, TimeSpan.FromMinutes(1))
        assert_that(calling(net_dt.net_date_time_offset_as_datetime).with_args(net_date_time_offset),
                    raises(net_dt.NetDateTimeOffsetNonZeroOffsetError,
                           pattern=r'`Offset`.*2026-03-17T16:42:47.6940000\+00:01'))


if __name__ == '__main__':
    unittest.main()
