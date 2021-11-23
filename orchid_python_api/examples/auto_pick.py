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
from System import (DateTime, String)
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


BAKKEN_PROJECT_FILE_NAME = 'frankNstein_Bakken_UTM13_FEET.ifrac'


def auto_pick_observations(native_project, native_monitor):
    stgParts = MonitorExtensions.FindPossiblyVisibleStageParts(native_monitor, native_project.Wells.Items)

    fracture_diagnostics_factory = FractureDiagnosticsFactory.Create()
    observationSet = fracture_diagnostics_factory.CreateObservationSet(native_project, 'Auto-picked Observation Set3')

    for part in stgParts:

        timeRange = fracture_diagnostics_factory.CreateDateTimeOffsetRange(part.StartTime.AddDays(-1),
                                                                           part.StopTime.AddDays(1))
        ticks = native_monitor.TimeSeries.GetOrderedTimeSeriesHistory(timeRange)

        xvals = List[float]()
        yvals = List[float]()

        nTicks = ticks.Length
        for i in range(0, nTicks):
            tick = ticks[i]
            xvals.Add(tick.Timestamp.Ticks)
            yvals.Add(tick.Value)

        timeSeriesInterpolant = Interpolation.Interpolant1DFactory.CreatePchipInterpolant(xvals.ToArray(),
                                                                                          yvals.ToArray())
        L1 = LeakoffCurves.LeakoffCurveControlPointTime()
        L1.Active = 1
        L1.Time = part.StartTime.AddMinutes(-20)

        L2 = LeakoffCurves.LeakoffCurveControlPointTime()
        L2.Active = 1
        L2.Time = part.StartTime

        L3 = LeakoffCurves.LeakoffCurveControlPointTime()
        L3.Active = 0
        L3.Time = part.StartTime.AddMinutes(10)

        timeSeriesInterpolationPoints = List[float]()
        timeSeriesInterpolationPoints.Add(L1.Time.Ticks)
        timeSeriesInterpolationPoints.Add(L2.Time.Ticks)

        pVals = timeSeriesInterpolant.Interpolate(timeSeriesInterpolationPoints.ToArray(), 0)

        controlPointTimes = List[Leakoff.ControlPoint]()
        controlPointTimes.Add(Leakoff.ControlPoint(
            DateTime=L1.Time, Pressure=UnitsNet.Pressure(pVals[0],
                                                         UnitsNet.Units.PressureUnit.PoundForcePerSquareInch)))
        controlPointTimes.Add(Leakoff.ControlPoint(
            DateTime=L2.Time,
            Pressure=UnitsNet.Pressure(pVals[1],
                                       UnitsNet.Units.PressureUnit.PoundForcePerSquareInch)))

        leakoffCurve = fracture_diagnostics_factory.CreateLeakoffCurve(Leakoff.LeakoffCurveType.Linear,
                                                                       controlPointTimes)

        maxP = -1000
        ts = DateTime.MinValue
        for tick in ticks:
            if tick.Timestamp >= part.StartTime and tick.Timestamp <= part.StopTime and tick.Value > maxP:
                maxP = tick.Value
                ts = tick.Timestamp

        queryTimes = List[DateTime]()
        queryTimes.Add(ts)
        leakoffP = leakoffCurve.GetPressureValues(queryTimes)[0]

        observation = fracture_diagnostics_factory.CreateObservation(native_monitor, part)
        obsCtrlPointTimes = List[DateTime]()
        obsCtrlPointTimes.Add(L1.Time)
        obsCtrlPointTimes.Add(L2.Time)

        mutableObservation = observation.ToMutable()
        mutableObservation.LeakoffCurveType = Leakoff.LeakoffCurveType.Linear
        mutableObservation.ControlPointTimes = obsCtrlPointTimes
        mutableObservation.VisibleRangeXminTime = part.StartTime.AddHours(-1)
        mutableObservation.VisibleRangeXmaxTime = part.StopTime.AddHours(1)
        mutableObservation.Position = ts
        mutableObservation.DeltaPressure = UnitsNet.Pressure.op_Subtraction(
                UnitsNet.Pressure(maxP, UnitsNet.Units.PressureUnit.PoundForcePerSquareInch), leakoffP)
        mutableObservation.Notes = "Auto-picked"
        mutableObservation.SignalQuality = Observation.SignalQualityValue.UndrainedCompressive
        mutableObservation.Dispose()

        mutableObservationSet = observationSet.ToMutable()
        mutableObservationSet.AddEvent(observation)
        mutableObservationSet.Dispose()

    mutableProject = native_project.ToMutable()
    mutableProject.AddObservationSet(observationSet)
    mutableProject.Dispose()


def main():
    # Read Orchid project
    orchid_training_data_path = orchid.training_data_path()
    project = orchid.load_project(str(orchid_training_data_path.joinpath(BAKKEN_PROJECT_FILE_NAME)))
    monitor_name = 'Demo_3H - MonitorWell'
    candidate_monitors = list(project.monitors().find_by_display_name(monitor_name))
    # I actually expect one or more monitors, but I only need one (arbitrarily the first one)
    assert len(candidate_monitors) > 0, f'One or monitors with display name, "{monitor_name}", expected.' \
                                        f' Found {len(candidate_monitors)}.'
    native_monitor = candidate_monitors[0].dom_object
    native_project = project.dom_object
    auto_pick_observations(native_project, native_monitor)

    # Print changed data
    print(native_project.Name)
    print(f'{len(native_project.ObservationSets.Items)=}')
    for observation_set in native_project.ObservationSets.Items:
        print(f'Observation set name: {observation_set.Name}')
        print(f'{len(observation_set.LeakOffObservations.Items)=}')
    print(f'{len(observation_set.GetObservations())=}')

    # Write Orchid project
    source_file_name = pathlib.Path(BAKKEN_PROJECT_FILE_NAME)
    target_file_name = ''.join([source_file_name.stem, '.999', source_file_name.suffix])
    target_path_name = str(orchid_training_data_path.joinpath(target_file_name))
    with orchid.script_adapter_context.ScriptAdapterContext():
        writer = ScriptAdapter.CreateProjectFileWriter()
        use_binary_format = False
        writer.Write(native_project, target_path_name, use_binary_format)

    return


if __name__ == '__main__':
    main()
