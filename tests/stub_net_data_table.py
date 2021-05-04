#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


import datetime as dt

import orchid

import option
import toolz.curried as toolz

# noinspection PyUnresolvedReferences
from System import DateTime, DBNull, Type
# noinspection PyUnresolvedReferences
from System.Data import DataTable, DataColumn


# The `dump_xxx` and `format_yyy` functions are currently diagnostic tools.
def dump_table(data_table):
    dump_column_names(data_table)
    dump_rows(data_table)


def dump_column_names(data_table):
    print(f'{"".join([" "] * 8):8}'
          f' | {data_table.Columns[0].ColumnName:8}'
          f' | {data_table.Columns[1].ColumnName:8}'
          f' | {data_table.Columns[2].ColumnName:12}'
          f' | {data_table.Columns[2].ColumnName:32} |')


def dump_rows(data_table):
    for i, row in enumerate(data_table.Rows):
        print(format_row(i, row))


def format_row(i, row):
    return (f'row {i: 4}'
            f' | {format_row_value(maybe_row_value(row[0])):8}'
            f' | {format_row_value(maybe_row_value(row[1])):8}'
            f' | {format_row_value(maybe_row_value(row[2])):12}'
            f' | {format_row_value(maybe_row_value(row[3])):32} |')


def dump_column_details(data_table):
    print('Column Details:')
    for c in data_table.Columns:
        print(f'    Name: {c.ColumnName}')
        print(f'    Type: {str(c.DataType)}')
        print(f'    Read-only: {c.ReadOnly}')
    print('')


def format_row_value(maybe_value):
    return maybe_value.map_or_else(format_some_value, lambda: 'Nothing')


def format_some_value(value):
    if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
        return value

    if type(value) == DateTime:
        return value.ToString('o')

    raise TypeError(value)


def maybe_row_value(value):
    if DBNull.Value.Equals(value):
        return option.NONE

    return option.Some(value)


# The `populate_data_table` function converts an iterable of identically structured `dicts` into a .NET `DataTable`
# example_to_convert = [
#     {'foo': 3, 'bar': 3.414, 'baz': 'abc', 'quux': dup.isoparse('3414-02-07T18:14:14Z')},
#     {'foo': 2, 'bar': 2.718, 'baz': 'def', 'quux': dup.isoparse('2718-01-04T14:01:07Z')},
#     {'foo': 1, 'bar': 1.414, 'baz': 'ghi', 'quux': dup.isoparse('1414-01-07T17:34:14Z')},
# ]


def populate_data_table(data_tag_to_net_column_name_func, from_data):
    """
    Construct a .NET `DataTable` from an iterable of `dicts`

    The `populate_data_table` function converts an iterable of identically structured `dicts` into a .NET `DataTable`
    example_to_convert = [
        {'foo': 3, 'bar': 3.414, 'baz': 'abc', 'quux': dup.isoparse('3414-02-07T18:14:14Z')},
        {'foo': 2, 'bar': 2.718, 'baz': 'def', 'quux': dup.isoparse('2718-01-04T14:01:07Z')},
        {'foo': 1, 'bar': 1.414, 'baz': 'ghi', 'quux': dup.isoparse('1414-01-07T17:34:14Z')},
    ]

    Args:
        data_tag_to_net_column_name_func: Callable to convert data "tags" to .NET `DataTable` column names
        from_data: The iterable of `dicts` (tag-value pairs) to convert

    Returns:
        The .NET DataTable whose cells contain the data in `from_data`
    """
    if len(from_data) == 0:
        return DataTable()

    with_columns = toolz.pipe(
        from_data,
        toolz.map(toolz.keymap(data_tag_to_net_column_name_func)),
        list,
    )

    result = toolz.pipe(
        DataTable(),
        add_data_table_columns(with_columns),
        add_data_table_rows(with_columns),
    )
    return result


@toolz.curry
def add_data_table_columns(from_data, data_table):
    for net_column_name, row_value in toolz.first(from_data).items():
        new_column = make_data_table_column(net_column_name, row_value)
        data_table.Columns.Add(new_column)
    return data_table


def make_data_table_column(net_column_name, row_value):
    new_column = DataColumn()
    new_column.ColumnName = net_column_name
    new_column.DataType = make_data_column_type(row_value)
    new_column.ReadOnly = True
    return new_column


# An example of a callable to convert a sequence of `str` "tags" to .NET column names
# @toolz.curry
# def data_tag_to_net_column_name(data_name):
#     mapper = {'foo': 'Foo',
#               'bar': 'Bar',
#               'baz': 'Baz', }
#     try:
#         return mapper[data_name]
#     except KeyError:
#         if data_name == 'quux':
#             return "Quark"
#         raise


def make_data_column_type(row_value):
    mapper = {int: 'System.Int32',
              float: 'System.Double',
              str: 'System.String'}

    sought = type(row_value)
    try:
        return Type.GetType(mapper[sought])
    except KeyError:
        if sought == dt.datetime:
            return Type.GetType('System.DateTime')
        raise


@toolz.curry
def add_data_table_rows(from_data, data_table):
    for row_data in from_data:
        new_row = make_data_table_row(data_table, row_data)
        data_table.Rows.Add(new_row)
    return data_table


def make_data_table_row(data_table, row_data):
    data_table_row = data_table.NewRow()
    for net_column_name, row_value in row_data.items():
        if data_table.Columns[net_column_name].DataType != DateTime:
            data_table_row[net_column_name] = row_value
        else:
            # noinspection PyUnresolvedReferences
            data_table_row[net_column_name] = orchid.net_quantity.as_net_date_time(row_value)
    return data_table_row
