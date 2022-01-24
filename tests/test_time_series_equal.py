#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest.mock

import toolz.curried as toolz

import numpy as np
import pandas as pd
import pandas.testing as pdt

from orchid import (
    project_loader as loader,
)
from tests import (
    stub_net as tsn,
)


def assert_time_series_equal(expected_name, start_time_point, values, create_sut_func, **data_samples_kwargs):
    """
    Assert that a created time series equals a generated and expected time series.

    Args:
        expected_name: The expected name of the created time series
        start_time_point: The starting time of the time series samples. (Assumes 30-second sample time.)
        values: The expected time series values.
        create_sut_func: The function that creates the time series to be tested.
        **data_samples_kwargs: A single additional keyword argument that specifies the argument to the
                creation function that specifies, perhaps indirectly, the generated samples.
    """
    sut = create_sut_func(name=expected_name, **data_samples_kwargs)
    stub_unix_time_stamps = toolz.pipe(
        tsn.create_30_second_time_points(start_time_point, len(values)),
        toolz.map(lambda dt: int(dt.timestamp())),
        list,
    )
    stub_python_time_series_arrays_dto = tsn.StubPythonTimesSeriesArraysDto(values,
                                                                            stub_unix_time_stamps)
    with unittest.mock.patch('orchid.base_time_series_adapter.loader.as_python_time_series_arrays',
                             spec=loader.as_python_time_series_arrays,
                             return_value=stub_python_time_series_arrays_dto):
        expected_time_points = toolz.pipe(
            start_time_point,
            lambda st: tsn.create_30_second_time_points(st, len(values)),
            toolz.map(lambda dt: int(dt.timestamp())),
            toolz.map(lambda uts: np.datetime64(uts, 's')),
            lambda tss: pd.DatetimeIndex(tss, tz='UTC'),
        )
        expected = pd.Series(data=values, index=expected_time_points, name=expected_name)
        pdt.assert_series_equal(sut.data_points(), expected)
