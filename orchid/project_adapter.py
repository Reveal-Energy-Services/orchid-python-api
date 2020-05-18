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

from typing import List

import clr
import deal
import numpy as np

from orchid.project_loader import ProjectLoader

clr.AddReference('UnitsNet')
# noinspection PyUnresolvedReferences
import UnitsNet


class ProjectAdapter:
    """Adapts a .NET `IProject` to a Pythonic interface."""

    @deal.pre(lambda self, project_loader: project_loader is not None)
    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting he project available from project_loader.

        :param project_loader: Loads an IProject to be adapted.
        """
        self._project_loader = project_loader

    def name(self):
        """
        Return the name of the project of interest.

        :return:  The name of this project.
        """
        return self._project_loader.loaded_project().Name

    def length_unit(self):
        project_length_unit = self._project_loader.loaded_project().ProjectUnits.LengthUnit
        result = UnitsNet.Length.GetAbbreviation(project_length_unit)
        return result
