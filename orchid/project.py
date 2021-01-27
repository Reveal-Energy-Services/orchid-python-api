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
from typing import List, Tuple, Iterable

import deal
import toolz.curried as toolz

from orchid import (
    dot_net_dom_access as dna,
    measurement as om,
    native_well_adapter as nwa,
    native_monitor_curve_adapter as mca,
    net_quantity as onq,
    unit_system as units,
)
from orchid.project_loader import ProjectLoader

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell, UnitSystem
# noinspection PyUnresolvedReferences
import UnitsNet

from orchid.unit_system import as_unit_system


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
    project_units = dna.transformed_dom_property('project_units', 'The project unit system.', as_unit_system)
    wells = dna.transformed_dom_property_iterator('wells', 'An iterator of all the wells in this project.',
                                                  nwa.NativeWellAdapter)

    @property
    def fluid_density(self):
        """The fluid density of the project in project units."""
        return onq.as_measurement(self.project_units.DENSITY, self._adaptee.FluidDensity)

    def default_well_colors(self) -> List[Tuple[float, float, float]]:
        """
        Calculate the default well colors for this project.
        :return: A list of RGB tuples.
        """
        result = list(map(tuple, self._project_loader.native_project().PlottingSettings.GetDefaultWellColors()))
        return result

    def monitor_curves(self) -> Iterable[mca.NativeMonitorCurveAdapter]:
        """
            Return a sequence of well time series for this project.
        Returns:
            An iterable of well time series.
        """
        native_time_series_list_items = self._project_loader.native_project().WellTimeSeriesList.Items
        if len(native_time_series_list_items) > 0:
            return toolz.map(mca.NativeMonitorCurveAdapter,
                             self._project_loader.native_project().WellTimeSeriesList.Items)
        else:
            return []

    def project_center(self) -> SurfacePoint:
        """
        Return the location of the project center on the surface measured in project units.
        """
        return SurfacePoint(om.Measurement(0, units.Metric.LENGTH), om.Measurement(0, units.Metric.LENGTH))

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
