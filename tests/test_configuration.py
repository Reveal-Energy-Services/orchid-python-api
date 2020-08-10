#  Copyright 2017-2020 Reveal Energy Services, Inc 
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

import os
import pathlib
import unittest.mock

from hamcrest import assert_that, equal_to
import toolz.curried as toolz

import orchid.configuration


def multi_mock_open(*file_contents):
    """Create a mock "open" that will mock open multiple files in sequence

    This implementation is from https://gist.github.com/adammartinez271828/137ae25d0b817da2509c1a96ba37fc56.

    Args:
        *file_contents ([str]): a list of file contents to be returned by open
    Returns:
        (MagicMock) a mock opener that will return the contents of the first
            file when opened the first time, the second file when opened the
            second time, etc.
    """
    mock_files = [unittest.mock.mock_open(read_data=content).return_value for content in file_contents]
    mock_opener = unittest.mock.mock_open()
    mock_opener.side_effect = mock_files

    return mock_opener


# Test ideas
class ConfigurationTest(unittest.TestCase):
    PROGRAM_FILES_PATH = pathlib.Path('K:').joinpath(os.sep, 'dolavi')
    REVEAL_ROOT = PROGRAM_FILES_PATH.joinpath('Reveal Energy Services, Inc', 'Orchid')
    no_candidates = []
    one_candidate = REVEAL_ROOT.joinpath('Orchid-2020.4.101.13633')
    many_candidates = list(toolz.map(toolz.curry(REVEAL_ROOT.joinpath), ['Orchid-2020.4.101.86940',
                                                                         'Orchid-2020.4.139.82023',
                                                                         'Orchid-2020.4.151.44838']))
    no_dash_candidate = [REVEAL_ROOT.joinpath('Orchid2020.4.101.13633')]
    no_dots_candidate = [REVEAL_ROOT.joinpath('Orchid-2020')]
    non_int_candidate = [REVEAL_ROOT.joinpath('Orchid-2020.4.101.cf1f55b')]

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  # Setting Path.exists to return False ensures that the
                                  # SUT *does not* read the (developer) configuration file.
                                  exists=unittest.mock.MagicMock(return_value=False),
                                  # Path.open is actually called by orchid.configuration.Version()
                                  open=unittest.mock.mock_open(read_data='2020.4.101.13633'))
    def test_orchid_one_installed(self):
        assert_that(orchid.configuration.python_api()['directory'],
                    equal_to(str(ConfigurationTest.one_candidate)))

    @staticmethod
    def test_custom_orchid_directory():
        expected_directory = r'I:\diluvialis\Indus\Orchid'
        with unittest.mock.patch.multiple(pathlib.Path,
                                          exists=unittest.mock.MagicMock(return_value=True),
                                          open=multi_mock_open('2020.4.101.13633', f'directory: {expected_directory}')):
            assert_that(orchid.configuration.python_api()['directory'], equal_to(expected_directory))


if __name__ == '__main__':
    unittest.main()
