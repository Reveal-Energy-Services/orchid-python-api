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

import unittest.mock

from hamcrest import assert_that, equal_to, is_
import pendulum
import toolz.curried as toolz

import numpy as np
import pandas as pd
import pandas.testing as pdt

from orchid import (
    base_time_series_adapter as bca,
    net_date_time as net_dt,
    project_loader as loader,
    unit_system as units,
)

from tests import stub_net as tsn


class StubBaseTimeSeriesAdapter(bca.BaseTimeSeriesAdapter):
    def __init__(self, adaptee=None, net_project_callable=None):
        super().__init__(adaptee if adaptee else unittest.mock.MagicMock(name='stub_adaptee'),
                         (net_project_callable if net_project_callable
                          else unittest.mock.MagicMock(name='stub_net_project_callable')))

    def quantity_name_unit_map(self, project_units):
        pass


# Test ideas:
class TestBaseCurveAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_no_data_points_time_series(self):
        stub_net_time_series = tsn.create_stub_net_time_series(tsn.DONT_CARE_ID_A, data_points=())
        sut = StubBaseTimeSeriesAdapter(stub_net_time_series)

        with unittest.mock.patch('orchid.base_time_series_adapter.loader.as_python_time_series_arrays',
                                 spec=loader.as_python_time_series_arrays,
                                 return_value=tsn.StubPythonTimesSeriesArraysDto((), ())):
            actual_data_points = sut.data_points()
        assert_that(actual_data_points.empty, is_(True))

    def test_single_data_point_time_series(self):
        object_id = tsn.DONT_CARE_ID_B
        name = 'canis'
        start_time = pendulum.parse('2019-04-30T17:36:54.311915Z')
        sample_values = (-149.037, )
        assert_equal_data_points(name, object_id, sample_values, start_time)

    def test_many_data_points_time_series(self):
        object_id = tsn.DONT_CARE_ID_C
        name = 'arbor'
        start_time = pendulum.parse('2021-02-28T13:15:01.437180')
        sample_values = (16.12, -90.80, -27.59,)
        assert_equal_data_points(name, object_id, sample_values, start_time)

    @unittest.mock.patch('orchid.dot_net_dom_access.DotNetAdapter.expect_project_units',
                         name='stub_expect_project_units',
                         new_callable=unittest.mock.PropertyMock)
    def test_sampled_quantity_units_returns_correct_units_for_pressure(self, stub_expect_project_units):
        test_data = {
            'PRESSURE': [('compressus', units.UsOilfield), ('nisus', units.Metric)],
            'TEMPERATURE': [('frigus', units.UsOilfield), ('calidus', units.Metric)],
            'PROPPANT_CONCENTRATION': [('intensio', units.UsOilfield), ('apozema', units.Metric)],
            'SLURRY_RATE': [('secundarius', units.UsOilfield), ('caputalis', units.Metric)],
        }
        for expected_quantity in test_data.keys():
            for quantity_name, unit_system in test_data[expected_quantity]:
                with self.subTest(f'Testing quantity name, "{quantity_name}", and unit system, {unit_system}'):
                    sut = StubBaseTimeSeriesAdapter()
                    stub_expect_project_units.return_value = unit_system
                    type(sut).sampled_quantity_name = unittest.mock.PropertyMock(
                        name='stub_sampled_quantity_name',
                        return_value=quantity_name,
                    )
                    sut.quantity_name_unit_map = unittest.mock.MagicMock(
                        name='stub_quantity_name_unit_map',
                        return_value={quantity_name: unit_system[expected_quantity]}
                    )
                    actual = sut.sampled_quantity_unit()

                    assert_that(actual, equal_to(unit_system[expected_quantity]))

    @unittest.mock.patch('orchid.dot_net_dom_access.DotNetAdapter.expect_project_units',
                         name='stub_expect_project_units',
                         new_callable=unittest.mock.PropertyMock)
    def test_sampled_quantity_unit_calls_quantity_name_unit_map_with_correct_project_units(self,
                                                                                           stub_expect_project_units):
        unit_system = units.Metric
        quantity_name = 'energiae'
        quantity = 'ENERGY'
        sut = StubBaseTimeSeriesAdapter()
        stub_expect_project_units.return_value = unit_system
        type(sut).sampled_quantity_name = unittest.mock.PropertyMock(
            name='stub_sampled_quantity_name',
            return_value=quantity_name,
        )
        sut.quantity_name_unit_map = unittest.mock.MagicMock(
            name='stub_quantity_name_unit_map',
            return_value={quantity_name: unit_system[quantity]}
        )

        sut.sampled_quantity_unit()

        sut.quantity_name_unit_map.assert_called_once_with(unit_system)


def assert_equal_data_points(name, object_id, sample_values, start_time):
    stub_net_time_series = tsn.create_stub_net_time_series(object_id, name)
    sut = StubBaseTimeSeriesAdapter(stub_net_time_series)
    stub_unix_time_stamps = toolz.pipe(
        tsn.create_1_second_time_points(start_time, len(sample_values)),
        toolz.map(lambda dt: int(dt.timestamp())),
        list,
    )
    stub_python_time_series_arrays_dto = tsn.StubPythonTimesSeriesArraysDto(sample_values,
                                                                            stub_unix_time_stamps)
    with unittest.mock.patch('orchid.base_time_series_adapter.loader.as_python_time_series_arrays',
                             spec=loader.as_python_time_series_arrays,
                             return_value=stub_python_time_series_arrays_dto):
        actual_data_points = sut.data_points()
        expected_sample_times = toolz.pipe(
            start_time,
            lambda st: tsn.create_1_second_time_points(st, len(sample_values)),
            toolz.map(lambda dt: int(dt.timestamp())),
            toolz.map(lambda uts: np.datetime64(uts, 's')),
            lambda tss: pd.DatetimeIndex(tss, tz='UTC'),
        )
        expected_data_points = pd.Series(index=expected_sample_times, data=sample_values, name=name)
        pdt.assert_series_equal(actual_data_points, expected_data_points)


if __name__ == '__main__':
    unittest.main()
