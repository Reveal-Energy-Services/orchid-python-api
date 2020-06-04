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

import deal
from hamcrest import assert_that, equal_to, is_, calling, raises

import orchid


class TestCoreLoadProject(unittest.TestCase):
    def test_canary (self):
        assert_that(2 + 2, is_(equal_to(4)))

    def test_no_pathname_load_project_raises_exception(self):
        assert_that(calling(orchid.load_project).with_args(None), raises(deal.PreContractError))

    def test_empty_pathname_load_project_raises_exception(self):
        assert_that(calling(orchid.load_project).with_args(''), raises(deal.PreContractError))

    def test_whitespace_pathname_load_project_raises_exception(self):
        assert_that(calling(orchid.load_project).with_args('\t'), raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
