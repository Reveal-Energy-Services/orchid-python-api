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

import uuid
from typing import Mapping

import deal
import vectormath as vmath

from .project_adapter import ProjectAdapter
from .project_loader import ProjectLoader


class TrajectoryCoordinator:
    """Provides services to support using trajectories."""

    @deal.pre(lambda self, pathname: pathname is not None)
    @deal.pre(lambda self, pathname: len(pathname.strip()) != 0)
    def __init__(self, project_pathname: str):
        """
        Initializes an instance for the project whose data is in pathname with the specified time zone

        :param project_pathname: Identifies the data file for the project of interest.
        """
        self._project_provider = ProjectLoader(project_pathname)
        self._project = None

    @property
    def _project_adapter(self):
        if not self._project:
            self._project = ProjectAdapter(self._project_provider)
        return self._project

    def trajectories_for_all_wells(self) -> Mapping[uuid.UUID, vmath.Vector3Array]:
        result = {well_id: self._project_adapter.trajectory_points(well_id)
                  for well_id in self._project_adapter.well_ids()}
        return result
