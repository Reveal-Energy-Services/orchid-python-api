#  Copyright (c) 2017-2024 KAPPA
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

import pathlib
import unittest
import unittest.mock

from hamcrest import assert_that, equal_to

import orchid.version as ov

import tests.custom_matchers as tcm


class TestVersion(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_api_version(self):
        for text_version, version_tuple in [('2018.3.3497', (2018, 3, 3497)), ('4.93.26.b2', (4, 93, 26, ('b', 2))), ]:
            with self.subTest(f'Testing version {text_version}'):
                with unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                                  open=unittest.mock.mock_open(read_data=text_version)):
                    assert_that(ov.api_version(),
                                tcm.equal_to_version(version_tuple))


if __name__ == '__main__':
    unittest.main()
