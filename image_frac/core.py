# -*- coding: utf-8 -*-

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

from image_frac.project_adapter import ProjectAdapter
from image_frac.project_loader import ProjectLoader


def load_project(ifrac_pathname: str) -> ProjectAdapter:
    """
    Return the project for the specified `.ifrac` file.

    :param ifrac_pathname: The path identifying the data file of the project of interest.
    :return: The project of interest.
    """

    loader = ProjectLoader(ifrac_pathname)
    result = ProjectAdapter(loader)
    return result


# TODO: Add **kwargs eventually?
# Although the original proposal included kwargs to control the plotting, I do not know what those arguments
# might actually be right now so I have not included the argument. Adding this argument is low-cost.
def plot_trajectories(ifrac_pathname: str) -> None:
    """
    Plot the trajectories for all the wells in the project of interest.

    :param ifrac_pathname: The path identifying the data file of the project of interest.
    :return: None
    """
    return
