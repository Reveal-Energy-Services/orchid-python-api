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

import unittest
import uuid

from hamcrest import assert_that, equal_to
import pandas as pd
import pandas.testing as pdt
import toolz.curried as toolz

from orchid import native_data_frame_adapter as dfa

from tests import stub_net as tsn


# Test ideas
# - DataTable with single cell and mapped column name produces DataFrame with mapped column name and cell
# - DataTable with single column and many rows produces DataFrame with same column and many cells
# - DataTable with single mapped column and many rows produces DataFrame with mapped column and many cells
# - DataTable with many columns and single row produces DataFrame with same columns and single cell
# - DataTable with many mapped columns and single row produces DataFrame with mapped columns and correct cell
# - DataTable with many columns and many rows produces DataFrame with correct columns and cells
# - DataTable with many mapped columns and many rows produces DataFrame with mapped columns and cells
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
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data=[])
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        pdt.assert_frame_equal(sut.pandas_data_frame(), pd.DataFrame())

    def test_single_cell_data_table_produces_correct_pandas_data_frame(self):
        data_dto = [{'oratio': 57.89}]
        stub_net_data_frame = tsn.create_stub_net_data_frame(table_data=data_dto)
        sut = dfa.NativeDataFrameAdapter(stub_net_data_frame)

        actual_data_frame = sut.pandas_data_frame()
        expected_data_frame = pd.DataFrame(data=toolz.merge_with(toolz.identity, *data_dto),
                                           columns=toolz.first(data_dto).keys())
        pdt.assert_frame_equal(actual_data_frame, expected_data_frame)


if __name__ == '__main__':
    unittest.main()
