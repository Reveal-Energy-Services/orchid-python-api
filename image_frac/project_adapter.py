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
from typing import KeysView
import uuid

import clr
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

    def trajectory_points(self, well_id: uuid.UUID) -> vmath.Vector3Array:
        """
        Return the subsurface points of the well bore of well_id in the specified reference frame and with depth datum.

        :param well_id: Identifies a specific well in the project.

        :return: A Vector3Array containing the trajectory (in project units using project reference frame and kelly
        bushing depth datum).

        :example:
            >>> # noinspection PyUnresolvedReferences
            >>> from project_loader import ProjectLoader
            >>> loader = ProjectLoader(r'c:/Users/larry.jones/tmp/ifa-test-data/Crane_II.ifrac')
            >>> project = ProjectAdapter(loader)
            >>> trajectory_points = [project.trajectory_points(well_id) for well_id in project.well_ids()]
            >>> len(trajectory_points)
            4
            >>> # noinspection PyTypeChecker
            >>> [len(points) for points in trajectory_points]
            [253, 246, 234, 257]
            >>> # Initial point of trajectories
            >>> # noinspection PyUnresolvedReferences
            >>> [trajectory_points[i][0] for i in range(4)]
            [Vector3([0.064, 0.56 , 0.   ]), Vector3([-22.902, -65.06 ,   0.   ]), Vector3([ 954.788, -803.25 ,    0.   ]), Vector3([ -50.166, -156.69 ,    0.   ])]
            >>> # Middle point of trajectories
            >>> # noinspection PyUnresolvedReferences
            >>> [trajectory_points[i][len(trajectory_points[i]) // 2] for i in range(4)]
            [Vector3([  262.64215124,  1297.3048967 , 10481.01160463]), Vector3([  242.37977858,   596.4535276 , 10573.78645779]), Vector3([  467.07593939,  -464.9789044 , 10767.02602787]), Vector3([  112.08522272, -1020.3832704 , 10625.70516618])]
            >>> # Last point of trajectories
            >>> # noinspection PyUnresolvedReferences
            >>> [trajectory_points[i][-1] for i in range(4)]
            [Vector3([-10015.68480859,   1330.8487571 ,  10705.24099079]), Vector3([-10029.48342696,    556.742598  ,  10712.00210724]), Vector3([-9854.81599078,   -71.6013143 , 10727.50321322]), Vector3([-10046.00226103,   -911.7090451 ,  10716.0042386 ])]
        """
        project = self._project_loader.loaded_project()
        well = self.well_map()[well_id]
        trajectory = well.Trajectory
        eastings = [e.As(project.ProjectUnits.LengthUnit)
                    for e in trajectory.GetEastingArray(WellReferenceFrameXy.Project)]
        northings = [n.As(project.ProjectUnits.LengthUnit)
                     for n in trajectory.GetNorthingArray(WellReferenceFrameXy.Project)]
        tvds = [tvd.As(project.ProjectUnits.LengthUnit)
                for tvd in trajectory.GetTvdArray(DepthDatum.KellyBushing)]
        points = map(lambda x, y, z: vmath.Vector3(x, y, z), eastings, northings, tvds)
        result = vmath.Vector3Array(list(points))
        return result

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

    def well_name(self, well_id : uuid.UUID):
        """
        Return the name of the specified well.

        :param well_id: The value identifying the well of interest.
        :return: The name of the well of interest.
        """
        return self.well_map()[well_id].Name

    def well_display_name(self, well_id : uuid.UUID):
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
