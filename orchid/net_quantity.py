#  Copyright 2017-2021 Reveal Energy Services, Inc 
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

import dateutil.tz
import toolz.curried as toolz

from orchid import (measurement as om,
                    physical_quantity as opq,
                    unit_system as units)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import (ProppantConcentration, SlurryRate)
# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, Decimal, Tuple
# noinspection PyUnresolvedReferences
import UnitsNet

_UNIT_NET_UNIT_MAP = {
    units.Common.ANGLE: UnitsNet.Units.AngleUnit.Degree,
    units.Common.DURATION: UnitsNet.Units.DurationUnit.Minute,
    units.UsOilfield.DENSITY: UnitsNet.Units.DensityUnit.PoundPerCubicFoot,
    units.Metric.DENSITY: UnitsNet.Units.DensityUnit.KilogramPerCubicMeter,
    units.UsOilfield.ENERGY: UnitsNet.Units.EnergyUnit.FootPound,
    units.Metric.ENERGY: UnitsNet.Units.EnergyUnit.Joule,
    units.UsOilfield.FORCE: UnitsNet.Units.ForceUnit.PoundForce,
    units.Metric.FORCE: UnitsNet.Units.ForceUnit.Newton,
    units.UsOilfield.LENGTH: UnitsNet.Units.LengthUnit.Foot,
    units.Metric.LENGTH: UnitsNet.Units.LengthUnit.Meter,
    units.UsOilfield.MASS: UnitsNet.Units.MassUnit.Pound,
    units.Metric.MASS: UnitsNet.Units.MassUnit.Kilogram,
    units.UsOilfield.POWER: UnitsNet.Units.PowerUnit.MechanicalHorsepower,
    units.Metric.POWER: UnitsNet.Units.PowerUnit.Watt,
    units.UsOilfield.PRESSURE: UnitsNet.Units.PressureUnit.PoundForcePerSquareInch,
    units.Metric.PRESSURE: UnitsNet.Units.PressureUnit.Kilopascal,
    units.UsOilfield.TEMPERATURE: UnitsNet.Units.TemperatureUnit.DegreeFahrenheit,
    units.Metric.TEMPERATURE: UnitsNet.Units.TemperatureUnit.DegreeCelsius,
    units.UsOilfield.VOLUME: UnitsNet.Units.VolumeUnit.OilBarrel,
    units.Metric.VOLUME: UnitsNet.Units.VolumeUnit.CubicMeter,
}


class NetQuantityTimeZoneError(ValueError):
    pass


class NetQuantityLocalDateTimeKindError(NetQuantityTimeZoneError):
    def __init__(self, net_time_point):
        """
        Construct an instance from a .NET DateTime point in time.

        Args:
            net_time_point: A .NET DateTime representing a specific point in time.
        """
        super().__init__(self, '.NET DateTime.Kind cannot be Local.', net_time_point.ToString("O"))


class NetQuantityUnspecifiedDateTimeKindError(NetQuantityTimeZoneError):

    ERROR_PREFACE = '.NET DateTime.Kind is unexpectedly Unspecified.'

    ERROR_SUFFIX = """
    Although .NET DateTime.Kind should not be Unspecified, it may be
    safe to ignore this error by catching the exception.
    
    However, because it unexpected, **please** report the issue to
    Reveal Energy Services. 
    """

    def __init__(self, net_time_point):
        """
        Construct an instance from a .NET DateTime point in time.

        Args:
            net_time_point: A .NET DateTime representing a specific point in time.
        """
        super().__init__(self, NetQuantityUnspecifiedDateTimeKindError.ERROR_PREFACE,
                         net_time_point.ToString("O"), NetQuantityUnspecifiedDateTimeKindError.ERROR_SUFFIX)


class NetQuantityNoTzInfoError(NetQuantityTimeZoneError):
    def __init__(self, time_point):
        """
        Construct an instance from a Python point in time.

        Args:
            time_point: A Python `datetime.datetime` representing a specific point in time.
        """
        super().__init__(self, f'The Python time point must specify the time zone.', time_point.isoformat())


def as_datetime(net_time_point: DateTime) -> datetime.datetime:
    """
    Convert a .NET `DateTime` instance to a `datetime.datetime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTime`.

    Returns:
        The `datetime.datetime` equivalent to the `net_time_point`.
    """
    if net_time_point.Kind == DateTimeKind.Utc:
        return datetime.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                                 net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                                 net_time_point.Millisecond * 1000, dateutil.tz.UTC)

    if net_time_point.Kind == DateTimeKind.Unspecified:
        raise NetQuantityUnspecifiedDateTimeKindError(net_time_point)

    if net_time_point.Kind == DateTimeKind.Local:
        raise NetQuantityLocalDateTimeKindError(net_time_point)

    raise ValueError(f'Unknown .NET DateTime.Kind, {net_time_point.Kind}.')


@toolz.curry
def as_measurement(physical_quantity: opq.PhysicalQuantity, net_quantity: UnitsNet.IQuantity) -> om.Measurement:
    """
    Convert a .NET UnitsNet.IQuantity to a `Measurement` instance.

    Args:
        net_quantity: The .NET IQuantity instance to convert.
        physical_quantity: The optional `PhysicalQuantity`. Although we try to determine a unique mapping
        between units in the `unit_system` module and .NET `UnitsNet` units, we cannot perform a unique
        mapping for density and proppant concentration measured in the metric system (the units of these
        physical quantities are "kg/m**3"".

    Returns:
        The equivalent `Measurement` instance.
    """
    unit = _unit_from_net_quantity(net_quantity, physical_quantity)
    # UnitsNet, for an unknown reason, handles the `Value` property of `Power` **differently** from almost all
    # other units (`Information` and `BitRate` appear to be handled in the same way). Specifically, the
    # `Value` property **does not** return a value of type `double` but of type `Decimal`. Python.NET
    # expectedly converts the value returned by `Value` to a Python `decimal.Decimal`. Then, additionally,
    # Pint has a problem handling a unit whose value is `decimal.Decimal`. I do not quite understand this
    # problem, but I have seen other issues on GitHub that seem to indicate similar problems.
    if physical_quantity == opq.PhysicalQuantity.POWER:
        return om.make_measurement(unit, net_decimal_to_float(net_quantity.Value))
    elif physical_quantity == opq.PhysicalQuantity.TEMPERATURE:
        return om.make_measurement(unit, net_quantity.Value)
    else:
        return om.make_measurement(unit, net_quantity.Value)


# It is common to convert UnitsNet Quantities in LengthUnit's to Python length measurements
as_length_measurement = as_measurement(opq.PhysicalQuantity.LENGTH)


def as_net_date_time(time_point: datetime.datetime) -> DateTime:
    """
    Convert a `datetime.datetime` instance to a .NET `DateTime` instance.

    Args:
        time_point: The `datetime.datetime` instance to covert.

    Returns:
        The equivalent .NET `DateTime` instance.
    """
    if time_point.tzinfo != dateutil.tz.UTC:
        raise NetQuantityNoTzInfoError(time_point)

    return DateTime(time_point.year, time_point.month, time_point.day, time_point.hour, time_point.minute,
                    time_point.second, round(time_point.microsecond / 1000))


_UNIT_CREATE_NET_UNIT_MAP = {
    units.Common.ANGLE: lambda q: UnitsNet.Angle.FromDegrees(q),
    units.Common.DURATION: lambda q: UnitsNet.Duration.FromMinutes(q),
    units.UsOilfield.DENSITY: lambda q: UnitsNet.Density.FromPoundsPerCubicFoot(q),
    units.Metric.DENSITY: lambda q: UnitsNet.Density.FromKilogramsPerCubicMeter(q),
    units.UsOilfield.ENERGY: lambda q: UnitsNet.Energy.FromFootPounds(q),
    units.Metric.ENERGY: lambda q: UnitsNet.Energy.FromJoules(q),
    units.UsOilfield.FORCE: lambda q: UnitsNet.Force.FromPoundsForce(q),
    units.Metric.FORCE: lambda q: UnitsNet.Force.FromNewtons(q),
    units.UsOilfield.PRESSURE: lambda q: UnitsNet.Pressure.FromPoundsForcePerSquareInch(q),
    units.Metric.PRESSURE: lambda q: UnitsNet.Pressure.FromKilopascals(q),
    units.UsOilfield.LENGTH: lambda q: UnitsNet.Length.FromFeet(q),
    units.Metric.LENGTH: lambda q: UnitsNet.Length.FromMeters(q),
    units.UsOilfield.MASS: lambda q: UnitsNet.Mass.FromPounds(q),
    units.Metric.MASS: lambda q: UnitsNet.Mass.FromKilograms(q),
    units.UsOilfield.POWER: lambda q: UnitsNet.Power.FromMechanicalHorsepower(q),
    units.Metric.POWER: lambda q: UnitsNet.Power.FromWatts(q),
    units.UsOilfield.TEMPERATURE: lambda q: UnitsNet.Temperature.FromDegreesFahrenheit(q),
    units.Metric.TEMPERATURE: lambda q: UnitsNet.Temperature.FromDegreesCelsius(q),
    units.UsOilfield.VOLUME: lambda q: UnitsNet.Volume.FromOilBarrels(q),
    units.Metric.VOLUME: lambda q: UnitsNet.Volume.FromCubicMeters(q),
}


def as_net_quantity(measurement: om.Measurement) -> UnitsNet.IQuantity:
    """
    Convert a `Quantity` instance to a .NET `UnitsNet.IQuantity` instance.

    Args:
        measurement: The `Quantity` instance to convert.

    Returns:
        The equivalent `UnitsNet.IQuantity` instance.
    """
    quantity = UnitsNet.QuantityValue.op_Implicit(measurement.magnitude)
    try:
        return _UNIT_CREATE_NET_UNIT_MAP[measurement.unit](quantity)
    except KeyError:
        if measurement.unit == units.UsOilfield.PROPPANT_CONCENTRATION:
            return ProppantConcentration(measurement.magnitude,
                                         UnitsNet.Units.MassUnit.Pound,
                                         UnitsNet.Units.VolumeUnit.UsGallon)
        elif measurement.unit == units.Metric.PROPPANT_CONCENTRATION:
            return ProppantConcentration(measurement.magnitude,
                                         UnitsNet.Units.MassUnit.Kilogram,
                                         UnitsNet.Units.VolumeUnit.CubicMeter)
        elif measurement.unit == units.UsOilfield.SLURRY_RATE:
            return SlurryRate(measurement.magnitude,
                              UnitsNet.Units.VolumeUnit.OilBarrel,
                              UnitsNet.Units.DurationUnit.Minute)
        elif measurement.unit == units.Metric.SLURRY_RATE:
            return SlurryRate(measurement.magnitude,
                              UnitsNet.Units.VolumeUnit.CubicMeter,
                              UnitsNet.Units.DurationUnit.Minute)
        else:
            raise ValueError(f'Unrecognized unit: "{measurement.unit}".')


def as_net_quantity_in_different_unit(measurement: om.Measurement, target_unit: units.Unit) -> UnitsNet.IQuantity:
    """
    Convert a `Quantity` into a .NET `UnitsNet.IQuantity` instance but in a different unit, `in_unit`.

    Args:
        measurement: The `Quantity` instance to convert.
        target_unit: The target unit of the converted `Quantity`.

    Returns:
        The  `NetUnits.IQuantity` instance equivalent to `measurement`.
    """
    net_to_convert = as_net_quantity(measurement)

    if _is_proppant_concentration(target_unit):
        return _create_proppant_concentration(net_to_convert, target_unit)

    if _is_slurry_rate(target_unit):
        return _create_slurry_rate(net_to_convert, target_unit)

    return net_to_convert.ToUnit(_UNIT_NET_UNIT_MAP[target_unit])


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

    if _is_proppant_concentration(target_unit):
        return _create_proppant_concentration(net_quantity, target_unit)

    if _is_slurry_rate(target_unit):
        return _create_slurry_rate(net_quantity, target_unit)

    result = net_quantity.ToUnit(_UNIT_NET_UNIT_MAP[target_unit])
    return result


_NET_UNIT_UNIT_MAP = {
    (UnitsNet.Units.AngleUnit.Degree, opq.PhysicalQuantity.ANGLE): units.Common.ANGLE,
    (UnitsNet.Units.DurationUnit.Minute, opq.PhysicalQuantity.DURATION): units.Common.DURATION,
    (UnitsNet.Units.DensityUnit.PoundPerCubicFoot, opq.PhysicalQuantity.DENSITY): units.UsOilfield.DENSITY,
    (UnitsNet.Units.DensityUnit.KilogramPerCubicMeter, opq.PhysicalQuantity.DENSITY): units.Metric.DENSITY,
    (UnitsNet.Units.EnergyUnit.FootPound, opq.PhysicalQuantity.ENERGY): units.UsOilfield.ENERGY,
    (UnitsNet.Units.EnergyUnit.Joule, opq.PhysicalQuantity.ENERGY): units.Metric.ENERGY,
    (UnitsNet.Units.ForceUnit.PoundForce, opq.PhysicalQuantity.FORCE): units.UsOilfield.FORCE,
    (UnitsNet.Units.ForceUnit.Newton, opq.PhysicalQuantity.FORCE): units.Metric.FORCE,
    (UnitsNet.Units.LengthUnit.Foot, opq.PhysicalQuantity.LENGTH): units.UsOilfield.LENGTH,
    (UnitsNet.Units.LengthUnit.Meter, opq.PhysicalQuantity.LENGTH): units.Metric.LENGTH,
    (UnitsNet.Units.MassUnit.Pound, opq.PhysicalQuantity.MASS): units.UsOilfield.MASS,
    (UnitsNet.Units.MassUnit.Kilogram, opq.PhysicalQuantity.MASS): units.Metric.MASS,
    (UnitsNet.Units.PowerUnit.MechanicalHorsepower, opq.PhysicalQuantity.POWER): units.UsOilfield.POWER,
    (UnitsNet.Units.PowerUnit.Watt, opq.PhysicalQuantity.POWER): units.Metric.POWER,
    (UnitsNet.Units.PressureUnit.PoundForcePerSquareInch, opq.PhysicalQuantity.PRESSURE): units.UsOilfield.PRESSURE,
    (UnitsNet.Units.PressureUnit.Kilopascal, opq.PhysicalQuantity.PRESSURE): units.Metric.PRESSURE,
    (UnitsNet.Units.TemperatureUnit.DegreeFahrenheit, opq.PhysicalQuantity.TEMPERATURE): units.UsOilfield.TEMPERATURE,
    (UnitsNet.Units.TemperatureUnit.DegreeCelsius, opq.PhysicalQuantity.TEMPERATURE): units.Metric.TEMPERATURE,
    (UnitsNet.Units.VolumeUnit.OilBarrel, opq.PhysicalQuantity.VOLUME): units.UsOilfield.VOLUME,
    (UnitsNet.Units.VolumeUnit.CubicMeter, opq.PhysicalQuantity.VOLUME): units.Metric.VOLUME,
}


def net_decimal_to_float(net_decimal: Decimal) -> float:
    """
    Convert a .NET Decimal value to a Python float.

    Python.NET currently leaves .NET values of type `Decimal` unconverted. For example, UnitsNet models units
    of the physical quantity, power, as values of type .NET 'QuantityValue` whose `Value` property returns a
    value of .NET `Decimal` type. This function assists in converting those values to Python values of type
    `float`.

    Args:
        net_decimal: The .NET `Decimal` value to convert.

    Returns:
        A value of type `float` that is "equivalent" to the .NET `Decimal` value. Note that this conversion is
        "lossy" because .NET `Decimal` values are exact, but `float` values are not.
    """
    return Decimal.ToDouble(net_decimal)


def microseconds_to_integral_milliseconds(to_convert):
    """
    Convert microseconds to an integral number of milliseconds.

    Args:
        to_convert: The milliseconds to convert.

    Returns:
        An integral number of milliseconds equaivalent to `to_convert` microseconds.

    """
    return round(to_convert / 1000)


def _unit_from_net_quantity(net_quantity, physical_quantity):
    def is_proppant_concentration(quantity):
        return quantity == opq.PhysicalQuantity.PROPPANT_CONCENTRATION

    def is_slurry_rate(quantity):
        return quantity == opq.PhysicalQuantity.SLURRY_RATE

    def ratio_units(quantity):
        return quantity.NumeratorUnit, quantity.DenominatorUnit

    def is_us_oilfield_proppant_concentration(numerator, denominator):
        return numerator == UnitsNet.Units.MassUnit.Pound and denominator == UnitsNet.Units.VolumeUnit.UsGallon

    def is_metric_proppant_concentration(numerator, denominator):
        return numerator == UnitsNet.Units.MassUnit.Kilogram and denominator == UnitsNet.Units.VolumeUnit.CubicMeter

    def is_us_oilfield_slurry_rate(numerator, denominator):
        return numerator == UnitsNet.Units.VolumeUnit.OilBarrel and denominator == UnitsNet.Units.DurationUnit.Minute

    def is_metric_slurry_rate(numerator, denominator):
        return numerator == UnitsNet.Units.VolumeUnit.CubicMeter and denominator == UnitsNet.Units.DurationUnit.Minute

    if is_proppant_concentration(physical_quantity) or is_slurry_rate(physical_quantity):
        numerator_unit, denominator_unit = ratio_units(net_quantity)
        if is_us_oilfield_proppant_concentration(numerator_unit, denominator_unit):
            return units.UsOilfield.PROPPANT_CONCENTRATION
        elif is_metric_proppant_concentration(numerator_unit, denominator_unit):
            return units.Metric.PROPPANT_CONCENTRATION
        elif is_us_oilfield_slurry_rate(numerator_unit, denominator_unit):
            return units.UsOilfield.SLURRY_RATE
        elif is_metric_slurry_rate(numerator_unit, denominator_unit):
            return units.Metric.SLURRY_RATE

    return _NET_UNIT_UNIT_MAP[(net_quantity.Unit, physical_quantity)]


def _create_proppant_concentration(net_to_convert, target_unit):
    if target_unit == units.UsOilfield.PROPPANT_CONCENTRATION:
        mass_unit = UnitsNet.Units.MassUnit.Pound
        volume_unit = UnitsNet.Units.VolumeUnit.UsGallon
    elif target_unit == units.Metric.PROPPANT_CONCENTRATION:
        mass_unit = UnitsNet.Units.MassUnit.Kilogram
        volume_unit = UnitsNet.Units.VolumeUnit.CubicMeter
    # noinspection PyUnboundLocalVariable
    converted_magnitude = net_to_convert.As(mass_unit, volume_unit)
    return ProppantConcentration(converted_magnitude, mass_unit, volume_unit)


def _create_slurry_rate(net_to_convert, target_unit):
    if target_unit == units.UsOilfield.SLURRY_RATE:
        volume_unit = UnitsNet.Units.VolumeUnit.OilBarrel
    elif target_unit == units.Metric.SLURRY_RATE:
        volume_unit = UnitsNet.Units.VolumeUnit.CubicMeter
    duration_unit = UnitsNet.Units.DurationUnit.Minute
    # noinspection PyUnboundLocalVariable
    converted_magnitude = net_to_convert.As(volume_unit, duration_unit)
    return SlurryRate(converted_magnitude, volume_unit, duration_unit)


def _is_proppant_concentration(to_test):
    return (to_test == units.UsOilfield.PROPPANT_CONCENTRATION
            or to_test == units.Metric.PROPPANT_CONCENTRATION)


def _is_slurry_rate(to_test):
    return (to_test == units.UsOilfield.SLURRY_RATE
            or to_test == units.Metric.SLURRY_RATE)
