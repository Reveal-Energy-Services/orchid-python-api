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

import orchid.native_treatment_curve_facade as ontc
import orchid.net_quantity as onq

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import (IProject, IPlottingSettings, IWell, IStage,
                                        IStageSampledQuantityTimeSeries, ISubsurfacePoint,
                                        IWellSampledQuantityTimeSeries, IWellTrajectory)
# noinspection PyUnresolvedReferences
import UnitsNet


MeasurementAsUnit = namedtuple('MeasurementAsUnit', ['measurement', 'as_unit_abbreviation'])


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
    return UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(scalar_quantity.magnitude),
                                scalar_quantity.unit.net_unit)


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


def set_project_unit(stub_net_project, abbreviation):
    def set_length_foot_unit():
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Foot

    def set_length_meter_unit():
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Meter

    def set_mass_lb_unit():
        stub_net_project.ProjectUnits.MassUnit = UnitsNet.Units.MassUnit.Pound

    def set_mass_kg_unit():
        stub_net_project.ProjectUnits.MassUnit = UnitsNet.Units.MassUnit.Kilogram

    def set_pressure_psi_unit():
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.PoundForcePerSquareInch

    def set_pressure_kpa_unit():
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.Kilopascal

    def set_pressure_mpa_unit():
        stub_net_project.ProjectUnits.PressureUnit = UnitsNet.Units.PressureUnit.Megapascal

    def set_slurry_rate_bpm_unit():
        stub_net_project.ProjectUnits.SlurryRateUnit.Item1 = UnitsNet.Units.VolumeUnit.OilBarrel
        stub_net_project.ProjectUnits.SlurryRateUnit.Item2 = UnitsNet.Units.DurationUnit.Minute

    def set_slurry_rate_m3_per_min_unit():
        stub_net_project.ProjectUnits.SlurryRateUnit.Item1 = UnitsNet.Units.VolumeUnit.CubicMeter
        stub_net_project.ProjectUnits.SlurryRateUnit.Item2 = UnitsNet.Units.DurationUnit.Minute

    def set_proppant_concentration_lb_gal_unit():
        stub_net_project.ProjectUnits.ProppantConcentrationUnit.Item1 = UnitsNet.Units.MassUnit.Pound
        stub_net_project.ProjectUnits.ProppantConcentrationUnit.Item2 = UnitsNet.Units.VolumeUnit.UsGallon

    def set_proppant_concentration_kg_per_m3_unit():
        stub_net_project.ProjectUnits.ProppantConcentrationUnit.Item1 = UnitsNet.Units.MassUnit.Kilogram
        stub_net_project.ProjectUnits.ProppantConcentrationUnit.Item2 = UnitsNet.Units.VolumeUnit.CubicMeter

    def set_temperature_f_unit():
        stub_net_project.ProjectUnits.TemperatureUnit = UnitsNet.Units.TemperatureUnit.DegreeFahrenheit

    def set_temperature_c_unit():
        stub_net_project.ProjectUnits.TemperatureUnit = UnitsNet.Units.TemperatureUnit.DegreeCelsius

    abbreviation_unit_map = {'ft': set_length_foot_unit,
                             'm': set_length_meter_unit,
                             'lb': set_mass_lb_unit,
                             'kg': set_mass_kg_unit,
                             'psi': set_pressure_psi_unit,
                             'kPa': set_pressure_kpa_unit,
                             'MPa': set_pressure_mpa_unit,
                             'bbl/min': set_slurry_rate_bpm_unit,
                             'm^3/min': set_slurry_rate_m3_per_min_unit,
                             'lb/gal (U.S.)': set_proppant_concentration_lb_gal_unit,
                             'kg/m^3': set_proppant_concentration_kg_per_m3_unit,
                             'F': set_temperature_f_unit,
                             'C': set_temperature_c_unit}

    if abbreviation in abbreviation_unit_map.keys():
        abbreviation_unit_map[abbreviation]()


def create_stub_stage(display_stage_no=-1, md_top=None, md_bottom=None, stage_location_center=None,
                      start_time=None, stop_time=None, treatment_curve_names=None):
    result = unittest.mock.MagicMock(name=display_stage_no, spec=IStage)
    result.DisplayStageNumber = display_stage_no
    if md_top is not None:
        result.MdTop = onq.as_net_quantity_in_different_unit(md_top.measurement, md_top.as_unit_abbreviation)
    if md_bottom is not None:
        result.MdBottom = onq.as_net_quantity_in_different_unit(md_bottom.measurement, md_bottom.as_unit_abbreviation)
    if stage_location_center is not None:
        if callable(stage_location_center):
            result.GetStageLocationCenter = unittest.mock.MagicMock('stub_get_stage_center_location',
                                                                    side_effect=stage_location_center)
    if start_time is not None:
        result.StartTime = onq.as_net_date_time(start_time)
    if stop_time is not None:
        result.StopTime = onq.as_net_date_time(stop_time)

    def make_stub_treatment_curve(name):
        stub_treatment_curve = unittest.mock.MagicMock(name='Treatment Curve', spec=IStageSampledQuantityTimeSeries)
        stub_treatment_curve.SampledQuantityName = name
        return stub_treatment_curve

    if treatment_curve_names is not None:
        result.TreatmentCurves.Items = list(toolz.map(make_stub_treatment_curve, treatment_curve_names))
    else:
        result.TreatmentCurves.Items = []

    return result


def create_stub_subsurface_point(x=None, y=None, depth=None, xy_origin=None, depth_origin=None):
    stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
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


def create_stub_net_well_trajectory(project_length_unit=None, easting_magnitudes=None, northing_magnitudes=None):
    stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
    if project_length_unit is not None:
        stub_trajectory.Well.Project = create_stub_net_project(
            project_length_unit_abbreviation=project_length_unit.abbreviation)
    if easting_magnitudes is not None and project_length_unit is not None:
        stub_eastings = create_stub_net_trajectory_array(easting_magnitudes,
                                                         project_length_unit.net_unit)
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=stub_eastings)
    if northing_magnitudes is not None and project_length_unit is not None:
        stub_northings = create_stub_net_trajectory_array(northing_magnitudes,
                                                          project_length_unit.net_unit)
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
                            project_length_unit_abbreviation='',
                            project_mass_unit_abbreviation='',
                            project_pressure_unit_abbreviation='',
                            slurry_rate_unit_abbreviation='', proppant_concentration_unit_abbreviation='',
                            project_temperature_unit_abbreviation='',
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

    stub_net_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
    stub_net_project.Name = name
    plotting_settings = unittest.mock.MagicMock(name='stub_plotting_settings', spec=IPlottingSettings)
    plotting_settings.GetDefaultWellColors = unittest.mock.MagicMock(name='stub_default_well_colors',
                                                                     return_value=default_well_colors)
    stub_net_project.PlottingSettings = plotting_settings
    set_project_unit(stub_net_project, project_length_unit_abbreviation)
    set_project_unit(stub_net_project, project_mass_unit_abbreviation)
    set_project_unit(stub_net_project, project_pressure_unit_abbreviation)
    set_project_unit(stub_net_project, slurry_rate_unit_abbreviation)
    set_project_unit(stub_net_project, proppant_concentration_unit_abbreviation)
    set_project_unit(stub_net_project, project_temperature_unit_abbreviation)

    stub_net_project.Wells.Items = [unittest.mock.MagicMock(name=well_name, spec=IWell) for well_name in well_names]

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

    stub_net_project.WellTimeSeriesList.Items = \
        [unittest.mock.MagicMock(name=curve_name, spec=IWellSampledQuantityTimeSeries)
         for curve_name in curve_names]
    quantity_name_type_map = {'pressure': UnitsNet.QuantityType.Pressure,
                              'temperature': UnitsNet.QuantityType.Temperature}
    for i in range(len(curve_names)):
        stub_curve = stub_net_project.WellTimeSeriesList.Items[i]
        stub_curve.DisplayName = curve_names[i] if curve_names else None
        stub_curve.SampledQuantityType = quantity_name_type_map[curves_physical_quantities[i]]
        stub_curve.GetOrderedTimeSeriesHistory.return_value = samples[i] if len(samples) > 0 else []

    return stub_net_project
