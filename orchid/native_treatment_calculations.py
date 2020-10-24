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


from collections import namedtuple

import orchid.net_quantity as onq

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Factories.Calculations import FractureDiagnosticsCalculationsFactory


CalculationResult = namedtuple('CalculationResult', ['measurement', 'warnings'])


def perform_calculation(native_calculation_func, stage, start, stop, calculations_factory):
    native_calculations_factory = FractureDiagnosticsCalculationsFactory() \
        if not calculations_factory else calculations_factory
    native_treatment_calculations = native_calculations_factory.TreatmentCalculations()
    native_calculation_result = native_calculation_func(native_treatment_calculations, stage, start, stop)
    calculation_measurement = onq.as_measurement(native_calculation_result.Result)
    warnings = native_calculation_result.Warnings
    return CalculationResult(calculation_measurement, warnings)


def median_treating_pressure(stage, start, stop, calculations_factory=None):

    def median_treatment_pressure_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetMedianTreatmentPressure(for_stage, start_time, stop_time)
        return calculation_result

    result = perform_calculation(median_treatment_pressure_calculation, stage, start, stop, calculations_factory)
    return result


def pumped_fluid_volume(stage, start, stop, calculations_factory=None):

    def pumped_fluid_volume_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetPumpedVolume(for_stage, start_time, stop_time)
        return calculation_result

    result = perform_calculation(pumped_fluid_volume_calculation, stage, start, stop, calculations_factory)
    return result


def total_proppant_mass(stage, start, stop, calculations_factory=None):

    def total_proppant_mass_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetTotalProppantMass(for_stage, start_time, stop_time)
        return calculation_result

    result = perform_calculation(total_proppant_mass_calculation, stage, start, stop, calculations_factory)
    return result
