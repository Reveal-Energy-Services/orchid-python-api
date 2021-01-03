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

from orchid import unit_system as units

from hamcrest import assert_that, equal_to


class TestUnitSystem(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_abbreviation(self):
        for expected, unit in [
            ('\u00b0', units.Common.ANGLE),
            ('min', units.Common.DURATION),
            ('lb/ft\u00b3', units.UsOilfield.DENSITY),
            ('ft-lb', units.UsOilfield.ENERGY),
            ('lbf', units.UsOilfield.FORCE),
            ('ft', units.UsOilfield.LENGTH),
            ('lb', units.UsOilfield.MASS),
            ('hp', units.UsOilfield.POWER),
            ('psi', units.UsOilfield.PRESSURE),
            ('lb/ft\u00b3', units.UsOilfield.PROPPANT_CONCENTRATION),
            ('bpm', units.UsOilfield.SLURRY_RATE),
            ('\u00b0F', units.UsOilfield.TEMPERATURE),
            ('bbl', units.UsOilfield.VOLUME),
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
            actual = units.abbreviation(unit)
            # Because DENSITY and PROPPANT_CONCENTRATION have the same unit, Python considers PROPPANT_CONCENTRATION
            # to be an alias for DENSITY. When invoking `str` and `repr`, these members appear to be the same.
            with self.subTest(f'Testing {unit.system_name()} {unit.name}.'):
                assert_that(actual, equal_to(expected))

    def test_str(self):
        for expected, unit in [
            ('Common.ANGLE (unit=degree, physical_quantity=angle)', units.Common.ANGLE),
            ('Common.DURATION (unit=minute, physical_quantity=duration)', units.Common.DURATION),
            ('USOilfield.DENSITY (unit=pound_per_cubic_foot, physical_quantity=density)', units.UsOilfield.DENSITY),
            ('USOilfield.ENERGY (unit=foot_pound, physical_quantity=energy)', units.UsOilfield.ENERGY),
            ('USOilfield.FORCE (unit=pound_force, physical_quantity=force)', units.UsOilfield.FORCE),
            ('USOilfield.LENGTH (unit=foot, physical_quantity=length)', units.UsOilfield.LENGTH),
            ('USOilfield.MASS (unit=pound, physical_quantity=mass)', units.UsOilfield.MASS),
            ('USOilfield.POWER (unit=horsepower, physical_quantity=power)', units.UsOilfield.POWER),
            ('USOilfield.PRESSURE (unit=psi, physical_quantity=pressure)', units.UsOilfield.PRESSURE),
            ('USOilfield.PROPPANT_CONCENTRATION (unit=pound_per_cubic_foot, physical_quantity=proppant concentration)',
             units.UsOilfield.PROPPANT_CONCENTRATION),
            ('USOilfield.SLURRY_RATE (unit=bpm, physical_quantity=slurry rate)', units.UsOilfield.SLURRY_RATE),
            ('USOilfield.TEMPERATURE (unit=degree_Fahrenheit, physical_quantity=temperature)',
             units.UsOilfield.TEMPERATURE),
            ('USOilfield.VOLUME (unit=barrel, physical_quantity=volume)', units.UsOilfield.VOLUME),
            ('Metric.DENSITY (unit=kilogram_per_cubic_meter, physical_quantity=density)', units.Metric.DENSITY),
            ('Metric.ENERGY (unit=J, physical_quantity=energy)', units.Metric.ENERGY),
            ('Metric.FORCE (unit=N, physical_quantity=force)', units.Metric.FORCE),
            ('Metric.LENGTH (unit=m, physical_quantity=length)', units.Metric.LENGTH),
            ('Metric.MASS (unit=kg, physical_quantity=mass)', units.Metric.MASS),
            ('Metric.POWER (unit=W, physical_quantity=power)', units.Metric.POWER),
            ('Metric.PRESSURE (unit=kPa, physical_quantity=pressure)', units.Metric.PRESSURE),
            ('Metric.PROPPANT_CONCENTRATION (unit=kilogram_per_cubic_meter, physical_quantity=proppant concentration)',
             units.Metric.PROPPANT_CONCENTRATION),
            ('Metric.SLURRY_RATE (unit=cubic_meter_per_minute, physical_quantity=slurry rate)',
             units.Metric.SLURRY_RATE),
            ('Metric.TEMPERATURE (unit=degree_Celsius, physical_quantity=temperature)', units.Metric.TEMPERATURE),
            ('Metric.VOLUME (unit=cubic_meter, physical_quantity=volume)', units.Metric.VOLUME),
        ]:
            actual = str(unit)
            # Because DENSITY and PROPPANT_CONCENTRATION have the same unit, Python considers these values to
            # be equal. Beware!
            with self.subTest(f'Testing {unit}.'):
                assert_that(actual, equal_to(expected))


if __name__ == '__main__':
    unittest.main()
