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

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime
# noinspection PyUnresolvedReferences
import UnitsNet


UNIT_CREATE_NET_UNIT_MAP = {
    units.UsOilfield.LENGTH: lambda q: UnitsNet.Length.FromFeet(q),
    units.Metric.LENGTH: lambda q: UnitsNet.Length.FromMeters(q),
    units.UsOilfield.MASS: lambda q: UnitsNet.Mass.FromPounds(q),
    units.Metric.MASS: lambda q: UnitsNet.Mass.FromKilograms(q),
    units.UsOilfield.PRESSURE: lambda q: UnitsNet.Pressure.FromPoundsForcePerSquareInch(q),
    units.Metric.PRESSURE: lambda q: UnitsNet.Pressure.FromKilopascals(q),
    units.UsOilfield.VOLUME: lambda q: UnitsNet.Volume.FromOilBarrels(q),
    units.Metric.VOLUME: lambda q: UnitsNet.Volume.FromCubicMeters(q),
}

ABBREVIATION_NET_UNIT_MAP = {units.UsOilfield.LENGTH.abbreviation: UnitsNet.Units.LengthUnit.Foot,
                             units.Metric.LENGTH.abbreviation: UnitsNet.Units.LengthUnit.Meter,
                             units.UsOilfield.MASS.abbreviation: UnitsNet.Units.MassUnit.Pound,
                             units.Metric.MASS.abbreviation: UnitsNet.Units.MassUnit.Kilogram,
                             units.UsOilfield.PRESSURE.abbreviation:
                                 UnitsNet.Units.PressureUnit.PoundForcePerSquareInch,
                             units.Metric.PRESSURE.abbreviation: UnitsNet.Units.PressureUnit.Kilopascal,
                             units.UsOilfield.VOLUME.abbreviation: UnitsNet.Units.VolumeUnit.OilBarrel,
                             units.Metric.VOLUME.abbreviation: UnitsNet.Units.VolumeUnit.CubicMeter}


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
    return UNIT_CREATE_NET_UNIT_MAP[measurement.unit](quantity)


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
    return net_to_convert.ToUnit(ABBREVIATION_NET_UNIT_MAP[target_unit])


@toolz.curry
def convert_net_quantity_to_different_unit(net_quantity: UnitsNet.IQuantity,
                                           target_unit: Union[units.UsOilfield, units.Metric]) -> UnitsNet.IQuantity:
    """
    Convert a .NET `UnitsNet.IQuantity` instance to a different unit, `target_unit`
    Args:
        net_quantity: The `UnitsNet.IQuantity` instance to convert.
        target_unit: The unit to which to convert `net_quantity`.

    Returns:
        The .NET `UnitsNet.IQuantity` converted to `target_unit`.
    """
    result = net_quantity.ToUnit(unit_to_net_unit(target_unit))
    return result


def unit_to_net_unit(unit: Union[units.UsOilfield, units.Metric]) -> UnitsNet.Units:
    """
    Convert a unit system unit to a .NET `UnitsNet.Units` instance

    Args:
        unit: The member identifying the unit system unit to convert.

    Returns:
        The .NET `UnitsNet.Units` equivalent to `unit`.
    """
    return ABBREVIATION_NET_UNIT_MAP[unit]
