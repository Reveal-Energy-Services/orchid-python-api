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

from typing import KeysView, List, Union

import deal
import more_itertools
import numpy as np
import pandas as pd
import vectormath as vmath

from orchid.project_loader import ProjectLoader
import orchid.time_series
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

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def trajectory_points(self, well_id: str) -> Union[vmath.Vector3Array, np.array]:
        """
        Return the subsurface points of the well bore of well_id in the specified reference frame and with depth datum.

        :param well_id: Identifies a specific well in the project.

        :return: A Vector3Array containing the trajectory (in project units using project reference frame and kelly
        bushing depth datum).
        """
        project = self._project_loader.native_project()
        well = self._well_map()[well_id]
        trajectory = well.Trajectory
        eastings = self._coordinates_to_array(trajectory.GetEastingArray(WellReferenceFrameXy.Project),
                                              project.ProjectUnits.LengthUnit)
        northings = self._coordinates_to_array(trajectory.GetNorthingArray(WellReferenceFrameXy.Project),
                                               project.ProjectUnits.LengthUnit)
        tvds = self._coordinates_to_array(trajectory.GetTvdArray(WellReferenceFrameXy.Project),
                                          project.ProjectUnits.LengthUnit)

        if _all_coordinates_available(eastings, northings, tvds):
            # The following code "zips" three arrays into a triple. See the StackOverflow post,
            # https://stackoverflow.com/questions/26193386/numpy-zip-function
            points = np.vstack([eastings, northings, tvds]).T
            result = vmath.Vector3Array(points)
            return result
        else:
            return np.empty((0,))

    @deal.pre(lambda _, well_name, stage_no: well_name is not None)
    @deal.pre(lambda _, well_name, stage_no: len(well_name.strip()) > 0)
    @deal.pre(lambda _, well_name, stage_no: stage_no > 0)
    def treatment_curves(self, well_name: str, stage_no: int) -> pd.DataFrame:
        """
        Extract the treatment curves for the well and stage number of interest.

        :param well_name: The name identifying the well of interest.
        :param stage_no: The number of the stage of interest.
        :return: The treatment curves as a pandas `DataFrame` indexed by a (time) `Series`.
        """
        candidate_wells = self.wells_by_name(well_name)
        if len(candidate_wells) != 1:
            raise ValueError(f'Found {len(candidate_wells)} wells with name, "{well_name}". Expected 1.')

        well_of_interest = more_itertools.one(candidate_wells)
        candidate_stages = list(filter(lambda s: s.DisplayStageNumber == stage_no, well_of_interest.Stages.Items))
        if len(candidate_stages) == 0:
            raise ValueError(f'Found {len(candidate_stages)} stages with stage number, {stage_no}, in well,'
                             f' "{well_name}". Expected 1.')
        stage_of_interest = more_itertools.one(candidate_stages)
        net_treatment_curves = stage_of_interest.TreatmentCurves.Items
        result = orchid.time_series.deprecated_transform_net_treatment(net_treatment_curves)
        return result

    @staticmethod
    def _coordinates_to_array(coordinates: List[UnitsNet.Length],
                              project_length_unit: UnitsNet.Units.LengthUnit) -> np.array:
        """
        Transform a project "coordinate" (easting, northing or tvd) list into a numpy array.
        :param coordinates: The coordinates (eastings, northings or tvds) to transform.
        :param project_length_unit: The project using these coordinators.
        :return: The numpy array equivalent to these coordinates.
        """
        return np.array([e.As(project_length_unit) for e in coordinates])

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


def _all_coordinates_available(eastings: np.array, northings: np.array, tvds: np.array) -> bool:
    """
    Are all coordinates available; that is, does each coordinate array have at least one element

    Although available in some import scenarios, the author intends this function to be private to this module.

    :param eastings: The numpy array of eastings
    :param northings: The numpy array of northings
    :param tvds: The numpy array of total vertical depths (TVD's)
    :return: True if each coordinate array has at least one item; otherwise, false.
    """

    # I had originally coded the following as `if eastings and northings and tvds`; however, PyCharm
    # warned that using an empty numpy array in a boolean context was "ambiguous" and would, in the
    # future, be flagged as an error.
    result = eastings.size > 0 and northings.size > 0 and tvds.size > 0
    return result
