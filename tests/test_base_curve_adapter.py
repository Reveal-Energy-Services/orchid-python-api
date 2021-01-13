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

from hamcrest import assert_that, equal_to, calling, raises

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
# - Raise exception if unrecognized unit system
class TestBaseCurveAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    @unittest.mock.patch('orchid.base_curve_adapter.UnitSystem')
    def test_sampled_quantity_units_returns_correct_units_for_us_oilfield(self, stub_net_unit_system):
        project_units = units.UsOilfield
        stub_net_us_oilfield_system = unittest.mock.MagicMock(name='stub_net_us_oilfield_system')
        stub_net_unit_system.USOilfield = unittest.mock.MagicMock(name='us_oilfield',
                                                                  return_value=stub_net_us_oilfield_system)
        self.verify_sampled_quantity_unit(project_units, stub_net_us_oilfield_system)

    def verify_sampled_quantity_unit(self, project_units, stub_net_us_oilfield_system):
        for quantity_name, expected in (('Pressure', project_units.PRESSURE),
                                        ('Temperature', project_units.TEMPERATURE),
                                        ('Surface Proppant Concentration', project_units.PROPPANT_CONCENTRATION),
                                        ('Slurry Rate', project_units.SLURRY_RATE)):
            with self.subTest(f'Testing sampled_quantity_units() for "{quantity_name}"'):
                sut = StubBaseCurveAdapter(net_project_units=stub_net_us_oilfield_system,
                                           quantity_name_unit_map={quantity_name: expected},
                                           sampled_quantity_name=quantity_name)

                actual = sut.sampled_quantity_unit()
                assert_that(actual, equal_to(expected))

    @unittest.mock.patch('orchid.base_curve_adapter.UnitSystem')
    def test_sampled_quantity_units_returns_correct_units_for_metric(self, stub_net_unit_system):
        project_units = units.Metric
        stub_net_metric_system = unittest.mock.MagicMock(name='stub_net_metric_system')
        stub_net_unit_system.Metric = unittest.mock.MagicMock(name='metric',
                                                              return_value=stub_net_metric_system)
        self.verify_sampled_quantity_unit(project_units, stub_net_metric_system)

    def test_sampled_quantity_units_raises_error_if_net_unit_system_unrecognized(self):
        sut = StubBaseCurveAdapter()

        assert_that(calling(StubBaseCurveAdapter.sampled_quantity_unit).with_args(sut), raises(KeyError))


if __name__ == '__main__':
    unittest.main()
