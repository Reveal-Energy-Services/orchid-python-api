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

from hamcrest import assert_that, equal_to
import datetimerange as dtr
import dateutil.tz as dtz

from orchid import native_monitor_adapter as nma
from tests import (
    custom_matchers as tcm,
    stub_net as tsn,
)


class TestNativeMonitorAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_time_range(self):
        expected_start = datetime.datetime(2027, 7, 3, 7, 9, 37, 54174, tzinfo=dtz.tzutc())
        expected_stop = datetime.datetime(2027, 7, 12, 8, 55, 56, 628905, tzinfo=dtz.tzutc())
        stub_net_monitor = tsn.create_stub_net_monitor(start=expected_start, stop=expected_stop)
        sut = nma.NativeMonitorAdapter(stub_net_monitor)

        actual_time_range = sut.time_range

        assert_that(actual_time_range, tcm.equal_to_time_range(dtr.DateTimeRange(expected_start, expected_stop)))


if __name__ == '__main__':
    unittest.main()
