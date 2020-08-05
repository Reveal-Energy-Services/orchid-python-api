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

import os
import pathlib
import re
import unittest.mock

from hamcrest import assert_that, equal_to, calling, raises
import toolz.curried as toolz

import orchid.configuration


# Test ideas
class ConfigurationTest(unittest.TestCase):
    PROGRAM_FILES_PATH = pathlib.Path('K:').joinpath(os.sep, 'dolavi')
    no_candidates = []
    one_candidate = [PROGRAM_FILES_PATH.joinpath('Orchid-2020.4.101.13633')]
    many_candidates = list(toolz.map(toolz.curry(PROGRAM_FILES_PATH.joinpath), ['Orchid-2020.4.101.86940',
                                                                                'Orchid-2020.4.139.82023',
                                                                                'Orchid-2020.4.151.44838']))
    no_dash_candidate = [PROGRAM_FILES_PATH.joinpath('Orchid2020.4.101.13633')]
    no_dots_candidate = [PROGRAM_FILES_PATH.joinpath('Orchid-2020')]
    non_int_candidate = [PROGRAM_FILES_PATH.joinpath('Orchid-2020.4.101.cf1f55b')]

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  # Setting Path.exists to return False ensures that the
                                  # SUT *does not* read the (developer) configuration file.
                                  exists=unittest.mock.MagicMock(return_value=False),
                                  glob=unittest.mock.MagicMock(return_value=one_candidate))
    def test_orchid_one_installed(self):
        assert_that(orchid.configuration.python_api()['directory'],
                    equal_to(str(ConfigurationTest.one_candidate[0])))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  # Setting Path.exists to return False ensures that the
                                  # SUT *does not* read the (developer) configuration file.
                                  exists=unittest.mock.MagicMock(return_value=False),
                                  glob=unittest.mock.MagicMock(return_value=no_candidates))
    def test_orchid_not_installed(self):
        assert_that('directory' not in orchid.configuration.python_api())

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  # Setting Path.exists to return False ensures that the
                                  # SUT *does not* read the (developer) configuration file.
                                  exists=unittest.mock.MagicMock(return_value=False),
                                  glob=unittest.mock.MagicMock(return_value=many_candidates))
    def test_orchid_many_installed(self):
        assert_that(orchid.configuration.python_api()['directory'],
                    equal_to(str(ConfigurationTest.many_candidates[-1])))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  glob=unittest.mock.MagicMock(return_value=no_dash_candidate))
    def test_orchid_no_dash_basename(self):
        expected_pattern = re.escape(
            r'Expected directories matching "Orchid-(major).(minor).(patch).(build)" (all integers) ' +
            fr'but found, "{str(self.no_dash_candidate[0])}".')
        assert_that(calling(orchid.configuration.python_api).with_args(),
                    raises(orchid.configuration.ConfigurationError, pattern=expected_pattern))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  glob=unittest.mock.MagicMock(return_value=no_dots_candidate))
    def test_orchid_no_dot_version(self):
        expected_pattern = re.escape(
            r'Expected directories matching "Orchid-(major).(minor).(patch).(build)" (all integers) ' +
            fr'but found, "{str(self.no_dots_candidate[0])}".')
        assert_that(calling(orchid.configuration.python_api).with_args(),
                    raises(orchid.configuration.ConfigurationError, pattern=expected_pattern))

    @unittest.mock.patch.dict('os.environ', {'ProgramFiles': os.fspath(PROGRAM_FILES_PATH)})
    @unittest.mock.patch.multiple(pathlib.Path, spec=pathlib.Path,
                                  glob=unittest.mock.MagicMock(return_value=non_int_candidate))
    def test_orchid_not_int_version(self):
        expected_pattern = re.escape(
            r'Expected directories matching "Orchid-(major).(minor).(patch).(build)" (all integers) ' +
            fr'but found, "{str(self.non_int_candidate[0])}".')
        assert_that(calling(orchid.configuration.python_api).with_args(),
                    raises(orchid.configuration.ConfigurationError, pattern=expected_pattern))

    @staticmethod
    def test_custom_orchid_directory():
        expected_directory = r'I:\diluvialis\Indus\Orchid'
        with unittest.mock.patch.multiple(pathlib.Path, exists=unittest.mock.MagicMock(return_value=True),
                                          open=unittest.mock.mock_open(read_data=f'directory: {expected_directory}')):
            assert_that(orchid.configuration.python_api()['directory'], equal_to(expected_directory))


if __name__ == '__main__':
    unittest.main()
