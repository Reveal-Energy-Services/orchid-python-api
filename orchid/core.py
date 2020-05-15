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

import deal
import matplotlib.pyplot as plt
# The following import is included for its "side-effects" of an improved color schemes and plot styles.
# (See the "Tip" in section 9.2 of "Python for Data Analysis" for details.)
# noinspection PyUnresolvedReferences
import seaborn as sns

from orchid.project_adapter import ProjectAdapter
from orchid.project_loader import ProjectLoader


@deal.pre(lambda ifrac_pathname: ifrac_pathname is not None)
@deal.pre(lambda ifrac_pathname: len(ifrac_pathname) != 0)
@deal.pre(lambda ifrac_pathname: len(ifrac_pathname.strip()) != 0)
def load_project(ifrac_pathname: str) -> ProjectAdapter:
    """
    Return the project for the specified `.ifrac` file.

    :param ifrac_pathname: The path identifying the data file of the project of interest.
    :return: The project of interest.
    """

    loader = ProjectLoader(ifrac_pathname.strip())
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
    project = load_project(ifrac_pathname)
    default_well_colors = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in project.default_well_colors()]
    well_ids = list(project.well_ids())
    trajectories = [project.trajectory_points(well_id) for well_id in well_ids]
    for i in range(len(well_ids)):
        plt.plot([p.x for p in trajectories[i]], [p.y for p in trajectories[i]],
                 label=f'{project.well_display_name(well_ids[i])}',
                 color=default_well_colors[i % len(default_well_colors)])
    plt.title(f'{project.name()} Well Trajectories (Project Coordinates)')
    plt.legend(loc='best')
    plt.xlabel(f'Easting ({project.length_unit()})')
    plt.ylabel(f'Northing ({project.length_unit()})')

    plt.show()
