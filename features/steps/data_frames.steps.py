#  Copyright (c) 2017-2022 Reveal Energy Services, Inc
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
import re
import uuid

from hamcrest import assert_that, not_none, equal_to, has_length, contains_exactly, is_, instance_of
import option
import parsy
import pendulum
import toolz.curried as toolz

import numpy as np
import pandas as pd

from orchid import (
    dot_net_dom_access as dna,
)


AboutDataFrameColumn = namedtuple('AboutDataFrameColumn', ['short_name', 'full_name', 'convert_func'])


@when("I query the project data frames identified by '{object_id}'")
def step_impl(context, object_id):
    """
    Args:
        context (behave.runner.Context): The test context.
        object_id (str): The string representation of the value identifying the data frame of interest.
    """
    context.data_frame_of_interest = context.project.data_frames().find_by_object_id(dna.as_object_id(object_id))
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
        name: [df.name for df
               in list(context.project.data_frames().find_by_name(name))],
        display_name: [df.display_name for df
                       in list(context.project.data_frames().find_by_display_name(display_name))],
    }


@when("I query the loaded project for the data frame named '{data_frame_name}'")
def step_impl(context, data_frame_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        data_frame_name (str): The name of the data frame of interest.
    """
    candidates = list(context.project.data_frames().find_by_name(data_frame_name))
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
    assert_that(context.data_frames_by_names[name], contains_exactly(name))
    assert_that(context.data_frames_by_names[display_name], contains_exactly(display_name))


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


@then("I see the columns")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    expected_column_names = [row['column_name'] for row in context.table.rows]
    actual_column_names = context.data_frame_of_interest.pandas_data_frame().columns

    assert_that(actual_column_names, contains_exactly(*expected_column_names))


@step("I see no rows")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    assert_that(context.data_frame_of_interest.pandas_data_frame().values.size, equal_to(0))


@then("I see an empty data frame")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    assert_that(context.data_frame_of_interest.pandas_data_frame().empty)


@then("I see a Python warning")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    # TODO: I know this test will fail. I need to create some structure to determine the appropriate error.
    assert_that(context.data_frame_find_by_id_warning, is_(instance_of(IndentationError)))


@step("I see a warning like")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    # TODO: I know this test will fail. I need to create some structure to determine the appropriate error.
    assert_that(re.search(context.text, context.data_from_find_by_id_warning.message), is_(not_none()))


def _as_data_frame(table):
    def reduce_row(so_far, row_to_reduce):
        row_data = {h: [row_to_reduce[h]] for h in row_to_reduce.headings}
        return toolz.merge_with(toolz.concat, so_far, row_data)

    initial_data = {h: [] for h in table.headings}
    raw_frame_data = toolz.reduce(reduce_row, table, initial_data)
    frame_mapped_data = toolz.itemmap(_table_cells_to_data_frame_cells, raw_frame_data)
    frame_data = toolz.valmap(list, frame_mapped_data)
    result = pd.DataFrame(data=frame_data, columns=frame_data.keys())

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
def _convert_maybe_value(convert_func, v):
    if v in _EMPTY_CONVERTER:
        return _EMPTY_CONVERTER[v]

    return convert_func(v)


def _convert_signal_quality(signal_quality_text):
    if signal_quality_text == 'Undrained Rock Deformation':
        return 'Undrained Rock Deformation - Compressive Interaction'

    return signal_quality_text


def _parsed_date_with_correct_utc(text_time_point):
    raw_parsed_time_point = pendulum.parse(text_time_point)
    parsed_time_point = raw_parsed_time_point.set(microsecond=round(raw_parsed_time_point.microsecond, -3))
    if parsed_time_point.timezone_name != '+00:00':
        return parsed_time_point

    return parsed_time_point.set(tz=pendulum.UTC)


about_data_frame_columns = [
    AboutDataFrameColumn('aplc_ls', 'APLC_LS', _convert_maybe_value(float)),
    AboutDataFrameColumn('bh_easting', 'Bottom Hole Easting ', _convert_maybe_value(float)),
    AboutDataFrameColumn('bh_northing', 'Bottom Hole Northing ', float),
    AboutDataFrameColumn('bh_tdv', 'Bottom Hole TDV ', float),
    AboutDataFrameColumn('boundary_type', 'Boundary Type', str),
    AboutDataFrameColumn('cum_slurry', ' cum slurry [bll]', _convert_maybe_value(float)),
    AboutDataFrameColumn('delta_t', 'DeltaT', _convert_maybe_value(hms)),
    AboutDataFrameColumn('delta_t_263', 'DeltaT', _convert_maybe_value(float)),
    AboutDataFrameColumn('delta_p', 'DeltaP', _convert_maybe_value(float)),
    AboutDataFrameColumn('dept_max', 'DEPTMax', _convert_maybe_value(float)),
    AboutDataFrameColumn('dept_min', 'DEPTMin', _convert_maybe_value(float)),
    AboutDataFrameColumn('depth_tvd_ss', 'DepthTvdSs', _convert_maybe_value(float)),
    AboutDataFrameColumn('dist_3d', 'Distance3d', _convert_maybe_value(float)),
    AboutDataFrameColumn('dist_along_azm', 'Distance along the Azimuth', _convert_maybe_value(float)),
    AboutDataFrameColumn('dist_azm', 'DistanceAzimuth', _convert_maybe_value(float)),
    AboutDataFrameColumn('dist_90', 'Distance90', _convert_maybe_value(float)),
    AboutDataFrameColumn('dpo_ls_min', 'DPO_LSMin', _convert_maybe_value(float)),
    AboutDataFrameColumn('dtco', 'DTCO', _convert_maybe_value(float)),
    AboutDataFrameColumn('dtco_min', 'DTCOMin', _convert_maybe_value(float)),
    AboutDataFrameColumn('fault_no', 'FaultNr', int),
    AboutDataFrameColumn('hcal_mean', 'HCALMean', _convert_maybe_value(float)),
    AboutDataFrameColumn('hdra', 'HDRA', _convert_maybe_value(float)),
    AboutDataFrameColumn('hdra_min', 'HDRAMin', _convert_maybe_value(float)),
    AboutDataFrameColumn('horizon_marker_set', 'Horizon Marker Set', str),
    AboutDataFrameColumn('hor_dist', 'HorizontalDistance', _convert_maybe_value(float)),
    AboutDataFrameColumn('hsgrd', 'HSGRD', _convert_maybe_value(float)),
    AboutDataFrameColumn('lcal', 'LCAL', _convert_maybe_value(float)),
    AboutDataFrameColumn('lcal_mean', 'LCALMean', _convert_maybe_value(float)),
    AboutDataFrameColumn('length', 'Length', float),
    AboutDataFrameColumn('marker_description', 'Marker Description', _convert_maybe_value(str)),
    AboutDataFrameColumn('md', 'MD', _convert_maybe_value(float)),
    AboutDataFrameColumn('md_bottom', 'MDBottom', _convert_maybe_value(float)),
    AboutDataFrameColumn('mean_azm', 'MeanAzimuth', _convert_maybe_value(float)),
    AboutDataFrameColumn('monitor_name', 'MonitorName', _convert_maybe_value(str)),
    AboutDataFrameColumn('northing', 'Northing', _convert_maybe_value(float)),
    AboutDataFrameColumn('obs_set_name', 'ObservationSetName', _convert_maybe_value(str)),
    AboutDataFrameColumn('p_amplitude', 'P Amplitude', _convert_maybe_value(float)),
    AboutDataFrameColumn('part_end_time', 'PartEndTime', _convert_maybe_value(_parsed_date_with_correct_utc)),
    AboutDataFrameColumn('part_num', 'PartNumber', _convert_maybe_value(float)),
    AboutDataFrameColumn('part_end_time', 'PartEndTime', _convert_maybe_value(_parsed_date_with_correct_utc)),
    AboutDataFrameColumn('part_pump_time', 'PartPumpTime', _convert_maybe_value(float)),
    AboutDataFrameColumn('part_pumped_vol', 'StagePartPumpedVolume', _convert_maybe_value(float)),
    AboutDataFrameColumn('pefz_mean', 'PEFZMean', _convert_maybe_value(float)),
    AboutDataFrameColumn('planar_dist_azm', 'PlanarDistanceAzimuth', _convert_maybe_value(float)),
    AboutDataFrameColumn('p_net', 'Pnet', _convert_maybe_value(float)),
    AboutDataFrameColumn('proppant_conc', ' proppant concentration [ppg]', _convert_maybe_value(float)),
    AboutDataFrameColumn('proppant_mass', 'ProppantMass', _convert_maybe_value(float)),
    AboutDataFrameColumn('pump_time', 'PumpTime', _convert_maybe_value(int)),
    AboutDataFrameColumn('rhom', 'RHOM', _convert_maybe_value(float)),
    AboutDataFrameColumn('rhom_max', 'RHOMMax', _convert_maybe_value(float)),
    AboutDataFrameColumn('rhoz', 'RHOZ', _convert_maybe_value(float)),
    AboutDataFrameColumn('rla3', 'RLA3', _convert_maybe_value(float)),
    AboutDataFrameColumn('rla4_max', 'RLA4Max', _convert_maybe_value(float)),
    AboutDataFrameColumn('rla5_max', 'RLA5Max', _convert_maybe_value(float)),
    AboutDataFrameColumn('sample', 'Sample', int),
    AboutDataFrameColumn('sh_easting', 'Surface  Hole Easting ', float),
    AboutDataFrameColumn('sh_elev_msl', 'Surface Hole Elevation above MSL', _convert_maybe_value(float)),
    AboutDataFrameColumn('shortest_distance', 'Shortest distance', _convert_maybe_value(float)),
    AboutDataFrameColumn('signal_quality', 'SignalQuality', _convert_maybe_value(_convert_signal_quality)),
    AboutDataFrameColumn('slurry_rate', ' slurry rate [bpm]', _convert_maybe_value(float)),
    AboutDataFrameColumn('stage_guid', 'StageGUID', _convert_maybe_value(uuid.UUID)),
    AboutDataFrameColumn('stage_length', 'StageLength', _convert_maybe_value(float)),
    AboutDataFrameColumn('stage_pumped_vol', 'StagePumpedVolume', _convert_maybe_value(float)),
    AboutDataFrameColumn('stage_no', 'StageNumber', _convert_maybe_value(float)),
    AboutDataFrameColumn('tend_max', 'TENDMax', _convert_maybe_value(float)),
    AboutDataFrameColumn('timestamp', 'Timestamp', _convert_maybe_value(_parsed_date_with_correct_utc)),
    AboutDataFrameColumn('timestamp_local', 'Timestamp((UTC-06:00) Central Time (US & Canada))',
                         _convert_maybe_value(_parsed_date_with_correct_utc)),
    AboutDataFrameColumn('tnph_ls', 'TNPH_LS', _convert_maybe_value(float)),
    AboutDataFrameColumn('tr_pressure', ' treatment pressure [psi]', _convert_maybe_value(float)),
    AboutDataFrameColumn('tr_stg_part_no', 'TreatmentStagePartNumber', _convert_maybe_value(str)),
    AboutDataFrameColumn('tvd', 'TVD', _convert_maybe_value(float)),
    AboutDataFrameColumn('tvd_ss', 'TVDSS', _convert_maybe_value(float)),
    AboutDataFrameColumn('vert_dist', 'VerticalDistance', _convert_maybe_value(float)),
    AboutDataFrameColumn('vol_to_pick', 'VolumeToPick', _convert_maybe_value(float)),
    AboutDataFrameColumn('well', 'Well', str),
    AboutDataFrameColumn('well_name', 'WellName', _convert_maybe_value(str)),
    AboutDataFrameColumn('xf', ' Xf [ft] (Monitor: Crane-3B - stage 22)', _convert_maybe_value(float)),
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

    table_column_name, table_cells = items
    about_column = short_column_names[table_column_name]
    return about_column.full_name, toolz.map(about_column.convert_func, table_cells)


def _find_data_frame_by_id(object_id, data_frames):
    candidates = toolz.pipe(
        data_frames,
        toolz.filter(lambda df: df.object_id == object_id),
        list
    )
    assert_that(candidates, has_length(1))

    return toolz.first(candidates)
