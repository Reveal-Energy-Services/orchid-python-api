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

import unittest

from hamcrest import assert_that, equal_to
import pendulum

from orchid import (
    native_monitor_adapter as nma,
    net_date_time as net_dt,
)
from tests import stub_net as tsn


class TestNativeMonitorAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name(self):
        stub_net_monitor = tsn.create_stub_net_monitor(display_name='maiores')
        sut = nma.NativeMonitorAdapter(stub_net_monitor)

        assert_that(sut.display_name, equal_to('maiores'))

    def test_name(self):
        stub_net_monitor = tsn.create_stub_net_monitor(name='credula')
        sut = nma.NativeMonitorAdapter(stub_net_monitor)

        assert_that(sut.name, equal_to('credula'))

    def test_time_range(self):
        def microseconds_to_milliseconds(tp):
            carry, milliseconds = net_dt.microseconds_to_milliseconds_with_carry(tp.microsecond)
            return tp.set(second=tp.second + carry, microsecond=milliseconds * 1000)

        expected_start = pendulum.datetime(2027, 7, 3, 7, 9, 37, 54174)
        expected_stop = pendulum.datetime(2027, 7, 12, 8, 55, 56, 628905)
        stub_net_monitor = tsn.create_stub_net_monitor(start=expected_start, stop=expected_stop)
        sut = nma.NativeMonitorAdapter(stub_net_monitor)

        actual_time_range = sut.time_range

        assert_that(actual_time_range,
                    equal_to(pendulum.period(microseconds_to_milliseconds(expected_start),
                                             microseconds_to_milliseconds(expected_stop))))


if __name__ == '__main__':
    unittest.main()
