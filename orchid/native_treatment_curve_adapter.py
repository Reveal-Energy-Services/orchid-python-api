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
import enum

from orchid import (base_curve_adapter as bca,
                    dot_net_dom_access as dna)

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

    def get_net_project_units(self):
        """
        Returns the .NET project units (a `UnitSystem`) for this instance.

        This method plays the role of "Primitive Operation" in the _Template Method_ design pattern. In this
        role, the "Template Method" defines an algorithm and delegates some steps of the algorithm to derived
        classes through invocation of "Primitive Operations".
        """
        result = self._adaptee.Stage.Well.Project.ProjectUnits
        return result

    def quantity_name_unit_map(self, project_units):
        """
        Return a map (dictionary) between quantity names and units (from `unit_system`) of the samples.

        This method plays the role of "Primitive Operation" in the _Template Method_ design pattern. In this
        role, the "Template Method" defines an algorithm and delegates some steps of the algorithm to derived
        classes through invocation of "Primitive Operations".

        Args:
            project_units: The unit system of the project.
        """
        result = {
            TreatmentCurveTypes.TREATING_PRESSURE.value.net_curve_type: project_units.PRESSURE,
            TreatmentCurveTypes.PROPPANT_CONCENTRATION.value.net_curve_type: project_units.PROPPANT_CONCENTRATION,
            TreatmentCurveTypes.SLURRY_RATE.value.net_curve_type: project_units.SLURRY_RATE,
        }
        return result
