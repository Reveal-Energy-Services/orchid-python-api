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

import datetime

import deal
import more_itertools
import numpy as np
import pandas as pd

# noinspection PyUnresolvedReferences
from System import DateTime

# noinspection PyUnresolvedReferences
import UnitsNet


def _as_datetime(net_time_point: DateTime) -> datetime.datetime:
    """
    Convert a .NET `DateTime` struct to a Python `datetime.datetime` object.
    :param net_time_point:  The .NET `DateTime` instance to convert.
    :return: The Python `datetime.datetime` instance equivalent to `net_time_point`.
    """
    result = datetime.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                               net_time_point.Hour, net_time_point.Minute, net_time_point.Second)
    return result


@deal.pre(lambda net_time_series, **kwargs: net_time_series is not None)
def transform_net_time_series(net_time_series, name=None) -> pd.Series:
    """
    Transform a sequence of .NET samples (ticks) to a pandas (Time) Series
    :param net_time_series: The sequence of .NET samples (each an implementation of `ITick<double>`).
    :param name: The name used to identify this time series (used to identify columns in pandas `DataFrame`s.
    :return: The pandas (Time) `Series` for the values.
    """
    result = pd.Series(data=[s.Value for s in net_time_series],
                       index=[_as_datetime(s.Timestamp) for s in net_time_series],
                       dtype=np.float64, name=name)
    return result


@deal.pre(lambda net_treatment_curve: net_treatment_curve is not None)
def transform_net_treatment(net_treatment_curves):
    """
    Transform the (3) .NET treatment curves into a pandas DataFrame.
    :param net_treatment_curves: The sequence of .NET treatment curves
    :return: The pandas `DataFrame` for the .NET treatment curves.
    """
    if len(net_treatment_curves) == 0:
        return pd.DataFrame()

    treating_pressure = _net_treatment_curve_to_time_series(
        net_treatment_curves, lambda c: c.SampledQuantityType == UnitsNet.QuantityType.Pressure, 'Treating Pressure')
    rate = _net_treatment_curve_to_time_series(
        net_treatment_curves, lambda c: (c.SampledQuantityType == UnitsNet.QuantityType.Ratio and
                                         c.SampledQuantityName == 'Slurry Rate'))
    concentration = _net_treatment_curve_to_time_series(
        net_treatment_curves, lambda c: (c.SampledQuantityType == UnitsNet.QuantityType.Ratio and
                                         c.SampledQuantityName == 'Proppant Concentration'))

    result = pd.concat([treating_pressure, rate, concentration], axis=1)
    return result


def _net_treatment_curve_to_time_series(net_treatment_curves, predicate_fn, series_name=None):
    """
    Convert a .NET treatment curve to a pandas (Time) Series
    :param net_treatment_curves: The sequence of .NET treatment curves containing the curve of interest
    :param predicate_fn: The function used to identify the treatment curve of interest
    :param series_name: The name identifying the Time Series. If `None`, use the curve `SampledQuantityName` property.
    :return: The pandas (Time) Series corresponding to the .NET treatment curve
    """
    selected_curve = more_itertools.one(filter(predicate_fn, net_treatment_curves))
    result = transform_net_time_series(selected_curve.GetOrderedTimeSeriesHistory(),
                                       name=series_name if series_name else selected_curve.SampledQuantityName)
    return result