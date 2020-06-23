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

import pandas as pd
from toolz.curried import map, partial

import orchid.dot_net_dom_access as dna
from orchid.net_quantity import as_datetime
import orchid.project_units as opu


class NativeTreatmentCurveFacade:
    def __init__(self, net_treatment_curve):
        self._adaptee = net_treatment_curve
        self._quantity_name_physical_quantity_map = {'Pressure': 'pressure',
                                                     'Slurry Rate': 'slurry rate',
                                                     'Proppant Concentration': 'proppant concentration'}
        # noinspection PyArgumentList
        self._sample_unit_func = partial(opu.unit, net_treatment_curve.Stage.Well.Project)

    display_name = dna.dom_property('display_name', 'Return the display name for this treatment curve.')
    name = dna.dom_property('name', 'Return the name for this treatment curve.')
    sampled_quantity_name = dna.dom_property('sampled_quantity_name',
                                             'Return the sampled quantity name for this treatment curve.')
    suffix = dna.dom_property('suffix', 'Return the suffix for this treatment curve.')

    def sampled_quantity_unit(self) -> str:
        """
        Return the measurement unit of the samples in this treatment curve.
        :return: A string containing an abbreviation for the unit  of each sample in this treatment curve.
        """
        result = self._sample_unit_func(self._quantity_name_physical_quantity_map[self.sampled_quantity_name])
        return result

    def time_series(self) -> pd.Series:
        """
        Return the suffix for this treatment curve.
        :return: The suffix of this treatment curve.
        """
        # Because I use `samples` twice in the subsequent expression, I must *actualize* the map by invoking `list`.
        samples = list(map(lambda s: (s.Timestamp, s.Value), self._adaptee.GetOrderedTimeSeriesHistory()))
        result = pd.Series(data=map(lambda s: s[1], samples), index=map(as_datetime, map(lambda s: s[0], samples)),
                           name=self.name)
        return result
