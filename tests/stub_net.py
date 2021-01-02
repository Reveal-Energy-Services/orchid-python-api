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

"""A module for creating 'stub" .NET classes for use in testing.

Note that these stubs are "duck typing" stubs for .NET classes; that is, they have the same methods and
properties required during testing but do not actually implement the .NET class interfaces.
"""

from collections import namedtuple
from datetime import datetime, timedelta
import itertools
import unittest.mock
from typing import Sequence

import toolz.curried as toolz

from orchid import (
    native_treatment_curve_adapter as ontc,
    net_quantity as onq,
    unit_system as units,
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import (IProject, IPlottingSettings, IWell, IStage,
                                        IStageSampledQuantityTimeSeries, ISubsurfacePoint,
                                        IWellSampledQuantityTimeSeries, IWellTrajectory,
                                        UnitSystem)
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import ITreatmentCalculations, IFractureDiagnosticsCalculationsFactory
# noinspection PyUnresolvedReferences
import UnitsNet

MeasurementAsUnit = namedtuple('MeasurementAsUnit', ['measurement', 'as_unit'])
StubMeasurement = namedtuple('StubMeasurement', ['magnitude', 'unit'])
StubSample = namedtuple('StubSample', ['Timestamp', 'Value'], module=__name__)
StubSubsurfaceLocation = namedtuple('StubSubsurfaceLocation', ['x', 'y', 'depth'])


class StubNetSample:
    def __init__(self, time_point: datetime, value: float):
        # I chose to use capitalized names for compatability with .NET
        self.Timestamp = DateTime(time_point.year, time_point.month, time_point.day, time_point.hour,
                                  time_point.minute, time_point.second)
        self.Value = value


def create_30_second_time_points(start_time_point: datetime, count: int):
    """
    Create a sequence of `count` time points, 30-seconds apart.
    :param start_time_point: The starting time point of the sequence.
    :param count: The number of time points in the sequence.
    :return: The sequence of time points.
    """
    return [start_time_point + i * timedelta(seconds=30) for i in range(count)]


def create_stub_net_time_series(start_time_point: datetime, sample_values) -> Sequence[StubNetSample]:
    """
    Create a stub .NET time series.

    The "stub .NET" nature is satisfied by returning a sequence in which each item is an instance of `StubNetSample`.

    :param start_time_point: The time point at which the time series starts.
    :param sample_values: The values in the stub samples.
    :return: A sequence a samples implementing the `ITick<double>` interface using "duck typing."
    """
    sample_time_points = create_30_second_time_points(start_time_point, len(sample_values))
    samples = [StubNetSample(st, sv) for (st, sv) in zip(sample_time_points, sample_values)]
    return samples


class StubNetTreatmentCurve:
    def __init__(self, curve_name, curve_quantity, time_series):
        self._time_series = time_series
        self.SampledQuantityName = curve_name
        if curve_quantity == 'pressure':
            self.SampledQuantityType = UnitsNet.QuantityType.Pressure
        elif curve_quantity == 'ratio':
            self.SampledQuantityType = UnitsNet.QuantityType.Ratio

    # noinspection PyPep8Naming
    def GetOrderedTimeSeriesHistory(self):
        return self._time_series


def make_length_unit(scalar_quantity):
    if scalar_quantity.unit == units.UsOilfield.LENGTH:
        return UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(scalar_quantity.magnitude),
                                    UnitsNet.Units.LengthUnit.Foot)
    elif scalar_quantity.unit == units.Metric.LENGTH:
        return UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(scalar_quantity.magnitude),
                                    UnitsNet.Units.LengthUnit.Meter)

    raise ValueError(f'Unknown (length) unit: {scalar_quantity.unit.unit}')


def create_net_treatment(start_time_point, treating_pressure_values, rate_values, concentration_values):
    treating_pressure_time_series = create_stub_net_time_series(start_time_point, treating_pressure_values)
    treating_pressure_curve = StubNetTreatmentCurve(ontc.TREATING_PRESSURE, 'pressure',
                                                    treating_pressure_time_series)
    rate_time_series = create_stub_net_time_series(start_time_point, rate_values)
    rate_curve = StubNetTreatmentCurve(ontc.SLURRY_RATE, 'ratio', rate_time_series)
    concentration_time_series = create_stub_net_time_series(start_time_point, concentration_values)
    concentration_curve = StubNetTreatmentCurve(ontc.PROPPANT_CONCENTRATION, 'ratio',
                                                concentration_time_series)

    return [treating_pressure_curve, rate_curve, concentration_curve]


def create_stub_net_calculations_factory(warnings=None, calculation_unit=None,
                                         pressure_magnitude=None, volume_magnitude=None, mass_magnitude=None):
    stub_native_calculation_result = unittest.mock.MagicMock(name='stub_calculation_result')
    stub_native_calculation_result.Warnings = warnings if warnings is not None else []

    stub_native_treatment_calculations = unittest.mock.MagicMock(name='stub_calculations',
                                                                 autospec=ITreatmentCalculations)

    if pressure_magnitude is not None:
        net_pressure = UnitsNet.Pressure.From(UnitsNet.QuantityValue.op_Implicit(pressure_magnitude),
                                              calculation_unit.net_unit)
        stub_native_calculation_result.Result = net_pressure
        stub_native_treatment_calculations.GetMedianTreatmentPressure = unittest.mock.MagicMock(
            return_value=stub_native_calculation_result)

    if volume_magnitude is not None:
        net_volume = UnitsNet.Volume.From(UnitsNet.QuantityValue.op_Implicit(volume_magnitude),
                                          calculation_unit.net_unit)
        stub_native_calculation_result.Result = net_volume
        stub_native_treatment_calculations.GetPumpedVolume = unittest.mock.MagicMock(
            return_value=stub_native_calculation_result)

    if mass_magnitude is not None:
        net_mass = UnitsNet.Mass.From(UnitsNet.QuantityValue.op_Implicit(mass_magnitude),
                                      calculation_unit.net_unit)
        stub_native_calculation_result.Result = net_mass
        stub_native_treatment_calculations.GetTotalProppantMass = unittest.mock.MagicMock(
            return_value=stub_native_calculation_result)

    stub_native_calculations_factory = unittest.mock.MagicMock(name='stub_calculations_factory',
                                                               autospec=IFractureDiagnosticsCalculationsFactory)
    stub_native_calculations_factory.CreateTreatmentCalculations = unittest.mock.MagicMock(
        return_value=stub_native_treatment_calculations)

    return stub_native_calculations_factory


def create_stub_net_stage(cluster_count=-1, display_stage_no=-1, md_top=None, md_bottom=None,
                          stage_location_bottom=None, stage_location_cluster=None,
                          stage_location_center=None, stage_location_top=None,
                          start_time=None, stop_time=None, treatment_curve_names=None):
    stub_net_stage_name = 'stub_net_stage'
    try:
        result = unittest.mock.MagicMock(name=stub_net_stage_name, spec=IStage)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        result = unittest.mock.MagicMock(name=stub_net_stage_name)
    result.NumberOfClusters = cluster_count
    result.DisplayStageNumber = display_stage_no
    if md_top is not None:
        result.MdTop = onq.as_net_quantity_in_different_unit(md_top.measurement, md_top.as_unit)
    if md_bottom is not None:
        result.MdBottom = onq.as_net_quantity_in_different_unit(md_bottom.measurement, md_bottom.as_unit)
    if stage_location_bottom is not None:
        if callable(stage_location_bottom):
            result.GetStageLocationBottom = unittest.mock.MagicMock('stub_get_stage_bottom_location',
                                                                    side_effect=stage_location_bottom)
    if stage_location_center is not None:
        if callable(stage_location_center):
            result.GetStageLocationCenter = unittest.mock.MagicMock('stub_get_stage_center_location',
                                                                    side_effect=stage_location_center)
    if stage_location_cluster is not None:
        if callable(stage_location_cluster):
            result.GetStageLocationCluster = unittest.mock.MagicMock('stub_get_stage_cluster_location',
                                                                     side_effect=stage_location_cluster)
    if stage_location_top is not None:
        if callable(stage_location_top):
            result.GetStageLocationTop = unittest.mock.MagicMock('stub_get_stage_top_location',
                                                                 side_effect=stage_location_top)
    if start_time is not None:
        result.StartTime = onq.as_net_date_time(start_time)
    if stop_time is not None:
        result.StopTime = onq.as_net_date_time(stop_time)

    if treatment_curve_names is not None:
        result.TreatmentCurves.Items = list(toolz.map(
            lambda sampled_quantity_name: create_stub_net_treatment_curve(
                sampled_quantity_name=sampled_quantity_name), treatment_curve_names))
    else:
        result.TreatmentCurves.Items = []

    return result


def create_stub_net_subsurface_point(x=None, y=None, depth=None, xy_origin=None, depth_origin=None):
    try:
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point')
    if x is not None:
        stub_subsurface_point.X = make_length_unit(x)
    if y is not None:
        stub_subsurface_point.Y = make_length_unit(y)
    if depth is not None:
        stub_subsurface_point.Depth = make_length_unit(depth)
    if xy_origin is not None:
        stub_subsurface_point.WellReferenceFrameXy = xy_origin
    if depth_origin is not None:
        stub_subsurface_point.DepthDatum = depth_origin
    return stub_subsurface_point


def create_stub_net_trajectory_array(magnitudes, net_unit):
    result = [UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(magnitude), net_unit)
              for magnitude in magnitudes] if magnitudes else []
    return result


def create_stub_net_treatment_curve(name=None, display_name=None,
                                    sampled_quantity_name=None, suffix=None,
                                    values_starting_at=None, project=None):
    try:
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                           spec=IStageSampledQuantityTimeSeries)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_net_treatment_curve = unittest.mock.MagicMock(name='stub_treatment_curve')
    if name is not None:
        stub_net_treatment_curve.Name = name
    if display_name is not None:
        stub_net_treatment_curve.DisplayName = display_name
    if sampled_quantity_name is not None:
        stub_net_treatment_curve.SampledQuantityName = sampled_quantity_name
    if suffix is not None:
        stub_net_treatment_curve.Suffix = suffix
    if values_starting_at is not None:
        values, start_time_point = values_starting_at
        time_points = [start_time_point + n * timedelta(seconds=30) for n in range(len(values))]
        samples = [StubSample(t, v) for (t, v) in zip(map(onq.as_net_date_time, time_points), values)]
        stub_net_treatment_curve.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(name='stub_time_series',
                                                                                       return_value=samples)
    if project is not None:
        stub_net_treatment_curve.Stage.Well.Project = project

    return stub_net_treatment_curve


def create_stub_net_monitor_curve(name, display_name, sampled_quantity_name, sampled_quantity_type,
                                  samples, project):
    try:
        stub_net_monitor_curve = unittest.mock.MagicMock(name='stub_treatment_curve',
                                                         spec=IWellSampledQuantityTimeSeries)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_net_monitor_curve = unittest.mock.MagicMock(name='stub_treatment_curve')
    stub_net_monitor_curve.Name = name
    stub_net_monitor_curve.DisplayName = display_name
    stub_net_monitor_curve.SampledQuantityName = sampled_quantity_name
    stub_net_monitor_curve.SampledQuantityType = sampled_quantity_type
    stub_net_monitor_curve.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(name='stub_time_series',
                                                                                 return_value=samples)
    if project is not None:
        stub_net_monitor_curve.Well.Project = project

    return stub_net_monitor_curve


def create_stub_net_well_trajectory(project_units=None, easting_magnitudes=None, northing_magnitudes=None):
    try:
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory')
    if project_units is not None:
        stub_trajectory.Well.Project = create_stub_net_project(project_units=project_units)
    if easting_magnitudes is not None and project_units is not None:
        stub_eastings = create_stub_net_trajectory_array(easting_magnitudes,
                                                         project_units.LENGTH.value.net_unit)
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=stub_eastings)
    if northing_magnitudes is not None and project_units is not None:
        stub_northings = create_stub_net_trajectory_array(northing_magnitudes,
                                                          project_units.LENGTH.value.net_unit)
        stub_trajectory.GetNorthingArray = unittest.mock.MagicMock(name='stub_northings', return_value=stub_northings)

    return stub_trajectory


def get_mock_easting_array(stub_new_well_trajectory):
    return stub_new_well_trajectory.GetEastingArray


def get_mock_northing_array(stub_new_well_trajectory):
    return stub_new_well_trajectory.GetNorthingArray


def quantity_coordinate(raw_coordinates, i, stub_net_project):
    result = [UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(c), stub_net_project.ProjectUnits.LengthUnit)
              for c in raw_coordinates[i]] if raw_coordinates else []
    return result


def create_stub_net_project(name='', default_well_colors=None,
                            project_units=None,
                            well_names=None, well_display_names=None, uwis=None,
                            eastings=None, northings=None, tvds=None,
                            curve_names=None, samples=None, curves_physical_quantities=None):
    default_well_colors = default_well_colors if default_well_colors else [[]]
    well_names = well_names if well_names else []
    well_display_names = well_display_names if well_display_names else []
    uwis = uwis if uwis else []
    eastings = eastings if eastings else []
    northings = northings if northings else []
    tvds = tvds if tvds else []
    curve_names = curve_names if curve_names else []
    samples = samples if samples else []
    curves_physical_quantities = (curves_physical_quantities
                                  if curves_physical_quantities
                                  else list(itertools.repeat('pressure', len(curve_names))))

    try:
        stub_net_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_net_project = unittest.mock.MagicMock(name='stub_net_project')
    stub_net_project.Name = name
    try:
        plotting_settings = unittest.mock.MagicMock(name='stub_plotting_settings', spec=IPlottingSettings)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        plotting_settings = unittest.mock.MagicMock(name='stub_plotting_settings')
    plotting_settings.GetDefaultWellColors = unittest.mock.MagicMock(name='stub_default_well_colors',
                                                                     return_value=default_well_colors)
    stub_net_project.PlottingSettings = plotting_settings

    if project_units == units.UsOilfield:
        stub_net_project.ProjectUnits = UnitSystem.USOilfield()
    elif project_units == units.Metric:
        stub_net_project.ProjectUnits = UnitSystem.Metric()

    try:
        stub_net_project.Wells.Items = [unittest.mock.MagicMock(name=well_name, spec=IWell) for well_name in well_names]
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_net_project.Wells.Items = [unittest.mock.MagicMock(name=well_name) for well_name in well_names]

    for i in range(len(well_names)):
        stub_well = stub_net_project.Wells.Items[i]
        stub_well.Uwi = uwis[i] if uwis else None
        stub_well.DisplayName = well_display_names[i] if well_display_names else None
        stub_well.Name = well_names[i]

        # The Pythonnet package has an open issue that the "Implicit Operator does not work from python"
        # (https://github.com/pythonnet/pythonnet/issues/253).
        #
        # One of the comments identifies a work-around from StackOverflow
        # (https://stackoverflow.com/questions/11544056/how-to-cast-implicitly-on-a-reflected-method-call/11563904).
        # This post states that "the trick is to realize that the compiler creates a special static method
        # called `op_Implicit` for your implicit conversion operator."
        stub_well.Trajectory.GetEastingArray.return_value = quantity_coordinate(eastings, i, stub_net_project)
        stub_well.Trajectory.GetNorthingArray.return_value = quantity_coordinate(northings, i, stub_net_project)
        stub_well.Trajectory.GetTvdArray.return_value = quantity_coordinate(tvds, i, stub_net_project)

    try:
        stub_net_project.WellTimeSeriesList.Items = [unittest.mock.MagicMock(
            name=curve_name, spec=IWellSampledQuantityTimeSeries) for curve_name in curve_names]
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_net_project.WellTimeSeriesList.Items = [unittest.mock.MagicMock(name=curve_name)
                                                     for curve_name in curve_names]
    quantity_name_type_map = {'pressure': UnitsNet.QuantityType.Pressure,
                              'temperature': UnitsNet.QuantityType.Temperature}
    for i in range(len(curve_names)):
        stub_curve = stub_net_project.WellTimeSeriesList.Items[i]
        stub_curve.DisplayName = curve_names[i] if curve_names else None
        stub_curve.SampledQuantityType = quantity_name_type_map[curves_physical_quantities[i]]
        stub_curve.GetOrderedTimeSeriesHistory.return_value = samples[i] if len(samples) > 0 else []

    return stub_net_project
