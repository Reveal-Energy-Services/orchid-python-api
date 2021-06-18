#  Copyright 2017-2021 Reveal Energy Services, Inc
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

# noinspection PyPackageRequirements
from behave import *
use_step_matcher("parse")

from collections import namedtuple
import datetime as dt

from hamcrest import assert_that, not_none, equal_to, has_length
import option
import parsy
import pendulum
import toolz.curried as toolz

import numpy as np
import pandas as pd

from orchid import (
    dot_net_dom_access as dna,
    net_date_time as net_dt,
)


AboutDataFrameColumn = namedtuple('AboutDataFrameColumn', ['short_name', 'full_name', 'convert_func'])


@when("I query the project data frames identified by '{object_id}'")
def step_impl(context, object_id):
    """
    Args:
        context (behave.runner.Context): The test context.
        object_id (str): The string representation of the value identifying the data frame of interest.
    """
    context.data_frame_of_interest = context.project.data_frame(dna.as_object_id(object_id)).unwrap()
    assert_that(context.data_frame_of_interest, not_none())


@when("I query all the project data frames by {name} and by {display_name}")
def step_impl(context, name, display_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        name (str): The name of the data frame of interest.
        display_name (str): The display name of the data frame of interest.
    """
    context.data_frames_by_names = {
        name: list(context.project.find_data_frames_with_name(name)),
        display_name: list(context.project.find_data_frames_with_display_name(display_name)),
    }


@when("I query the loaded project for the data frame named '{data_frame_name}'")
def step_impl(context, data_frame_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        data_frame_name (str): The name of the data frame of interest.
    """
    candidates = list(context.project.find_data_frames_with_name(data_frame_name))
    assert_that(len(candidates), equal_to(1))

    context.data_frame_of_interest = candidates[0]


@then("I see a single data frame identified by {object_id}")
def step_impl(context, object_id):
    """
    Args:
        context (behave.runner.Context): The test context.
        object_id (str): The textual representation of the UUID identifying the data frame of interest.
    """
    data_frame_of_interest = context.data_frame_of_interest
    assert_that(data_frame_of_interest.object_id, equal_to(dna.as_object_id(object_id)))


@then("I see a single data frame alternatively identified by {name} and {display_name}")
def step_impl(context, name, display_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        name (str): The name of the data frame of interest.
        display_name (str): The name of the data frame of interest used for display purposes.
    """
    assert_that(len(context.data_frames_by_names[name]), equal_to(1))
    assert_that(len(context.data_frames_by_names[display_name]), equal_to(1))
    assert_that(context.data_frames_by_names[name] is context.data_frames_by_names[display_name])


@then("I see the specified data frame {is_potentially_corrupt}")
def step_impl(context, is_potentially_corrupt):
    """
    Args:
        context (behave.runner.Context): The test context.
        is_potentially_corrupt (str): Indicates if the data frame of interest is potentially corrupt.
        corrupt.
    """
    data_frame_of_interest = context.data_frame_of_interest
    assert_that(str(data_frame_of_interest.is_potentially_corrupt), equal_to(is_potentially_corrupt),
                f'Data frame, "{data_frame_of_interest.name}", is potentially corrupt.')


@then("I see the sampled cells")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """

    def _fix_gng_project_data_frame_pnet_column_data_type(source, name):
        if 'GnG project data frame' not in name:
            return source

        # TODO: Consider moving "fix" to `native_frame_adapter.data_frame` to correctly handle other similar problems.
        # The `Pnet` column of the GnG project data frame is unusual. In general, the net pressure is a floating point
        # value; however, for this specific data frame, **all** the values in the actual `Pnet` column of the .NET
        # `DataFrame` are `null/DBNull.Value` so all the values in my expected sample table are `NaN`. Because `pandas`
        # **only** knows that all the values are `NaN` values, it determines the data type of the column to be `object`
        # instead of the expected `float64`.
        source["Pnet"] = pd.to_numeric(source["Pnet"])
        return source

    expected = _as_data_frame(context.table)
    actual_data_frame = context.data_frame_of_interest.pandas_data_frame()
    sampled_data_frame_rows = actual_data_frame.iloc[list(expected['Sample'].values), :]
    sampled_data_frame_cols = sampled_data_frame_rows.loc[:, expected.columns[1:]]
    sampled_data_frame_cols.reset_index(inplace=True)
    raw_sampled_data_frame = sampled_data_frame_cols.rename(columns={'index': 'Sample'})
    sampled_data_frame = _fix_gng_project_data_frame_pnet_column_data_type(raw_sampled_data_frame,
                                                                           context.scenario.name)
    pd.testing.assert_frame_equal(sampled_data_frame, expected)


def _as_data_frame(table):
    def reduce_row(so_far, row_to_reduce):
        row_data = {h: [row_to_reduce[h]] for h in row_to_reduce.headings}
        return toolz.merge_with(toolz.concat, so_far, row_data)

    initial_data = {h: [] for h in table.headings}
    raw_frame_data = toolz.reduce(reduce_row, table, initial_data)
    frame_mapped_data = toolz.itemmap(_table_cells_to_data_frame_cells, raw_frame_data)
    frame_data = toolz.valmap(list, frame_mapped_data)
    raw_result = pd.DataFrame(data=frame_data, columns=frame_data.keys())

    # result = _fix_gng_project_data_frame_pnet_column_data_type(raw_result, scenario_name)
    result = raw_result
    return result


_hours = parsy.regex(r'[0-9]{2}').map(int).desc('hours')
_minutes = parsy.regex(r'[0-9]{2}').map(int).desc('minutes')
_seconds = parsy.regex(r'[0-9]{2}').map(int).desc('seconds')
_hms_sep = parsy.string(':')

_fractional_seconds = parsy.regex(r'[0-9]{1,7}').map(int).desc('fractional_seconds')
_decimal_sep = parsy.string('.')
_fractional = _decimal_sep >> _fractional_seconds
_optional_fractional = _fractional.optional().map(option.maybe)


@parsy.generate
def _parse_hms():
    hours = yield _hours
    yield _hms_sep
    minutes = yield _minutes
    yield _hms_sep
    seconds = yield _seconds
    fractional_seconds = yield _optional_fractional
    # fractional_seconds, if present, contains 7 digits; that is, tenths of microseconds. The following code rounds
    # those seven digits to six to fit in microseconds. Note that this calculation involves half-even rounding.
    microseconds = fractional_seconds.map(lambda fs: round(fs, -1) / 10)
    return microseconds.map_or_else(lambda us: dt.timedelta(hours=hours, minutes=minutes, seconds=seconds,
                                                            microseconds=us),
                                    lambda: dt.timedelta(hours=hours, minutes=minutes, seconds=seconds))


def hms(t):
    result = _parse_hms.parse(t)
    return result


_EMPTY_CONVERTER = {
    'None': None,
    'NaN': np.NaN,
    'NaT': pd.NaT,
}


@toolz.curry
def convert_maybe_value(convert_func, v):
    if v in _EMPTY_CONVERTER:
        return _EMPTY_CONVERTER[v]

    return convert_func(v)


about_data_frame_columns = [
    AboutDataFrameColumn('sample', 'Sample', int),
    AboutDataFrameColumn('sh_easting', 'Surface  Hole Easting ', float),
    AboutDataFrameColumn('bh_northing', 'Bottom Hole Northing ', float),
    AboutDataFrameColumn('bh_tdv', 'Bottom Hole TDV ', float),
    AboutDataFrameColumn('stage_no', 'StageNumber', convert_maybe_value(int)),
    AboutDataFrameColumn('stage_length', 'StageLength', convert_maybe_value(float)),
    AboutDataFrameColumn('p_net', 'Pnet', convert_maybe_value(float)),
    AboutDataFrameColumn('length', 'Length', float),
    AboutDataFrameColumn('mean_azimuth', 'MeanAzimuth', float),
    AboutDataFrameColumn('dept_max', 'DEPTMax', convert_maybe_value(float)),
    AboutDataFrameColumn('rla4_max', 'RLA4Max', convert_maybe_value(float)),
    AboutDataFrameColumn('tend_max', 'TENDMax', convert_maybe_value(float)),
    AboutDataFrameColumn('pefz_mean', 'PEFZMean', convert_maybe_value(float)),
    AboutDataFrameColumn('lcal_mean', 'LCALMean', convert_maybe_value(float)),
    AboutDataFrameColumn('dpo_ls_min', 'DPO_LSMin', convert_maybe_value(float)),
    AboutDataFrameColumn('tvd_ss', 'TVDSS', convert_maybe_value(float)),
    AboutDataFrameColumn('rla3', 'RLA3', convert_maybe_value(float)),
    AboutDataFrameColumn('dtco', 'DTCO', convert_maybe_value(float)),
    AboutDataFrameColumn('hdra', 'HDRA', convert_maybe_value(float)),
    AboutDataFrameColumn('rhoz', 'RHOZ', convert_maybe_value(float)),
    AboutDataFrameColumn('lcal', 'LCAL', convert_maybe_value(float)),
    AboutDataFrameColumn('marker_description', 'Marker Description', convert_maybe_value(str)),
    AboutDataFrameColumn('horizon_marker_set', 'Horizon Marker Set', str),
    AboutDataFrameColumn('boundary_type', 'Boundary Type', str),
    AboutDataFrameColumn('well', 'Well', str),
    AboutDataFrameColumn('md', 'MD', convert_maybe_value(float)),
    AboutDataFrameColumn('tvd', 'TVD', convert_maybe_value(float)),
]

short_column_names = {about.short_name: about for about in about_data_frame_columns}


def _table_cells_to_data_frame_cells(items):
    """
    Map table cell data to data frame cells.

    Args:
        items(tuple): A tuple of the table column name and an iterable of table cells.

    Returns:
        A tuple of the transformed table column name and the transformed cells
    """

    def parsed_date_with_correct_utc(text_time_point):
        parsed_time_point = pendulum.parse(text_time_point)
        if parsed_time_point.timezone_name != '+00:00':
            return parsed_time_point

        return parsed_time_point.set(tz=pendulum.UTC)

    table_data_frame_cells = {
        # Permian project data frame
        'bh_easting': convert_maybe_value(float),
        'md_bottom': convert_maybe_value(float),
        'md_top': convert_maybe_value(float),
        'part_start_time': convert_maybe_value(parsed_date_with_correct_utc),
        'part_end_time': convert_maybe_value(parsed_date_with_correct_utc),
        'part_pumped_vol': convert_maybe_value(float),
        'pnet': convert_maybe_value(float),
        'pump_time': convert_maybe_value(int),
        # 'sh_easting': float,
        'stage_start_time': convert_maybe_value(parsed_date_with_correct_utc),
        'stage_pumped_vol': convert_maybe_value(float),
        'well_name': convert_maybe_value(str),
        # Permian FDI data frame
        'obs_set_name': str,
        'part_no': str,
        'timestamp': convert_maybe_value(parsed_date_with_correct_utc),
        'delta_t': convert_maybe_value(hms),
        'delta_p': convert_maybe_value(float),
        'vol_to_pick': convert_maybe_value(float),
        # Permian microseismic data frame
        # 'timestamp': convert_maybe_value(hms),
        'northing': convert_maybe_value(float),
        'depth_tvd_ss': convert_maybe_value(float),
        'dist_3d': convert_maybe_value(float),
        'planar_dist_azm': convert_maybe_value(float),
        'vert_dist': convert_maybe_value(float),
    }
    table_column_name, table_cells = items
    about_column = short_column_names.get(table_column_name)
    if about_column is not None:
        return about_column.full_name, toolz.map(about_column.convert_func, table_cells)
    else:
        print('None')
        return (_table_column_to_data_frame_column(table_column_name),
                toolz.map(table_data_frame_cells.get(table_column_name), table_cells))


def _table_column_to_data_frame_column(table_column_name):
    """
    Convert a table column heading ta a data frame column heading.

    Args:
        table_column_name: The expected table column heading.

    Returns:
        The data frame column name corresponding to `table_column_name`.
    """
    table_data_frame_columns = {
        # Permian project data frame
        'bh_easting': 'Bottom Hole Easting ',
        'md_top': 'MDTop',
        'md_bottom': 'MDBottom',
        'part_end_time': 'PartEndTime',
        'part_start_time': 'PartStartTime',
        'part_pumped_vol': 'StagePartPumpedVolume',
        'pnet': 'Pnet',
        'pump_time': 'PumpTime',
        'stage_start_time': 'StageStartTime',
        'stage_pumped_vol': 'StagePumpedVolume',
        'well_name': 'WellName',
        # Permian FDI data frame
        'obs_set_name': 'ObservationSetName',
        'part_no': 'TreatmentStagePartNumber',
        'timestamp': 'Timestamp',
        'delta_t': 'DeltaT',
        'delta_p': 'DeltaP',
        'vol_to_pick': 'VolumeToPick',
        # Permian microseismic data frame
        # 'timestamp': 'Timestamp',
        'northing': 'Northing',
        'depth_tvd_ss': 'DepthTvdSs',
        'dist_3d': 'Distance3d',
        'planar_dist_azm': 'PlanarDistanceAzimuth',
        'vert_dist': 'VerticalDistance',
    }
    return toolz.get(table_column_name, table_data_frame_columns)


def _find_data_frame_by_id(object_id, data_frames):
    candidates = toolz.pipe(
        data_frames,
        toolz.filter(lambda df: df.object_id == object_id),
        list
    )
    assert_that(candidates, has_length(1))

    return toolz.first(candidates)
