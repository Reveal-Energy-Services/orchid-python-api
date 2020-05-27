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

import more_itertools
import numpy as np

# TODO: Replace some of this code with configuration and/or a method to use `clr.AddReference`
import sys
# noinspection PyUnresolvedReferences
import clr
IMAGE_FRAC_ASSEMBLIES_DIR = r'c:/src/OrchidApp/ImageFrac/ImageFrac.Application/bin/Debug'
if IMAGE_FRAC_ASSEMBLIES_DIR not in sys.path:
    sys.path.append(IMAGE_FRAC_ASSEMBLIES_DIR)
import pandas as pd

# noinspection PyUnresolvedReferences
from System import DateTime

clr.AddReference('UnitsNet')
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


def transform_net_time_series(net_time_series, name=None) -> pd.Series:
    """
    Transform a sequence of .NET samples (ticks) to a
    :param net_time_series: The sequence of .NET samples (each an implementation of `ITick<double>`).
    :param name: The name used to identify this time series (used to identify columns in pandas `DataFrame`s.
    :return: The pandas (Time) `Series` for the values.
    """
    result = pd.Series(data=[s.Value for s in net_time_series],
                       index=[_as_datetime(s.Timestamp) for s in net_time_series],
                       dtype=np.float64, name=name)
    return result


def transform_net_treatment(net_treatment_curves):
    """
    Transform the (3) .NET treatment curves into a pandas DataFrame.
    :param net_treatment_curves: The sequence of .NET treatment curves
    :return: The pandas `DataFrame` for the .NET treatment curves.
    """
    if len(net_treatment_curves) == 0:
        return pd.DataFrame()

    net_treating_pressure = more_itertools.one(filter(lambda c: c.SampledQuantityType == UnitsNet.QuantityType.Pressure,
                                                      net_treatment_curves))
    treating_pressure = transform_net_time_series(net_treating_pressure.GetOrderedTimeSeriesHistory(),
                                                  name='Treating Pressure')
    net_rate = more_itertools.one(filter(lambda c: (c.SampledQuantityType == UnitsNet.QuantityType.Ratio and
                                                    c.SampledQuantityName == 'Slurry Rate'),
                                         net_treatment_curves))
    rate = transform_net_time_series(net_rate.GetOrderedTimeSeriesHistory(),
                                     name=net_rate.SampledQuantityName)
    net_concentration = more_itertools.one(filter(lambda c: (c.SampledQuantityType == UnitsNet.QuantityType.Ratio and
                                                             c.SampledQuantityName == 'Proppant Concentration'),
                                                  net_treatment_curves))
    concentration = transform_net_time_series(net_concentration.GetOrderedTimeSeriesHistory(),
                                              name=net_concentration.SampledQuantityName)
    result = pd.concat([treating_pressure, rate, concentration], axis=1)
    return result
