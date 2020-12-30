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


def abbreviation(unit: Unit) -> str:
    """
    Return the abbreviation for a `Unit`.

    Args:
        unit: The unit whose abbreviation is sought.

    Returns:
        The abbreviation of `unit` as a `str`.
    """
    return f'{unit:~P}'


# TODO: remove
class UnitSystem(Enum):
    def __repr__(self):
        return f'<{self.system_name()}: {str(self.value)}>'

    abbreviation = property(lambda self: str(self))

    def __str__(self):
        return str(self.value)

    @abstractmethod
    def system_name(self):
        raise NotImplementedError()


class Common(UnitSystem):
    """The enumeration of units common to both U. S. oilfield and metric unit systems."""

    ANGLE = _registry.deg
    DURATION = _registry.min

    def system_name(self):
        return 'Common'


# TODO: remove
class UsOilfield(UnitSystem):
    """The enumeration of U. S. oilfield units available via the Orchid Python API."""

    DENSITY = _registry.pound_per_cubic_foot
    ENERGY = _registry.foot_pound
    FORCE = _registry.pound_force
    LENGTH = _registry.foot
    MASS = _registry.pound
    POWER = _registry.horsepower
    PRESSURE = _registry.pound_force_per_square_inch
    PROPPANT_CONCENTRATION = _registry.oil_barrel_per_minute
    SLURRY_RATE = _registry.oil_barrel_per_minute
    TEMPERATURE = _registry.degree_Fahrenheit
    VOLUME = _registry.oil_barrel

    def system_name(self):
        return 'USOilfield'


# TODO: remove
class Metric(UnitSystem):
    """The enumeration of metric units available via the Orchid Python API."""

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
