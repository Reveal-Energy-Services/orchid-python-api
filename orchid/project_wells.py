#  Copyright 2017-2020 Reveal Energy Services, Inc 
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

from typing import KeysView

import deal

from orchid.project_loader import ProjectLoader
import orchid.validation

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import (WellReferenceFrameXy, DepthDatum, IWell)

# noinspection PyUnresolvedReferences
import UnitsNet


def net_well_id(net_well: IWell) -> str:
    """
    Extract the "well ID" from a .NET `IWell` instance.

    Although this method is available "publicly," the author intends it to be "private" to this module.

    :param net_well:  The .NET IWell whose ID is sought.
    :return: The value used to identify this well.
    """

    # TODO: This method should be available from `IWell` instead of here.
    #  When that method / property is available, we **must** change this method.
    if net_well.Uwi and net_well.Uwi.strip():
        return net_well.Uwi.strip()

    if net_well.DisplayName and net_well.DisplayName.strip():
        return net_well.DisplayName.strip()

    if net_well.Name and net_well.Name.strip():
        return net_well.Name.strip()

    raise ValueError('No well ID available.')


class ProjectWells:
    """Provides a single class to access information about all wells in a project.

    In this role, this class has three responsibilities. First, it acts as a GOF Facade, providing a simpler
    interface than that provided by navigation through and interaction with the .NET DOM. Second, it adapts
    DOM interfaces to be more Pythonic. Finally, it acts as a "registry" providing a single instance for
    accessing wells of a project.
    """

    # TODO: I currently call this class a "Facade"; however, I open open to other suggestions.
    # This post on StackOverflow describes alternative names to "<Whatever>Manager":
    # https://stackoverflow.com/questions/1866794/naming-classes-how-to-avoid-calling-everything-a-whatevermanager

    @deal.pre(orchid.validation.arg_not_none)
    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting the .NET `IProject` available from project_loader.

        :param project_loader: Loads an `IProject` to be adapted.
        """
        self._project_loader = project_loader

        self._wells = {}

    def name(self):
        """
        Return the name of the project of interest.

        :return:  The name of this project.
        """
        return self._project_loader.native_project().Name

    def _well_map(self):
        if not self._wells:
            self._wells.update({net_well_id(w): w for w in self._project_loader.native_project().Wells.Items})
        return self._wells

    def well_ids(self) -> KeysView[str]:
        """
        Return sequence identifiers for all wells in this project.
        """
        return self._well_map().keys()

    def wells_by_name(self, well_name):
        """
        Return all wells with the name, well_name.
        :param well_name: The name of the well of interest
        """
        result = [w for w in self._well_map().values() if w.Name == well_name]
        return result

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def well_name(self, well_id: str):
        """
        Return the name of the specified well.

        :param well_id: The value identifying the well of interest.
        :return: The name of the well of interest.
        """
        return self._well_map()[well_id].Name

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def well_display_name(self, well_id: str):
        """
        Return the name of the specified well for displays.

        :param well_id: The value identifying the well of interest.
        :return: The name of the well of interest.
        """
        return self._well_map()[well_id].DisplayName

    def default_well_colors(self):
        return [tuple(map(lambda color_component: round(color_component * 255), color))
                for color in self._project_loader.native_project().PlottingSettings.GetDefaultWellColors()]
