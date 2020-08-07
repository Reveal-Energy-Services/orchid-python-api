#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
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
import unittest.mock as mock

from hamcrest import assert_that, equal_to

import orchid.native_well_time_series_adapter as nwtsa


class TestWellTimeSeries(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_name(self):
        expected_display_name = 'excoriaverunt'
        stub_native_well_time_series = mock.MagicMock(name='stub_native_well_time_series')
        stub_native_well_time_series.DisplayName = expected_display_name
        sut = nwtsa.NativeWellTimeSeriesAdapter(stub_native_well_time_series)

        assert_that(sut.display_name, equal_to(expected_display_name))



if __name__ == '__main__':
    unittest.main()
