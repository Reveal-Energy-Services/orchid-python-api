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

# noinspection PyUnresolvedReferences
import clr
import numpy as np
import pandas as pd

# noinspection PyUnresolvedReferences
from System import DateTime


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


def _as_datetime(net_time_point: DateTime) -> datetime.datetime:
    """
    Convert a .NET `DateTime` struct to a Python `datetime.datetime` object.
    :param net_time_point:  The .NET `DateTime` instance to convert.
    :return: The Python `datetime.datetime` instance equivalent to `net_time_point`.
    """
    result = datetime.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                               net_time_point.Hour, net_time_point.Minute, net_time_point.Second)
    return result
