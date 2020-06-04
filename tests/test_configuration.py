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

import os.path
import unittest.mock

from hamcrest import assert_that, equal_to

import orchid.configuration


class ConfigurationTest(unittest.TestCase):
    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch.dict('os.environ', {'LOCALAPPDATA': os.path.join('K:', os.sep, 'dolavi')})
    @unittest.mock.patch.object(os.path, 'exists', return_value=False)
    def test_default_orchid_directory(self, _):
        expected_directory = os.path.join('K:', os.sep, 'dolavi', 'Reveal')
        assert_that(orchid.configuration.python_api()['directory'], equal_to(expected_directory))

    @unittest.mock.patch.dict('os.environ', {'LOCALAPPDATA': os.path.join('K:', os.sep, 'dolavi')})
    @unittest.mock.patch.object(os.path, 'exists', return_value=True)
    def test_custom_orchid_directory(self, _):
        expected_directory = r'I:\diluvialis\Indus\Orchid'
        with unittest.mock.patch('orchid.configuration.open',
                                 unittest.mock.mock_open(read_data=f'directory: {expected_directory}')):
            assert_that(orchid.configuration.python_api()['directory'], equal_to(expected_directory))


if __name__ == '__main__':
    unittest.main()
