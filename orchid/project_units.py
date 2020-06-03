#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

# noinspection PyUnresolvedReferences
import UnitsNet


def pressure_unit(net_project):
    return UnitsNet.Pressure.GetAbbreviation(net_project.ProjectUnits.PressureUnit)


def length_unit(net_project):
    return UnitsNet.Length.GetAbbreviation(net_project.ProjectUnits.LengthUnit)


def slurry_rate_unit(net_project):
    volume_abbreviation = UnitsNet.Volume.GetAbbreviation(net_project.ProjectUnits.SlurryRateUnit.Item1)
    duration_abbreviation = \
        ('min'
         if (net_project.ProjectUnits.SlurryRateUnit.Item2 == UnitsNet.Units.DurationUnit.Minute)
         else UnitsNet.Volume.GetAbbreviation(net_project.ProjectUnits.SlurryRateUnit.Item2))
    return f'{volume_abbreviation}/{duration_abbreviation}'


def proppant_concentration_unit(net_project):
    mass_abbreviation = UnitsNet.Mass.GetAbbreviation(
        net_project.ProjectUnits.ProppantConcentrationUnit.Item1)
    volume_abbreviation = UnitsNet.Volume.GetAbbreviation(
        net_project.ProjectUnits.ProppantConcentrationUnit.Item2)
    return f'{mass_abbreviation}/{volume_abbreviation}'


def unit(net_project, physical_quantity):
    """
    Return the abbreviation for the specified `physical_quantity` of this project.
    :param net_project: The .NET project to query
    :param physical_quantity: The name of the physical quantity.
    :return: The abbreviation of the specified physical quantity.
    """
    quantity_function_map = {'pressure': pressure_unit,
                             'length': length_unit,
                             'slurry rate': slurry_rate_unit,
                             'proppant concentration': proppant_concentration_unit}

    return quantity_function_map[physical_quantity](net_project)
