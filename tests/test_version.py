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

import unittest
from unittest.mock import patch
from orchid.version import get_orchid_sdk_version
import pathlib


class TestVersion(unittest.TestCase):
    def test_api_version(self):
        for text_version in ['2018.3.3497', '4.93.26.2823']:
            with self.subTest(f'Testing version {text_version}'):
                with unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path, open=unittest.mock.mock_open(read_data=text_version)):
                    self.assertEqual(get_orchid_sdk_version(), text_version)

    def test_api_version_file_not_found(self) -> None:
        with patch.object(pathlib.Path, 'open', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                get_orchid_sdk_version()

    def test_api_version_invalid_format(self) -> None:
        with patch.object(pathlib.Path, 'open', unittest.mock.mock_open(read_data="invalid version")):
            with self.assertRaises(ValueError):
                get_orchid_sdk_version()


if __name__ == '__main__':
    unittest.main()
