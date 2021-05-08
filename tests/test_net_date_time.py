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

import datetime
import unittest

from hamcrest import assert_that, calling, equal_to, raises
import dateutil.tz as duz

from orchid import net_date_time as ndt

from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind


class TestNetDateTime(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_as_datetime_net_time_point_kind_utc(self):
        net_time_point = DateTime(2020, 8, 5, 6, 59, 41, 726, DateTimeKind.Utc)
        actual = ndt.as_datetime(net_time_point)

        assert_that(actual, equal_to(datetime.datetime(2020, 8, 5, 6, 59, 41, 726000, tzinfo=duz.UTC)))

    def test_as_datetime_net_time_point_kind_local(self):
        net_time_point = DateTime(2024, 11, 24, 18, 56, 35, 45, DateTimeKind.Local)
        expected_error_message = f'{net_time_point.ToString("O")}.'
        assert_that(calling(ndt.as_datetime).with_args(net_time_point),
                    raises(ndt.NetQuantityLocalDateTimeKindError, pattern=expected_error_message))

    def test_as_datetime_net_time_point_kind_unspecified_throws_exception(self):
        net_time_point = tsn.StubDateTime(2023, 7, 31, 1, 11, 26, 216, tsn.StubDateTimeKind.UNSPECIFIED)
        expected_error_message = f'{net_time_point.ToString("O")}'
        assert_that(calling(ndt.as_datetime).with_args(net_time_point),
                    raises(ndt.NetQuantityUnspecifiedDateTimeKindError, pattern=expected_error_message))

    def test_as_datetime_net_time_point_kind_unknown_throws_exception(self):
        net_time_point = tsn.StubDateTime(2019, 2, 10, 9, 36, 36, 914, tsn.StubDateTimeKind.INVALID)
        expected_error_pattern = f'Unknown .NET DateTime.Kind, {tsn.StubDateTimeKind.INVALID}.'
        assert_that(calling(ndt.as_datetime).with_args(net_time_point),
                    raises(ValueError, pattern=expected_error_pattern))

    def test_as_net_date_time(self):
        for expected, time_point in [(DateTime(2017, 3, 22, 3, 0, 37, 23, DateTimeKind.Utc),
                                      datetime.datetime(2017, 3, 22, 3, 0, 37, 23124, duz.UTC)),
                                     (DateTime(2020, 9, 20, 22, 11, 51, 655, DateTimeKind.Utc),
                                      datetime.datetime(2020, 9, 20, 22, 11, 51, 654859, duz.UTC)),
                                     # The Python `round` function employs "half-even" rounding; however, the
                                     # following test rounds to an *odd* value instead. See the "Note" in the
                                     # Python documentation of `round` for an explanation of this (unexpected)
                                     # behavior.
                                     (DateTime(2022, 2, 2, 23, 35, 39, 979, DateTimeKind.Utc),
                                      datetime.datetime(2022, 2, 2, 23, 35, 39, 978531, duz.UTC)),
                                     (DateTime(2019, 2, 7, 10, 18, 17, 488, DateTimeKind.Utc),
                                      datetime.datetime(2019, 2, 7, 10, 18, 17, 487500, duz.UTC)),
                                     (DateTime(2022, 1, 14, 20, 29, 18, 852, DateTimeKind.Utc),
                                      datetime.datetime(2022, 1, 14, 20, 29, 18, 852500, duz.UTC))
                                     ]:
            with self.subTest(f'Test as_net_date_time for {expected}'):
                actual = ndt.as_net_date_time(time_point)
                assert_that(actual, tcm.equal_to_net_date_time(expected))

    def test_as_net_date_time_raises_error_if_not_utc(self):
        to_test_datetime = datetime.datetime(2025, 12, 21, 9, 15, 7, 896671)
        assert_that(calling(ndt.as_net_date_time).with_args(to_test_datetime),
                    raises(ndt.NetQuantityNoTzInfoError, pattern=to_test_datetime.isoformat()))


if __name__ == '__main__':
    unittest.main()
