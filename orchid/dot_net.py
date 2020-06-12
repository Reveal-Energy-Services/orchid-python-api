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
import sys

import orchid.configuration

import clr


def add_orchid_assemblies() -> None:
    """
    Add references to the Orchid assemblies needed by the Python API.

    Although not all modules in the `orchid` package need .NET types from all the available Orchid assemblies,
    I believe the additional cost of adding those references is far less than the cost of maintaining the
    copy-paste, boilerplate code that results without this common function.
    :return:
    """
    clr.AddReference('Orchid.FractureDiagnostics')
    clr.AddReference('Orchid.FractureDiagnostics.SDKFacade')
    clr.AddReference('UnitsNet')
    return None


def append_orchid_assemblies_directory_path() -> None:
    """
    Append the directory containing the required Orchid assemblies to `sys.path`.
    """
    orchid_bin_dir = orchid.configuration.python_api()['directory']
    if orchid_bin_dir not in sys.path:
        sys.path.append(orchid_bin_dir)


def app_settings_path() -> str:
    """
    Return the pathname of the `appSettings.json` file needed by the `SDKFacade `assembly.

    :return: The required pathname.
    """
    result = os.fspath(pathlib.Path(orchid.configuration.python_api()['directory']).joinpath('appSettings.json'))
    return result


def prepare_imports() -> None:
    orchid.dot_net.append_orchid_assemblies_directory_path()
    # This function call must occur *after* the call to `append_orchid_assemblies_directory_path`
    orchid.dot_net.add_orchid_assemblies()