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

from orchid import unit_system as units

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
            ('bpm', units.UsOilfield.SLURRY_RATE),
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
            ('oil_barrel_per_minute', units.UsOilfield.SLURRY_RATE),
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
