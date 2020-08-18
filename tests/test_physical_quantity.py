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

from orchid.physical_quantity import PhysicalQuantity


class TestPhysicalQuantity(unittest.TestCase):
    @staticmethod
    def test_canary():
        assert_that(2 + 2, equal_to(4))

    def test_enumerate_physical_quantities(self):
        actual_values = [qty.value for qty in PhysicalQuantity]
        expected_values = ['length', 'mass', 'pressure', 'proppant concentration', 'slurry rate', 'temperature']

        # noinspection PyTypeChecker
        assert_that(actual_values, contains_exactly(*expected_values))

    def test_length_to_units_net_quantity_type(self):
        # Hard-coded from UnitsNet.QuantityType.Length
        assert_that(PhysicalQuantity.LENGTH.to_units_net_quantity_type(), equal_to(47))

    def test_mass_to_units_net_quantity_type(self):
        # Hard-coded from UnitsNet.QuantityType.Mass
        assert_that(PhysicalQuantity.MASS.to_units_net_quantity_type(), equal_to(55))

    def test_pressure_to_units_net_quantity_type(self):
        # Hard-coded from UnitsNet.QuantityType.Pressure
        assert_that(PhysicalQuantity.PRESSURE.to_units_net_quantity_type(), equal_to(68))

    def test_proppant_concentration_to_units_net_quantity_type(self):
        # Hard-coded from UnitsNet.QuantityType.Ratio
        assert_that(PhysicalQuantity.PROPPANT_CONCENTRATION.to_units_net_quantity_type(), equal_to(70))

    def test_slurry_rate_to_units_net_quantity_type(self):
        # Hard-coded from UnitsNet.QuantityType.Ratio
        assert_that(PhysicalQuantity.SLURRY_RATE.to_units_net_quantity_type(), equal_to(70))

    def test_temperature_to_units_net_quantity_type(self):
        # Hard-coded from UnitsNet.QuantityType.Temperature
        assert_that(PhysicalQuantity.TEMPERATURE.to_units_net_quantity_type(), equal_to(83))
