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

import argparse
from typing import Mapping
import uuid

import numpy
import dateutil.tz

import image_frac.trajectory_coordinator as trajectory_coordinator


def plot_trajectories(trajectory_points:  Mapping[uuid.UUID, numpy.ndarray]):
    """
    :param trajectory_points: The mapping between wells and trajectories to be plotted.
    """
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pathname', help="Path name of the IMAGEFrac project file ('.ifrac').")

    options = parser.parse_args()
    project = trajectory_coordinator.build_project(options.pathname, dateutil.tz.UTC)
    trajectories_for_wells = {well_id:  project.trajectory_points(well_id, 'project', 'kelly_bushing')
                              for well_id in project.well_ids()}
    plot_trajectories(trajectories_for_wells)
