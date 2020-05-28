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

from orchid.project_pressure_curves import ProjectPressureCurves
from orchid.project_loader import ProjectLoader
from orchid.project_wells import ProjectWells

# TODO: Replace some of this code with configuration and/or a method to use `clr.AddReference`
import sys
import clr
IMAGE_FRAC_ASSEMBLIES_DIR = r'c:/src/OrchidApp/ImageFrac/ImageFrac.Application/bin/Debug'
if IMAGE_FRAC_ASSEMBLIES_DIR not in sys.path:
    sys.path.append(IMAGE_FRAC_ASSEMBLIES_DIR)

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

    def unit(self, physical_quantity):
        """
        Return the abbreviation for the specified `physical_quantity` of this project.
        :param physical_quantity: The name of the physical quantity.
        :return: The abbreviation of the specified physical quantity.
        """
        def pressure_unit():
            return UnitsNet.Pressure.GetAbbreviation(self._project_loader.loaded_project().ProjectUnits.PressureUnit)

        def length_unit():
            return UnitsNet.Length.GetAbbreviation(self._project_loader.loaded_project().ProjectUnits.LengthUnit)

        quantity_function_map = {'pressure': pressure_unit,
                                 'length': length_unit}

        return quantity_function_map[physical_quantity]()
