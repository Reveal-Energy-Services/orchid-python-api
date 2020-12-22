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
import toolz.curried as toolz

from orchid import physical_quantity as opq


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

# Aliases for Pint units. These aliases allow consuming code to use expressions like
# `2.718 * units.us_oilfield[opq.SLURRY_RATE]` to express, for example, a slurry rate.

# Expose units common to both US oilfield and metric unit systems.

common = {
    opq.ANGLE: _registry.deg,
    opq.DURATION: _registry.min,
}

# Expose basic units for US oilfield and metric units

us_oilfield = {
    opq.DENSITY: _registry.lb_per_cu_ft,
    opq.ENERGY: _registry.ft_lb,
    opq.FORCE: _registry.lbf,
    opq.LENGTH: _registry.ft,
    opq.MASS: _registry.lb,
    opq.POWER: _registry.hp,
    opq.PRESSURE: _registry.psi,
    opq.PROPPANT_CONCENTRATION: _registry.lb_per_gal,
    opq.TEMPERATURE: _registry.degF,
    opq.SLURRY_RATE: _registry.oil_bbl_per_min,
    opq.VOLUME: _registry.oil_bbl,
}

metric = {
    opq.DENSITY: _registry.kg_per_cu_m,
    opq.ENERGY: _registry.J,
    opq.FORCE: _registry.N,
    opq.LENGTH: _registry.m,
    opq.MASS: _registry.kg,
    opq.POWER: _registry.W,
    opq.PRESSURE: _registry.kPa,
    opq.PROPPANT_CONCENTRATION: _registry.kg_per_cu_m,
    opq.SLURRY_RATE: _registry.cu_m_per_min,
    opq.TEMPERATURE: _registry.degC,
    opq.VOLUME: (_registry.m ** 3)
}


# All units in a dictionary keyed to physical quantity. Designed to only be used **internally**.
_all_units = toolz.merge(common, us_oilfield, metric)


def abbreviation(unit: Unit) -> str:
    """
    Return the abbreviation for a `Unit`.

    Args:
        unit: The unit whose abbreviation is sought.

    Returns:
        The abbreviation of `unit` as a `str`.
    """
    return f'{unit:~P}'


def find_by_abbreviation(abbreviation_to_find: str) -> Unit:
    """
    Find the `Unit` with the specified abbreviation.

    Args:
        abbreviation_to_find: The abbreviation sought.

    Returns:
        The Unit having the specified abbreviation.
    """
    quantity_abbreviation_map = toolz.valmap(abbreviation, _all_units)
    quantity_candidates_map = toolz.valfilter(lambda a: a == abbreviation_to_find, quantity_abbreviation_map)
    if len(quantity_candidates_map) == 2:
        candidate_quantities = set(quantity_candidates_map.keys())
        candidate_units = set(quantity_candidates_map.values())
        if len(candidate_units) == 1:
            # Even though I have two keys in `quantity_candidates_map`, I only have a single (unit) value so
            # it is safe to return either.
            selected_physical_quantity = list(candidate_quantities)[0]
            return _all_units[selected_physical_quantity]
    elif len(quantity_candidates_map) != 1:
        raise ValueError(f'Expected one unit with abbreviation, "{abbreviation_to_find}". Found {quantity_candidates_map}.')

    return _all_units[toolz.first(quantity_candidates_map.keys())]


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
    PROPPANT_CONCENTRATION = _registry.lb_per_gal
    SLURRY_RATE = _registry.oil_bbl_per_min
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
    PROPPANT_CONCENTRATION = _registry.kg_per_cu_m
    SLURRY_RATE = _registry.cu_m_per_min
    TEMPERATURE = _registry.degC
    VOLUME = (_registry.m ** 3)

    def system_name(self):
        return 'Metric'
