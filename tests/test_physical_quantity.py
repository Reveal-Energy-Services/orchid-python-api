#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
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

from hamcrest import assert_that, equal_to, contains_exactly

from orchid.physical_quantity import (PhysicalQuantity,
                                      to_physical_quantity,
                                      to_units_net_quantity_type,
                                      PROPPANT_CONCENTRATION_NAME,
                                      SLURRY_RATE_NAME)


class TestPhysicalQuantity(unittest.TestCase):
    @staticmethod
    def test_canary():
        assert_that(2 + 2, equal_to(4))

    def test_enumerate_physical_quantities(self):
        actual_values = [str(qty) for qty in PhysicalQuantity]
        expected_values = ['length', 'mass', 'pressure', 'proppant concentration', 'slurry rate', 'temperature']

        # noinspection PyTypeChecker
        assert_that(actual_values, contains_exactly(*expected_values))

    def test_physical_quantity_to_units_net_quantity_type(self):
        # The values in this map are all hard-coded from the corresponding `UnitsNet.QuantityType` member.
        physical_quantity_type_map = {PhysicalQuantity.LENGTH: 47,
                                      PhysicalQuantity.MASS: 55,
                                      PhysicalQuantity.PRESSURE: 68,
                                      PhysicalQuantity.PROPPANT_CONCENTRATION: 70,
                                      PhysicalQuantity.SLURRY_RATE: 70,
                                      PhysicalQuantity.TEMPERATURE: 83}
        for physical_quantity, quantity_type in physical_quantity_type_map.items():
            with self.subTest(physical_quantity=physical_quantity, quantity_type=quantity_type):
                assert_that(to_units_net_quantity_type(physical_quantity), equal_to(quantity_type))

    def test_units_net_quantity_type_to_physical_quantity(self):
        # The values in this map are all hard-coded from the corresponding `UnitsNet.QuantityType` member.
        quantity_type_physical_quantity_map = {(47,): PhysicalQuantity.LENGTH,
                                               (55,): PhysicalQuantity.MASS,
                                               (68,): PhysicalQuantity.PRESSURE,
                                               (70, PROPPANT_CONCENTRATION_NAME):
                                                   PhysicalQuantity.PROPPANT_CONCENTRATION,
                                               (70, SLURRY_RATE_NAME): PhysicalQuantity.SLURRY_RATE,
                                               (83,): PhysicalQuantity.TEMPERATURE}
        for quantity_type, physical_quantity in quantity_type_physical_quantity_map.items():
            with self.subTest(quantity_type=quantity_type, physical_quantity=physical_quantity):
                units_net_quantity_type = quantity_type[0]
                if len(quantity_type) == 1:
                    assert_that(to_physical_quantity(units_net_quantity_type),
                                equal_to(physical_quantity))
                else:
                    name = quantity_type[1]
                    assert_that(to_physical_quantity(units_net_quantity_type, name),
                                equal_to(physical_quantity))
