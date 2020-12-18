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

from orchid import unit_system as units


Measurement = collections.namedtuple('measurement', ['magnitude', 'unit'], module=__name__)


def _is_known_unit(_magnitude, unit):
    if isinstance(unit, units.UsOilfield):
        return True
    elif isinstance(unit, units.Metric):
        return True
    elif unit is units.DURATION:
        return True

    return False


def get_conversion_factor(source_unit: Union[units.UsOilfield, units.Metric],
                          target_unit: Union[units.UsOilfield, units.Metric]) -> float:
    """
    Returns the conversion factor from `source_unit` to `target_unit`.

    Args:
        source_unit: The source unit for the conversion.
        target_unit: The target unit for the conversion.
    """
    pass


@deal.pre(lambda magnitude, _unit: isinstance(magnitude, numbers.Real))
@deal.pre(_is_known_unit)
def make_measurement(magnitude: numbers.Real, unit: Union[units.UsOilfield, units.Metric]) -> Measurement:
    """
    Construct a measurement.

    Args:
        magnitude: The magnitude of the measurement.
        unit: The unit of this measurement.

    Returns:
        The Measurement consisting of the supplied `magnitude` and `unit`.
    """
    return Measurement(magnitude, unit)
