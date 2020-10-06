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
    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_file_configuration_returns_default(self, stub_get_fallback_configuration, stub_get_file_configuration):
        expected_configuration = {'coniunx': 'barbarus/ponet'}
        stub_get_fallback_configuration.return_value = expected_configuration
        stub_get_file_configuration.return_value = {}
        actual = orchid.configuration.python_api()

        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_file_configuration_overrides_default(self, stub_get_fallback_configuration, stub_get_file_configuration):
        fallback_configuration = {'coniunx': 'barbarus/ponet'}
        stub_get_fallback_configuration.return_value = fallback_configuration
        expected_configuration = {'coniunx': 'magnitudo/colubrae'}
        stub_get_file_configuration.return_value = expected_configuration
        actual = orchid.configuration.python_api()

        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_merge_file_and_fallback_configuration_if_distinct(self, stub_get_fallback_configuration,
                                                               stub_get_file_configuration):
        fallback_configuration = {'coniunx': 'barbarus/ponet'}
        stub_get_fallback_configuration.return_value = fallback_configuration
        expected_configuration = {'fur': 'deliciam/providit'}
        stub_get_file_configuration.return_value = expected_configuration
        actual = orchid.configuration.python_api()

        assert_that(actual, equal_to({'coniunx': 'barbarus/ponet',
                                      'fur': 'deliciam/providit'}))


# Test ideas
class EnvironmentConfigurationTest(unittest.TestCase):
    @staticmethod
    def test_configuration_contains_orchid_bin_value_if_orchid_bin_exists_in_environment():
        expected_path = pathlib.Path('N:/', 'pons', 'rudem', 'dilitavit')
        with unittest.mock.patch.dict('os.environ', {'ORCHID_BIN': str(expected_path)}):
            actual = orchid.configuration.get_environment_configuration()

            # noinspection PyTypeChecker
            assert_that(actual, has_entry('directory', str(expected_path)))

    @staticmethod
    def test_configuration_empty_if_no_orchid_bin_exists_in_environment():
        with unittest.mock.patch.dict('os.environ', {}):
            actual = orchid.configuration.get_environment_configuration()

            # noinspection PyTypeChecker
            assert_that(actual, empty())


# Test ideas
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
