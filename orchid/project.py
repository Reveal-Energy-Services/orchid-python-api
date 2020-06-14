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

from typing import List, Tuple, Iterable

import deal

from orchid.native_well_adapter import NativeWellAdapter
from orchid.project_loader import ProjectLoader
from orchid.project_monitor_pressure_curves import ProjectMonitorPressureCurves
import orchid.project_units as project_units
from orchid.project_wells import ProjectWells

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell
# noinspection PyUnresolvedReferences
import UnitsNet


class Project:
    """Adapts a .NET `IProject` to a Pythonic interface."""

    @deal.pre(lambda self, project_loader: project_loader is not None)
    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting he project available from net_project.

        :param project_loader: Loads an IProject to be adapted.
        """
        self._project_loader = project_loader
        self._are_well_loaded = False
        self._wells = []

    def all_wells(self):
        """
        Return an object managing all wells from this project.

        :return: The object managing all wells for this project.
        """
        result = ProjectWells(self._project_loader)
        return result

    def default_well_colors(self) -> List[Tuple[float, float, float]]:
        """
        Calculate the default well colors for this project.
        :return: A list of RGB tuples.
        """
        result = list(map(tuple, self._project_loader.native_project().PlottingSettings.GetDefaultWellColors()))
        return result

    def monitor_pressure_curves(self):
        """
        Return a container of pressure curves indexed by time series id.
        :return: The container of pressure curves.
        """
        result = ProjectMonitorPressureCurves(self._project_loader)
        return result

    def name(self):
        """
        Return the name of the project of interest.

        :return:  The name of this project.
        """
        return self._project_loader.native_project().Name

    def unit(self, physical_quantity):
        """
        Return the abbreviation for the specified `physical_quantity` of this project.
        :param physical_quantity: The name of the physical quantity.
        :return: The abbreviation of the specified physical quantity.
        """
        return project_units.unit(self._project_loader.native_project(), physical_quantity)

    def wells(self) -> Iterable[IWell]:
        """
        Return all the wells in this project.
        :return: A list of all the wells in this project.
        """
        return map(NativeWellAdapter, self._project_loader.native_project().Wells.Items)

    def wells_by_name(self, name) -> Iterable[IWell]:
        """
        Return all the wells in this project with the specified name.
        :param name: The name of the well(s) of interest.
        :return: A list of all the wells in this project.
        """
        return [w for w in list(map(NativeWellAdapter, self._project_loader.native_project().Wells.Items)) if
                name == w.name()]
