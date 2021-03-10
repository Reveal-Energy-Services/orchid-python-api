#  Copyright 2017-2021 Reveal Energy Services, Inc 
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
import sys

import orchid.configuration

import toolz.curried as toolz

# noinspection PyPackageRequirements
import clr
# noinspection PyUnresolvedReferences
from System import InvalidOperationException


def append_orchid_assemblies_directory_path() -> None:
    """
    Append the directory containing the required Orchid assemblies to `sys.path`.
    """
    orchid_bin_dir = toolz.get_in(['orchid', 'root'], orchid.configuration.python_api())
    if orchid_bin_dir not in sys.path:
        sys.path.append(orchid_bin_dir)


append_orchid_assemblies_directory_path()

clr.AddReference('Orchid.FractureDiagnostics.SDKFacade')
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import ScriptAdapter


class ScriptAdapterContext:
    """
    A "private" class with the responsibility to initialize and shutdown the .NET ScriptAdapter class.

    I considered making `ProjectLoader` a context manager; however, the API then becomes somewhat unclear.
    - Does the constructor enter the context? Must a caller initialize the instance and then enter the
      context?
    - What results if a caller *does not* enter the context?
    - Enters the context twice?

    Because I was uncertain I created this private class to model the `ScriptAdapter` context. The property,
    `ProjectLoader.native_project`, enters the context if it will actually read the project and exits the
    context when the read operation is finished.

    For information on Python context managers, see
    [the Python docs](https://docs.python.org/3.8/library/stdtypes.html#context-manager-types)
    """

    def __enter__(self):
        try:
            ScriptAdapter.Init()
            return self
        except InvalidOperationException as ioe:
            if 'REVEAL-CORE-0xDEADFA11' in ioe.Message:
                print('Orchid licensing error. Please contact Orchid technical support.')
                sys.exit(-1)
            else:
                raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        ScriptAdapter.Shutdown()
        # Returning no value will propagate the exception to the caller in the normal way
        return


def add_orchid_assemblies() -> None:
    """
    Add references to the Orchid assemblies needed by the Python API.

    Although not all modules in the `orchid` package need .NET types from all the available Orchid assemblies,
    I believe the additional cost of adding those references is far less than the cost of maintaining the
    copy-paste, boilerplate code that results without this common function.
    :return:
    """
    clr.AddReference('Orchid.FractureDiagnostics')
    clr.AddReference('Orchid.FractureDiagnostics.Factories')
    clr.AddReference('UnitsNet')
    return None


def app_settings_path() -> str:
    """
    Return the pathname of the `appSettings.json` file needed by the `SDKFacade `assembly.

    :return: The required pathname.
    """
    result = os.fspath(pathlib.Path(toolz.get_in(['orchid', 'root'],
                                                 orchid.configuration.python_api())).joinpath('appSettings.json'))
    return result


def prepare_imports() -> None:
    orchid.dot_net.append_orchid_assemblies_directory_path()

    # This function call must occur *after*
    # - Importing clr
    # - Adding a reference to `Orchid.FractureDiagnostics.SDKFacade`
    # - Importing ScriptAdapter from `Orchid.FractureDiagnostics.SDKFacade`
    # - The call to `append_orchid_assemblies_directory_path`
    with ScriptAdapterContext():
        orchid.dot_net.add_orchid_assemblies()
