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

import decimal
import unittest

from orchid import (
    measurement as om,
    unit_system as units,
)

from tests import (custom_matchers as tcm)

from hamcrest import assert_that, equal_to


class TestUnitSystem(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_abbreviation(self):
        for expected, unit in [
            ('deg', units.Common.ANGLE),
            ('min', units.Common.DURATION),
            ('lb/ft\u00b3', units.UsOilfield.DENSITY),
            ('ft_lb', units.UsOilfield.ENERGY),
            ('lbf', units.UsOilfield.FORCE),
            ('ft', units.UsOilfield.LENGTH),
            ('lb', units.UsOilfield.MASS),
            ('hp', units.UsOilfield.POWER),
            ('psi', units.UsOilfield.PRESSURE),
            ('lb/gal', units.UsOilfield.PROPPANT_CONCENTRATION),
            ('oil_bbl/min', units.UsOilfield.SLURRY_RATE),
            ('\u00b0F', units.UsOilfield.TEMPERATURE),
            ('oil_bbl', units.UsOilfield.VOLUME),
            ('kg/m\u00b3', units.Metric.DENSITY),
            ('J', units.Metric.ENERGY),
            ('N', units.Metric.FORCE),
            ('m', units.Metric.LENGTH),
            ('kg', units.Metric.MASS),
            ('W', units.Metric.POWER),
            ('kPa', units.Metric.PRESSURE),
            ('kg/m\u00b3', units.Metric.PROPPANT_CONCENTRATION),
            ('m\u00b3/min', units.Metric.SLURRY_RATE),
            ('\u00b0C', units.Metric.TEMPERATURE),
            ('m\u00b3', units.Metric.VOLUME),
        ]:
            with self.subTest(f'Testing abbreviation for unit {unit!r}'):
                assert_that(unit.abbreviation(), equal_to(expected))

    def test_abbreviation_function(self):
        for expected, unit in [
            ('deg', units.Common.ANGLE),
            ('min', units.Common.DURATION),
            ('ft_lb', units.UsOilfield.ENERGY),
            ('lbf', units.UsOilfield.FORCE),
            ('lb/gal', units.UsOilfield.PROPPANT_CONCENTRATION),
            ('oil_bbl/min', units.UsOilfield.SLURRY_RATE),
            ('kg/m\u00b3', units.Metric.DENSITY),
            ('kg/m\u00b3', units.Metric.PROPPANT_CONCENTRATION),
            ('m\u00b3/min', units.Metric.SLURRY_RATE),
            ('\u00b0C', units.Metric.TEMPERATURE),
        ]:
            with self.subTest(f'Testing abbreviation for unit {unit!r}'):
                assert_that(unit.abbreviation(), equal_to(expected))

    def test_make_measurement_from_unit(self):
        for expected_magnitude, actual_unit, expected_unit, tolerance in [
            (94.17, units.Common.ANGLE, om.registry.deg, decimal.Decimal('0.01')),
            (34.34, units.Common.DURATION, om.registry.min, decimal.Decimal('0.01')),
            (71.08, units.UsOilfield.DENSITY, om.registry.lb / om.registry.ft ** 3, decimal.Decimal('0.01')),
            (971.8, units.Metric.DENSITY, om.registry.kg / om.registry.m ** 3, decimal.Decimal('0.1')),
            (4.679, units.UsOilfield.ENERGY, om.registry.ft_lb, decimal.Decimal('0.001')),
            (8809, units.Metric.ENERGY, om.registry.J, decimal.Decimal('1')),
            (99.47e3, units.UsOilfield.FORCE, om.registry.lbf, decimal.Decimal('0.01')),
            (530.6e3, units.Metric.FORCE, om.registry.N, decimal.Decimal('0.1e3')),
            (127.0, units.UsOilfield.LENGTH, om.registry.ft, decimal.Decimal('0.1')),
            (45.12, units.Metric.LENGTH, om.registry.m, decimal.Decimal('0.01')),
            (7087, units.UsOilfield.MASS, om.registry.lb, decimal.Decimal('1')),
            (132.8, units.Metric.MASS, om.registry.kg, decimal.Decimal('0.1')),
            (20.31, units.UsOilfield.POWER, om.registry.hp, decimal.Decimal('0.01')),
            (13.55, units.Metric.POWER, om.registry.W, decimal.Decimal('0.01')),
            (7743, units.UsOilfield.PRESSURE, om.registry.psi, decimal.Decimal('1')),
            (54.54, units.Metric.PRESSURE, om.registry.kPa, decimal.Decimal('0.01')),
            (3.500, units.UsOilfield.PROPPANT_CONCENTRATION,
             om.registry.lb / om.registry.gal, decimal.Decimal('0.001')),
            (679.9, units.Metric.PROPPANT_CONCENTRATION,
             om.registry.kg / om.registry.m ** 3, decimal.Decimal('0.1')),
            (90.96, units.UsOilfield.SLURRY_RATE, om.registry.oil_bbl / om.registry.min, decimal.Decimal('0.01')),
            (13.02, units.Metric.SLURRY_RATE, om.registry.m ** 3 / om.registry.min, decimal.Decimal('0.01')),
            (52.74, units.UsOilfield.TEMPERATURE, om.registry.degF, decimal.Decimal('0.01')),
            (17.88, units.Metric.TEMPERATURE, om.registry.degC, decimal.Decimal('0.01')),
            (9318, units.UsOilfield.VOLUME, om.registry.oil_bbl, decimal.Decimal('1')),
            (766.4, units.Metric.VOLUME, om.registry.m ** 3, decimal.Decimal('0.1')),
        ]:
            with self.subTest(f'Test making measurement from unit, {actual_unit!r}'):
                actual = units.make_measurement(actual_unit, expected_magnitude)

                tcm.assert_that_measurements_close_to(actual, om.Quantity(expected_magnitude, expected_unit),
                                                      tolerance)

    def test_str(self):
        for expected, unit in [
            ('degree', units.Common.ANGLE),
            ('minute', units.Common.DURATION),
            ('pound / foot ** 3', units.UsOilfield.DENSITY),
            ('foot_pound', units.UsOilfield.ENERGY),
            ('force_pound', units.UsOilfield.FORCE),
            ('foot', units.UsOilfield.LENGTH),
            ('pound', units.UsOilfield.MASS),
            ('horsepower', units.UsOilfield.POWER),
            ('pound_force_per_square_inch', units.UsOilfield.PRESSURE),
            ('pound / gallon', units.UsOilfield.PROPPANT_CONCENTRATION),
            ('oil_barrel / minute', units.UsOilfield.SLURRY_RATE),
            ('degree_Fahrenheit', units.UsOilfield.TEMPERATURE),
            ('oil_barrel', units.UsOilfield.VOLUME),
            ('kilogram / meter ** 3', units.Metric.DENSITY),
            ('joule', units.Metric.ENERGY),
            ('newton', units.Metric.FORCE),
            ('meter', units.Metric.LENGTH),
            ('kilogram', units.Metric.MASS),
            ('watt', units.Metric.POWER),
            ('kilopascal', units.Metric.PRESSURE),
            ('kilogram / meter ** 3', units.Metric.PROPPANT_CONCENTRATION),
            ('meter ** 3 / minute', units.Metric.SLURRY_RATE),
            ('degree_Celsius', units.Metric.TEMPERATURE),
            ('meter ** 3', units.Metric.VOLUME),
        ]:
            actual = str(unit)
            with self.subTest(f'Testing string representation of {unit!r}.'):
                assert_that(actual, equal_to(expected))


if __name__ == '__main__':
    unittest.main()
