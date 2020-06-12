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
import unittest.mock

from hamcrest import assert_that, equal_to

import orchid.configuration


class ConfigurationTest(unittest.TestCase):
    APP_DATA_PATH = pathlib.Path('K:').joinpath(os.sep, 'dolavi')

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch.dict('os.environ', {'LOCALAPPDATA': os.fspath(APP_DATA_PATH)})
    @unittest.mock.patch.object(pathlib.Path, 'exists', return_value=False)
    def test_default_orchid_directory(self, _):
        expected_directory = ConfigurationTest.APP_DATA_PATH.joinpath('Reveal')
        assert_that(orchid.configuration.python_api()['directory'], equal_to(expected_directory))

    @staticmethod
    def test_custom_orchid_directory():
        expected_directory = r'I:\diluvialis\Indus\Orchid'
        with unittest.mock.patch.multiple(pathlib.Path, exists=unittest.mock.MagicMock(return_value=True),
                                          open=unittest.mock.mock_open(read_data=f'directory: {expected_directory}')):
            assert_that(orchid.configuration.python_api()['directory'], equal_to(expected_directory))


if __name__ == '__main__':
    unittest.main()