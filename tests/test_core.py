#  Copyright (c) 2017-2025 KAPPA
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

import unittest

import deal
from hamcrest import assert_that, equal_to, is_, calling, raises

import orchid


class TestCoreLoadProject(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, is_(equal_to(4)))

    def test_no_pathname_load_project_raises_exception(self):
        assert_that(calling(orchid.load_project).with_args(None), raises(deal.PreContractError))

    def test_empty_pathname_load_project_raises_exception(self):
        assert_that(calling(orchid.load_project).with_args(''), raises(deal.PreContractError))

    def test_whitespace_pathname_load_project_raises_exception(self):
        assert_that(calling(orchid.load_project).with_args('\t'), raises(deal.PreContractError))


if __name__ == '__main__':
    unittest.main()
