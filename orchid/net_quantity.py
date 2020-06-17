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

"""This module contains functions for converting between instances of the (Python) `Measurement` class and
instances of .NET UnitsNet.Quantity."""

from orchid.measurement import make_measurement

# noinspection PyUnresolvedReferences
import UnitsNet

ABBREVIATION_NET_UNIT_MAP = {'ft': UnitsNet.Units.LengthUnit.Foot,
                             'm': UnitsNet.Units.LengthUnit.Meter,
                             'psi': UnitsNet.Units.PressureUnit.PoundForcePerSquareInch,
                             'kPa': UnitsNet.Units.PressureUnit.Kilopascal}

NET_UNIT_ABBREVIATION_MAP = {v: k for (k, v) in ABBREVIATION_NET_UNIT_MAP.items()}


def as_measurement(net_quantity):
    """
    Convert a .NET UnitsNet.Quantity to a Python Measurement.
    :param net_quantity: The Python Measurement to convert.
    :return: The Python Measurement corresponding to net_quantity.
    """
    result = make_measurement(net_quantity.Value, NET_UNIT_ABBREVIATION_MAP[net_quantity.Unit])
    return result


def as_net_quantity(measurement):
    """
    Convert a Measurement to a .NET UnitsNet.Quantity in the same unit as the Measurement.
    :param measurement: The Python Measurement to convert.
    :return: The .NET UnitsNet.Quantity corresponding to measurement.
    """
    result = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(measurement.magnitude),
                                  ABBREVIATION_NET_UNIT_MAP[measurement.unit])
    return result


def as_net_quantity_in_different_unit(measurement, in_unit):
    """
    Convert a Measurement to a .NET UnitsNet measurement in a specific unit.
    :param measurement: The Python Measurement to convert.
    :param in_unit: An unit abbreviation that can be converted to a .NET UnitsNet.Unit
    :return:
    """
    net_to_convert = as_net_quantity(measurement)
    return net_to_convert.ToUnit(ABBREVIATION_NET_UNIT_MAP[in_unit])


def convert_net_quantity_to_different_unit(net_quantity, to_unit):
    """
    Convert one .NET UnitsNet.Quantity to a .NET UnitsNet.Quantity in a specific unit.
    :param net_quantity: The .NET UnitsNet.Quantity to convert.
    :param to_unit: An unit abbreviation that can be converted to a .NET UnitsNet.Unit
    :return: The corresponding .NET UnitsNet.Quantity in the specified unit.
    """

    result = net_quantity.ToUnit(unit_abbreviation_to_unit(to_unit))
    return result


def unit_abbreviation_to_unit(unit_abbreviation: str):
    """
    Convert a unit abbreviation to a .NET UnitsNet.Unit
    :param unit_abbreviation: The abbreviation identifying the target .NET UnitsNet.Unit.
    :return: The corresponding .NET UnitsNet.Unit
    """
    return ABBREVIATION_NET_UNIT_MAP[unit_abbreviation]
