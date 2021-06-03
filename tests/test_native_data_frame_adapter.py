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

import dataclasses
import datetime as dt
import unittest
import uuid

from dateutil import parser as dup
from hamcrest import assert_that, equal_to, calling, raises
import pandas as pd
import pandas.testing as pdt
import toolz.curried as toolz

from orchid import (
    net_date_time as net_dt,
    native_data_frame_adapter as dfa,
)

from tests import (
    stub_net_date_time as tdt,
    stub_net as tsn,
)

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, DateTimeOffset, DBNull, TimeSpan


def datetime_to_integral_milliseconds(value):
    if isinstance(value, type(dt.datetime.utcnow())):
        return value.replace(microsecond=round(value.microsecond / 1000) * 1000)
    return value


# Test ideas
# - Correctly translate `None` values
#   - `None` in string columns
#   - `NaN` in int columns
#   - `NaN` in float columns
#   - 'NaT` in time (DateTimeOffset) columns
# - "3 Mday" (large) work-around
# - .NET cell values to pandas cell values
#   - Translate
#     - DateTimeOffset.MaxValue to pd.NaT
#     - DateTimeOffset to dt.datetime
#     - TimeSpan to dt.timedelta
#     - Work around: "large" TimeSpan to dt.timedelta.max
#   - Raise exceptions
#     - DateTimeOffset.MinValue
#     # TimeSpan.MinValue
#     - DateTime
class TestNativeDataFrameAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name_if_set(self):
        expected = 'lucrum'
        stub_net_data_frame = tsn.create_stub_net_data_frame(display_name=expected)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        assert_that(sut.display_name, equal_to(expected))

    def test_display_name_if_none(self):
        net_value = None
        stub_net_data_frame = tsn.create_stub_net_data_frame(display_name=net_value)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        # Because `display_name` is a `property` and not simply an attribute, one cannot simply pass
        # `sut.display_name` to `calling`. (This simple action results in sending the **result** of
        # invoking the `__get__` method of `sut.display_name` (a property is a descriptor). Consequently, I create a
        # function of no arguments that simply calls `sut.display_name` to run the test.
        assert_that(calling(lambda: sut.display_name).with_args(), raises(ValueError, pattern=f'`None`'))

    def test_name(self):
        stub_net_data_frame = tsn.create_stub_net_data_frame(name='avus')
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        assert_that(sut.name, equal_to('avus'))

    def test_net_cell_to_pandas_cell(self):
        for net_value, expected in [
            (108, 108),
            (49.4775, 49.4775),
            ('succurro', 'succurro'),
            (DBNull.Value, None),
            (DateTimeOffset.MaxValue, pd.NaT),
            (DateTimeOffset(DateTime(2021, 1, 31, 20, 52, 52, 766, DateTimeKind.Utc).Add(TimeSpan(5108))),
             # TODO: converted value is incorrect. See GitHub bug #21.
             # Should be dt.datetime(2021, 1, 31, 20, 52, 52, 766511, tzinfo=dt.timezone.utc),
             dt.datetime(2021, 1, 31, 20, 52, 52, 766000, tzinfo=dt.timezone.utc)),
            (TimeSpan(0, 11, 52, 16, 444).Add(TimeSpan(7307)),
             dt.timedelta(hours=11, minutes=52, seconds=16, microseconds=444731)),
        ]:
            with self.subTest(f'Convert .NET cell, {net_value}, to {expected}'):
                actual = dfa.net_cell_value_to_pandas_cell_value(net_value)

                if net_value != DateTimeOffset.MaxValue:
                    assert_that(actual, equal_to(expected))
                else:
                    assert_that(pd.isna(actual), equal_to(True))


    def test_net_cell_to_pandas_cell_raises_specified_exception(self):
        for net_cell, expected in [
            (DateTimeOffset.MinValue, (ValueError, '`DateTimeOffset.MinValue` unexpected')),
            (DateTime(2027, 10, 11, 20, 44, 23, 483, DateTimeKind.Utc).Add(TimeSpan(9350)),
             (TypeError, '`System.DateTime` unexpected')),
        ]:
            with self.subTest(f'Convert .NET cell, {net_cell}, raises {expected}'):
                assert_that(calling(dfa.net_cell_value_to_pandas_cell_value).with_args(net_cell),
                            raises(expected[0], pattern=expected[1]))

    def test_object_id(self):
        stub_net_data_frame = tsn.create_stub_net_data_frame(object_id='35582fd2-7499-4259-99b8-04b01876f309')
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        assert_that(sut.object_id, equal_to(uuid.UUID('35582fd2-7499-4259-99b8-04b01876f309')))

    def test_empty_net_data_frame_produces_empty_pandas_data_frame(self):
        sut = _create_sut(tsn.TableDataDto([], [], toolz.identity))

        pdt.assert_frame_equal(sut.pandas_data_frame(), pd.DataFrame())

    def test_single_cell_net_data_frame_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([float], [{'oratio': 57.89}], toolz.identity)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_single_cell_net_data_frame_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_column_func = toolz.flip(toolz.get)({'stultus': 'fulmino'})
        table_data_dto = tsn.TableDataDto([str], [{'stultus': 'timeo'}], rename_column_func)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()

        expected_data_frame = _create_expected_data_frame_with_renamed_columns(rename_column_func, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_single_column_many_rows_net_data_frame_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([str],
                                          [{'rident': 'pauci'},
                                           {'rident': 'sapientes'},
                                           {'rident': 'rident'}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_single_column_many_rows_net_data_frame_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_column_func = toolz.flip(toolz.get)({'rident': 'hic'})
        table_data_dto = tsn.TableDataDto([str],
                                          [{'rident': 'pauci'},
                                           {'rident': 'sapientes'},
                                           {'rident': 'rident'}],
                                          rename_column_func)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = _create_expected_data_frame_with_renamed_columns(rename_column_func, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_single_row_net_data_frame_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([str, float, int],
                                          [{'nespila': 'pendet', 'scrupum': -23.14, 'nascor': -116}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_single_row_net_data_frame_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_column_func = toolz.flip(toolz.get)({'Servius': 'calcaverimus',
                                                    'onus': 'Patavium',
                                                    'timoris': 'timoris'})
        table_data_dto = tsn.TableDataDto([float, int, str],
                                          [{'Servius': 3.414, 'onus': 8, 'timoris': 'alescet'}],
                                          rename_column_func)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = _create_expected_data_frame_with_renamed_columns(rename_column_func, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_many_rows_net_data_frame_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([str, int, float],
                                          [{'cana': 'imbris', 'querula': -203, 'recidebimus': 8.700},
                                           {'cana': 'privat', 'querula': 111, 'recidebimus': 52.02},
                                           {'cana': 'desperant', 'querula': -44, 'recidebimus': 19.52}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_many_rows_net_data_frame_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_column_func = toolz.flip(toolz.get)({'commoda': 'Manius', 'mutabilis': 'annui', 'lenit': 'lenit'})
        table_data_dto = tsn.TableDataDto([int, str, float],
                                          [{'mutabilis': 6, 'lenit': 'imbris', 'commoda': 31.71},
                                           {'mutabilis': 52, 'lenit': 'privat', 'commoda': 65.52},
                                           {'mutabilis': 36, 'lenit': 'desperant', 'commoda': -95.01}],
                                          rename_column_func)
        sut = _create_sut(table_data_dto)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = _create_expected_data_frame_with_renamed_columns(rename_column_func, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_many_rows_net_data_frame_with_db_null_values_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto(
            [str, float, dt.datetime, int],
            [
                {
                    'vitis': None,
                    'controversum': -14.52,
                    'indicis': dt.datetime(2018, 11, 20, 13, 36, 0, 331602, tdt.utc_time_zone()),
                    'inane': -92,
                },
                {
                    'vitis': 'magistri',
                    'controversum': None,
                    'indicis': dt.datetime(2021, 5, 2, 14, 21, 11, 0, tdt.utc_time_zone()),
                    'inane': 169,
                },
                {
                    'vitis': 'inter cenam',
                    'controversum': -73.83,
                    'indicis': None,
                    'inane': 148,
                },
                {
                    'vitis': 'profuit',
                    'controversum': -40.88,
                    'indicis': dt.datetime(2021, 11, 13, 4, 2, 46, 651626, tdt.utc_time_zone()),
                    'inane': None,
                },
            ],
            toolz.identity)

        sut = _create_sut(table_data_dto)
        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = _create_expected_data_frame_with_renamed_columns(toolz.identity, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_net_data_frame_with_date_time_column_raises_error(self):
        rename_column_func = toolz.flip(toolz.get)({'pulchritudo': 'probum'})
        table_data_dto = tsn.TableDataDto(['DateTime'],
                                          [{'pulchritudo': dup.isoparse('2024-03-15T10:09:18Z')}],
                                          rename_column_func)
        sut = _create_sut(table_data_dto)

        assert_that(calling(sut.pandas_data_frame).with_args(),
                    raises(dfa.DataFrameAdapterDateTimeError, pattern='System.DateTime'))

    def test_net_data_frame_with_date_time_offset_column_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([dt.datetime],
                                          [{'obdurabis': dup.isoparse('20260329T054049.228576Z')}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)
        actual_data_frame = sut.pandas_data_frame()

        expected_data_frame = _create_expected_data_frame_with_renamed_columns(toolz.identity, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_net_data_frame_with_min_date_time_offset_raises_error(self):
        table_data_dto = tsn.TableDataDto([dt.datetime],
                                          [{'prius': dt.datetime.min}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)
        expect = (f'Unexpectedly found `DateTimeOffset.MinValue`'
                  f' at row, 0, and column, "prius", of Orchid `DataFrame`.')
        # I use the `pattern` keyword argument even though `expect` is a "degenerate" pattern; that is, it contains
        # no (significant) pattern matching characters. (It contains periods.) I use this argument because using the
        # expression `matching=equal_to(expect)` always fails even though the strings are **identical**. Either I do
        # not understand the usage of the `matching` keyword or a bug exists in the `hamcrest` package.
        assert_that(calling(sut.pandas_data_frame).with_args(),
                    raises(dfa.DataFrameAdapterDateTimeOffsetMinValueError, pattern=expect))

    def test_net_fdi_data_frame_with_max_date_time_offset_produces_nat_cell_in_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([dt.datetime],
                                          [{'dies': dt.datetime.max}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)
        actual_data_frame = sut.pandas_data_frame()
        actual = actual_data_frame.at[0, 'dies']

        assert_that(actual is pd.NaT, equal_to(True))


def _create_sut(table_data_dto):
    stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
    sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)
    return sut


def _create_expected_data_frame_with_renamed_columns(rename_column_func, table_data_dto):
    expected_table_data = toolz.pipe(table_data_dto.table_data,
                                     toolz.map(toolz.valmap(datetime_to_integral_milliseconds)),
                                     toolz.map(toolz.valmap(net_dt.dateutil_utc_to_datetime_utc)),
                                     list,
                                     )
    expected_data = toolz.keymap(rename_column_func, toolz.merge_with(toolz.identity, *expected_table_data))
    expected_columns = list(toolz.map(rename_column_func, toolz.first(table_data_dto.table_data).keys()))
    expected_data_frame = pd.DataFrame(data=expected_data,
                                       columns=expected_columns)
    return expected_data_frame


if __name__ == '__main__':
    unittest.main()
