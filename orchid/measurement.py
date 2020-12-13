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

import collections
import numbers
from typing import Union

import deal

import orchid.unit_system as units


Measurement = collections.namedtuple('measurement', ['magnitude', 'unit'], module=__name__)


def get_conversion_factor(source_unit, target_unit):
    pass


def make_measurement(magnitude: Union[int, float], unit_text: Union[units.UsOilfield, units.Metric]) -> Measurement:
    """
    Construct a measurement.

    Args:
        magnitude: The magnitude of the measurement.
        unit_text: An abbreviation for the unit of this measurement.

    Returns:
        The measurement consisting of a magnitude and a unit.
    """
    pass


def slurry_rate_volume_unit(slurry_rate_unit: str) -> str:
    """
    Extract the volume unit from the compound `slurry_rate_unit`.

    Args:
        slurry_rate_unit: The abbreviation for the compound slurry rate unit.
Q
    Returns:
        The abbreviation for the volume unit of the slurry rate unit.
    """
    pass


def proppant_concentration_mass_unit(proppant_concentration_unit: str) -> str:
    """
    Extract the mass unit from the compound `proppant_concentration_unit`.

    Args:
        proppant_concentration_unit: The abbreviation for the proppant concentration unit.

    Returns:
        The abbreviation for the mass unit of the proppant concentration unit.
    """
    pass
