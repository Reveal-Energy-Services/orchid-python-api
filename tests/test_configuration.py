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

from hamcrest import assert_that, equal_to, has_entry, empty

from orchid.version import Version, VersionId
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
    one_candidate = REVEAL_ROOT.joinpath('Orchid-2020.4.151')

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  # Setting Path.exists to return False ensures that the
                                  # SUT *does not* read the (developer) configuration file.
                                  exists=unittest.mock.MagicMock(return_value=False),
                                  # Path.open is actually called by orchid.configuration.Version()
                                  open=unittest.mock.mock_open(read_data='2020.4.151'))
    def test_orchid_one_installed(self):
        assert_that(orchid.configuration.python_api()['directory'],
                    equal_to(str(ConfigurationTest.one_candidate)))

    @staticmethod
    def test_custom_orchid_directory():
        expected_directory = r'I:\diluvialis\Indus\Orchid'
        with unittest.mock.patch.multiple(pathlib.Path,
                                          exists=unittest.mock.MagicMock(return_value=True),
                                          open=multi_mock_open('2020.4.101', f'directory: {expected_directory}')):
            assert_that(orchid.configuration.python_api()['directory'], equal_to(expected_directory))


# Test ideas
# - Default location of Orchid binaries
class FallbackConfigurationTest(unittest.TestCase):
    PROGRAM_FILES_PATH = pathlib.Path('K:').joinpath(os.sep, 'dolavi')
    ORCHID_VER_ROOT = PROGRAM_FILES_PATH.joinpath('Reveal Energy Services, Inc', 'Orchid')

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    def test_orchid_bin_dir_based_on_version_id(self):
        version_id = VersionId(3, 1, 4)
        with unittest.mock.patch('orchid.version.Version', spec=Version) as stub_version:
            to_patch = stub_version.return_value
            to_patch.id.return_value = version_id
            actual_fallback = orchid.configuration.get_fallback_configuration()

            expected_fallback_bin_directory = pathlib.Path(self.ORCHID_VER_ROOT).joinpath(
                f'Orchid-{version_id.major}.{version_id.minor}.{version_id.patch}')
            assert_that(actual_fallback['directory'], equal_to(str(expected_fallback_bin_directory)))


# Test ideas
# - Location of Orchid binaries from file system
class FileConfigurationTest(unittest.TestCase):
    PROGRAM_FILES_PATH = pathlib.Path('K:').joinpath(os.sep, 'dolavi')

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @staticmethod
    def test_file_config_returns_empty_if_no_config_file():
        home_path = pathlib.Path(r'I:\diluvialis\Indus')
        with unittest.mock.patch.multiple(pathlib.Path,
                                          home=unittest.mock.MagicMock(return_value=home_path),
                                          exists=unittest.mock.MagicMock(return_value=False)):
            actual = orchid.configuration.get_file_configuration()

            # noinspection PyTypeChecker
            assert_that(actual, empty())

    @unittest.mock.patch('orchid.configuration.yaml')
    def test_config_file_exists_configuration_contains_file_version(self, yaml_stub):
        home_path = pathlib.Path(r'O:\pretium\inane')
        expected_directory = r'I:\diluvialis\Indus\Orchid'
        yaml_stub.full_load = unittest.mock.MagicMock(return_value={'directory': expected_directory})
        with unittest.mock.patch.multiple(pathlib.Path,
                                          home=unittest.mock.MagicMock(return_value=home_path),
                                          exists=unittest.mock.MagicMock(return_value=True),
                                          open=multi_mock_open('foobar')):
            actual = orchid.configuration.get_file_configuration()

            # noinspection PyTypeChecker
            assert_that(actual, has_entry('directory', expected_directory))


if __name__ == '__main__':
    unittest.main()
