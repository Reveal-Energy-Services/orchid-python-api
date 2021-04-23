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

from orchid import native_data_frame_adapter as dfa

from tests import stub_net as tsn


class TestNativeDataFrameAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name(self):
        for net_display_name, expected_display_name in [('lucrum', 'lucrum'), (None, 'Not set')]:
            with self.subTest(f'Testing .NET display name, "{net_display_name}",'
                              f' and display name "{expected_display_name}"'):
                stub_net_data_frame = tsn.create_stub_net_data_frame(display_name=net_display_name)
                sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

                assert_that(sut.display_name, equal_to(expected_display_name))

    def test_name(self):
        stub_net_data_frame = tsn.create_stub_net_data_frame(name='avus')
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        assert_that(sut.name, equal_to('avus'))


if __name__ == '__main__':
    unittest.main()
