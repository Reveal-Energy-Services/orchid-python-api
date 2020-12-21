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
import pathlib

from pint import UnitRegistry

# noinspection PyUnresolvedReferences
import UnitsNet


# This is the single location to find the `pint.UnitRegistry`. The `pint` package considers units returned
# from different instances of `UnitRegistry` to be different. See the documentation at
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects for details.
_registry = UnitRegistry()
_registry.load_definitions(str(pathlib.Path(__file__).parent.joinpath('orchid_units.txt')))

# Expose general types for use by type annotations
Quantity = _registry.Quantity
Unit = _registry.Unit

# Expose basic units for US oilfield and metric units

# Aliases for Pint units. These aliases allow consuming code to use expressions like
# `2.718 * units.oil_bbl_per_min` to express, for example, a slurry rate.

# Both US oilfield and metric

deg = _registry.deg  # angle
# noinspection PyShadowingBuiltins
min = _registry.min  # duration (time span)

# US Oilfield

lb_per_cu_ft = _registry.lb_per_cu_ft  # density
ft_lb = _registry.ft_lb  # energy
lbf = _registry.lbf  # force
ft = _registry.ft  # length
lb = _registry.lb  # mass
hp = _registry.hp  # power
psi = _registry.psi  # pressure
lb_per_gal = _registry.lb_per_gal  # proppant concentration
degF = _registry.degF  # temperature
oil_bbl_per_min = _registry.oil_bbl_per_min  # slurry rate
oil_bbl = _registry.oil_bbl  # volume

# Metric

kg_per_cu_m = _registry.kg_per_cu_m  # density (and proppant concentration)
J = _registry.J  # energy
N = _registry.N  # force
m = _registry.m  # length
kg = _registry.kg  # mass
W = _registry.W  # power
kPa = _registry.kPa  # pressure
cu_m_per_min = ((_registry.m ** 3) / _registry.min)  # slurry rate
degC = _registry.degC  # temperature
cu_m = (_registry.m ** 3)  # volume


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


# TODO: remove
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


# TODO remove
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
