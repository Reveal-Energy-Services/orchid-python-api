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

from typing import Iterable

import option
import pandas as pd
import toolz.curried as toolz

from orchid import (
    base,
    dot_net_dom_access as dna,
    net_date_time as ndt,
)

# noinspection PyUnresolvedReferences
from System import DateTimeOffset, DBNull
# noinspection PyUnresolvedReferences
from System.Data import DataTable


class NativeDataFrameAdapterDateTimeError(TypeError):
    pass


def transform_display_name(net_display_name):
    maybe_display_name = option.maybe(net_display_name)
    return maybe_display_name.unwrap_or('Not set')


class NativeDataFrameAdapter(dna.DotNetAdapter):
    def __init__(self, net_data_frame):
        super().__init__(net_data_frame, base.constantly(net_data_frame.Project))

    name = dna.dom_property('name', 'The name of this data frame.')
    display_name = dna.transformed_dom_property('display_name', 'The display name of this data frame.',
                                                transform_display_name)

    def pandas_data_frame(self) -> pd.DataFrame:
        """
        Return the `pandas` `DataFrame` built from the native `IStaticDataFrame`.

        Returns:
            A `pandas` `DataFrame`.
        """
        return _table_to_data_frame(self.dom_object.DataTable)


def _table_to_data_frame(data_table: DataTable):
    """
    Converts a .NET `DataTable` to a `pandas` `DataFrame`.

    Args:
        data_table: The .NET `DataTable` to convert.

    Returns:
        The `pandas` `DataFrame` converted from the .NET `DataTable`.
    """
    return pd.DataFrame(data=[r for r in _read_data_table(data_table)])


def _read_data_table(data_table: DataTable) -> Iterable[dict]:
    """
    Read each row of the .NET `DataTable` into an `Iterable` of  `dicts`.

    Args:
        data_table: The .NET `DataTable` to read.

    Returns:
        Yields a
    """
    # Adapted from code at
    # https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/dataset-datatable-dataview/creating-a-datareader
    # retrieved on 18-Apr-2021.

    # TODO: Use `disposable` function from https://github.com/pythonnet/pythonnet/issues/79#issuecomment-187107566
    reader = data_table.CreateDataReader()
    try:
        while True:
            if reader.HasRows:
                has_row = reader.Read()
                while has_row:
                    yield _table_row_to_dict(reader)
                    has_row = reader.Read()
            else:
                return
            if not reader.NextResult():
                break
    finally:
        reader.Dispose()


def _table_row_to_dict(reader):
    def add_to_dict(so_far, to_accumulate):
        column_name, cell_value = to_accumulate
        return toolz.assoc(so_far, column_name, cell_value)

    def to_dict(pairs):
        dict_result = toolz.reduce(add_to_dict, pairs, {})
        return dict_result

    def net_value_to_python_value(value):
        if value == DBNull.Value:
            return None

        if value == DateTimeOffset.MaxValue:
            return pd.NaT

        try:
            if str(value.GetType()) == 'System.DateTime':
                raise NativeDataFrameAdapterDateTimeError(value.GetType())

            if str(value.GetType()) == 'System.DateTimeOffset':
                return ndt.net_date_time_offset_as_datetime(value)

        except AttributeError as ae:
            if 'GetType' in str(ae):
                # Not a .NET type so simply return it
                return value

            # Re-raise the original error
            raise

    result = toolz.pipe(
        range(reader.FieldCount),
        toolz.map(lambda i: reader.GetName(i)),
        toolz.map(lambda cn: (cn, reader[cn])),
        to_dict,
        toolz.valmap(net_value_to_python_value),
    )
    return result
