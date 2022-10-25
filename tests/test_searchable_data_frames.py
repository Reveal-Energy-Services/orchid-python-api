#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
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
import uuid

import toolz.curried as toolz
from hamcrest import assert_that, equal_to, calling, raises

from orchid import (
    searchable_data_frames as sdf,
)
from tests import stub_net as tsn

# noinspection PyUnresolvedReferences
from System import Guid


class TestSearchableDataFrames(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))


if __name__ == '__main__':
    unittest.main()
