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

import clr
import os
import sys

sys.path.append(os.path.join(r'c:/src/ImageFracApp/ImageFrac/ImageFrac.FractureDiagnostics.SDKFacade/bin/Debug/net48'))
clr.AddReference('ImageFrac.FractureDiagnostics.SDKFacade')
# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics.SDKFacade import ScriptAdapter
# noinspection PyUnresolvedReferences
from System import TimeZoneInfo


class ProjectLoader:
    """Provides an .NET IProject to be adapted."""

    def __init__(self, project_pathname: str):
        """
        Construct an instance that loads project data from project_pathname

        :param project_pathname: Identifies the data file for the project of interest.
        """
        self._project_pathname = project_pathname
        self._project = None

    @property
    def loaded_project(self):
        """
        Return the loaded ImageFrac4 project.

        :return: The loaded `IProject`.

        :example:
            >>> from project_loader import ProjectLoader
            >>> loader = ProjectLoader(r'c:/Users/larry.jones/tmp/ifa-test-data/Crane_II.ifrac')
            >>> loader.loaded_project.Name
            'Oasis_Crane_II'
        """
        if not self._project:
            reader = ScriptAdapter.CreateProjectFileReader()
            self._project = reader.Read(self._project_pathname, TimeZoneInfo.Utc, False)
        return self._project


if __name__ == '__main__':
    import doctest
    doctest.testmod()
