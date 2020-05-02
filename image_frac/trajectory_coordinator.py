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

import datetime
import uuid
from typing import Mapping

import vectormath as vmath

from .project_adapter import ProjectAdapter


class TrajectoryCoordinator:
    """Provides services to support using trajectories."""

    def __init__(self, pathname: str, timezone: datetime.tzinfo):
        """
        Initializes an instance for the project whose data is in pathname with the specified time zone

        :param pathname: Identifies the data file for the project of interest.
        :param timezone: The timezone for the project of interest.
        """
        self._pathname = pathname
        self._project_timezone = timezone
        self._project = None

    def trajectories_for_all_wells(self, reference_frame_xy: str, depth_datum: str) -> Mapping[uuid.UUID,
                                                                                               vmath.Vector3Array]:
        result = {well_id: self._get_project().trajectory_points(well_id, reference_frame_xy, depth_datum)
                  for well_id in self._get_project().well_ids()}
        return result

    def _get_project(self) -> ProjectAdapter:
        """
        Returns the ProjectAdapter wrapping the project of interest.

        This function is a self-initializing function; that is, if _project has not yet been initialized,
        it will initialize it.
        """
        if not self._project:
            self._project = ProjectAdapter()
        return self._project
