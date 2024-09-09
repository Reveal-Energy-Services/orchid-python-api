#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2024 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest
import uuid

from hamcrest import assert_that, equal_to, calling, raises
import pendulum

import pandas as pd
import pandas.testing as pdt
import toolz.curried as toolz

from orchid import (
    native_data_frame_adapter as dfa,
)

from tests import stub_net as tsn

# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, DateTimeOffset, DBNull, Guid, TimeSpan


def date_time_to_integral_milliseconds(value):
    if isinstance(value, pendulum.DateTime):
        result = value.replace(microsecond=microseconds_to_integral_milliseconds(value.microsecond))
        return result

    return value


def microseconds_to_integral_milliseconds(microseconds):
    result = round(microseconds / 1000) * 1000
    return result


# Test ideas
# - Report potentially corrupt if data frame name has tag
# - Report not potentially corrupt if data frame name no tag
class TestNativeDataFrameAdapter(unittest.TestCase):

    def test_display_name_if_set(self):
        expected = 'lucrum'
        stub_net_data_frame = tsn.create_stub_net_data_frame(display_name=expected)
        sut = dfa.NativeDataFrameAdapterIdentified(stub_net_data_frame)

        assert_that(sut.display_name, equal_to(expected))

    def test_display_name_if_none(self):
        net_value = None
        stub_net_data_frame = tsn.create_stub_net_data_frame(display_name=net_value)
        sut = dfa.NativeDataFrameAdapterIdentified(stub_net_data_frame)

        # Because `display_name` is a `property` and not simply an attribute, one cannot simply pass
        # `sut.display_name` to `calling`. (This simple action results in sending the **result** of
        # invoking the `__get__` method of `sut.display_name` (a property is a descriptor). Consequently, I create a
        # function of no arguments that simply calls `sut.display_name` to run the test.
        assert_that(calling(lambda: sut.display_name).with_args(), raises(ValueError, pattern=f'`None`'))

    def test_name(self):
        stub_net_data_frame = tsn.create_stub_net_data_frame(name='avus')
        sut = dfa.NativeDataFrameAdapterIdentified(stub_net_data_frame)

        assert_that(sut.name, equal_to('avus'))

    def test_net_cell_to_pandas_cell(self):
        for net_value, expected in [
            (108, 108),
            (49.4775, 49.4775),
            ('succurro', 'succurro'),
            (DBNull.Value, None),
            (DateTimeOffset(DateTime(2021, 1, 31, 20, 52, 52, 766, DateTimeKind.Utc).Add(TimeSpan(5108))),
             # TODO: converted value is incorrect. See GitHub bug #21.
             # Should be pendulum.datetime(2021, 1, 31, 20, 52, 52, 766511),
             pendulum.datetime(2021, 1, 31, 20, 52, 52, 766000)),
            (TimeSpan(0, 11, 52, 16, 444).Add(TimeSpan(7307)),
             pendulum.duration(hours=11, minutes=52, seconds=16, microseconds=444731)),
            (Guid('54504a96-81e6-47a0-b9dc-6770898517f8'), uuid.UUID('54504a96-81e6-47a0-b9dc-6770898517f8'))
        ]:
            with self.subTest(f'Convert .NET cell, {net_value}, to {expected}'):
                actual = dfa.net_cell_value_to_pandas_cell_value(net_value)

                assert_that(actual, equal_to(expected))

    def test_net_cell_to_pandas_cell_date_time_offset_max_value(self):
        for net_value, expected in [
            (DateTimeOffset.MaxValue, pd.NaT),
        ]:
            with self.subTest(f'Convert .NET cell, {net_value}, to {expected}'):
                actual = dfa.net_cell_value_to_pandas_cell_value(net_value)

                assert_that(pd.isna(actual), equal_to(True))

    def test_net_cell_to_pandas_cell_time_span_max_and_min_values(self):
        for net_value, expected in [
            (TimeSpan.MaxValue, pd.NaT),
            (TimeSpan.MinValue, pd.NaT),
        ]:
            with self.subTest(f'Convert .NET cell, {net_value}, to {expected}'):
                actual = dfa.net_cell_value_to_pandas_cell_value(net_value)

                assert_that(pd.isna(actual), equal_to(True))

    def test_net_cell_to_pandas_cell_3Mdays_work_around(self):
        for net_value, expected in [
            # TODO: TimeSpan 3 Mdays calculation work-around
            # The Orchid code to create the `ObservationSetDataFrame` calculates a `TimeSpan` from the "Pick Time"
            # and the stage part start time; however, one item in the .NET `DataFrame` has the corresponding
            # "Pick Time" of `DateTimeOffset.MaxValue`. Unfortunately, the calculation simply subtracts which results
            # in a very large (<~ 3 million days) but valid value. The work-around I chose to implement is to
            # transform these kinds of values into `pd.NaT`.
            #
            # This test considers the situation in which the "Pick Time" is undefined.
            (DateTimeOffset.MaxValue.Subtract(
                DateTimeOffset(DateTime(2022, 8, 17, 10, 39, 4, 470).Add(TimeSpan(6671)),
                               TimeSpan.FromTicks(0))), pd.NaT),
            # This test considers the situation in which the "Stage Part Start Time" is undefined.
            (DateTimeOffset(DateTime(2024, 9, 26, 17, 10, 29, 645).Add(TimeSpan(8001)),
                            TimeSpan.FromTicks(0)).Subtract(DateTimeOffset.MinValue), pd.NaT),
            # This test considers the situation in which the "Stage Part Start Time" is undefined.
            (DateTimeOffset(DateTime(2024, 9, 26, 17, 10, 29, 645).Add(TimeSpan(8001)),
                            TimeSpan.FromTicks(0)).Subtract(DateTimeOffset.MinValue), pd.NaT),
        ]:
            with self.subTest(f'Convert .NET cell, {net_value.ToString()}, to {expected} for too large time span'):
                actual = dfa.net_cell_value_to_pandas_cell_value(net_value)

                assert_that(pd.isna(actual))

    def test_net_cell_to_pandas_cell_net_max_date_time_offset_sentinel(self):
        for net_value, expected in [
            # TODO: Loss of fractional second work-around
            # MaxValue minus 9999998 Ticks => NaT
            (DateTimeOffset.MaxValue.Subtract(TimeSpan(9999998)), pd.NaT),
            # MaxValue minus 9999999 Ticks => NaT
            (DateTimeOffset.MaxValue.Subtract(TimeSpan(9999999)), pd.NaT),
            # MaxValue minus 1 second => actual date time offset to millisecond precision.
            # Somewhere in my conversions, a millisecond is lost
            (DateTimeOffset.MaxValue.Subtract(TimeSpan(0, 0, 1)),
             pendulum.datetime(9999, 12, 31, 23, 59, 58, 999000)),
        ]:
            with self.subTest(f'Convert .NET cell, {net_value.ToString("o")}, to {expected}'
                              f' for max date time offset sentinel'):
                actual = dfa.net_cell_value_to_pandas_cell_value(net_value)

                if pd.isna(expected):
                    assert_that(pd.isna(actual))
                else:
                    assert_that(actual, equal_to(expected))

    def test_net_cell_to_pandas_cell_too_large_time_span(self):
        too_large_time_span_boundary_in_days = 36525  # Value copied net_cell_value_to_pandas_cell_value(TimeSpan)
        for net_value, expected in [
            (TimeSpan(too_large_time_span_boundary_in_days, 0, 0, 0).Add(TimeSpan(10)), pd.NaT),
            (TimeSpan(too_large_time_span_boundary_in_days, 0, 0, 0),
             pendulum.duration(days=too_large_time_span_boundary_in_days)),
            (TimeSpan(too_large_time_span_boundary_in_days, 0, 0, 0).Subtract(TimeSpan(10)),
             pendulum.duration(days=too_large_time_span_boundary_in_days - 1, hours=23, minutes=59,
                               seconds=59, microseconds=999999)),
        ]:
            with self.subTest(f'Convert .NET cell, {net_value}, to {expected} for too large time span'):
                actual = dfa.net_cell_value_to_pandas_cell_value(net_value)

                if pd.isna(expected):
                    assert_that(pd.isna(actual))
                else:
                    assert_that(actual, equal_to(expected))

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
        sut = dfa.NativeDataFrameAdapterIdentified(stub_net_data_frame)

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
            [str, float, pendulum.DateTime, int],
            [
                {
                    'vitis': None,
                    'controversum': -14.52,
                    'indicis': pendulum.datetime(2018, 11, 20, 13, 36, 0, 331602),
                    'inane': -92,
                },
                {
                    'vitis': 'magistri',
                    'controversum': None,
                    'indicis': pendulum.datetime(2021, 5, 2, 14, 21, 11, 0),
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
                    'indicis': pendulum.datetime(2021, 11, 13, 4, 2, 46, 651626),
                    'inane': None,
                },
            ],
            toolz.identity)

        sut = _create_sut(table_data_dto)
        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = _create_expected_data_frame_with_renamed_columns(toolz.identity, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_many_rows_not_square_net_data_frame_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([int, pendulum.Duration, str, float, pendulum.DateTime],
                                          [
                                              {
                                                  'fundo': 174,
                                                  'satias': pendulum.duration(hours=5, minutes=20, seconds=0,
                                                                              microseconds=492296),
                                                  'subtile': 'moribunda',
                                                  'incumbet': 37.57,
                                                  'manemus': pendulum.datetime(year=2023, month=8, day=24,
                                                                               hour=7, minute=38, second=50,
                                                                               microsecond=10058),
                                              },
                                              {
                                                  'fundo': -304,
                                                  'satias': pendulum.duration(hours=14, minutes=39, seconds=36,
                                                                              microseconds=568450),
                                                  'subtile': 'ubique',
                                                  'incumbet': -29.82,
                                                  'manemus': pendulum.datetime(year=2026, month=12, day=22,
                                                                               hour=8, minute=54, second=55,
                                                                               microsecond=277107),
                                              },
                                              {
                                                  'fundo': 122,
                                                  'satias': pendulum.duration(hours=19, minutes=20, seconds=39,
                                                                              microseconds=232291),
                                                  'subtile': 'liminis',
                                                  'incumbet': -14.07,
                                                  'manemus': pendulum.datetime(year=2022, month=2, day=15,
                                                                               hour=13, minute=20, second=8,
                                                                               microsecond=161748),
                                              },
                                              {
                                                  'fundo': 183,
                                                  'satias': pendulum.duration(hours=10, minutes=44, seconds=8,
                                                                              microseconds=437037),
                                                  'subtile': 'trudetis',
                                                  'incumbet': 3.112,
                                                  'manemus': pendulum.datetime(year=2021, month=8, day=10,
                                                                               hour=5, minute=58, second=35,
                                                                               microsecond=277734),
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
                                          [{'pulchritudo': pendulum.parse('2024-03-15T10:09:18Z')}],
                                          rename_column_func)
        sut = _create_sut(table_data_dto)

        assert_that(calling(sut.pandas_data_frame).with_args(),
                    raises(dfa.DataFrameAdapterDateTimeError, pattern='System.DateTime'))

    def test_net_data_frame_with_date_time_offset_column_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([pendulum.DateTime],
                                          [{'obdurabis': pendulum.parse('20260329T054049.228576Z')}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)
        actual_data_frame = sut.pandas_data_frame()

        expected_data_frame = _create_expected_data_frame_with_renamed_columns(toolz.identity, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_net_data_frame_with_min_date_time_offset_raises_error(self):
        table_data_dto = tsn.TableDataDto([pendulum.DateTime],
                                          [{'prius': pendulum.DateTime.min}],
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

    def test_net_data_frame_with_max_date_time_offset_produces_nat_cell_in_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([pendulum.DateTime],
                                          [{'dies': pendulum.DateTime.max}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)
        actual_data_frame = sut.pandas_data_frame()
        actual = actual_data_frame.at[0, 'dies']

        assert_that(actual is pd.NaT, equal_to(True))

    def test_net_data_frame_with_time_span_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([pendulum.Duration],
                                          [{'strinxemus': pendulum.duration(hours=12, minutes=16,
                                                                            seconds=37, microseconds=939613)}],
                                          toolz.identity)
        sut = _create_sut(table_data_dto)
        actual_data_frame = sut.pandas_data_frame()

        expected_data_frame = _create_expected_data_frame_with_renamed_columns(toolz.identity, table_data_dto)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_potentially_corrupted(self):
        tag = ' (Potentially Corrupted)'
        for name, expected in [
            ('aequus eram' + tag, True),
            ('praenomen perspecio' + tag.replace(')', ''), False),  # no closing parenthesis (')')
            ('silis' + tag[1:], False),  # remove leading space in tag
        ]:
            with self.subTest(f'{name} is {"" if expected else " not"} potentially corrupt'):
                stub_net_data_frame = tsn.create_stub_net_data_frame(name=name)
                sut = dfa.NativeDataFrameAdapterIdentified(stub_net_data_frame)

                assert_that(sut.is_potentially_corrupt, equal_to(expected))


def _create_sut(table_data_dto):
    stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
    sut = dfa.NativeDataFrameAdapterIdentified(stub_net_data_frame)
    return sut


def _create_expected_data_frame_with_renamed_columns(rename_column_func, table_data_dto):
    expected_table_data = toolz.pipe(table_data_dto.table_data,
                                     toolz.map(toolz.valmap(date_time_to_integral_milliseconds)),
                                     list,
                                     )
    expected_data = toolz.keymap(rename_column_func, toolz.merge_with(toolz.identity, *expected_table_data))
    expected_columns = list(toolz.map(rename_column_func, toolz.first(table_data_dto.table_data).keys()))
    expected_data_frame = pd.DataFrame(data=expected_data,
                                       columns=expected_columns)
    return expected_data_frame


if __name__ == '__main__':
    unittest.main()
