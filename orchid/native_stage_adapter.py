#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

from toolz.curried import pipe, map, reduce, merge

import orchid.dot_net_dom_access as dna
from orchid.measurement import Measurement
from orchid.native_treatment_curve_facade import NativeTreatmentCurveFacade
from orchid.net_quantity import as_datetime, as_measurement, convert_net_quantity_to_different_unit


class NativeStageAdapter(dna.DotNetAdapter):
    """Adapts a .NET IStage to be more Pythonic."""

    display_stage_number = dna.dom_property('display_stage_number', 'The display stage number for the stage.')
    start_time = dna.transformed_dom_property('start_time', 'The start time of the stage treatment.', as_datetime)
    stop_time = dna.transformed_dom_property('stop_time', 'The stop time of the stage treatment.', as_datetime)

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
        if not self._adaptee.TreatmentCurves.Items:
            return {}

        def add_curve(so_far, treatment_curve):
            treatment_curve_map = {treatment_curve.sampled_quantity_name: treatment_curve}
            return merge(treatment_curve_map, so_far)

        result = pipe(self._adaptee.TreatmentCurves.Items,  # start with .NET treatment curves
                      map(NativeTreatmentCurveFacade),  # wrap them in a facade
                      # Transform the map to a dictionary keyed by the sampled quantity name
                      lambda cs: reduce(add_curve, cs, {}))
        return result
