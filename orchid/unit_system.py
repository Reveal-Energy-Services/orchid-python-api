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


from abc import abstractmethod
from enum import Enum
import pathlib

from pint import UnitRegistry


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


# TODO: remove
class UnitSystem(Enum):

    def __str__(self):
        """
        Return a string representation of the member.

        Note that this method plays the role of "Template Method" in the _Template Method_ design pattern. In
        this role it calls the "Primitive Operation", `unit_str()` to get the string identifying the unit.

        Returns:
            The string representing the enumeration member.
        """
        to_format = f'{self.system_name()}.{self.name} ({{}})'
        return to_format.format(self.unit_str())

    @abstractmethod
    def system_name(self):
        raise NotImplementedError()

    def unit_str(self):
        return f'{str(self.value)}'


class Common(UnitSystem):
    """The enumeration of units common to both U. S. oilfield and metric unit systems."""

    ANGLE = _registry.deg
    DURATION = _registry.min

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

    DENSITY = _registry.pound_per_cubic_foot
    ENERGY = _registry.foot_pound
    FORCE = _registry.pound_force
    LENGTH = _registry.foot
    MASS = _registry.pound
    POWER = _registry.horsepower
    PRESSURE = _registry.pound_force_per_square_inch
    PROPPANT_CONCENTRATION = _registry.pound_per_cubic_foot
    SLURRY_RATE = _registry.oil_barrel_per_minute
    TEMPERATURE = _registry.degree_Fahrenheit
    VOLUME = _registry.oil_barrel

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

    DENSITY = _registry.kilogram_per_cubic_meter
    ENERGY = _registry.joule
    FORCE = _registry.newton
    LENGTH = _registry.meter
    MASS = _registry.kilogram
    POWER = _registry.watt
    PRESSURE = _registry.kilopascal
    PROPPANT_CONCENTRATION = _registry.kilogram_per_cubic_meter
    SLURRY_RATE = _registry.cubic_meter_per_minute
    TEMPERATURE = _registry.degree_Celsius
    VOLUME = (_registry.m ** 3)

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
    if unit == UsOilfield.ENERGY:
        return 'ft-lb'

    if unit == UsOilfield.VOLUME:
        return 'bbl'

    return f'{unit.value:~P}'
