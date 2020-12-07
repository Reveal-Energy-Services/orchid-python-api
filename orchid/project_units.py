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

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import ProppantConcentration, SlurryRate

# noinspection PyUnresolvedReferences
import UnitsNet


def length_unit(net_project):
    return UnitsNet.Length.GetAbbreviation(net_project.ProjectUnits.LengthUnit)


def mass_unit(net_project):
    return UnitsNet.Mass.GetAbbreviation(net_project.ProjectUnits.MassUnit)


def pressure_unit(net_project):
    return UnitsNet.Pressure.GetAbbreviation(net_project.ProjectUnits.PressureUnit)


def slurry_rate_unit(net_project):
    return SlurryRate.GetAbbreviation(net_project.ProjectUnits.SlurryRateUnit.Item1,
                                      net_project.ProjectUnits.SlurryRateUnit.Item2)


def proppant_concentration_unit(net_project):
    return ProppantConcentration.GetAbbreviation(net_project.ProjectUnits.ProppantConcentrationUnit.Item1,
                                                 net_project.ProjectUnits.ProppantConcentrationUnit.Item2)


def temperature_unit(net_project):
    return UnitsNet.Temperature.GetAbbreviation(net_project.ProjectUnits.TemperatureUnit)


def unit_abbreviation(net_project, physical_quantity):
    """
    Return the abbreviation for the specified `physical_quantity` of this project.
    :param net_project: The .NET project to query
    :param physical_quantity: The name of the physical quantity.
    :return: The abbreviation of the specified physical quantity.
    """
    quantity_function_map = {'length': length_unit,
                             'mass': mass_unit,
                             'pressure': pressure_unit,
                             'slurry rate': slurry_rate_unit,
                             'proppant concentration': proppant_concentration_unit,
                             'temperature': temperature_unit}

    try:
        physical_quantity_name = physical_quantity.value.name
    except AttributeError:
        physical_quantity_name = physical_quantity
    return quantity_function_map[physical_quantity_name](net_project)
