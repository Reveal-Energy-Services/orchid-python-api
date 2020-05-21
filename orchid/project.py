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
import deal

from orchid.pressure_curve import ProjectPressureCurves
from orchid.project_loader import ProjectLoader
from orchid.project_wells import ProjectWells

clr.AddReference('UnitsNet')
# noinspection PyUnresolvedReferences
import UnitsNet


class ProjectAdapter:
    """Adapts a .NET `IProject` to a Pythonic interface."""

    @deal.pre(lambda self, project_loader: project_loader is not None)
    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting he project available from net_project.

        :param project_loader: Loads an IProject to be adapted.
        """
        self._project_loader = project_loader

    def all_pressure_curves(self):
        """
        Return a container of pressure curves indexed by time series id.
        :return: The container of pressure curves.
        """
        result = ProjectPressureCurves(self._project_loader)
        return result

    def all_wells(self):
        """
        Return an object managing all wells from this project.

        :return: The object managing all wells for this project.
        """
        result = ProjectWells(self._project_loader)
        return result

    def name(self):
        """
        Return the name of the project of interest.

        :return:  The name of this project.
        """
        return self._project_loader.loaded_project().Name

    # TODO: On third unit, change to single implementation perhaps using a dictionary
    def length_unit(self):
        """
        Return the length unit for the project.
        :return: The length unit for the project.
        """
        project_length_unit = self._project_loader.loaded_project().ProjectUnits.LengthUnit
        result = UnitsNet.Length.GetAbbreviation(project_length_unit)
        return result

    def pressure_unit(self):
        """
        Return the pressure unit for the project.
        :return: The pressure unit for the project.
        """
        project_pressure_unit = self._project_loader.loaded_project().ProjectUnits.PressureUnit
        result = UnitsNet.Pressure.GetAbbreviation(project_pressure_unit)
        return result
