#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
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
import datetime as dt
from typing import Callable, Union

import deal
import pendulum

from orchid import (
    project_loader as loader,
    net_date_time as net_dt,
    net_quantity as net_qty,
    physical_quantity as opq,
)

#
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import IStage
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import (ICalculationResult,
                                                     ITreatmentCalculations)
# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime


CalculationResult = namedtuple('CalculationResult', ['measurement', 'warnings'])


def perform_calculation(native_calculation_func: Callable[[ITreatmentCalculations, IStage, DateTime, DateTime],
                                                          ICalculationResult],
                        stage: IStage, start: DateTime, stop: DateTime, physical_quantity: opq.PhysicalQuantity):
    """
    Perform the specific native calculation function for stage from start through (and including) stop.

    Args:
        native_calculation_func: The specific native treatment calculation function.
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.
        physical_quantity: The physical quantity of the measurement to be returned as the result.

    Returns:
        The calculation result (measurement and warnings) for the calculation.
    """
    native_treatment_calculations = loader.native_treatment_calculations()
    native_calculation_result = native_calculation_func(native_treatment_calculations, stage, start, stop)
    calculation_measurement = net_qty.as_measurement(physical_quantity, native_calculation_result.Result)
    warnings = native_calculation_result.Warnings
    return CalculationResult(calculation_measurement, warnings)


@deal.require(lambda _stage, start, _stop: net_dt.is_utc(start), message='Expected UTC for start time zone.')
@deal.require(lambda _stage, _start, stop: net_dt.is_utc(stop), message='Expected UTC for stop time zone.')
def median_treating_pressure(stage: IStage,
                             start: Union[pendulum.DateTime, dt.datetime],
                             stop: Union[pendulum.DateTime, dt.datetime]):
    """
    Return the median treating pressure for stage from start to (and including) stop.

    Args:
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.

    Returns:
        The median treating pressure result (measurement and warnings).
    """
    def median_treatment_pressure_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetMedianTreatmentPressure(for_stage.dom_object,
                                                                     net_dt.as_net_date_time(start_time),
                                                                     net_dt.as_net_date_time(stop_time))
        return calculation_result

    result = perform_calculation(median_treatment_pressure_calculation, stage,
                                 _datetime_to_pendulum(start), _datetime_to_pendulum(stop),
                                 opq.PhysicalQuantity.PRESSURE)
    return result


@deal.require(lambda _stage, start, _stop: net_dt.is_utc(start), message='Expected UTC for start time zone.')
@deal.require(lambda _stage, _start, stop: net_dt.is_utc(stop), message='Expected UTC for stop time zone.')
def pumped_fluid_volume(stage: IStage,
                        start: Union[pendulum.DateTime, dt.datetime],
                        stop: Union[pendulum.DateTime, dt.datetime]):
    """
    Return the pumped (fluid) volume for stage from start to (and including) stop.

    Args:
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.

    Returns:
        The pumped (fluid) volume result (measurement and warnings).
    """

    def pumped_fluid_volume_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetPumpedVolume(for_stage.dom_object,
                                                          net_dt.as_net_date_time(start_time),
                                                          net_dt.as_net_date_time(stop_time))
        return calculation_result

    result = perform_calculation(pumped_fluid_volume_calculation, stage,
                                 _datetime_to_pendulum(start), _datetime_to_pendulum(stop),
                                 opq.PhysicalQuantity.VOLUME)
    return result


@deal.require(lambda _stage, start, _stop: net_dt.is_utc(start), message='Expected UTC for start time zone.')
@deal.require(lambda _stage, _start, stop: net_dt.is_utc(stop), message='Expected UTC for stop time zone.')
def total_proppant_mass(stage: IStage,
                        start: Union[pendulum.DateTime, dt.datetime],
                        stop: Union[pendulum.DateTime, dt.datetime]):
    """
    Return the pumped (fluid) volume for stage from start to (and including) stop.

    Args:
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.

    Returns:
        The pumped (fluid) volume result (measurement and warnings).
    """
    def total_proppant_mass_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetTotalProppantMass(for_stage.dom_object,
                                                               net_dt.as_net_date_time(start_time),
                                                               net_dt.as_net_date_time(stop_time))
        return calculation_result

    result = perform_calculation(total_proppant_mass_calculation, stage,
                                 _datetime_to_pendulum(start), _datetime_to_pendulum(stop),
                                 opq.PhysicalQuantity.MASS)
    return result


def _datetime_to_pendulum(source: dt.datetime) -> pendulum.DateTime:
    return pendulum.instance(source).set(tz=pendulum.UTC)
