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
from typing import Union

import toolz.curried as toolz

import orchid.measurement as om
import orchid.unit_system as units

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import (ProppantConcentration, SlurryRate)
# noinspection PyUnresolvedReferences
from System import DateTime
# noinspection PyUnresolvedReferences
import UnitsNet


UNIT_CREATE_NET_UNIT_MAP = {
    units.DURATION: lambda q: UnitsNet.Duration.FromMinutes(q),
    units.UsOilfield.LENGTH: lambda q: UnitsNet.Length.FromFeet(q),
    units.Metric.LENGTH: lambda q: UnitsNet.Length.FromMeters(q),
    units.UsOilfield.MASS: lambda q: UnitsNet.Mass.FromPounds(q),
    units.Metric.MASS: lambda q: UnitsNet.Mass.FromKilograms(q),
    units.UsOilfield.PRESSURE: lambda q: UnitsNet.Pressure.FromPoundsForcePerSquareInch(q),
    units.Metric.PRESSURE: lambda q: UnitsNet.Pressure.FromKilopascals(q),
    units.UsOilfield.VOLUME: lambda q: UnitsNet.Volume.FromOilBarrels(q),
    units.Metric.VOLUME: lambda q: UnitsNet.Volume.FromCubicMeters(q),
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


def as_measurement(net_quantity: UnitsNet.IQuantity) -> om.Measurement:
    """
    Convert a .NET UnitsNet.IQuantity to a `Measurement` instance.

    Args:
        net_quantity: The .NET IQuantity instance to convert.

    Returns:
        The equivalent `Measurement` instance.
    """
    # UnitsNet has chosen to use 'm' for both minutes and meters...
    if is_minute_unit(net_quantity):
        return om.make_measurement(net_quantity.Value, units.DURATION)
    elif is_ratio_unit(net_quantity):
        numerator_unit, denominator_unit = ratio_units(net_quantity)
        if numerator_unit == UnitsNet.Units.MassUnit.Pound and denominator_unit == UnitsNet.Units.VolumeUnit.UsGallon:
            return om.make_measurement(net_quantity.Value, units.UsOilfield.PROPPANT_CONCENTRATION)
        elif numerator_unit == UnitsNet.Units.MassUnit.Kilogram and \
                denominator_unit == UnitsNet.Units.VolumeUnit.CubicMeter:
            return om.make_measurement(net_quantity.Value, units.Metric.PROPPANT_CONCENTRATION)
        elif numerator_unit == UnitsNet.Units.VolumeUnit.OilBarrel and\
                denominator_unit == UnitsNet.Units.DurationUnit.Minute:
            return om.make_measurement(net_quantity.Value, units.UsOilfield.SLURRY_RATE)
        elif numerator_unit == UnitsNet.Units.VolumeUnit.CubicMeter and \
                denominator_unit == UnitsNet.Units.DurationUnit.Minute:
            return om.make_measurement(net_quantity.Value, units.Metric.SLURRY_RATE)
    else:
        # Python.NET converts .NET Enum types to Python `int`s so I search by (assumed unique) abbreviation.
        net_unit_abbreviation = str(net_quantity).split(maxsplit=1)[1]
        us_oilfield_candidates = toolz.filter(lambda u: u.value.unit == net_unit_abbreviation, units.UsOilfield)
        metric_candidates = toolz.filter(lambda u: u.value.unit == net_unit_abbreviation, units.Metric)
        candidates = list(toolz.concatv(us_oilfield_candidates, metric_candidates))
        if len(candidates) == 1:
            return om.make_measurement(net_quantity.Value, candidates[0])
        elif toolz.count(candidates) > 1:
            raise ValueError(f'Expected at most 1 matching candidate for "{net_unit_abbreviation}". Found '
                             f'{[str(c) for c in candidates]}.')
        else:
            # No matching candidates so test Unicode units
            if net_unit_abbreviation == 'm\u00b3':
                return om.make_measurement(net_quantity.Value, units.Metric.VOLUME)
            else:
                raise ValueError(f'No matching candidates for "{net_unit_abbreviation}".')


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


def as_net_quantity_in_different_unit(measurement: om.Measurement,
                                      target_unit: Union[units.UsOilfield, units.Metric]) -> UnitsNet.IQuantity:
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
                                           target_unit: Union[units.UsOilfield, units.Metric]) -> UnitsNet.IQuantity:
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


def is_minute_unit(net_quantity_to_test):
    """
    Determine if the .NET IQuantity instance is a `DurationUnit` of `Minutes'.
    Args:
        net_quantity_to_test: The .NET IQuantity instance to test.

    Returns:
        True if the `Unit` attribute is a `Minute` duration; otherwise, false.
    """
    try:
        if net_quantity_to_test.Unit == UnitsNet.Units.DurationUnit.Minute:
            return True
    except AttributeError:
        # Both ProppantConcentration and SlurryRate have **no** `Unit` attribute, but are not a minute duration
        return False
    else:
        # Anything else must be some other unit.
        return False


def is_ratio_unit(net_quantity_to_test):
    """
    Determine if the .NET IQuantity instance is either `ProppantConcentration` or `SlurryRate`.
    Args:
        net_quantity_to_test: The .NET IQuantity instance to test.

    Returns:
        True if the quantity to test has a numerator and a denominator unit; otherwise, false.
    """
    if ratio_units(net_quantity_to_test):
        return True
    else:
        return False


def ratio_units(net_quantity):
    try:
        return net_quantity.NumeratorUnit, net_quantity.DenominatorUnit
    except AttributeError:
        return tuple()
