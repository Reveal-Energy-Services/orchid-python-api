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
import os

import image_frac


def build_project(pathname: os.PathLike, timezone: datetime.tzinfo) -> image_frac.ProjectAdapter:
    """
    Returns the ProjectAdapter for the project whose data is in pathname

    :param pathname: Identifies the data file for the project of interest.
    :param timezone: The timezone for the project of interest.
    """
    result = image_frac.ProjectAdapter()
    return result
