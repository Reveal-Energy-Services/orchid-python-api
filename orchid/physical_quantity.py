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

# noinspection PyUnresolvedReferences
import UnitsNet


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


# Expose symbols at top-level for convenience
ANGLE = PhysicalQuantity.ANGLE.value
DENSITY = PhysicalQuantity.DENSITY.value
DURATION = PhysicalQuantity.DURATION.value
ENERGY = PhysicalQuantity.ENERGY.value
FORCE = PhysicalQuantity.FORCE.value
LENGTH = PhysicalQuantity.LENGTH.value
MASS = PhysicalQuantity.MASS.value
POWER = PhysicalQuantity.POWER.value
PRESSURE = PhysicalQuantity.PRESSURE.value
PROPPANT_CONCENTRATION = PhysicalQuantity.PROPPANT_CONCENTRATION.value
SLURRY_RATE = PhysicalQuantity.SLURRY_RATE.value
TEMPERATURE = PhysicalQuantity.TEMPERATURE.value
VOLUME = PhysicalQuantity.VOLUME.value
