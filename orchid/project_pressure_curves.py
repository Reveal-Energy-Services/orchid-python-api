#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

import datetime
import sys
from typing import Sequence

import clr
import deal
import pandas as pd

from orchid.project_loader import ProjectLoader
import orchid.validation

sys.path.append(r'c:\src\OrchidApp\ImageFrac\ImageFrac.Application\bin\Debug')
clr.AddReference('UnitsNet')
# noinspection PyUnresolvedReferences
import UnitsNet


class ProjectPressureCurves:
    """
    A container for .NET Wells indexed by time series IDs.
    """

    @deal.pre(orchid.validation.arg_not_none)
    def __init__(self, net_project: ProjectLoader):
        """
        Construct an instance wrapping the loaded .NET `IProject`.

        :param net_project: The `IProject` being wrapped.
        """
        self._project_loader = net_project

        self._pressure_curves = {}

    def _pressure_curve_map(self):
        if not self._pressure_curves:
            self._pressure_curves.update({c.DisplayName: c for
                                          c in self._project_loader.loaded_project().WellTimeSeriesList.Items if
                                          c.SampledQuantityType == UnitsNet.QuantityType.Pressure})
        return self._pressure_curves

    def pressure_curve_ids(self) -> Sequence[str]:
        """
        Return the pressure curve identifiers for all pressure curves.
        :return: A list of all pressure curve identifiers.
        """

        return list(self._pressure_curve_map().keys())

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def pressure_curve_samples(self, curve_id: str) -> pd.Series:
        """
        Return a pandas time series containing the samples for the pressure curve identified by `curve_id`.

        :param curve_id: Identifies a specific pressure curve in the project.

        :return: A sequence of sample pressures (implicitly in the project pressure units)."""
        curve = self._pressure_curve_map()[curve_id]

        # TODO: Premature optimization?
        # The following code uses a technique from a StackOverflow post on creating a pandas `Series` from a
        # sequence of Python tuples. All the code is less clear, it avoids looping over a relatively "large"
        # array (> 100k items) multiple time.
        # https://stackoverflow.com/questions/53363688/converting-a-list-of-tuples-to-a-pandas-series
        stamp_value_pairs = [(self._as_datetime(s.Timestamp), s.Value) for s in curve.GetOrderedTimeSeriesHistory()]
        if stamp_value_pairs:
            (timestamps, values) = zip(*stamp_value_pairs)
            result = pd.Series(values, timestamps)
            return result
        else:
            return pd.Series([], dtype=float)

    @staticmethod
    def _as_datetime(net_time_point) -> datetime.datetime:
        result = datetime.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                                   net_time_point.Hour, net_time_point.Minute, net_time_point.Second)
        return result

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def display_name(self, curve_id: str) -> str:
        """
        Return the name used to recognize the pressure curve identified by curve_id.

        :param curve_id: The value used to identify a specific pressure curve.
        :return: The name used by engineers to describe this curve.
        """
        return self._pressure_curve_map()[curve_id].DisplayName
