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

from toolz.curried import partial

import orchid.project_units as opu


class NativeTreatmentCurveFacade:

    def __init__(self, net_treatment_curve):
        self._adaptee = net_treatment_curve
        self._quantity_name_physical_quantity_map = {'Pressure': 'pressure',
                                                     'Slurry Rate': 'slurry rate',
                                                     'Proppant Concentration': 'proppant concentration'}
        # noinspection PyArgumentList
        self._sample_unit_func = partial(opu.unit, net_treatment_curve.Stage.Well.Project)

    def display_name(self) -> str:
        """
        Return the display name for this treatment curve.
        :return: The display name of this treatment curve.
        """
        return self._adaptee.DisplayName

    def sampled_quantity_name(self) -> str:
        """
        Return the quantity name of the samples in this treatment curve.
        :return: The quantity name of each sample in this treatment curve.
        """
        return self._adaptee.SampledQuantityName

    def sampled_quantity_unit(self) -> str:
        """
        Return the measurement unit of the samples in this treatment curve.
        :return: A string containing an abbreviation for the unit  of each sample in this treatment curve.
        """
        result = self._sample_unit_func(self._quantity_name_physical_quantity_map[self.sampled_quantity_name()])
        return result
