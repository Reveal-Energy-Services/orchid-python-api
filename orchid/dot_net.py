#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#


import os
import sys
import orchid.configuration


def append_bin_path():
    orchid_bin_dir = orchid.configuration.python_api()['directory']
    if orchid_bin_dir not in sys.path:
        sys.path.append(orchid_bin_dir)


def app_settings_path():
    """
    Return the pathname of the `appSettings.json` file needed by the `SDKFacade `assembly.

    :return: The required pathname.
    """
    result = os.path.join(orchid.configuration.python_api()['directory'], 'appSettings.json')
    return result
