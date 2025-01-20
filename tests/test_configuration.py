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

import os
import pathlib
import unittest.mock
import warnings

from hamcrest import assert_that, equal_to, has_entry, empty, not_, has_key, has_entries, all_of, is_, instance_of

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
# - Fallback only (no env, no file)
# - No env. File overrides fallback.
# - No env. File and fallback merge.
# - No env. File and fallback distinct at top.
# - No file. Env overrides fallback.
# - No file. Env and fallback merge.
# - All three. Env overrides file.
# - All three. Env and file merge.
# - All three. Env and file distinct at top.
class ConfigurationTest(unittest.TestCase):
    """Defines the unit tests for the `configuration` module.

    BEWARE: The current unit tests assume that the configuration used by the Orchid Python API is a "two-level"
    configuration. If the dictionary becomes deeper or shallower, one would need to change these tests.
    """

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_env_no_file_configuration_returns_fallback(self, stub_get_fallback_configuration,
                                                           stub_get_file_configuration,
                                                           stub_get_environment_configuration):
        expected_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = expected_configuration
        stub_get_file_configuration.return_value = {}
        stub_get_environment_configuration.return_value = {}
        actual = orchid.configuration.get_configuration()

        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_env_file_overrides_fallback(self, stub_get_fallback_configuration,
                                            stub_get_file_configuration,
                                            stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        # file_configuration = {'coniunx': {'magnitudo': 'colubrae'}}
        expected_configuration = {'coniunx': {'barbarus': 'colubrae'}}
        stub_get_file_configuration.return_value = expected_configuration
        stub_get_environment_configuration.return_value = {}
        actual = orchid.configuration.get_configuration()

        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_env_file_and_fallback_merges(self, stub_get_fallback_configuration,
                                             stub_get_file_configuration,
                                             stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        file_configuration = {'coniunx': {'magnitudo': 'colubrae'}}
        stub_get_file_configuration.return_value = file_configuration
        stub_get_environment_configuration.return_value = {}
        actual = orchid.configuration.get_configuration()

        expected_configuration = {'coniunx': {'barbarus': 'ponet',
                                              'magnitudo': 'colubrae'}}
        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_env_file_and_fallback_distinct_top(self, stub_get_fallback_configuration,
                                                   stub_get_file_configuration,
                                                   stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        file_configuration = {'coniugis': {'barbarus': 'colubrae'}}
        stub_get_file_configuration.return_value = file_configuration
        stub_get_environment_configuration.return_value = {}
        actual = orchid.configuration.get_configuration()

        expected_configuration = {'coniunx': {'barbarus': 'ponet'},
                                  'coniugis': {'barbarus': 'colubrae'}}
        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_file_env_overrides_fallback(self, stub_get_fallback_configuration,
                                            stub_get_file_configuration,
                                            stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        stub_get_file_configuration.return_value = {}
        expected_configuration = {'coniunx': {'barbarus': 'grandisit'}}
        stub_get_environment_configuration.return_value = expected_configuration
        actual = orchid.configuration.get_configuration()

        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_file_env_and_fallback_merge(self, stub_get_fallback_configuration,
                                            stub_get_file_configuration,
                                            stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        stub_get_file_configuration.return_value = {}
        environment_configuration_configuration = {'coniunx': {'Gnaeus': 'grandisit'}}
        stub_get_environment_configuration.return_value = environment_configuration_configuration
        actual = orchid.configuration.get_configuration()

        expected_configuration = {'coniunx': {'barbarus': 'ponet',
                                              'Gnaeus': 'grandisit'}}
        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_no_file_env_and_fallback_distinct_at_top(self, stub_get_fallback_configuration,
                                                      stub_get_file_configuration,
                                                      stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        stub_get_file_configuration.return_value = {}
        environment_configuration = {'coniugis': {'barbarus': 'grandisit'}}
        stub_get_environment_configuration.return_value = environment_configuration
        actual = orchid.configuration.get_configuration()

        expected_configuration = {'coniunx': {'barbarus': 'ponet'},
                                  'coniugis': {'barbarus': 'grandisit'}}
        assert_that(actual, equal_to(expected_configuration))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_all_three_env_overrides_file(self, stub_get_fallback_configuration,
                                          stub_get_file_configuration,
                                          stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        file_configuration = {'coniunx': {'deliciam': 'providit'}}
        stub_get_file_configuration.return_value = file_configuration
        environment_configuration = {'coniunx': {'deliciam': 'lapidarium'}}
        stub_get_environment_configuration.return_value = environment_configuration
        actual = orchid.configuration.get_configuration()

        assert_that(actual, equal_to({'coniunx': {'barbarus': 'ponet',
                                                  'deliciam': 'lapidarium'}}))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_all_three_env_and_file_merge(self, stub_get_fallback_configuration,
                                          stub_get_file_configuration,
                                          stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        file_configuration = {'coniunx': {'deliciam': 'providit'}}
        stub_get_file_configuration.return_value = file_configuration
        environment_configuration = {'coniunx': {'patruelis': 'lapidarium'}}
        stub_get_environment_configuration.return_value = environment_configuration
        actual = orchid.configuration.get_configuration()

        assert_that(actual, equal_to({'coniunx': {'barbarus': 'ponet',
                                                  'deliciam': 'providit',
                                                  'patruelis': 'lapidarium'}}))

    @unittest.mock.patch('orchid.configuration.get_environment_configuration')
    @unittest.mock.patch('orchid.configuration.get_file_configuration')
    @unittest.mock.patch('orchid.configuration.get_fallback_configuration')
    def test_all_three_env_overrides_file(self, stub_get_fallback_configuration,
                                          stub_get_file_configuration,
                                          stub_get_environment_configuration):
        fallback_configuration = {'coniunx': {'barbarus': 'ponet'}}
        stub_get_fallback_configuration.return_value = fallback_configuration
        file_configuration = {'coniunx': {'deliciam': 'providit'}}
        stub_get_file_configuration.return_value = file_configuration
        environment_configuration = {'coniugis': {'deliciam': 'lapidarium'}}
        stub_get_environment_configuration.return_value = environment_configuration
        actual = orchid.configuration.get_configuration()

        assert_that(actual, equal_to({'coniunx': {'barbarus': 'ponet',
                                                  'deliciam': 'providit'},
                                      'coniugis': {'deliciam': 'lapidarium'}}))


# Test ideas
class EnvironmentConfigurationTest(unittest.TestCase):
    @staticmethod
    def test_configuration_contains_root_and_training_data_if_root_and_training_data_exist_in_environment():
        expected_root_path = pathlib.Path('N:/', 'pons', 'rudem', 'dilitavit')
        expected_training_data_path = pathlib.Path('W:/', 'Venus', 'et', 'epistula')
        with unittest.mock.patch.dict('os.environ', {'ORCHID_ROOT': str(expected_root_path),
                                                     'ORCHID_TRAINING_DATA': str(expected_training_data_path)},
                                      clear=True):
            actual = orchid.configuration.get_environment_configuration()

            # noinspection PyTypeChecker
            assert_that(actual['orchid'], has_entries(root=str(expected_root_path),
                                                      training_data=str(expected_training_data_path)))

    @staticmethod
    def test_configuration_contains_root_but_no_training_data_if_only_root_in_environment():
        expected_root_path = pathlib.Path('N:/', 'pons', 'rudem', 'dilitavit')
        expected_training_data_path = pathlib.Path('W:/', 'Venus', 'et', 'epistula')
        with unittest.mock.patch.dict('os.environ', {'ORCHID_ROOT': str(expected_root_path),
                                                     'ORCHID_TRAINING_DATUM': str(expected_training_data_path)},
                                      clear=True):
            actual = orchid.configuration.get_environment_configuration()

            # noinspection PyTypeChecker
            assert_that(actual['orchid'], all_of(has_entries(root=str(expected_root_path)),
                                                 not_(has_key('training_data'))))

    @staticmethod
    def test_configuration_contains_no_root_but_training_data_if_only_training_data_in_environment():
        expected_root_path = pathlib.Path('N:/', 'pons', 'rudem', 'dilitavit')
        expected_training_data_path = pathlib.Path('W:/', 'Venus', 'et', 'epistula')
        with unittest.mock.patch.dict('os.environ', {'ORCHID_ROOF': str(expected_root_path),
                                                     'ORCHID_TRAINING_DATA': str(expected_training_data_path)},
                                      clear=True):
            actual = orchid.configuration.get_environment_configuration()

            # noinspection PyTypeChecker
            assert_that(actual['orchid'], all_of(has_entries(training_data=str(expected_training_data_path)),
                                                 not_(has_key('root'))))

    @staticmethod
    def test_configuration_empty_if_neither_root_nor_training_data_in_environment():
        expected_root_path = pathlib.Path('N:/', 'pons', 'rudem', 'dilitavit')
        expected_training_data_path = pathlib.Path('W:/', 'Venus', 'et', 'epistula')
        with unittest.mock.patch.dict('os.environ', {'ORCHID_ROOF': str(expected_root_path),
                                                     'ORCHID_TRAINING_DATUM': str(expected_training_data_path)},
                                      clear=True):
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
    def test_orchid_root_dir_based_on_1_glob_match_does_not_have_training_data(self):
        with unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                          open=unittest.mock.mock_open(read_data='2023.3.466')):

            with unittest.mock.patch('glob.glob') as patch_glob:
                patch_glob.return_value = ['cheesecake factory']
                actual_fallback = orchid.configuration.get_fallback_configuration()

                assert_that(actual_fallback['orchid'], not_(has_key('training_data')))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    def test_orchid_root_dir_based_on_1_glob_match_has_correct_path(self):
        with unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                          open=unittest.mock.mock_open(read_data='2022.3.466')):
            with unittest.mock.patch('glob.glob') as patch_glob:
                stub_dir = 'obiwan_kenobi'
                patch_glob.return_value = [stub_dir]
                actual_fallback = orchid.configuration.get_fallback_configuration()

                assert_that(actual_fallback['orchid']['root'], equal_to(stub_dir))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    def test_orchid_root_dir_returns_empty_if_0_glob_matches(self):
        with unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                          open=unittest.mock.mock_open(read_data='2022.3.466')):

            with unittest.mock.patch('glob.glob') as patch_glob:
                patch_glob.return_value = []
                actual_fallback = orchid.configuration.get_fallback_configuration()

                # noinspection PyTypeChecker
                assert_that(actual_fallback, not_(has_key('orchid')))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    def test_orchid_root_dir_returns_empty_if_multiple_glob_matches(self):
        with unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                          open=unittest.mock.mock_open(read_data='2022.3.466')):
            with unittest.mock.patch('glob.glob') as patch_glob:
                patch_glob.return_value = ['legalos', 'gimli', 'gandalf']
                with warnings.catch_warnings(record=True) as caught_warning:
                    actual_fallback = orchid.configuration.get_fallback_configuration()

                    # noinspection PyTypeChecker
                    assert_that(actual_fallback, not_(has_key('orchid')))
                    assert_that(len(caught_warning), equal_to(1))
                    # noinspection PyTypeChecker
                    assert_that(caught_warning[0].message, is_(instance_of(UserWarning)))


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
    def test_config_file_contains_root_returns_configuration_with_same_root(self, yaml_stub):
        home_path = pathlib.Path(r'O:\pretium\inane')
        expected_root = r'I:\diluvialis\Indus\Orchid'
        yaml_stub.full_load = unittest.mock.MagicMock(return_value={'orchid': {'root': expected_root}})
        with unittest.mock.patch.multiple(pathlib.Path,
                                          home=unittest.mock.MagicMock(return_value=home_path),
                                          exists=unittest.mock.MagicMock(return_value=True),
                                          open=multi_mock_open("don't care")):
            actual = orchid.configuration.get_file_configuration()

            # noinspection PyTypeChecker
            assert_that(actual['orchid'], has_entry('root', expected_root))

    @unittest.mock.patch('orchid.configuration.yaml')
    def test_config_file_contains_training_data_returns_configuration_with_same_training_data(self, yaml_stub):
        home_path = pathlib.Path(r'O:\pretium\inane')
        expected_training_data = r'V:\Aegyptus\humanum\fastidiosum'
        yaml_stub.full_load = unittest.mock.MagicMock(
            return_value={'orchid': {'training_data': expected_training_data}})
        with unittest.mock.patch.multiple(pathlib.Path,
                                          home=unittest.mock.MagicMock(return_value=home_path),
                                          exists=unittest.mock.MagicMock(return_value=True),
                                          open=multi_mock_open("don't care")):
            actual = orchid.configuration.get_file_configuration()

            # noinspection PyTypeChecker
            assert_that(actual['orchid'], has_entry('training_data', expected_training_data))


if __name__ == '__main__':
    unittest.main()
