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

import argparse
import functools
import logging
import pathlib

import clr
import orchid

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import (MonitorExtensions, Leakoff, Observation)
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Factories import FractureDiagnosticsFactory
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Factories.Implementations import LeakoffCurves
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import (
    ScriptAdapter,
)
# noinspection PyUnresolvedReferences
from System import (Array, Double, DateTime, String)
# noinspection PyUnresolvedReferences
from System.IO import (FileStream, FileMode, FileAccess, FileShare)
# noinspection PyUnresolvedReferences
import UnitsNet

clr.AddReference('Orchid.Math')
clr.AddReference('System.Collections')
# noinspection PyUnresolvedReferences
from Orchid.Math import Interpolation
# noinspection PyUnresolvedReferences
from System.Collections.Generic import List


object_factory = FractureDiagnosticsFactory.Create()


def calculate_delta_pressure(leak_off_pressure, maximum_pressure_sample):
    return UnitsNet.Pressure.op_Subtraction(
        UnitsNet.Pressure(maximum_pressure_sample.Value, UnitsNet.Units.PressureUnit.PoundForcePerSquareInch),
        leak_off_pressure)


def calculate_leak_off_control_point_times(interpolation_point_1, interpolation_point_2, ticks):
    time_series_interpolation_points = Array.CreateInstance(Double, 2)
    time_series_interpolation_points[0] = interpolation_point_1.Ticks
    time_series_interpolation_points[1] = interpolation_point_2.Ticks
    time_stamp_ticks = Array.CreateInstance(Double, ticks.Length)
    magnitudes = Array.CreateInstance(Double, ticks.Length)
    for i in range(0, ticks.Length):
        tick = ticks[i]
        time_stamp_ticks[i] = tick.Timestamp.Ticks
        magnitudes[i] = tick.Value
    time_series_interpolant = Interpolation.Interpolant1DFactory.CreatePchipInterpolant(time_stamp_ticks,
                                                                                        magnitudes)
    pressure_values = time_series_interpolant.Interpolate(time_series_interpolation_points, 0)
    control_point_times = List[Leakoff.ControlPoint]()
    control_point_times.Add(Leakoff.ControlPoint(
        DateTime=interpolation_point_1,
        Pressure=UnitsNet.Pressure(pressure_values[0], UnitsNet.Units.PressureUnit.PoundForcePerSquareInch)))
    control_point_times.Add(Leakoff.ControlPoint(
        DateTime=interpolation_point_2,
        Pressure=UnitsNet.Pressure(pressure_values[1], UnitsNet.Units.PressureUnit.PoundForcePerSquareInch)))
    return control_point_times


def calculate_leak_off_pressure(leak_off_curve, maximum_pressure_sample):
    query_times = List[DateTime]()
    query_times.Add(maximum_pressure_sample.Timestamp)
    leak_off_pressure = leak_off_curve.GetPressureValues(query_times)[0]
    return leak_off_pressure


def calculate_maximum_pressure_sample(stage_part, ticks):
    def maximum_pressure_reducer(so_far, candidate):
        if stage_part.StartTime <= candidate.Timestamp <= stage_part.StopTime and candidate.Value > so_far.Value:
            return candidate
        else:
            return so_far

    sentinel_maximum = object_factory.CreateTick[float](DateTime.MinValue, -1000)
    maximum_pressure_sample = functools.reduce(maximum_pressure_reducer, ticks, sentinel_maximum)
    return maximum_pressure_sample


def calculate_stage_part_pressure_samples(native_monitor, stage_part):
    time_range = object_factory.CreateDateTimeOffsetRange(stage_part.StartTime.AddDays(-1),
                                                          stage_part.StopTime.AddDays(1))
    stage_part_pressure_samples = native_monitor.TimeSeries.GetOrderedTimeSeriesHistory(time_range)
    return stage_part_pressure_samples


def calculate_stage_part_visible_time_range(stage_part):
    return stage_part.StartTime.AddHours(-1), stage_part.StopTime.AddHours(1)


def create_observation_control_points(leak_off_curve_times):
    observation_control_points = List[DateTime]()
    observation_control_points.Add(leak_off_curve_times['L1'])
    observation_control_points.Add(leak_off_curve_times['L2'])
    return observation_control_points


def auto_pick_observation_details(unpicked_observation, native_monitor, stage_part):
    # Auto pick observation details to be set
    # - Leak off curve type
    # - Control point times
    # - Visible range x-min time
    # - Visible range x-max time
    # - Position
    # - Delta pressure
    # - Notes
    # - Signal quality

    stage_part_pressure_samples = calculate_stage_part_pressure_samples(native_monitor, stage_part)

    leak_off_curve_times = {
        'L1': stage_part.StartTime.AddMinutes(-20),
        'L2': stage_part.StartTime,
    }
    control_point_times = calculate_leak_off_control_point_times(leak_off_curve_times['L1'],
                                                                 leak_off_curve_times['L2'],
                                                                 stage_part_pressure_samples)

    leak_off_curve = object_factory.CreateLeakoffCurve(Leakoff.LeakoffCurveType.Linear,
                                                       control_point_times)

    maximum_pressure_sample = calculate_maximum_pressure_sample(stage_part, stage_part_pressure_samples)
    leak_off_pressure = calculate_leak_off_pressure(leak_off_curve, maximum_pressure_sample)

    picked_observation = unpicked_observation  # An alias to better communicate intent
    mutable_observation = picked_observation.ToMutable()
    mutable_observation.LeakoffCurveType = Leakoff.LeakoffCurveType.Linear
    mutable_observation.ControlPointTimes = create_observation_control_points(leak_off_curve_times)
    (mutable_observation.VisibleRangeXminTime,
     mutable_observation.VisibleRangeXmaxTime) = calculate_stage_part_visible_time_range(stage_part)
    mutable_observation.Position = maximum_pressure_sample.Timestamp
    mutable_observation.DeltaPressure = calculate_delta_pressure(leak_off_pressure, maximum_pressure_sample)
    mutable_observation.Notes = "Auto-picked"
    mutable_observation.SignalQuality = Observation.SignalQualityValue.UndrainedCompressive
    mutable_observation.Dispose()

    return picked_observation


def auto_pick_observations(native_project, native_monitor):
    stage_parts = MonitorExtensions.FindPossiblyVisibleStageParts(native_monitor, native_project.Wells.Items)

    observation_set = object_factory.CreateObservationSet(native_project, 'Auto-picked Observation Set3')
    for part in stage_parts:
        # Create unpicked observation
        unpicked_observation = object_factory.CreateObservation(native_monitor, part)

        # Auto-pick observation details
        picked_observation = auto_pick_observation_details(unpicked_observation, native_monitor, part)

        # Add picked observation to observation set
        mutable_observation_set = observation_set.ToMutable()
        mutable_observation_set.AddEvent(picked_observation)
        mutable_observation_set.Dispose()

    # Add observation set to project
    project_with_observation_set = native_project  # An alias to better communicate intent
    mutable_project = native_project.ToMutable()
    mutable_project.AddObservationSet(observation_set)
    mutable_project.Dispose()

    return project_with_observation_set


def main(cli_args):
    logging.basicConfig(level=logging.INFO)

    # Read Orchid project
    project = orchid.load_project(cli_args.input_project)
    native_project = project.dom_object
    monitor_name = 'Demo_3H - MonitorWell'
    candidate_monitors = list(project.monitors().find_by_display_name(monitor_name))
    # I actually expect one or more monitors, but I only need one (arbitrarily the first one)
    assert len(candidate_monitors) > 0, (f'One or monitors with display name, "{monitor_name}", expected.'
                                         f' Found {len(candidate_monitors)}.')
    native_monitor = candidate_monitors[0].dom_object
    auto_pick_observations(native_project, native_monitor)

    # Log changed project data
    if cli_args.verbosity >= 2:
        logging.info(f'{native_project.Name=}')
        logging.info(f'{len(native_project.ObservationSets.Items)=}')
        for observation_set in native_project.ObservationSets.Items:
            logging.info(f'{observation_set.Name=}')
            logging.info(f'{len(observation_set.LeakOffObservations.Items)=}')
            logging.info(f'{len(observation_set.GetObservations())=}')

    # Write Orchid project
    target_path_name = cli_args.output_project
    with orchid.script_adapter_context.ScriptAdapterContext():
        writer = ScriptAdapter.CreateProjectFileWriter()
        use_binary_format = False
        writer.Write(native_project, target_path_name, use_binary_format)
        if cli_args.verbosity >= 1:
           logging.info(f'Wrote changes to "{target_path_name}"')

    return


def make_project_path_name(project_dir_name, project_file_name):
    return str(project_dir_name.joinpath(project_file_name))


def make_target_file_name_from_source(source_file_name):
    return ''.join([source_file_name.stem, '.999', source_file_name.suffix])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automatically pick leak off observations.")
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2], default=0,
                        help='Increase output verbosity. (Default: 0; that is, least output.)')

    default_file_name_to_read = pathlib.Path('frankNstein_Bakken_UTM13_FEET.ifrac')
    default_project_path_name_to_read = make_project_path_name(orchid.training_data_path(),
                                                               default_file_name_to_read)
    parser.add_argument('input_project', help=f'Path name of project to read.')

    default_file_name_to_write = make_target_file_name_from_source(default_file_name_to_read)
    default_project_path_name_to_write = make_project_path_name(orchid.training_data_path(),
                                                                default_file_name_to_write)
    parser.add_argument('-o', '--output_project', default=default_project_path_name_to_write,
                        help=f'Filename of project to write. (Default: {default_project_path_name_to_write}')

    args = parser.parse_args()
    main(args)

