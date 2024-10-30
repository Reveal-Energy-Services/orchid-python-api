#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2024 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import datetime as dt
import unittest

from hamcrest import assert_that, calling, equal_to, raises, is_, same_instance
import pendulum

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
# - is_max_value() for values below, at and above boundary
# - is_min_value() for values below, at and above boundary
# - as_date_time returns correct value if .NET DateTimeOffset has non-zero offset
class TestNetDateTime(unittest.TestCase):

    def test_as_date_time_net_time_point_kind_utc(self):
        time_point_dto = stub_dt.TimePointDto(2020, 8, 5, 6, 59, 41, stub_dt.make_milliseconds(726),
                                              net_dt.TimePointTimeZoneKind.UTC)
        actual = net_dt.as_date_time(stub_dt.make_net_date_time(time_point_dto))

        assert_that(actual, equal_to(time_point_dto.to_datetime()))

    def test_as_date_time_net_time_point_kind_local(self):
        time_point_dto = stub_dt.TimePointDto(2024, 11, 24, 18, 56, 35, stub_dt.make_milliseconds(45),
                                              net_dt.TimePointTimeZoneKind.LOCAL)
        net_time_point = stub_dt.make_net_date_time(time_point_dto)
        expected_error_message = f'{net_time_point.ToString("O")}.'
        assert_that(calling(net_dt.as_date_time).with_args(net_time_point),
                    raises(net_dt.NetDateTimeLocalDateTimeKindError, pattern=expected_error_message))

    def test_as_date_time_net_time_point_kind_unspecified_throws_exception(self):
        time_point_dto = stub_dt.TimePointDto(2023, 7, 31, 1, 11, 26, stub_dt.make_milliseconds(216),
                                              net_dt.TimePointTimeZoneKind.UNSPECIFIED)
        net_time_point = stub_dt.make_net_date_time(time_point_dto)
        expected_error_message = f'{net_time_point.ToString("o")}'
        assert_that(calling(net_dt.as_date_time).with_args(net_time_point),
                    raises(net_dt.NetDateTimeUnspecifiedDateTimeKindError, pattern=expected_error_message))

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
                actual = net_dt.as_net_date_time(time_point.to_datetime())
                assert_that(actual, tcm.equal_to_net_date_time(expected))

    def test_as_net_date_time_from_parsed_time_is_correct(self):
        parsed_date_time = pendulum.parse('2025-12-16T23:19:56.095891Z')
        expected_dto = stub_dt.TimePointDto(2025, 12, 16, 23, 19, 56,
                                            95891 * om.registry.microseconds, net_dt.TimePointTimeZoneKind.UTC)

        expected = stub_dt.make_net_date_time(expected_dto)
        assert_that(net_dt.as_net_date_time(parsed_date_time), tcm.equal_to_net_date_time(expected))

    def test_as_net_date_time_raises_error_if_not_utc(self):
        to_test_date_time = pendulum.datetime(2025, 12, 21, 9, 15, 7, 896671).naive()
        assert_that(calling(net_dt.as_net_date_time).with_args(to_test_date_time),
                    raises(net_dt.NetDateTimeNoTzInfoError, pattern=to_test_date_time.isoformat()))

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
                actual = net_dt.as_net_date_time_offset(time_point.to_datetime())
                assert_that(actual, tcm.equal_to_net_date_time_offset(expected))

    def test_as_net_date_time_offset_from_parsed_time_is_correct(self):
        parsed_date_time = pendulum.parse('2019-06-18T11:14:29.901487Z')
        expected_dto = stub_dt.TimePointDto(2019, 6, 18, 11, 14, 29,
                                            901487 * om.registry.microseconds,
                                            net_dt.TimePointTimeZoneKind.UTC)

        expected = stub_dt.make_net_date_time_offset(expected_dto)
        assert_that(net_dt.as_net_date_time_offset(parsed_date_time), tcm.equal_to_net_date_time_offset(expected))

    def test_as_net_date_time_offset_raises_error_if_not_utc(self):
        to_test_datetime = pendulum.datetime(2027, 4, 5, 10, 14, 13, 696066).naive()
        assert_that(calling(net_dt.as_net_date_time_offset).with_args(to_test_datetime),
                    raises(net_dt.NetDateTimeNoTzInfoError, pattern=to_test_datetime.isoformat()))

    def test_convert_net_sentinel_to_date_time_sentinel(self):
        for net_sentinel_name, net_sentinel, sut_func, date_time_sentinel_name, date_time_sentinel in [
            ('DateTime.MinValue', DateTime.MinValue,
             net_dt.as_date_time, 'pendulum.DateTime.min', pendulum.DateTime.min),
            ('DateTimeOffset.MinValue', DateTimeOffset.MinValue,
             net_dt.as_date_time, 'pendulum.DateTime.min', pendulum.DateTime.min),
            ('DateTime.MaxValue', DateTime.MaxValue,
             net_dt.as_date_time, 'pendulum.DateTime.max', pendulum.DateTime.max),
            ('DateTimeOffset.MaxValue', DateTimeOffset.MaxValue,
             net_dt.as_date_time, 'pendulum.DateTime.max', pendulum.DateTime.max),
        ]:
            with self.subTest(f'Convert {net_sentinel_name} to {date_time_sentinel_name}'):
                assert_that(sut_func(net_sentinel), is_(same_instance(date_time_sentinel)))

    def test_as_net_time_span(self):
        for duration, expected in [
            (pendulum.duration(hours=22, minutes=48, seconds=30, microseconds=756193),
             TimeSpan(0, 22, 48, 30, 756).Add(TimeSpan(1930))),
            # Don't think rounding is an issue here, but let's verify.
            (pendulum.duration(hours=14, minutes=10, seconds=22, microseconds=456499),
             TimeSpan(0, 14, 10, 22, 456).Add(TimeSpan(4990))),
            (pendulum.duration(hours=16, minutes=8, seconds=32, microseconds=917500),
             TimeSpan(0, 16, 8, 32, 917).Add(TimeSpan(5000))),
            (pendulum.duration(hours=23, minutes=7, seconds=57, microseconds=910600),
             TimeSpan(0, 23, 7, 57, 910).Add(TimeSpan(6000))),
        ]:
            with self.subTest(f'Convert pendulum.Duration, {duration}'):
                actual = net_dt.as_net_time_span(duration)
                assert_that(actual, equal_to(expected))

    def test_as_duration(self):
        for net_time_span, expected in [
            (TimeSpan(0, 0, 36, 36, 989), pendulum.duration(hours=0, minutes=36, seconds=36, microseconds=989000)),
            (TimeSpan(0), pendulum.duration()),
            # The printed representation of the following time span is "-1 day, 8:44:17.856000"
            (TimeSpan(0, -15, -15, -42, -144), pendulum.duration(hours=-15, minutes=-15,
                                                                 seconds=-42, microseconds=-144000)),
        ]:
            with self.subTest(f'Convert .NET TimeSpan, {str(net_time_span)}'):
                actual = net_dt.as_duration(net_time_span)
                assert_that(actual, equal_to(expected))

    def test_as_duration_from_rounded_net_time_span(self):
        for net_time_span, expected in [
            # 346 milliseconds + 714 microseconds + 0.4 microseconds rounded to 346714 microseconds
            (TimeSpan(0, 6, 59, 18, 346).Add(TimeSpan(7140)).Add(TimeSpan(4)),
             pendulum.duration(hours=6, minutes=59, seconds=18, microseconds=346714)),
            # 71 milliseconds + 677 microseconds + 0.6 microseconds rounded to 71578 microseconds
            (TimeSpan(0, 2, 58, 1, 71).Add(TimeSpan(6770)).Add(TimeSpan(6)),
             pendulum.duration(hours=2, minutes=58, seconds=1, microseconds=71678)),
            # Half-even rounding (See https://en.wikipedia.org/wiki/Rounding#Round_half_to_even)
            # 799 milliseconds + 877 microseconds + 0.5 microseconds rounded to 799878 microseconds
            (TimeSpan(0, 12, 20, 24, 799).Add(TimeSpan(8770)).Add(TimeSpan(5)),
             pendulum.duration(hours=12, minutes=20, seconds=24, microseconds=799878)),
            # 310 milliseconds + 94 microseconds + 0.5 microseconds rounded to 310094 microseconds
            (TimeSpan(0, 3, 30, 15, 310).Add(TimeSpan(940)).Add(TimeSpan(5)),
             pendulum.duration(hours=3, minutes=30, seconds=15, microseconds=310094)),
        ]:
            with self.subTest(f'Convert .NET TimeSpan, {str(net_time_span)}, to `pendulum.Duration` with rounding'):
                actual = net_dt.as_duration(net_time_span)
                assert_that(actual, equal_to(expected))

    def test_as_time_delta(self):
        for time_delta_dto in [
            stub_dt.TimeSpanDto(23, 49, 53, is_negative=True),
            stub_dt.TimeSpanDto(0, 0, 0),
            stub_dt.TimeSpanDto(0, 59, 57),
        ]:
            net_time_span = stub_dt.make_net_time_span(time_delta_dto)
            with self.subTest(f'Test converting .NET TimeSpan, {net_time_span}, to time_delta'):
                actual = net_dt.as_time_delta(net_time_span)

                expected = dt.timedelta(hours=time_delta_dto.hour, minutes=time_delta_dto.minute,
                                        seconds=time_delta_dto.second)
                if time_delta_dto.is_negative:
                    expected = dt.timedelta(hours=-time_delta_dto.hour, minutes=-time_delta_dto.minute,
                                            seconds=-time_delta_dto.second)
                assert_that(actual, equal_to(expected))

    def test_convert_date_time_sentinel_to_net_sentinel(self):
        for date_time_sentinel_name, date_time_sentinel, sut_func, net_sentinel_name, net_sentinel in [
            ('pendulum.DateTime.min', pendulum.DateTime.min,
             net_dt.as_net_date_time, 'DateTime.MinValue', DateTime.MinValue),
            ('pendulum.DateTime.min', pendulum.DateTime.min,
             net_dt.as_net_date_time_offset, 'DateTimeOffset.MinValue', DateTimeOffset.MinValue),
            ('pendulum.DateTime.max', pendulum.DateTime.max,
             net_dt.as_net_date_time, 'DateTime.MaxValue', DateTime.MaxValue),
            ('pendulum.DateTime.max', pendulum.DateTime.max,
             net_dt.as_net_date_time_offset, 'DateTimeOffset.MaxValue', DateTimeOffset.MaxValue),
        ]:
            with self.subTest(f'Convert {date_time_sentinel_name} to {net_sentinel_name}'):
                assert_that(sut_func(date_time_sentinel), equal_to(net_sentinel))

    def test_microseconds_to_milliseconds_with_carry(self):
        for to_convert, expected_carry, expected_milliseconds in [
            (999499, 0, 999),
            (999599, 1, 0),
            (999600, 1, 0),
        ]:
            with self.subTest(f'{to_convert} microseconds to'
                              f' {expected_carry} seconds and {expected_milliseconds} milliseconds'):
                actual = net_dt.microseconds_to_milliseconds_with_carry(to_convert)
                assert_that(actual, equal_to((expected_carry, expected_milliseconds)))

    def test_net_date_time_offset_as_date_time(self):
        time_point = stub_dt.TimePointDto(
            2026, 2, 19, 12, 26, 58, 226 * om.registry.milliseconds, net_dt.TimePointTimeZoneKind.UTC
        )
        net_date_time_offset = stub_dt.make_net_date_time_offset(time_point)
        actual = net_dt.as_date_time(net_date_time_offset)
        expected = time_point.to_datetime()
        assert_that(actual, tcm.equal_to_datetime(expected))

    def test_net_date_time_offset_with_non_zero_offset_as_date_time(self):
        net_date_time_offset = DateTimeOffset(2021, 12, 23, 1, 0, 19, 421, TimeSpan(-8, 0, 0))
        expected = pendulum.parse('2021-12-23T01:00:19.421000-08:00')
        actual = net_dt.as_date_time(net_date_time_offset)
        assert_that(actual, tcm.equal_to_datetime(expected))


if __name__ == '__main__':
    unittest.main()
