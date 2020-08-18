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


from enum import Enum

# noinspection PyUnresolvedReferences
import UnitsNet


class NoValue(Enum):
    """"An 'abstract base class' for enumerations with na values such as `PhysicalQuantity`."""
    def __repr__(self):
        """
            Calculate the representation of this class.
        Returns:
            str: The textual representation of this class. (See
            https://docs.python.org/3/reference/datamodel.html#object.__repr__ for details.)
        """
        return f'{self.__class__.__name__}({self.name})'


class PhysicalQuantity(NoValue):
    """Models the set of physical quantities support by the Orchid Python API."""
    LENGTH = 'length'
    MASS = 'mass'
    PRESSURE = 'pressure'
    PROPPANT_CONCENTRATION = 'proppant concentration'
    SLURRY_RATE = 'slurry rate'
    TEMPERATURE = 'temperature'

    def to_units_net_quantity_type(self) -> UnitsNet.QuantityType:
        """
        Returns:
            The UnitsNet QuantityType corresponding to this quantity.
        """
        quantity_quantity_type_map = {
            PhysicalQuantity.LENGTH: UnitsNet.QuantityType.Length,
            PhysicalQuantity.MASS: UnitsNet.QuantityType.Mass,
            PhysicalQuantity.PRESSURE: UnitsNet.QuantityType.Pressure,
            PhysicalQuantity.PROPPANT_CONCENTRATION: UnitsNet.QuantityType.Ratio,
            PhysicalQuantity.SLURRY_RATE: UnitsNet.QuantityType.Ratio,
            PhysicalQuantity.TEMPERATURE: UnitsNet.QuantityType.Temperature,
        }
        return quantity_quantity_type_map[self]
