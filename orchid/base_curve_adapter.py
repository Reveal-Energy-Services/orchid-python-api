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


from abc import ABCMeta, abstractmethod

import pandas as pd

from orchid import (dot_net_dom_access as dna,
                    net_quantity as onq)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IQuantityTimeSeries, UnitSystem


class BaseCurveAdapter(dna.DotNetAdapter, metaclass=ABCMeta):
    name = dna.dom_property('name', 'Return the name for this treatment curve.')
    display_name = dna.dom_property('display_name', 'Return the display name for this curve.')
    sampled_quantity_name = dna.dom_property('sampled_quantity_name',
                                             'Return the sampled quantity name for this curve.')

    def __init__(self, adaptee: IQuantityTimeSeries):
        """
        Construct an instance that adapts a .NET `IStageSampledQuantityTimeSeries` instance.

        Args:
            adaptee: The .NET stage time series to be adapted.
        """
        super().__init__(adaptee)

    @abstractmethod
    def sampled_quantity_unit(self):
        """
        Return the measurement unit of the samples in this treatment curve.

        Returns:
            A `UnitSystem` member containing the unit for the sample in this treatment curve.
        """
        pass

    def time_series(self) -> pd.Series:
        """
        Return the time series for this well curve.

        Returns
            The time series of this well curve.
        """
        # Because I use `samples` twice in the subsequent expression, I must *actualize* the map by invoking `list`.
        samples = list(map(lambda s: (s.Timestamp, s.Value), self._adaptee.GetOrderedTimeSeriesHistory()))
        result = pd.Series(data=map(lambda s: s[1], samples), index=map(onq.as_datetime, map(lambda s: s[0], samples)),
                           name=self.name)
        return result