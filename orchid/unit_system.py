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
import numbers

import toolz.curried as toolz

from orchid import (
    measurement as om,
    physical_quantity as opq,
)


# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import UnitSystem as NetUnitSystem
# noinspection PyUnresolvedReferences
import UnitsNet


# TODO: Remove the duplicate code (when removing the module `obs_unit_system`.
# Because I copied the contents of this module from the original `unit_system` (now named `obs_unit_system`),
# this module is filled with duplicate code fragments. Over time these should disappear and should completely
# disappear when one removes `obs_unit_system` from the system.


# I use this private class to distinguish units that measure **different** physical quantities but use the
# same measurement unit. Currently, this applies to DENSITY and PRESSURE.
_AboutUnit = namedtuple('AboutUnit', ['unit', 'physical_quantity'])


class UnitSystem(Enum):

    def __str__(self):
        """
        Return a string representation of the member.

        Returns:
            The string representing the enumeration member.
        """
        return f'{self.value.unit}'

    def abbreviation(self):
        """
        Return the abbreviation for a unit.

        Returns:
            The abbreviation of 'unit'.
        """
        return f'{self.value.unit:~P}'

    @abstractmethod
    def system_name(self):
        raise NotImplementedError()


class Common(UnitSystem):
    """The enumeration of units common to both U. S. oilfield and metric unit systems."""

    ANGLE = _AboutUnit(om.registry.deg, opq.PhysicalQuantity.ANGLE)
    DURATION = _AboutUnit(om.registry.min, opq.PhysicalQuantity.DURATION)

    def system_name(self):
        return 'Common'


class UsOilfield(UnitSystem):
    """The enumeration of U. S. oilfield units available via the Orchid Python API."""

    DENSITY = _AboutUnit(om.registry.pound / om.registry.ft ** 3, opq.PhysicalQuantity.DENSITY)
    ENERGY = _AboutUnit(om.registry.foot_pound, opq.PhysicalQuantity.ENERGY)
    FORCE = _AboutUnit(om.registry.pound_force, opq.PhysicalQuantity.FORCE)
    LENGTH = _AboutUnit(om.registry.foot, opq.PhysicalQuantity.LENGTH)
    MASS = _AboutUnit(om.registry.pound, opq.PhysicalQuantity.MASS)
    POWER = _AboutUnit(om.registry.horsepower, opq.PhysicalQuantity.POWER)
    PRESSURE = _AboutUnit(om.registry.pound_force_per_square_inch, opq.PhysicalQuantity.PRESSURE)
    PROPPANT_CONCENTRATION = _AboutUnit(om.registry.pound / om.registry.gallon,
                                        opq.PhysicalQuantity.PROPPANT_CONCENTRATION)
    SLURRY_RATE = _AboutUnit(om.registry.oil_barrel / om.registry.minute, opq.PhysicalQuantity.SLURRY_RATE)
    TEMPERATURE = _AboutUnit(om.registry.degree_Fahrenheit, opq.PhysicalQuantity.TEMPERATURE)
    VOLUME = _AboutUnit(om.registry.oil_barrel, opq.PhysicalQuantity.VOLUME)

    def system_name(self):
        return 'USOilfield'


class Metric(UnitSystem):
    """The enumeration of metric units available via the Orchid Python API."""

    DENSITY = _AboutUnit(om.registry.kilogram / om.registry.meter ** 3, opq.PhysicalQuantity.DENSITY)
    ENERGY = _AboutUnit(om.registry.joule, opq.PhysicalQuantity.ENERGY)
    FORCE = _AboutUnit(om.registry.newton, opq.PhysicalQuantity.FORCE)
    LENGTH = _AboutUnit(om.registry.meter, opq.PhysicalQuantity.LENGTH)
    MASS = _AboutUnit(om.registry.kilogram, opq.PhysicalQuantity.MASS)
    POWER = _AboutUnit(om.registry.watt, opq.PhysicalQuantity.POWER)
    PRESSURE = _AboutUnit(om.registry.kilopascal, opq.PhysicalQuantity.PRESSURE)
    PROPPANT_CONCENTRATION = _AboutUnit(om.registry.kilogram / om.registry.meter ** 3,
                                        opq.PhysicalQuantity.PROPPANT_CONCENTRATION)
    SLURRY_RATE = _AboutUnit(om.registry.meter ** 3 / om.registry.minute, opq.PhysicalQuantity.SLURRY_RATE)
    TEMPERATURE = _AboutUnit(om.registry.degree_Celsius, opq.PhysicalQuantity.TEMPERATURE)
    VOLUME = _AboutUnit((om.registry.m ** 3), opq.PhysicalQuantity.VOLUME)

    def system_name(self):
        return 'Metric'


def as_unit_system(net_unit_system: UnitSystem):
    if net_unit_system == NetUnitSystem.USOilfield():
        return UsOilfield
    elif net_unit_system == NetUnitSystem.Metric():
        return Metric
    else:
        raise ValueError(f'Unrecognized unit system: {net_unit_system}')


@toolz.curry
def make_measurement(unit: UnitSystem, magnitude: numbers.Real) -> om.Quantity:
    """
    Construct a measurement.

    This function provides a "functional" mechanism to create Measurement instances. It is more common to
    create a sequence of measurements from a sequence of numbers and a **single** unit. By putting the `unit`
    argument first in the function arguments, it allows callers to write code similar to the following:

    > make_length_measurement = make_measurement(units.UsOilfield.LENGTH)
    > length_measurements = [make_length_measurement(l) for l in lengths]
    > # or toolz.map(make_length_measurement, lengths)

    Args:
        unit: The unit of this measurement.
        magnitude: The magnitude of the measurement.

    Returns:
        The created `pint` `Quantity` instance.
    """
    return om.Quantity(magnitude, unit.value.unit)


def abbreviation(unit: UnitSystem):
    """
    Return the abbreviation of `unit`.

    This function provides a functional interface for calculating abbreviations of `UnitSystem` members.

    Args:
        unit: The `UnitSystem` member whose abbreviation is sought.

    Returns:
        The abbreviation for `unit`.
    """
    return unit.abbreviation()
