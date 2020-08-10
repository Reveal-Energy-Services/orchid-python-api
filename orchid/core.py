# -*- coding: utf-8 -*-

#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

from typing import Tuple

import deal
import numpy as np
import matplotlib.axes
import matplotlib.pyplot as plt
import pandas as pd
# The following import is included for its "side-effects" of an improved color schemes and plot styles.
# (See the "Tip" in section 9.2 of "Python for Data Analysis" for details.)
# noinspection PyUnresolvedReferences
import seaborn as sns

from orchid.project import Project
from orchid.project_loader import ProjectLoader


@deal.pre(lambda ifrac_pathname: ifrac_pathname is not None)
@deal.pre(lambda ifrac_pathname: len(ifrac_pathname) != 0)
@deal.pre(lambda ifrac_pathname: len(ifrac_pathname.strip()) != 0)
def load_project(ifrac_pathname: str) -> Project:
    """
    Return the project for the specified `.ifrac` file.

    :param ifrac_pathname: The path identifying the data file of the project of interest.
    :return: The project of interest.
    """

    loader = ProjectLoader(ifrac_pathname.strip())
    result = Project(loader)
    return result


# TODO: Add **kwargs eventually?
# Although the original proposal included kwargs to control the plotting, I do not know what those arguments
# might actually be right now so I have not included the argument. Adding this argument is low-cost.
def plot_monitor_pressures(ifrac_pathname: str) -> None:
    """
    Plot all the the surface pressure curves for the project of interest.

    :param ifrac_pathname: The path identifying the data file of the project of interest.
    :return: None
    """
    project = load_project(ifrac_pathname)
    project_wells = project.all_wells()
    default_well_colors = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in project_wells.default_well_colors()]
    monitor_pressure_curves = project.monitor_pressure_curves()
    monitor_pressure_curve_ids = monitor_pressure_curves.monitor_pressure_curve_ids()
    monitor_pressure_curve_display_names = [monitor_pressure_curves.display_name(curve_id)
                                            for curve_id in monitor_pressure_curve_ids]
    surface_pressure_curves = [monitor_pressure_curves.monitor_pressure_curve_time_series(pressure_curve_id)
                               for pressure_curve_id in monitor_pressure_curve_ids]

    # TODO: Remove hard-coding
    curves_shape = (2, 2)
    max_curve_count = curves_shape[0] * curves_shape[1]
    figure, axes = plt.subplots(*curves_shape)
    curves_to_plot = np.reshape(surface_pressure_curves[:max_curve_count], curves_shape)
    names_to_display = np.reshape(monitor_pressure_curve_display_names[:max_curve_count], curves_shape)
    # TODO: Do we need a better way to map colors to curves?
    # The following code assumes that the colors on the trajectories for each well will be identical to the
    # colors for the curves. I do not know of any guarantee that the order of curves in the time series is
    # the same order as the pressure curves. :(
    colors_to_use = np.reshape(default_well_colors[:4], (2, 2))
    for i in range(len(axes)):
        for j in range(len(axes[0])):
            series_to_plot = curves_to_plot[i, j]
            series_name = names_to_display[i, j]
            pressure_unit_abbreviation = project.unit('pressure')
            ax = axes[i, j]
            colors = colors_to_use[i, j]

            plot_monitor_pressure_curve(series_to_plot, ax, colors, pressure_unit_abbreviation, series_name)

    plt.show()


def plot_monitor_pressure_curve(series_to_plot: pd.Series, axes: matplotlib.axes.Axes,
                                series_color: Tuple[int, int, int], pressure_unit_abbreviation: str,
                                series_name: str) -> None:
    """
    Plot the specified time series using the supplied details
    :param series_to_plot:  The (pandas) time series to plot.
    :param axes: The matplotlib.axes.Axes on which to plot the curve.
    :param series_color: The color of the curve to plot (an RGB tuple)
    :param pressure_unit_abbreviation: The abbreviation of the (project) pressure unit.
    :param series_name: The name of the series to plot.
    :return: None
    """
    series_to_plot.plot(ax=axes, color=series_color)
    axes.set_ylabel(f'Pressure ({pressure_unit_abbreviation})')
    axes.title.set_text(series_name)
    x_tick_labels = axes.get_xticklabels()
    plt.setp(x_tick_labels, rotation=30)
