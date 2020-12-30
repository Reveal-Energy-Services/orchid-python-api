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
            ('deg', units.Common.ANGLE),
            ('min', units.Common.DURATION),
            ('lb_per_cu_ft', units.UsOilfield.DENSITY),
            ('ft-lb', units.UsOilfield.ENERGY),
            ('lbf', units.UsOilfield.FORCE),
            ('ft', units.UsOilfield.LENGTH),
            ('lb', units.UsOilfield.MASS),
            ('hp', units.UsOilfield.POWER),
            ('psi', units.UsOilfield.PRESSURE),
            ('lb_per_cu_ft', units.UsOilfield.PROPPANT_CONCENTRATION),
            ('bpm', units.UsOilfield.SLURRY_RATE),
            ('\u00b0F', units.UsOilfield.TEMPERATURE),
            ('bbl', units.UsOilfield.VOLUME),
            ('kg_per_cu_m', units.Metric.DENSITY),
            ('J', units.Metric.ENERGY),
            ('N', units.Metric.FORCE),
            ('m', units.Metric.LENGTH),
            ('kg', units.Metric.MASS),
            ('W', units.Metric.POWER),
            ('kPa', units.Metric.PRESSURE),
            ('kg_per_cu_m', units.Metric.PROPPANT_CONCENTRATION),
            ('cu_m_per_min', units.Metric.SLURRY_RATE),
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
            ('Common.ANGLE (degree)', units.Common.ANGLE),
            ('Common.DURATION (minute)', units.Common.DURATION),
            ('USOilfield.DENSITY (pound_per_cubic_foot)', units.UsOilfield.DENSITY),
            ('USOilfield.ENERGY (foot_pound)', units.UsOilfield.ENERGY),
            ('USOilfield.FORCE (pound_force)', units.UsOilfield.FORCE),
            ('USOilfield.LENGTH (foot)', units.UsOilfield.LENGTH),
            ('USOilfield.MASS (pound)', units.UsOilfield.MASS),
            ('USOilfield.POWER (horsepower)', units.UsOilfield.POWER),
            ('USOilfield.PRESSURE (psi)', units.UsOilfield.PRESSURE),
            ('USOilfield.DENSITY (pound_per_cubic_foot)', units.UsOilfield.PROPPANT_CONCENTRATION),
            ('USOilfield.SLURRY_RATE (bpm)', units.UsOilfield.SLURRY_RATE),
            ('USOilfield.TEMPERATURE (degree_Fahrenheit)', units.UsOilfield.TEMPERATURE),
            ('USOilfield.VOLUME (barrel)', units.UsOilfield.VOLUME),
            ('Metric.DENSITY (kilogram_per_cubic_meter)', units.Metric.DENSITY),
            ('Metric.ENERGY (J)', units.Metric.ENERGY),
            ('Metric.FORCE (N)', units.Metric.FORCE),
            ('Metric.LENGTH (m)', units.Metric.LENGTH),
            ('Metric.MASS (kg)', units.Metric.MASS),
            ('Metric.POWER (W)', units.Metric.POWER),
            ('Metric.PRESSURE (kPa)', units.Metric.PRESSURE),
            ('Metric.DENSITY (kilogram_per_cubic_meter)', units.Metric.PROPPANT_CONCENTRATION),
            ('Metric.SLURRY_RATE (cubic_meter_per_minute)', units.Metric.SLURRY_RATE),
            ('Metric.TEMPERATURE (degree_Celsius)', units.Metric.TEMPERATURE),
            ('Metric.VOLUME (cubic_meter)', units.Metric.VOLUME),
        ]:
            actual = str(unit)
            # Because DENSITY and PROPPANT_CONCENTRATION have the same unit, Python considers these values to
            # be equal. Beware!
            with self.subTest(f'Testing {unit}.'):
                assert_that(actual, equal_to(expected))


if __name__ == '__main__':
    unittest.main()
