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
import unittest
import uuid

from hamcrest import assert_that, equal_to
import pandas as pd
import pandas.testing as pdt
import toolz.curried as toolz

from orchid import native_data_frame_adapter as dfa

from tests import stub_net as tsn


# Test ideas
# - DataTable with DateTime column produces DataFrame with correct datetime cells
# - DataTable with DBNull cells produces DataFrame with corresponding cells containing `None`
class TestNativeDataFrameAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_display_name(self):
        for net_display_name, expected_display_name in [('lucrum', 'lucrum'), (None, 'Not set')]:
            with self.subTest(f'Testing .NET display name, "{net_display_name}",'
                              f' and display name "{expected_display_name}"'):
                stub_net_data_frame = tsn.create_stub_net_data_frame(display_name=net_display_name)
                sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

                assert_that(sut.display_name, equal_to(expected_display_name))

    def test_name(self):
        stub_net_data_frame = tsn.create_stub_net_data_frame(name='avus')
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        assert_that(sut.name, equal_to('avus'))

    def test_object_id(self):
        stub_net_data_frame = tsn.create_stub_net_data_frame(object_id='35582fd2-7499-4259-99b8-04b01876f309')
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        assert_that(sut.object_id, equal_to(uuid.UUID('35582fd2-7499-4259-99b8-04b01876f309')))

    def test_empty_data_table_produces_empty_pandas_data_frame(self):
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=tsn.TableDataDto([], [], toolz.identity))
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        pdt.assert_frame_equal(sut.pandas_data_frame(), pd.DataFrame())

    def test_single_cell_data_table_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([float], [{'oratio': 57.89}], toolz.identity)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_single_cell_data_table_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_columns_func = toolz.flip(toolz.get)({'stultus': 'fulmino'})
        table_data_dto = tsn.TableDataDto([str], [{'stultus': 'timeo'}], rename_columns_func)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()

        expected_data = toolz.keymap(rename_columns_func, toolz.merge_with(toolz.identity, *table_data_dto.table_data))
        expected_columns = list(toolz.map(rename_columns_func, toolz.first(table_data_dto.table_data).keys()))
        expected_data_frame = pd.DataFrame(data=expected_data,
                                           columns=expected_columns)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_single_column_many_rows_data_table_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([str],
                                          [{'rident': 'pauci'},
                                           {'rident': 'sapientes'},
                                           {'rident': 'rident'}],
                                          toolz.identity)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_single_column_many_rows_data_table_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_columns_func = toolz.flip(toolz.get)({'rident': 'hic'})
        table_data_dto = tsn.TableDataDto([str],
                                          [{'rident': 'pauci'},
                                           {'rident': 'sapientes'},
                                           {'rident': 'rident'}],
                                          rename_columns_func)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data = toolz.keymap(rename_columns_func, toolz.merge_with(toolz.identity, *table_data_dto.table_data))
        expected_columns = list(toolz.map(rename_columns_func, toolz.first(table_data_dto.table_data).keys()))
        expected_data_frame = pd.DataFrame(data=expected_data,
                                           columns=expected_columns)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_single_row_data_table_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([int],
                                          [{'plectetis': 69},
                                           {'plectetis': -62},
                                           {'plectetis': -28}],
                                          toolz.identity)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_single_row_data_table_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_columns_func = toolz.flip(toolz.get)({'Servius': 'calcaverimus'})
        table_data_dto = tsn.TableDataDto([int],
                                          [{'Servius': 24},
                                           {'Servius': 8},
                                           {'Servius': -61}],
                                          rename_columns_func)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data = toolz.keymap(rename_columns_func, toolz.merge_with(toolz.identity, *table_data_dto.table_data))
        expected_columns = list(toolz.map(rename_columns_func, toolz.first(table_data_dto.table_data).keys()))
        expected_data_frame = pd.DataFrame(data=expected_data,
                                           columns=expected_columns)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_many_rows_data_table_produces_correct_pandas_data_frame(self):
        table_data_dto = tsn.TableDataDto([str, int, float],
                                          [{'cana': 'imbris', 'querula': -203, 'recidebimus': 8.700},
                                           {'cana': 'privat', 'querula': 111, 'recidebimus': 52.02},
                                           {'cana': 'desperant', 'querula': -44, 'recidebimus': 19.52}],
                                          toolz.identity)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *table_data_dto.table_data),
                                           columns=toolz.first(table_data_dto.table_data).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)

    def test_many_columns_many_rows_data_table_with_column_mapping_produces_correct_pandas_data_frame(self):
        rename_columns_func = toolz.flip(toolz.get)({'commoda': 'Manius', 'mutabilis': 'annui', 'lenit': 'lenit'})
        table_data_dto = tsn.TableDataDto([int, str, float],
                                          [{'mutabilis': 6, 'lenit': 'imbris', 'commoda': 31.71},
                                           {'mutabilis': 52, 'lenit': 'privat', 'commoda': 65.52},
                                           {'mutabilis': 36, 'lenit': 'desperant', 'commoda': -95.01}],
                                          rename_columns_func)
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data_dto=table_data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data = toolz.keymap(rename_columns_func, toolz.merge_with(toolz.identity, *table_data_dto.table_data))
        expected_columns = list(toolz.map(rename_columns_func, toolz.first(table_data_dto.table_data).keys()))
        expected_data_frame = pd.DataFrame(data=expected_data,
                                           columns=expected_columns)
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)


if __name__ == '__main__':
    unittest.main()
