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

from toolz.curried import pipe, map, reduce, merge

import orchid.dot_net_dom_access as dna
from orchid.measurement import Measurement
import orchid.native_treatment_curve_facade as ntc
from orchid.net_quantity import as_datetime, as_measurement, convert_net_quantity_to_different_unit


class NativeStageAdapter(dna.DotNetAdapter):
    """Adapts a .NET IStage to be more Pythonic."""

    display_stage_number = dna.dom_property('display_stage_number', 'The display stage number for the stage.')
    start_time = dna.transformed_dom_property('start_time', 'The start time of the stage treatment.', as_datetime)
    stop_time = dna.transformed_dom_property('stop_time', 'The stop time of the stage treatment.', as_datetime)
    display_name_with_well = dna.dom_property('display_name_with_well', 'The display stage number including the well')
    cluster_count = dna.dom_property('number_of_clusters', 'The number of clusters for this stage')

    @staticmethod
    def _sampled_quantity_name_curve_map(sampled_quantity_name):
        return {'Pressure': ntc.TREATING_PRESSURE, 'Slurry Rate': ntc.SLURRY_RATE,
                'Proppant Concentration': ntc.PROPPANT_CONCENTRATION}[sampled_quantity_name]

    def md_top(self, length_unit_abbreviation: str) -> Measurement:
        """
        Return the measured depth of the top of this stage (closest to the well head / farthest from the toe)
        in the specified unit.
        :param length_unit_abbreviation: An abbreviation of the unit of length for the returned Measurement.
        :return: The measured depth of the stage top in the specified unit.
        """
        original = self._adaptee.MdTop
        md_top_quantity = convert_net_quantity_to_different_unit(original, length_unit_abbreviation)
        result = as_measurement(md_top_quantity)
        return result

    def md_bottom(self, length_unit_abbreviation):
        """
        Return the measured depth of the bottom of this stage (farthest from the well head / closest to the toe)
        in the specified unit.
        :param length_unit_abbreviation: An abbreviation of the unit of length for the returned Measurement.
        :return: The measured depth of the stage bottom in the specified unit.
        """
        original = self._adaptee.MdBottom
        md_top_quantity = convert_net_quantity_to_different_unit(original, length_unit_abbreviation)
        result = as_measurement(md_top_quantity)
        return result

    def treatment_curves(self):
        """
        Returns the dictionary of treatment curves for this treatment_stage.

        Request a specific curve from the dictionary using the constants defined in `orchid`:

        - `PROPPANT_CONCENTRATION`
        - `SLURRY_RATE`
        - `TREATING_PRESSURE`

        Returns:
            The dictionary containing the available treatment curves.
        """
        if not self._adaptee.TreatmentCurves.Items:
            return {}

        def add_curve(so_far, treatment_curve):
            curve_name = self._sampled_quantity_name_curve_map(treatment_curve.sampled_quantity_name)
            treatment_curve_map = {curve_name: treatment_curve}
            return merge(treatment_curve_map, so_far)

        result = pipe(self._adaptee.TreatmentCurves.Items,  # start with .NET treatment curves
                      map(ntc.NativeTreatmentCurveFacade),  # wrap them in a facade
                      # Transform the map to a dictionary keyed by the sampled quantity name
                      lambda cs: reduce(add_curve, cs, {}))
        return result
