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
from typing import Sequence

import vectormath as vmath


class ProjectAdapter:
    """Adapts a .NET `IProject` to a Pythonic interface."""

    def trajectory_points(self, well_id: uuid.UUID) -> vmath.Vector3Array:
        """
        Return the subsurface points of the well bore of well_id in the specified reference frame and with depth datum.

        :param well_id: Identifies a specific well in the project.
        """
        pass

    def well_ids(self) -> Sequence[uuid.UUID]:
        """
        Return sequence identifiers for all wells in this project.
        """
        return []
