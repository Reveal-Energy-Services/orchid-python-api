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


def median_treating_pressure(stage, start, stop, calculations_factory=None):
    native_calculations_factory = FractureDiagnosticsCalculationsFactory() \
        if not calculations_factory else calculations_factory
    native_treatment_calculations = native_calculations_factory.TreatmentCalculations()
    native_calculation_result = native_treatment_calculations.GetMedianTreatmentPressure(stage, start, stop)
    pressure = onq.as_measurement(native_calculation_result.Result)
    warnings = native_calculation_result.Warnings
    return CalculationResult(pressure, warnings)
