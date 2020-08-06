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

import pathlib
import unittest
import unittest.mock

from hamcrest import assert_that, equal_to

import orchid.version as version


class TestVersion(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_supplied_version(self):
        assert_that(version.Version(version=(2017, 3, 6970, 466160)),
                    equal_to(version.Version(version=(2017, 3, 6970, 466160))))

    def test_read_version(self):
        with unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                          open=unittest.mock.mock_open(read_data='2018.3.3497.133205')):
            assert_that(version.Version(), equal_to(version.Version(version=(2018, 3, 3497, 133205))))


if __name__ == '__main__':
    unittest.main()
