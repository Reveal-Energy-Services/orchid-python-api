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

import clr
import orchid

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import (MonitorExtensions, Leakoff, Observation)
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Factories import FractureDiagnosticsFactory
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Factories.Implementations import LeakoffCurves
# noinspection PyUnresolvedReferences
from System import (DateTime, String)
# noinspection PyUnresolvedReferences
import UnitsNet

clr.AddReference('Orchid.Math')
clr.AddReference('System.Collections')
# noinspection PyUnresolvedReferences
from Orchid.Math import Interpolation
# noinspection PyUnresolvedReferences
from System.Collections.Generic import List


def auto_pick_observations(project):
    monitor = ''
    for mItem in project.Monitors.Items:
        if mItem.DisplayName == 'Demo_3H - MonitorWell':
            monitor = mItem

    stgParts = MonitorExtensions.FindPossiblyVisibleStageParts(monitor, project.Wells.Items)
    print(f'{len(stgParts)=}')

    fracture_diagnostics_factory = FractureDiagnosticsFactory.Create()
    observationSet = fracture_diagnostics_factory.CreateObservationSet(project, 'Auto-picked Observation Set3')

    for part in stgParts:

        timeRange = fracture_diagnostics_factory.CreateDateTimeOffsetRange(part.StartTime.AddDays(-1),
                                                                           part.StopTime.AddDays(1))
        ticks = monitor.TimeSeries.GetOrderedTimeSeriesHistory(timeRange)

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

        observation = fracture_diagnostics_factory.CreateObservation(monitor, part)
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

    mutableProject = project.ToMutable()
    mutableProject.AddObservationSet(observationSet)
    mutableProject.Dispose()


def main():
    orchid_training_data_path = orchid.training_data_path()
    project = orchid.load_project(str(orchid_training_data_path.joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')))
    native_project = project.dom_object
    auto_pick_observations(native_project)
    print(native_project.Name)
    print(f'{len(native_project.ObservationSets.Items)=}')
    for observation_set in native_project.ObservationSets.Items:
        print(f'{len(observation_set.LeakOffObservations.Items)=}')
    print(f'{len(observation_set.GetObservations())=}')
    return


if __name__ == '__main__':
    main()
