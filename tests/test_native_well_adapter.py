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

import unittest.mock

from hamcrest import assert_that, equal_to

from orchid.native_well_adapter import NativeWellAdapter


class TestNativeWellAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_name(self):
        expected_well_name = 'sapientiarum'
        stub_native_well = unittest.mock.MagicMock(name='stub_native_well')
        stub_native_well.Name = expected_well_name
        sut = NativeWellAdapter(stub_native_well)

        assert_that(sut.name(), equal_to(expected_well_name))


if __name__ == '__main__':
    unittest.main()
