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

from orchid import (base_curve_adapter as bca,
                    unit_system as units)


class StubBaseCurveAdapter(bca.BaseCurveAdapter):
    def __init__(self, adaptee=None,
                 net_project_units=None,
                 quantity_name_unit_map=None,
                 sampled_quantity_name=None):
        super().__init__(adaptee if adaptee else unittest.mock.MagicMock(name='stub_adaptee'))
        self._net_project_units = net_project_units
        self._quantity_name_unit_map = quantity_name_unit_map
        self._sampled_quantity_name = sampled_quantity_name

    def get_net_project_units(self):
        return self._net_project_units

    def quantity_name_unit_map(self, project_units):
        return self._quantity_name_unit_map

    @property
    def sampled_quantity_name(self):
        return self._sampled_quantity_name


# Test ideas:
class TestBaseCurveAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch('orchid.base_curve_adapter.units.as_unit_system')
    def test_sampled_quantity_units_returns_correct_units_for_pressure(self, stub_as_unit_system):
        test_data = {
            'PRESSURE': [('compressus', units.UsOilfield), ('nisus', units.Metric)],
            'TEMPERATURE': [('frigus', units.UsOilfield), ('calidus', units.Metric)],
            'PROPPANT_CONCENTRATION': [('intensio', units.UsOilfield), ('apozema', units.Metric)],
            'SLURRY_RATE': [('secundarius', units.UsOilfield), ('caputalis', units.Metric)],
        }
        for expected_quantity in test_data.keys():
            for quantity_name, unit_system in test_data[expected_quantity]:
                with self.subTest(f'Testing quantity name, "{quantity_name}", and unit system, {unit_system}'):
                    stub_as_unit_system.return_value = unit_system
                    sut = StubBaseCurveAdapter(quantity_name_unit_map={quantity_name: unit_system[expected_quantity]},
                                               sampled_quantity_name=quantity_name)
                    actual = sut.sampled_quantity_unit()

                    assert_that(actual, equal_to(unit_system[expected_quantity]))


if __name__ == '__main__':
    unittest.main()
