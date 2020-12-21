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


from collections import namedtuple
from enum import Enum
from typing import Union

# noinspection PyUnresolvedReferences
import UnitsNet

ANGLE = 'angle'
DENSITY = 'density'
DURATION = 'duration'
ENERGY = 'energy'
FORCE = 'force'
LENGTH = 'length'
MASS = 'mass'
POWER = 'power'
PRESSURE = 'pressure'
PROPPANT_CONCENTRATION = 'proppant concentration'
SLURRY_RATE = 'slurry rate'
TEMPERATURE = 'temperature'
VOLUME = 'volume'


About = namedtuple('About', ['name', 'quantity_type'])


class PhysicalQuantity(Enum):
    """The enumeration of physical quantities available via the Orchid Python API."""

    ANGLE = 'angle'
    DENSITY = 'density'
    DURATION = 'duration'
    ENERGY = 'energy'
    FORCE = 'force'
    LENGTH = 'length'
    MASS = 'mass'
    POWER = 'power'
    PRESSURE = 'pressure'
    PROPPANT_CONCENTRATION = 'proppant concentration'
    SLURRY_RATE = 'slurry rate'
    TEMPERATURE = 'temperature'
    VOLUME = 'volume'


def to_units_net_quantity_type(physical_quantity: PhysicalQuantity) -> UnitsNet.QuantityType:
    """
    Convert a PhysicalQuantity to a UnitsNet.QuantityType

    Args:
        physical_quantity: The PhysicalQuantity to convert.

    Returns:
        The UnitsNet.QuantityType corresponding to `physical_quantity`.
    """
    return physical_quantity.value.quantity_type


def to_physical_quantity(quantity_type: UnitsNet.QuantityType, name: Union[str, None] = None) -> PhysicalQuantity:
    """
    Convert a `UnitsNet.QuantityType` (with an optional `name`) to a `PhysicalQuantity`.

    Args:
        quantity_type: The UnitsNet.QuantityType to convert.
        name: The optional name of the physical quantity.

    Returns:
        The `PhysicalQuantity` corresponding to `quantity_type` and `name`.
    """
    quantity_types_name_map = {
        UnitsNet.QuantityType.Length: 'length',
        UnitsNet.QuantityType.Mass: 'mass',
        UnitsNet.QuantityType.Pressure: 'pressure',
        UnitsNet.QuantityType.Temperature: 'temperature',
    }
    if not name:
        name = quantity_types_name_map[quantity_type]
    return PhysicalQuantity((name, quantity_type))
