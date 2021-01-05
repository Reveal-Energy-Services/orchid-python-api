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

from orchid import (base_curve_adapter as bca,
                    dot_net_dom_access as dna,
                    unit_system as units)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import UnitSystem

AboutTreatmentCurveType = namedtuple('AboutTreatmentCurveType', ['curve_type', 'net_curve_type'])


# TODO: Better repair for these curve types involving the .NET type `TreatmentCurvesPredefinedTypes` if possible
class TreatmentCurveTypes(enum.Enum):
    PROPPANT_CONCENTRATION = AboutTreatmentCurveType('Proppant Concentration', 'Surface Proppant Concentration')
    SLURRY_RATE = AboutTreatmentCurveType('Slurry Rate', 'Slurry Rate')
    TREATING_PRESSURE = AboutTreatmentCurveType('Pressure', 'Pressure')


# Convenience constants, perhaps temporary, so that users need not navigate the object tree to access needed value
PROPPANT_CONCENTRATION = TreatmentCurveTypes.PROPPANT_CONCENTRATION.value.curve_type
SLURRY_RATE = TreatmentCurveTypes.SLURRY_RATE.value.curve_type
TREATING_PRESSURE = TreatmentCurveTypes.TREATING_PRESSURE.value.curve_type


class NativeTreatmentCurveAdapter(bca.BaseCurveAdapter):
    suffix = dna.dom_property('suffix', 'Return the suffix for this treatment curve.')

    def sampled_quantity_unit(self) -> Union[units.UsOilfield, units.Metric]:
        """
        Return the measurement unit of the samples in this treatment curve.

        Returns:
            A `UnitSystem` member containing the unit for the sample in this treatment curve.
        """
        net_project_units = self._adaptee.Stage.Well.Project.ProjectUnits
        if net_project_units == UnitSystem.USOilfield():
            project_units = units.UsOilfield
        elif net_project_units == UnitSystem.Metric():
            project_units = units.Metric
        else:
            raise ValueError(f'Unrecognised unit system for {self._adaptee.Stage.Well.Project.Name}')

        sampled_quantity_name_unit_map = {
            TreatmentCurveTypes.TREATING_PRESSURE.value.net_curve_type: project_units.PRESSURE,
            TreatmentCurveTypes.PROPPANT_CONCENTRATION.value.net_curve_type: project_units.PROPPANT_CONCENTRATION,
            TreatmentCurveTypes.SLURRY_RATE.value.net_curve_type: project_units.SLURRY_RATE,
        }
        return sampled_quantity_name_unit_map[self.sampled_quantity_name]
