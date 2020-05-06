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
from typing import KeysView

import vectormath as vmath

from .project_loader import ProjectLoader


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
        """
        pass

    def well_ids(self) -> KeysView[uuid.UUID]:
        """
        Return sequence identifiers for all wells in this project.
        """
        return self.well_map().keys()
