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


from abc import abstractmethod
from collections import namedtuple
from enum import Enum
import pathlib

from pint import UnitRegistry

from orchid import (physical_quantity as opq)


# noinspection PyUnresolvedReferences
import UnitsNet


# This is the single location to find the `pint.UnitRegistry`. The `pint` package considers units returned
# from different instances of `UnitRegistry` to be different. See the documentation at
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects for details.
_registry = UnitRegistry()
_registry.load_definitions(str(pathlib.Path(__file__).parent.resolve().joinpath('orchid_units.txt')))

# Expose general types for use by type annotations
Quantity = _registry.Quantity
Unit = _registry.Unit


# I use this private class to distinguish units that measure **different** physical quantities but use the
# same measurement unit. Currently, this applies to DENSITY and PRESSURE.
_AboutUnit = namedtuple('AboutUnit', ['unit', 'physical_quantity'])


class UnitSystem(Enum):

    def __str__(self):
        """
        Return a string representation of the member.

        Note that this method plays the role of "Template Method" in the _Template Method_ design pattern. In
        this role it calls the "Primitive Operation", `unit_str()` to get the string identifying the unit.

        Returns:
            The string representing the enumeration member.
        """
        return f'{self.system_name()}.{self.name} (unit={self.unit_str()},' \
               f' physical_quantity={self.value.physical_quantity.value})'

    @abstractmethod
    def system_name(self):
        raise NotImplementedError()

    def unit_str(self):
        return f'{str(self.value.unit)}'


class Common(UnitSystem):
    """The enumeration of units common to both U. S. oilfield and metric unit systems."""

    ANGLE = _AboutUnit(_registry.deg, opq.PhysicalQuantity.ANGLE)
    DURATION = _AboutUnit(_registry.min, opq.PhysicalQuantity.DURATION)

    def system_name(self):
        return 'Common'


# TODO: remove
class UsOilfield(UnitSystem):
    """The enumeration of U. S. oilfield units available via the Orchid Python API.

    BEWARE!

    Because DENSITY and PROPPANT_CONCENTRATION have the same unit, Python considers PROPPANT_CONCENTRATION
    to be an alias for DENSITY. When invoking `str` and `repr`, these members appear to be the same.

    BEWARE!
    """

    DENSITY = _AboutUnit(_registry.pound_per_cubic_foot, opq.PhysicalQuantity.DENSITY)
    ENERGY = _AboutUnit(_registry.foot_pound, opq.PhysicalQuantity.ENERGY)
    FORCE = _AboutUnit(_registry.pound_force, opq.PhysicalQuantity.FORCE)
    LENGTH = _AboutUnit(_registry.foot, opq.PhysicalQuantity.LENGTH)
    MASS = _AboutUnit(_registry.pound, opq.PhysicalQuantity.MASS)
    POWER = _AboutUnit(_registry.horsepower, opq.PhysicalQuantity.POWER)
    PRESSURE = _AboutUnit(_registry.pound_force_per_square_inch, opq.PhysicalQuantity.PRESSURE)
    PROPPANT_CONCENTRATION = _AboutUnit(_registry.pound_per_gallon, opq.PhysicalQuantity.PROPPANT_CONCENTRATION)
    SLURRY_RATE = _AboutUnit(_registry.oil_barrel_per_minute, opq.PhysicalQuantity.SLURRY_RATE)
    TEMPERATURE = _AboutUnit(_registry.degree_Fahrenheit, opq.PhysicalQuantity.TEMPERATURE)
    VOLUME = _AboutUnit(_registry.oil_barrel, opq.PhysicalQuantity.VOLUME)

    def system_name(self):
        return 'USOilfield'

    def unit_str(self):
        """
        Returns a string representing the unit of this enumeration member.

        This method plays the role of "Primitive Operation" in the _Template Method_ design pattern.
        This method is called by the "Template Method" to allow customization of the "Template Method"
        **without** changing the algorithm of the "Template Method."

        Returns:
            The string representation of the unit.
        """
        if self == UsOilfield.FORCE:
            return 'pound_force'

        if self == UsOilfield.PRESSURE:
            return 'psi'

        if self == UsOilfield.SLURRY_RATE:
            return 'bpm'

        if self == UsOilfield.VOLUME:
            return 'barrel'

        return super().unit_str()


# TODO: remove
class Metric(UnitSystem):
    """The enumeration of metric units available via the Orchid Python API.

    BEWARE!

    Because DENSITY and PROPPANT_CONCENTRATION have the same unit, Python considers PROPPANT_CONCENTRATION
    to be an alias for DENSITY. When invoking `str` and `repr`, these members appear to be the same.

    BEWARE!
    """

    DENSITY = _AboutUnit(_registry.kilogram_per_cubic_meter, opq.PhysicalQuantity.DENSITY)
    ENERGY = _AboutUnit(_registry.joule, opq.PhysicalQuantity.ENERGY)
    FORCE = _AboutUnit(_registry.newton, opq.PhysicalQuantity.FORCE)
    LENGTH = _AboutUnit(_registry.meter, opq.PhysicalQuantity.LENGTH)
    MASS = _AboutUnit(_registry.kilogram, opq.PhysicalQuantity.MASS)
    POWER = _AboutUnit(_registry.watt, opq.PhysicalQuantity.POWER)
    PRESSURE = _AboutUnit(_registry.kilopascal, opq.PhysicalQuantity.PRESSURE)
    PROPPANT_CONCENTRATION = _AboutUnit(_registry.kilogram_per_cubic_meter, opq.PhysicalQuantity.PROPPANT_CONCENTRATION)
    SLURRY_RATE = _AboutUnit(_registry.cubic_meter_per_minute, opq.PhysicalQuantity.SLURRY_RATE)
    TEMPERATURE = _AboutUnit(_registry.degree_Celsius, opq.PhysicalQuantity.TEMPERATURE)
    VOLUME = _AboutUnit((_registry.m ** 3), opq.PhysicalQuantity.VOLUME)

    def system_name(self):
        return 'Metric'

    def unit_str(self):
        """
        Returns a string representing the unit of this enumeration member.

        This method plays the role of "Primitive Operation" in the _Template Method_ design pattern.
        This method is called by the "Template Method" to allow customization of the "Template Method"
        **without** changing the algorithm of the "Template Method."

        Generally, this method returns the unit with the correct capitalization.

        Returns:
            The string representation of the unit.
        """
        def use_abbreviation(unit):
            return (unit == Metric.ENERGY or
                    unit == Metric.FORCE or
                    unit == Metric.LENGTH or
                    unit == Metric.MASS or
                    unit == Metric.POWER or
                    unit == Metric.PRESSURE)

        if self == Metric.VOLUME:
            return 'cubic_meter'

        if use_abbreviation(self):
            return abbreviation(self)

        return super().unit_str()


def abbreviation(unit: UnitSystem) -> str:
    """
    Return the abbreviation for a unit.

    Args:
        unit: The UnitSystem member whose abbreviation is sought.

    Returns:
        The abbreviation of 'unit'.
    """
    unit_abbreviation_map = {
        Common.ANGLE: '\u00b0',
        UsOilfield.DENSITY: 'lb/ft\u00b3',
        UsOilfield.ENERGY: 'ft-lb',
        UsOilfield.VOLUME: 'bbl',
        UsOilfield.PROPPANT_CONCENTRATION: 'lb/gal',
        Metric.DENSITY: 'kg/m\u00b3',
        Metric.PROPPANT_CONCENTRATION: 'kg/m\u00b3',
        Metric.SLURRY_RATE: 'm\u00b3/min',
    }

    # noinspection PyTypeChecker
    return unit_abbreviation_map.get(unit, f'{unit.value.unit:~P}')
