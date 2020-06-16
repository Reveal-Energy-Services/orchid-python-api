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
.NET UnitsNet instances."""

# noinspection PyUnresolvedReferences
import UnitsNet


ABBREVIATION_UNIT_MAP = {'ft': UnitsNet.Units.LengthUnit.Foot,
                         'm': UnitsNet.Units.LengthUnit.Meter,
                         'psi': UnitsNet.Units.PressureUnit.PoundForcePerSquareInch,
                         'kPa': UnitsNet.Units.PressureUnit.Kilopascal}


def as_net_measurement(measurement):
    """
    Convert a Measurement to a .NET UnitsNet measurement in the same unit as the measurement.
    :param measurement: The Python Measurement to convert.
    :return:
    """
    result = UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(measurement.magnitude),
                                  ABBREVIATION_UNIT_MAP[measurement.unit])
    return result


def as_net_measurement_in_different_unit(measurement, in_unit):
    """
    Convert a Measurement to a .NET UnitsNet measurement in a specific unit.
    :param measurement: The Python Measurement to convert.
    :param in_unit: An unit abbreviation that can be converted to a .NET UnitsNet.Unit
    :return:
    """
    net_to_convert = as_net_measurement(measurement)
    return net_to_convert.ToUnit(ABBREVIATION_UNIT_MAP[in_unit])


def unit_abbreviation_to_unit(unit_abbreviation: str):
    """
    Convert a unit abbreviation to a .NET UnitsNet.Unit
    :param unit_abbreviation: The abbreviation identifying the target .NET UnitsNet.Unit.
    :return: The corresponding .NET UnitsNet.Unit
    """
    return ABBREVIATION_UNIT_MAP[unit_abbreviation]
