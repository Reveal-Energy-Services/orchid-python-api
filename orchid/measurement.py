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

"""This module contains functions and classes supporting the (Python) Measurement 'class.'"""

import numbers

import deal

from orchid import unit_system as units


class Measurement:
    """Models a physical measurement: a magnitude and a unit of measure."""

    @deal.pre(lambda _self, magnitude, _unit: isinstance(magnitude, numbers.Real))
    @deal.pre(lambda _self, _magnitude, unit: isinstance(unit, units.UnitSystem))
    def __init__(self, magnitude: numbers.Real, unit: units.UnitSystem):
        self._magnitude = magnitude
        self._unit = unit

    @property
    def magnitude(self) -> numbers.Real:
        return self._magnitude

    @property
    def unit(self):
        return self._unit


def make_measurement(magnitude: numbers.Real, unit: units.UnitSystem) -> Measurement:
    """
    Construct a measurement.

    Args:
        magnitude: The magnitude of the measurement.
        unit: The unit of this measurement.

    Returns:
        The created `Measurement` instance.
    """
    return Measurement(magnitude, unit)
