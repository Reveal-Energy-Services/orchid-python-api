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

from dateutil import parser as dup
from hamcrest import assert_that, not_none, equal_to, has_length
import toolz.curried as toolz
import pandas as pd

from orchid import (
    dot_net_dom_access as dna,
    net_date_time as net_dt,
)


@when("I query the project data frames identified by '{object_id}'")
def step_impl(context, object_id):
    """
    Args:
        context (behave.runner.Context): The test context.
        object_id (str): The string representation of the value identifying the data frame of interest.
    """
    context.data_frame_of_interest = context.project.data_frame(dna.as_object_id(object_id)).unwrap()
    assert_that(context.data_frame_of_interest, not_none())


@then("I see a single data frame identified by {object_id}, {name} and {display_name}")
def step_impl(context, object_id, name, display_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        object_id (str): The textual representation of the UUID identifying the data frame of interest.
        name (str): The name of the data frame of interest.
        display_name (str): The name of the data frame of interest used for display purposes.
    """
    data_frame_of_interest = context.data_frame_of_interest
    assert_that(data_frame_of_interest.object_id, equal_to(dna.as_object_id(object_id)))

    assert_that(data_frame_of_interest.name, equal_to(name))
    assert_that(data_frame_of_interest.display_name, equal_to(display_name))


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


@then("I see the sampled cells")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    expected = _as_data_frame(context.table)
    actual_data_frame = context.data_frame_of_interest.pandas_data_frame()
    sampled_data_frame_rows = actual_data_frame.iloc[list(expected['Sample'].values), :]
    sampled_data_frame_cols = sampled_data_frame_rows.loc[:, expected.columns[1:]]
    sampled_data_frame_cols.reset_index(inplace=True)
    sampled_data_frame = sampled_data_frame_cols.rename(columns={'index': 'Sample'})
    pd.testing.assert_frame_equal(sampled_data_frame, expected)


def _as_data_frame(table):
    def reduce_row(so_far, row_to_reduce):
        row_data = {h: [row_to_reduce[h]] for h in row_to_reduce.headings}
        return toolz.merge_with(toolz.concat, so_far, row_data)

    initial_data = {h: [] for h in table.headings}
    raw_frame_data = toolz.reduce(reduce_row, table, initial_data)
    frame_mapped_data = toolz.itemmap(_table_cells_to_data_frame_cells, raw_frame_data)
    frame_data = toolz.valmap(list, frame_mapped_data)
    return pd.DataFrame(data=frame_data, columns=frame_data.keys())


def _table_cells_to_data_frame_cells(items):
    """
    Map table cell data to data frame cells.

    Args:
        items(tuple): A tuple of the table column name and an iterable of table cells.

    Returns:
        A tuple of the transformed table column name and the transformed cells
    """
    @toolz.curry
    def convert_maybe_value(convert_func, v):
        return convert_func(v) if v else None

    parsed_date_with_correct_utc = toolz.compose(net_dt.dateutil_utc_to_datetime_utc,
                                                 dup.parse, )

    table_data_frame_cells = {
        # GnG project data frame
        'sample': int,
        'sh_easting': float,
        'bh_northing': float,
        'bh_tdv': float,
        'stage_no': convert_maybe_value(int),
        'stage_length': convert_maybe_value(float),
        'p_net': convert_maybe_value(float),
        # GnG fault trace set data frame
        'length': float,
        'mean_azimuth': float,
        # GnG stage data frame
        'dept_max': convert_maybe_value(float),
        'rla4_max': convert_maybe_value(float),
        'tend_max': convert_maybe_value(float),
        'pefz_mean': convert_maybe_value(float),
        'lcal_mean': convert_maybe_value(float),
        'dpo_ls_min': convert_maybe_value(float),
        # GnG well log set data frame
        'tvd_ss': convert_maybe_value(float),
        'rla3': convert_maybe_value(float),
        'dtco': convert_maybe_value(float),
        'hdra': convert_maybe_value(float),
        'rhoz': convert_maybe_value(float),
        'lcal': convert_maybe_value(float),
        # GnG horizon marker set data frame
        'marker_description': convert_maybe_value(str),
        'horizon_marker_set': str,
        'boundary_type': str,
        'well': str,
        'md': convert_maybe_value(float),
        'tvd': convert_maybe_value(float),
        # Permian project data frame
        'bh_easting': convert_maybe_value(float),
        'md_bottom': convert_maybe_value(float),
        'part_end_time': convert_maybe_value(parsed_date_with_correct_utc),
        'part_pumped_vol': convert_maybe_value(float),
        'pnet': convert_maybe_value(float),
        'pump_time': convert_maybe_value(int),
        # Permian FDI data frame
        'obs_set_name': str,
        'part_no': str,
        'timestamp': convert_maybe_value(parsed_date_with_correct_utc),
        'delta_t': convert_maybe_value(str),
        'delta_p': convert_maybe_value(float),
        'vol_to_pick': convert_maybe_value(float),
        # Permian microseismic data frame
        # 'timestamp': convert_maybe_value(parsed_date_with_correct_utc),
        'northing': convert_maybe_value(float),
        'depth_tvd_ss': convert_maybe_value(float),
        'dist_3d': convert_maybe_value(float),
        'planar_dist_azm': convert_maybe_value(float),
        'vert_dist': convert_maybe_value(float),
    }
    table_column_name, table_cells = items
    return (_table_column_to_data_frame_column(table_column_name),
            toolz.map(table_data_frame_cells[table_column_name], table_cells),
            )


def _table_column_to_data_frame_column(table_column_name):
    """
    Convert a table column heading ta a data frame column heading.

    Args:
        table_column_name: The expected table column heading.

    Returns:
        The data frame column name corresponding to `table_column_name`.
    """
    table_data_frame_columns = {
        # GnG project data frame
        'sample': 'Sample',
        'sh_easting': 'Surface  Hole Easting ',
        'bh_northing': 'Bottom Hole Northing ',
        'bh_tdv': 'Bottom Hole TDV ',
        'stage_no': 'StageNumber',
        'stage_length': 'StageLength',
        'p_net': 'Pnet',
        # GnG fault trace set data frame
        'length': 'Length',
        'mean_azimuth': 'MeanAzimuth',
        # GnG stage data frame
        'dept_max': 'DEPTMax',
        'rla4_max': 'RLA4Max',
        'tend_max': 'TENDMax',
        'pefz_mean': 'PEFZMean',
        'lcal_mean': 'LCALMean',
        'dpo_ls_min': 'DPO_LSMin',
        # GnG well log set data frame
        'tvd_ss': 'TVDSS',
        'rla3': 'RLA3',
        'dtco': 'DTCO',
        'hdra': 'HDRA',
        'rhoz': 'RHOZ',
        'lcal': 'LCAL',
        # GnG horizon marker set data frame
        'marker_description': 'Marker Description',
        'horizon_marker_set': 'Horizon Marker Set',
        'boundary_type': 'Boundary Type',
        'well': 'Well',
        'md': 'MD',
        'tvd': 'TVD',
        # Permian project data frame
        'bh_easting': 'Bottom Hole Easting ',
        'md_bottom': 'MDBottom',
        'part_end_time': 'PartEndTime',
        'part_pumped_vol': 'StagePartPumpedVolume',
        'pnet': 'Pnet',
        'pump_time': 'PumpTime',
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
