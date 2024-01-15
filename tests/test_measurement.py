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

import unittest

from hamcrest import assert_that, equal_to, is_, raises, calling
import pint

from orchid import (
    measurement as om,
)


# Test ideas
# - Availability of basic units
# - Availability of Quantity and Unit
# - Unit registry is application registry (supports pickle / unpickle)
class TestMeasurement(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    # Although this test (and the tests for quantity and unit) are a bit weak (easy errors in spelling), they
    # mitigate our risks by ensuring that expected attributes are available (although they **may not** have
    # the correct units.
    #
    # I was uncertain how to test that `measurement` exposed the `pint` package without (re-)testing the
    # `pint` package itself.
    #
    # To mitigate the risk of incorrect "wiring", I have created a test that samples creation of measurements
    # using different techniques.
    def test_basic_unit_availability(self):
        for unit in [
            'deg', 'min',
            'ft', 'm',
            'lb', 'kg',
            'psi', 'kPa',
            'lb/gal', 'kg/m**3',  # proppant concentration
            'oil_bbl/min', 'm**3/min',  # slurry rate
            'degF', 'degC',
        ]:
            with self.subTest(f'Test availability of units, "{unit}"'):
                assert_that(hasattr(om.registry, unit), is_(True))

    def test_quantity_availability(self):
        assert_that(hasattr(om, 'Quantity'), is_(True))

    def test_unit_availability(self):
        assert_that(hasattr(om, 'Unit'), is_(True))

    def test_is_application_registry(self):
        assert_that(pint.get_application_registry().get(), equal_to(om.registry))

    def test_sample_measurements(self):
        for actual, expected_magnitude, expected_unit in [
            (3.142 * om.registry.min, 3.142, 'min'),
            (om.Quantity(526.8, 'kg/m**3'), 526.8, 'kg/m\u00b3'),  # proppant concentration
            (om.registry('9.844e3 lbf'), 9.844e3, 'lbf'),
            (om.Quantity(130.7e3, om.Unit('kg')), 130.7e3, 'kg'),
            (om.Quantity('106.6 oil_bbl/min'), 106.6, 'oil_bbl/min'),
            (13.60 * om.registry('m**3/min'), 13.60, 'm\u00b3/min'),
            # Although Pint supports the unit `cu_ft`, we have chosen to use the synonym, `ft ** 3` (which is
            # printed as 'ft\u00b3` (that is, 'ft' followed by a Unicode superscript 3)). According to a
            # citation on [Wikipedia article](https://en.wikipedia.org/wiki/Cubic_foot), this "is the IEEE
            # symbol for the cubic foot." Our general rule: we accept the Pint unit `cu_ft` as **input**,
            # but, on various conversion, produce the Pint unit `ft**3`.
            (om.Quantity('70.10lb/ft**3'), 70.10, 'lb/ft\u00b3'),  # density (US oilfield)
        ]:
            with self.subTest(f'Test sampling unit creation with magnitude, {expected_magnitude},'
                              f' and unit, {expected_unit}.'):
                assert_that(actual.magnitude, equal_to(expected_magnitude))
                assert_that(f'{actual.units:~P}', equal_to(expected_unit))

    def test_temperature_measurements_successfully(self):
        for actual, expected_magnitude, expected_unit in [
            (om.Quantity(47.63, 'degF'), 47.63, '\u00b0F'),  # Remember that temperature **must** use `Quantity`
        ]:
            with self.subTest(f'Test sampling unit creation with magnitude, {expected_magnitude},'
                              f' and unit, {expected_unit}.'):
                assert_that(actual.magnitude, equal_to(expected_magnitude))
                assert_that(f'{actual.units:~P}', equal_to(expected_unit))

    def test_parse_temperature_text_fails(self):
        with self.subTest(f'Test exceeding limits of temperature units.'):
            assert_that(calling(om.Quantity).with_args('68.29 degC'), raises(pint.OffsetUnitCalculusError))


if __name__ == '__main__':
    unittest.main()
