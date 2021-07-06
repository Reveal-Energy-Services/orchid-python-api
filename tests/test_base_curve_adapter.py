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

from hamcrest import assert_that, equal_to

from orchid import (
    base_time_series_adapter as bca,
    unit_system as units,
)


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


if __name__ == '__main__':
    unittest.main()
