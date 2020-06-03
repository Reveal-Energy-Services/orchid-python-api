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

import deal

import orchid.validation

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import ScriptAdapter
# noinspection PyUnresolvedReferences
from System.IO import (FileStream, FileMode, FileAccess, FileShare)


class OrchidError(Exception):
    pass


class ProjectLoader:
    """Provides an .NET IProject to be adapted."""

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def __init__(self, project_pathname: str):
        """
        Construct an instance that loads project data from project_pathname

        :param project_pathname: Identifies the data file for the project of interest.
        """
        self._project_pathname = project_pathname
        self._project = None
        self._in_context = False

    def loaded_project(self):
        """
        Return the loaded Orchid project.

        :return: The loaded `IProject`.

        :example:
            >>> # noinspection PyUnresolvedReferences
            >>> from project_loader import ProjectLoader
            >>> loader = ProjectLoader(r'c:/Users/larry.jones/tmp/ifa-test-data/Crane_II.ifrac')
            >>> loader.loaded_project().Name
            'Oasis_Crane_II'
        """
        if not self._project:
            with ScriptAdapterContext():
                reader = ScriptAdapter.CreateProjectFileReader(orchid.dot_net.app_settings_path())
                # TODO: These arguments are *copied* from `ProjectFileReaderWriterV2`
                stream_reader = FileStream(self._project_pathname, FileMode.Open, FileAccess.Read, FileShare.Read)
                try:
                    self._project = reader.Read(stream_reader)
                finally:
                    stream_reader.Close()
        return self._project


class ScriptAdapterContext:
    """
    A "private" class with the responsibility to initialize and shutdown the .NET ScriptAdapter class.

    I considered making `ProjectLoader` a context manager; however, the API then becomes somewhat unclear.
    - Does the constructor enter the context? Must a caller initialize the instance and then enter the
      context?
    - What results if a caller *does not* enter the context?
    - Enters the context twice?

    Because I was uncertain I created this private class to model the `ScriptAdapter` context. The property,
    `ProjectLoader.loaded_project`, enters the context if it will actually read the project and exits the
    context when the read operation is finished.

    For information on Python context managers, see
    [the Python docs](https://docs.python.org/3.7/library/stdtypes.html#context-manager-types)
    """

    def __enter__(self):
        ScriptAdapter.Init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ScriptAdapter.Shutdown()
        # Returning no value will propagate the exception to the caller in the normal way
        return


if __name__ == '__main__':
    import doctest
    doctest.testmod()
