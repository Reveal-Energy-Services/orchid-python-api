#  Copyright 2017-2021 Reveal Energy Services, Inc 
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

from collections import namedtuple
from typing import Dict, Iterable, List, Mapping, Tuple
import uuid

import deal
import option
import toolz.curried as toolz

from orchid import (
    dot_net_dom_access as dna,
    native_data_frame_adapter as dfa,
    native_monitor_adapter as nma,
    native_monitor_curve_adapter as mca,
    native_well_adapter as nwa,
    net_quantity as onq,
    unit_system as units,
)
from orchid.project_loader import ProjectLoader

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell, UnitSystem
# noinspection PyUnresolvedReferences
import UnitsNet


ProjectBounds = namedtuple('ProjectBounds', [
    'min_x', 'max_x',
    'min_y', 'max_y',
    'min_depth', 'max_depth',
])
SurfacePoint = namedtuple('SurfacePoint', ['x', 'y'])


class Project(dna.DotNetAdapter):
    """Adapts a .NET `IProject` to a Pythonic interface."""

    @deal.pre(lambda self, project_loader: project_loader is not None)
    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting he project available from net_project.

        :param project_loader: Loads an IProject to be adapted.
        """
        super().__init__(project_loader.native_project())
        self._project_loader = project_loader
        self._are_well_loaded = False
        self._wells = []

    azimuth = dna.transformed_dom_property('azimuth', 'The azimuth of the project.', onq.as_angle_measurement)
    name = dna.dom_property('name', 'The name of this project.')
    project_units = dna.transformed_dom_property('project_units', 'The project unit system.', units.as_unit_system)
    wells = dna.transformed_dom_property_iterator('wells', 'An iterator of all the wells in this project.',
                                                  nwa.NativeWellAdapter)

    @property
    def fluid_density(self):
        """The fluid density of the project in project units."""
        return onq.as_measurement(self.project_units.DENSITY, self.dom_object.FluidDensity)

    def default_well_colors(self) -> List[Tuple[float, float, float]]:
        """
        Calculate the default well colors for this project.
        :return: A list of RGB tuples.
        """
        result = list(map(tuple, self._project_loader.native_project().PlottingSettings.GetDefaultWellColors()))
        return result

    def all_data_frames(self) -> Iterable[dfa.NativeDataFrameAdapter]:
        """
        Return a sequence of data frames for this project.

        Returns:
            An iterable of data frames.
        """
        result = self.all_data_frames_by_object_ids().values()
        return result

    def all_data_frames_by_object_ids(self) -> Mapping[uuid.UUID, dfa.NativeDataFrameAdapter]:
        """
        Return a mapping between object IDs and data frames.

        Returns:
            The mapping between the data frames of this project and their object IDs.

        """
        def by_id(so_far, df):
            return toolz.assoc(so_far, df.object_id, df)

        result = toolz.pipe(
            self._project_loader.native_project().DataFrames.Items,
            toolz.map(lambda net_df: dfa.NativeDataFrameAdapter(net_df)),
            lambda dfs: toolz.reduce(by_id, dfs, {}),
        )
        return result

    def data_frame(self, id_to_match: uuid.UUID) -> option.Option[dfa.NativeDataFrameAdapter]:
        """
        Return the single data frame from this project identified by `id_to_match`.
        Args:
            id_to_match: The `uuid.UUID` sought.

        Returns:
            `option.Some`(data frame) if one match; otherwise, `option.NONE`.
        """
        candidates = list(toolz.filter(lambda df: df.object_id == id_to_match, self.all_data_frames()))
        assert len(candidates) <= 1, f'More than 1 data frame with object ID, {id_to_match}.'
        return option.maybe(candidates[0] if len(candidates) == 1 else None)

    # TODO: Extract common code into private method
    def find_data_frames_with_display_name(self, data_frame_display_name: str) -> Iterable[dfa.NativeDataFrameAdapter]:
        """
        Return all project data frames with `display_name`, `data_frame_name`.

        Args:
            data_frame_display_name: The display name of the data frame sought.
        """
        result = toolz.pipe(
            self.all_data_frames_by_object_ids(),
            toolz.valfilter(lambda df: df.display_name == data_frame_display_name),
            lambda dfs: dfs.values(),
        )
        return result

    def find_data_frames_with_name(self, data_frame_name: str) -> Iterable[dfa.NativeDataFrameAdapter]:
        """
        Return all project data frames named `data_frame_name`.

        Args:
            data_frame_name: The name of the data frame sought.
        """
        result = toolz.pipe(
            self.all_data_frames_by_object_ids(),
            toolz.valfilter(lambda df: df.name == data_frame_name),
            lambda dfs: dfs.values(),
        )
        return result

    def monitor_curves(self) -> Iterable[mca.NativeMonitorCurveAdapter]:

        """
        Return a sequence of well time series for this project.

        Returns:
            An iterable of well time series.
        """
        native_time_series_list_items = self._project_loader.native_project().WellTimeSeriesList.Items
        if len(native_time_series_list_items) > 0:
            return toolz.pipe(native_time_series_list_items,
                              toolz.map(mca.NativeMonitorCurveAdapter),
                              list)
        else:
            return []

    def monitors(self) -> Dict[str, nma.NativeMonitorAdapter]:
        """
        Return a dictionary of monitors for this project indexed by the monitor display name.

        Returns:
            An dictionary of `NativeMonitorAdapter`s indexed by the display name of each monitor.
        """
        def collect_monitors(so_far, monitor):
            return toolz.assoc(so_far, monitor.DisplayName, monitor)

        result = toolz.pipe(self._project_loader.native_project().Monitors.Items,
                            lambda ms: toolz.reduce(collect_monitors, ms, {}),
                            toolz.valmap(lambda m: nma.NativeMonitorAdapter(m)))
        return result

    def project_bounds(self) -> ProjectBounds:
        result = toolz.pipe(self.dom_object.GetProjectBounds(),
                            toolz.map(onq.as_measurement(self.project_units.LENGTH)),
                            list,
                            lambda ls: ProjectBounds(*ls))
        return result

    def project_center(self) -> SurfacePoint:
        """
        Return the location of the project center on the surface measured in project units.
        """
        net_center = self.dom_object.GetProjectCenter()
        result = toolz.pipe(net_center,
                            toolz.map(onq.as_measurement(self.project_units.LENGTH)),
                            list,
                            lambda ls: SurfacePoint(ls[0], ls[1]))
        return result

    def proppant_concentration_mass_unit(self):
        if self.project_units == units.UsOilfield:
            return units.UsOilfield.MASS
        elif self.project_units == units.Metric:
            return units.Metric.MASS
        else:
            raise ValueError(f'Unknown unit system: {self.project_units}')

    def slurry_rate_volume_unit(self):
        if self.project_units == units.UsOilfield:
            return units.UsOilfield.VOLUME
        elif self.project_units == units.Metric:
            return units.Metric.VOLUME
        else:
            raise ValueError(f'Unknown unit system: {self.project_units}')

    def wells_by_name(self, name) -> Iterable[IWell]:
        """
        Return all the wells in this project with the specified name.
        :param name: The name of the well(s) of interest.
        :return: A list of all the wells in this project.
        """
        return toolz.filter(lambda w: name == w.name, self.wells)
