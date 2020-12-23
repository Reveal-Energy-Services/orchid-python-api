#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

"""This module contains functions for converting between instances of the (Python) `Measurement` class and
instances of .NET classes like `UnitsNet.Quantity` and `DateTime`."""

import datetime

import toolz.curried as toolz

from orchid import (measurement as om,
                    physical_quantity as opq,
                    unit_system as units)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import (ProppantConcentration, SlurryRate)
# noinspection PyUnresolvedReferences
from System import DateTime
# noinspection PyUnresolvedReferences
import UnitsNet


UNIT_CREATE_NET_UNIT_MAP = {
    units.common[opq.DURATION]: lambda q: UnitsNet.Duration.FromMinutes(q),
    units.us_oilfield[opq.LENGTH]: lambda q: UnitsNet.Length.FromFeet(q),
    units.metric[opq.LENGTH]: lambda q: UnitsNet.Length.FromMeters(q),
    units.us_oilfield[opq.MASS]: lambda q: UnitsNet.Mass.FromPounds(q),
    units.metric[opq.MASS]: lambda q: UnitsNet.Mass.FromKilograms(q),
    units.us_oilfield[opq.PRESSURE]: lambda q: UnitsNet.Pressure.FromPoundsForcePerSquareInch(q),
    units.metric[opq.PRESSURE]: lambda q: UnitsNet.Pressure.FromKilopascals(q),
    units.us_oilfield[opq.VOLUME]: lambda q: UnitsNet.Volume.FromOilBarrels(q),
    units.metric[opq.VOLUME]: lambda q: UnitsNet.Volume.FromCubicMeters(q),
}


def as_datetime(net_time_point: DateTime) -> datetime.datetime:
    """
    Convert a .NET `DateTime` instance to a `datetime.datetime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTime`.

    Returns:
        The `datetime.datetime` equivalent to the `net_time_point`.
    """
    return datetime.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                             net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                             net_time_point.Millisecond * 1000)


def as_measurement(net_quantity: UnitsNet.IQuantity) -> units.Quantity:
    """
    Convert a .NET UnitsNet.IQuantity to a `Measurement` instance.

    Args:
        net_quantity: The .NET IQuantity instance to convert.

    Returns:
        The equivalent `Measurement` instance.
    """
    result = net_quantity.Value * _unit_from_net_quantity(net_quantity)
    return result


def as_net_date_time(time_point: datetime.datetime) -> DateTime:
    """
    Convert a `datetime.datetime` instance to a .NET `DateTime` instance.

    Args:
        time_point: The `datetime.datetime` instance to covert.

    Returns:
        The equivalent .NET `DateTime` instance.
    """
    return DateTime(time_point.year, time_point.month, time_point.day, time_point.hour, time_point.minute,
                    time_point.second, round(time_point.microsecond / 1e3))


def as_net_quantity(measurement: om.Measurement) -> UnitsNet.IQuantity:
    """
    Convert a `Measurement` instance to a .NET `UnitsNet.IQuantity` instance.

    Args:
        measurement: The `Measurement` instance to convert.

    Returns:
        The equivalent `UnitsNet.IQuantity` instance.
    """
    quantity = UnitsNet.QuantityValue.op_Implicit(measurement.magnitude)
    try:
        return UNIT_CREATE_NET_UNIT_MAP[measurement.unit](quantity)
    except KeyError:
        if measurement.unit == units.UsOilfield.PROPPANT_CONCENTRATION or \
                measurement.unit == units.Metric.PROPPANT_CONCENTRATION:
            return ProppantConcentration(measurement.magnitude, measurement.unit.value.net_unit[0],
                                         measurement.unit.value.net_unit[1])
        elif measurement.unit == units.UsOilfield.SLURRY_RATE or measurement.unit == units.Metric.SLURRY_RATE:
            return SlurryRate(measurement.magnitude, measurement.unit.value.net_unit[0],
                              measurement.unit.value.net_unit[1])
            pass
        else:
            raise ValueError(f'Unrecognized unit: "{measurement.unit}".')


def as_net_quantity_in_different_unit(measurement: om.Measurement, target_unit: units.Unit) -> UnitsNet.IQuantity:
    """
    Convert a `Measurement` into a .NET `UnitsNet.IQuantity` instance but in a different unit, `in_unit`.
    Args:
        measurement: The `Measurement` instance to convert.
        target_unit: The target unit of the converted `Measurement`.

    Returns:
        The  `NetUnits.IQuantity` instance equivalent to `measurement`.
    """
    net_to_convert = as_net_quantity(measurement)
    return net_to_convert.ToUnit(target_unit.value.net_unit)


@toolz.curry
def convert_net_quantity_to_different_unit(net_quantity: UnitsNet.IQuantity,
                                           target_unit: units.Unit) -> UnitsNet.IQuantity:
    """
    Convert one .NET `UnitsNet.IQuantity` to another .NET `UnitsNet.IQuantity` in a different unit `target_unit`
    Args:
        net_quantity: The `UnitsNet.IQuantity` instance to convert.
        target_unit: The unit to which to convert `net_quantity`.

    Returns:
        The .NET `UnitsNet.IQuantity` converted to `target_unit`.
    """
    result = net_quantity.ToUnit(target_unit.value.net_unit)
    return result


def _is_minute_unit(net_quantity):
    try:
        if net_quantity.Unit == UnitsNet.Units.DurationUnit.Minute:
            return True
    except AttributeError:
        # Both ProppantConcentration and SlurryRate have **no** `Unit` attribute, but are not a minute duration
        return False
    else:
        # Anything else must be some other unit.
        return False


def _is_ratio_unit(net_quantity_to_test):
    """
    Determine if the .NET IQuantity instance is either `ProppantConcentration` or `SlurryRate`.
    Args:
        net_quantity_to_test: The .NET IQuantity instance to test.

    Returns:
        True if the quantity to test has a numerator and a denominator unit; otherwise, false.
    """
    if _ratio_units(net_quantity_to_test):
        return True
    else:
        return False


def _ratio_units(net_quantity):
    try:
        return net_quantity.NumeratorUnit, net_quantity.DenominatorUnit
    except AttributeError:
        return tuple()


# Skip proppant concentration and slurry rate. The function, `_unit_from_net_quantity`, handles these physical
# quantities manually.
_NET_ABBREVIATION_UNIT_MAP = {
    'deg': units.common[opq.ANGLE],
    'min': units.common[opq.DURATION],
    'ft': units.us_oilfield[opq.LENGTH],
    'psi': units.us_oilfield[opq.PRESSURE],
    'lbf': units.us_oilfield[opq.FORCE],
    'bbl': units.us_oilfield[opq.VOLUME],
    'lb': units.us_oilfield[opq.MASS],
    'hp(I)': units.us_oilfield[opq.POWER],
    'lb/ft³': units.us_oilfield[opq.DENSITY],
    '°F': units.us_oilfield[opq.TEMPERATURE],
    'ft·lb': units.us_oilfield[opq.ENERGY],
    'm': units.metric[opq.LENGTH],
    'kPa': units.metric[opq.PRESSURE],
    'N': units.metric[opq.FORCE],
    'm³': units.metric[opq.VOLUME],
    'kg': units.metric[opq.MASS],
    'W': units.metric[opq.POWER],
    'kg/m³': units.metric[opq.DENSITY],
    '°C': units.metric[opq.TEMPERATURE],
    'J': units.metric[opq.ENERGY],
}


def _unit_from_net_quantity(net_quantity):
    if _is_minute_unit(net_quantity):
        return units.common[opq.DURATION]
    elif _is_ratio_unit(net_quantity):
        numerator_unit, denominator_unit = _ratio_units(net_quantity)
        if numerator_unit == UnitsNet.Units.MassUnit.Pound and denominator_unit == UnitsNet.Units.VolumeUnit.UsGallon:
            return units.us_oilfield[opq.PROPPANT_CONCENTRATION]
        elif numerator_unit == UnitsNet.Units.MassUnit.Kilogram and \
                denominator_unit == UnitsNet.Units.VolumeUnit.CubicMeter:
            return units.metric[opq.PROPPANT_CONCENTRATION]
        elif numerator_unit == UnitsNet.Units.VolumeUnit.OilBarrel and\
                denominator_unit == UnitsNet.Units.DurationUnit.Minute:
            return units.us_oilfield[opq.SLURRY_RATE]
        elif numerator_unit == UnitsNet.Units.VolumeUnit.CubicMeter and \
                denominator_unit == UnitsNet.Units.DurationUnit.Minute:
            return units.metric[opq.SLURRY_RATE]
    else:
        # Because UnitsNet uses an enumeration for each unit within a physical quantity (length, mass, and so
        # on) because Python.Net converts all .NET enumerations into Python `int`s, I cannot simply "dispatch'
        # on the UnitsNet Unit. Consequently, I "dispatch" on the UnitsNet unit abbreviation.
        net_unit_abbreviation = str(net_quantity).split(maxsplit=1)[1]
        result = _NET_ABBREVIATION_UNIT_MAP[net_unit_abbreviation]
        return result
