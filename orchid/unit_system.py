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
from collections import namedtuple
from enum import Enum

from pint import UnitRegistry

# noinspection PyUnresolvedReferences
import UnitsNet


# This is the single location to find the `pint.UnitRegistry`. The `pint` package considers units returned
# from different instances of `UnitRegistry` to be different. See the documentation at
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects for details.
_registry = UnitRegistry()

# Expose general types for use by type annotations
Quantity = _registry.Quantity
Unit = _registry.Unit

# Aliases for "ratio" units (proppant concentration and slurry rate). Although a consuming class can use an
# expression like `2.718 * units.oil_bbl_per_min` (or even, `2.718 * (units.oil_bbl / units.min); the preferred
# method is to use the expression, `2.718 * units.UsOilfield.PROPPANT_CONCENTRATION`.
lb_per_gal = (_registry.lb / _registry.gal)
kg_per_cu_m = (_registry.kg / (_registry.m ** 3))
oil_bbl_per_min = (_registry.oil_bbl / _registry.min)
cu_m_per_min = ((_registry.m ** 3) / _registry.min)


About = namedtuple('About', ['unit', 'net_unit'])


# DURATION is a special unit because it is the same between US oilfield and metric unit systems.
class _Duration:
    """
    _Duration is a class modeling the special unit, `DURATION`. `DURATION` is special because is its contained
    in both (or neither) unit system; that is, it is in both (or neither) US oilfield and metric units.

    It has the same members defined in the `UnitSystem` class, but because `UnitSystem` derives from `Enum`,
    it cannot inherit from that class.

    Additionally, I **do not** consumers to construct instances of this class. The only instance of this
    class that should exist is referenced by the `DURATION` module attribute.
    """
    def __init__(self):
        self.value = About('min', UnitsNet.Units.DurationUnit.Minute)

    net_unit = property(lambda self: self.value.net_unit)

    def __repr__(self):
        return f'<{self.system_name}: {str(self.value)}>'

    abbreviation = property(lambda self: str(self))

    def __str__(self):
        return self.value.unit

    @property
    def system_name(self):
        return 'Duration'


DURATION = _Duration()


class UnitSystem(Enum):
    def __repr__(self):
        return f'<{self.system_name()}: {str(self.value)}>'

    abbreviation = property(lambda self: str(self))

    def __str__(self):
        return self.value.unit

    @abstractmethod
    def system_name(self):
        raise NotImplementedError()


# TODO: expand both unit systems to all units in the .NET `UnitSystem` class:
# - Length
# - Angle
# - Pressure
# - Force
# - Volume
# - Mass
# - Power
# - Density
# - Temperature
# - ProppantConcentration
# - SlurryRate
# - Energy


class UsOilfield(UnitSystem):
    """The enumeration of U. S. oilfield units available via the Orchid Python API."""

    LENGTH = _registry.ft
    MASS = _registry.lb
    PRESSURE = _registry.psi
    PROPPANT_CONCENTRATION = lb_per_gal
    SLURRY_RATE = oil_bbl_per_min
    TEMPERATURE = _registry.degF
    VOLUME = _registry.oil_bbl

    def system_name(self):
        return 'USOilfield'


class Metric(UnitSystem):
    """The enumeration of metric units available via the Orchid Python API."""

    LENGTH = _registry.m
    MASS = _registry.kg
    PRESSURE = _registry.kPa
    PROPPANT_CONCENTRATION = kg_per_cu_m
    SLURRY_RATE = cu_m_per_min
    TEMPERATURE = _registry.degC
    VOLUME = (_registry.m ** 3)

    def system_name(self):
        return 'Metric'
