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

import uuid

from hamcrest import assert_that, not_none, equal_to, has_length
import toolz.curried as toolz
import pandas as pd


@when("I query the project data frames identified by '{object_id}'")
def step_impl(context, object_id):
    """
    Args:
        context (behave.runner.Context): The test context.
        object_id (str): The string representation of the value identifying the data frame of interest.
    """
    context.data_frame_of_interest = context.project.data_frame(_as_object_id(object_id)).unwrap()
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
    assert_that(data_frame_of_interest.object_id, equal_to(_as_object_id(object_id)))

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

    # frame_columns = toolz.map(_table_column_to_data_frame_column, table.headings)
    initial_data = {h: [] for h in table.headings}
    raw_frame_data = toolz.reduce(reduce_row, table, initial_data)
    frame_mapped_data = toolz.itemmap(_table_cells_to_data_frame_cells, raw_frame_data)
    frame_data = toolz.valmap(list, frame_mapped_data)
    return pd.DataFrame(data=frame_data, columns=frame_data.keys())


# TODO: Adapted from `dot_net_dom_access.py`:
def _as_object_id(guid_text: str):
    return uuid.UUID(guid_text)


def _table_cells_to_data_frame_cells(items):
    """
    Map table cell data to data frame cells.

    Args:
        items(tuple): A tuple of the table column name and an iterable of table cells.

    Returns:
        A tuple of the transformed table column name and the transformed cells
    """
    @toolz.curry
    def convert_maybe_number(convert_func, v):
        return convert_func(v) if v else None

    table_data_frame_cells = {
        # GnG project data frame
        'sample': int,
        'sh_easting': float,
        'bh_northing': float,
        'bh_tdv': float,
        'stage_no': convert_maybe_number(int),
        'stage_length': convert_maybe_number(float),
        'p_net': convert_maybe_number(float),
        # GnG fault trace set data frame
        'length': float,
        'mean_azimuth': float,
        # GnG stage data frame
        'dept_max': convert_maybe_number(float),
        'rla4_max': convert_maybe_number(float),
        'tend_max': convert_maybe_number(float),
        'pefz_mean': convert_maybe_number(float),
        'lcal_mean': convert_maybe_number(float),
        'dpo_ls_min': convert_maybe_number(float),
    }
    table_column_name, table_cells = items
    # print(f'{table_column_name}')
    return (_table_column_to_data_frame_column(table_column_name),
            # toolz.pipe(table_cells,
            #            toolz.do(lambda c: print(list(c))),
            #            toolz.map(table_data_frame_cells[table_column_name]),
            #            ),
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
