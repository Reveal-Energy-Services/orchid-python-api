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

import unittest
import uuid

from hamcrest import assert_that, equal_to
import pendulum

from orchid import (
    native_monitor_adapter as nma,
    net_date_time as net_dt,
)
from tests import stub_net as tsn


class TestNativeMonitorAdapter(unittest.TestCase):

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
                    equal_to(pendulum.Interval(microseconds_to_milliseconds(expected_start),
                                             microseconds_to_milliseconds(expected_stop))))

    def test_well_time_series(self):
        time_series_dto = {'object_id': '6de0edfa-dff5-47b1-9970-6eff0880bb86'}
        stub_net_monitor = tsn.create_stub_net_monitor(well_time_series_dto=time_series_dto)

        sut = nma.NativeMonitorAdapter(stub_net_monitor)

        expected_uuid = uuid.UUID(time_series_dto['object_id'])
        assert_that(sut.well_time_series.object_id, equal_to(expected_uuid))


if __name__ == '__main__':
    unittest.main()
