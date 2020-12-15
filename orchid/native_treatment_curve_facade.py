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

from collections import namedtuple
import enum
from typing import Union

import pandas as pd
import toolz.curried as toolz

import orchid.dot_net_dom_access as dna
import orchid.net_quantity as onq
import orchid.unit_system as units

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IStageSampledQuantityTimeSeries, UnitSystem

# noinspection PyUnresolvedReferences
import UnitsNet


AboutCurveType = namedtuple('AboutCurveType', ['curve_type', 'net_curve_type'])


# TODO: Better repair for these curve types involving the .NET type `TreatmentCurvesPredefinedTypes` if possible
class CurveTypes(enum.Enum):
    PROPPANT_CONCENTRATION = AboutCurveType('Proppant Concentration', 'Surface Proppant Concentration')
    SLURRY_RATE = AboutCurveType('Slurry Rate', 'Slurry Rate')
    TREATING_PRESSURE = AboutCurveType('Pressure', 'Pressure')


PROPPANT_CONCENTRATION = CurveTypes.PROPPANT_CONCENTRATION.value.curve_type
SLURRY_RATE = CurveTypes.SLURRY_RATE.value.curve_type
TREATING_PRESSURE = CurveTypes.TREATING_PRESSURE.value.curve_type


class NativeTreatmentCurveFacade(dna.DotNetAdapter):
    def __init__(self, net_treatment_curve: IStageSampledQuantityTimeSeries):
        """
        Constructs an instance adapting a .NET IStageSampledQuantityTimeSeries.
        :param net_treatment_curve: The .NET stage time series to be adapted.
        """
        super().__init__(net_treatment_curve)
        self._quantity_name_physical_quantity_map = {TREATING_PRESSURE: 'pressure',
                                                     SLURRY_RATE: 'slurry rate',
                                                     PROPPANT_CONCENTRATION: 'proppant concentration'}
        # noinspection PyArgumentList
        self._sample_unit_func = lambda: None

    display_name = dna.dom_property('display_name', 'Return the display name for this treatment curve.')
    name = dna.dom_property('name', 'Return the name for this treatment curve.')
    sampled_quantity_name = dna.dom_property('sampled_quantity_name',
                                             'Return the sampled quantity name for this treatment curve.')
    suffix = dna.dom_property('suffix', 'Return the suffix for this treatment curve.')

    def sampled_quantity_unit(self) -> Union[units.UsOilfield, units.Metric]:
        """
        Return the measurement unit of the samples in this treatment curve.
        :return: A string containing an unit for the unit  of each sample in this treatment curve.
        """
        net_project_units = self._adaptee.Stage.Well.Project.ProjectUnits
        if net_project_units == UnitSystem.USOilfield():
            project_units = units.UsOilfield
        elif net_project_units == UnitSystem.Metric():
            project_units = units.Metric
        else:
            raise ValueError(f'Unrecognised unit system for {self._adaptee.Stage.Well.Project.Name}')

        sampled_quantity_name_unit_map = {
            CurveTypes.TREATING_PRESSURE.value.net_curve_type: project_units.PRESSURE,
            CurveTypes.PROPPANT_CONCENTRATION.value.net_curve_type: project_units.PROPPANT_CONCENTRATION,
            CurveTypes.SLURRY_RATE.value.net_curve_type: project_units.SLURRY_RATE,
        }
        return sampled_quantity_name_unit_map[self.sampled_quantity_name]

    def time_series(self) -> pd.Series:
        """
        Return the time_series for this treatment curve.
        :return: The time_series of this treatment curve.
        """
        # Because I use `samples` twice in the subsequent expression, I must *actualize* the map by invoking `list`.
        samples = list(toolz.map(lambda s: (s.Timestamp, s.Value), self._adaptee.GetOrderedTimeSeriesHistory()))
        result = pd.Series(data=toolz.map(lambda s: s[1], samples),
                           index=toolz.map(onq.as_datetime, toolz.map(lambda s: s[0], samples)),
                           name=self.name)
        return result
