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

import os.path
import sys
from typing import KeysView, List, Union
import uuid

import clr
import numpy as np
import vectormath as vmath

from image_frac.project_loader import ProjectLoader

IMAGE_FRAC_ASSEMBLIES_DIR = r'c:/src/ImageFracApp/ImageFrac/ImageFrac.Application/bin/x64/Debug'

sys.path.append(os.path.join(IMAGE_FRAC_ASSEMBLIES_DIR))
clr.AddReference('ImageFrac.FractureDiagnostics.SDKFacade')
# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics import (WellReferenceFrameXy, DepthDatum)

clr.AddReference('UnitsNet')
# noinspection PyUnresolvedReferences
import UnitsNet


class ProjectAdapter:
    """Adapts a .NET `IProject` to a Pythonic interface."""

    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting he project available from project_loader.

        :param project_loader: Loads an IProject to be adapted.
        """
        self._project_loader = project_loader

        self._wells = None

    def well_map(self):
        if not self._wells:
            self._wells = {uuid.uuid4(): w for w in self._project_loader.loaded_project().Wells.Items}
        return self._wells

    def trajectory_points(self, well_id: uuid.UUID) -> Union[vmath.Vector3Array, np.array]:
        """
        Return the subsurface points of the well bore of well_id in the specified reference frame and with depth datum.

        :param well_id: Identifies a specific well in the project.

        :return: A Vector3Array containing the trajectory (in project units using project reference frame and kelly
        bushing depth datum).
        """
        project = self._project_loader.loaded_project()
        well = self.well_map()[well_id]
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

    def well_ids(self) -> KeysView[uuid.UUID]:
        """
        Return sequence identifiers for all wells in this project.
        """
        return self.well_map().keys()

    def name(self):
        """
        Return the name of the project of interest.

        :return:  The name of this project.
        """
        return self._project_loader.loaded_project().Name

    def well_name(self, well_id: uuid.UUID):
        """
        Return the name of the specified well.

        :param well_id: The value identifying the well of interest.
        :return: The name of the well of interest.
        """
        return self.well_map()[well_id].Name

    def well_display_name(self, well_id: uuid.UUID):
        """
        Return the name of the specified well for displays.

        :param well_id: The value identifying the well of interest.
        :return: The name of the well of interest.
        """
        return self.well_map()[well_id].DisplayName

    def length_unit(self):
        project_length_unit = self._project_loader.loaded_project().ProjectUnits.LengthUnit
        result = UnitsNet.Length.GetAbbreviation(project_length_unit)
        return result

    def default_well_colors(self):
        return [tuple(map(lambda color_component: round(color_component * 255), color))
                for color in self._project_loader.loaded_project().PlottingSettings.GetDefaultWellColors()]


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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
