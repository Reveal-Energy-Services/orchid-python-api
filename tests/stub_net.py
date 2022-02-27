#  Copyright (c) 2017-2022 Reveal Energy Services, Inc 
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
import itertools
import unittest.mock
from typing import Sequence

import pendulum
import toolz.curried as toolz

from orchid import (
    measurement as om,
    net_date_time as ndt,
    net_quantity as onq,
    unit_system as units,
)

from tests import (
    stub_net_data_table as stub_ndt,
    stub_net_date_time as stub_dt,
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import (IMonitor,
                                        IProject,
                                        IProjectObject,
                                        IPlottingSettings,
                                        IStage,
                                        IStagePart,
                                        ISubsurfacePoint,
                                        IWell,
                                        IWellTrajectory,
                                        UnitSystem)
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import ITreatmentCalculations, IFractureDiagnosticsCalculationsFactory
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.DataFrames import IStaticDataFrame
# noinspection PyUnresolvedReferences,PyPackageRequirementsk
from Orchid.FractureDiagnostics.TimeSeries import IStageSampledQuantityTimeSeries, IWellSampledQuantityTimeSeries
# noinspection PyUnresolvedReferences
import UnitsNet
# noinspection PyUnresolvedReferences
from System import Array, DateTime, Guid, Type
# noinspection PyUnresolvedReferences
from System.Data import DataColumn, DataTable


# A recognizable (hex word "testable") value for "don't care" Guid / UUID
_DONT_CARE_ID = '7e57ab1e-7e57-ab1e-7e57-ab1e7e57ab1e'

# Other recognizable hex word values for don't care
DONT_CARE_ID_A = 'acc01ade-acc0-1ade-acc0-1adeacc01ade'  # accolade
DONT_CARE_ID_B = 'ba5eba11-ba5e-ba11-ba5e-ba11ba5eba11'  # baseball
DONT_CARE_ID_C = 'ca11ab1e-ca11-ab1e-ca11-ab1eca11ab1e'  # callable
DONT_CARE_ID_D = 'de7ec7ed-de7e-c7ed-de7e-c7edde7ec7ed'  # detected
DONT_CARE_ID_E = 'e5ca1ade-e5ca-1ade-e5ca-1adee5ca1ade'  # escalade


MeasurementAsUnit = namedtuple('MeasurementAsUnit', ['measurement', 'as_unit'])
MeasurementDto = namedtuple('MeasurementDto', ['magnitude', 'unit'])
StubProjectBounds = namedtuple('StubProjectBounds', ['min_x', 'max_x', 'min_y', 'max_y', 'min_depth', 'max_depth'])
StubPythonTimesSeriesArraysDto = namedtuple('StubPythonTimesSeriesArraysDto', ['SampleMagnitudes',
                                                                               'UnixTimeStampsInSeconds'])
StubSample = namedtuple('StubSample', ['Timestamp', 'Value'], module=__name__)
StubSubsurfaceLocation = namedtuple('StubSubsurfaceLocation', ['x', 'y', 'depth'])
StubSurfaceLocation = namedtuple('StubSurfaceLocation', ['x', 'y'])
StubWellHeadLocation = namedtuple('StubWellHeadLocation', ['easting', 'northing', 'depth'])
TableDataDto = namedtuple('TableDataDto', ['column_types', 'table_data', 'rename_column_func'])


make_measurement_dto = toolz.flip(MeasurementDto)
"""This callable creates instances of `MeasurementDto` allowing a caller to supply a single unit as the first
argument and providing the magnitude later."""


class StubNetSample:
    def __init__(self, time_point: pendulum.DateTime, value: float):
        # I chose to use capitalized names for compatability with .NET
        if time_point.tzinfo != pendulum.tz.UTC:
            raise ValueError(f'Cannot create .NET DateTime with DateTimeKind.Utc from time zone, {time_point.tzinfo}.')

        carry_seconds, milliseconds = ndt.microseconds_to_milliseconds_with_carry(time_point.microsecond)
        self.Timestamp = DateTime(time_point.year, time_point.month, time_point.day,
                                  time_point.hour, time_point.minute, time_point.second + carry_seconds,
                                  milliseconds, stub_dt.StubDateTimeKind.UTC)
        self.Value = value

    def __repr__(self):
        return f'StubNetSample(Timestamp={self.Timestamp.ToString("o")}, Value={self.Value})'


def create_stub_net_time_series_data_points(start_time_point: pendulum.DateTime,
                                            sample_values) -> Sequence[StubNetSample]:
    """
    Create a stub .NET time series.

    The "stub .NET" nature is satisfied by returning a sequence in which each item is an instance of `StubNetSample`.

    :param start_time_point: The time point at which the time series starts.
    :param sample_values: The values in the stub data_points.
    :return: A sequence a data_points implementing the `ITick<double>` interface using "duck typing."
    """
    sample_time_points = create_30_second_time_points(start_time_point, len(sample_values))
    samples = [StubNetSample(st, sv) for (st, sv) in zip(sample_time_points, sample_values)]
    return samples


@toolz.curry
def create_regularly_sampled_time_points(interval: pendulum.Duration, start_time_point: pendulum.DateTime, count: int):
    """
    Create a sequence of `count` time points starting at `start_time_point`, `interval` apart.

    Args:
        interval: The time interval between each point.
        start_time_point: The starting time point of the sequence.
        count: The number of time points in the sequence.

    Returns:
        The sequence of time points.

    """
    # I must handle a count of 0 specially because `pendulum` **includes** the endpoint of the specified range.
    if count == 0:
        return []

    # The `pendulum` package, by default, **includes** the endpoint of the specified range. I want to exclude it when
    # I create these series so my end point must be `count - 1`.
    end_time_point = start_time_point + interval * (count - 1)
    result = pendulum.period(start_time_point, end_time_point).range('seconds', interval.total_seconds())
    return result


create_30_second_time_points = create_regularly_sampled_time_points(pendulum.duration(seconds=30))
create_1_second_time_points = create_regularly_sampled_time_points(pendulum.duration(seconds=1))


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


def make_measurement(measurement_dto):
    return units.make_measurement(measurement_dto.unit, measurement_dto.magnitude)


def make_net_measurement(measurement_dto):
    measurement = make_measurement(measurement_dto)
    return onq.as_net_quantity(measurement_dto.unit, measurement)


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


# TODO: Change implementation of many stub objects to call `create_stub_domain_object`


def create_stub_net_data_frame(display_name=None, name=None, object_id=None, table_data_dto=None):
    stub_net_data_frame_name = 'stub_net_data_frame'
    try:
        result = unittest.mock.MagicMock(name=stub_net_data_frame_name, spec=IStaticDataFrame)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        result = unittest.mock.MagicMock(name=stub_net_data_frame_name)

    result.Name = name
    result.DisplayName = display_name
    if object_id is not None:
        result.ObjectId = Guid(object_id)

    if table_data_dto is not None:
        result.DataTable = stub_ndt.populate_data_table(table_data_dto)

    return result


def _set_net_isip(isip, result):
    if hasattr(isip, 'unit'):
        result.Isip = make_net_measurement(isip)
    elif hasattr(isip, 'Unit'):
        result.Isip = isip
    else:
        raise ValueError(f'Unrecognized isip={isip}. The value, `isip`, must be a `Pint` `Quantity` or'
                         f' a UnitsNet `Unit`.')


def create_stub_net_stage_part(display_name_with_well=None, display_name_without_well=None,
                               isip=None, part_no=None, project=None,
                               start_time=None, stop_time=None):
    stub_net_stage_part_name = 'stub_net_stage_part'
    result = create_stub_domain_object(stub_name=stub_net_stage_part_name,
                                       stub_spec=IStagePart)

    if display_name_with_well is not None:
        result.DisplayNameWithWell = display_name_with_well
    if display_name_without_well is not None:
        result.DisplayNameWithoutWell = display_name_without_well
    if part_no is not None:
        result.PartNumber = part_no
    if project is not None:
        result.Project = project
    if start_time is not None:
        result.StartTime = ndt.as_net_date_time(start_time)
    if stop_time is not None:
        result.StopTime = ndt.as_net_date_time(stop_time)
    if isip is not None:
        _set_net_isip(isip, result)

    return result


def create_stub_net_stage(cluster_count=-1, display_name=None,
                          display_name_with_well=None, display_stage_no=-1,
                          md_top=None, md_bottom=None, name=None, object_id=None,
                          stage_location_bottom=None, stage_location_cluster=None,
                          stage_location_center=None, stage_location_top=None,
                          start_time=None, stop_time=None, treatment_curve_names=None,
                          shmin=None, pnet=None, isip=None):
    stub_net_stage_name = 'stub_net_stage'
    result = create_stub_domain_object(display_name=display_name,
                                       stub_name=stub_net_stage_name,
                                       stub_spec=IStage)

    if display_name_with_well is not None:
        result.DisplayNameWithWell = display_name_with_well
    result.NumberOfClusters = cluster_count
    result.DisplayStageNumber = display_stage_no
    if md_top is not None:
        result.MdTop = make_net_measurement(md_top)
    if md_bottom is not None:
        result.MdBottom = make_net_measurement(md_bottom)
    if name is not None:
        result.Name = name
    if object_id is not None:
        result.ObjectId = object_id
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
        result.StartTime = ndt.as_net_date_time(start_time)
    if stop_time is not None:
        result.StopTime = ndt.as_net_date_time(stop_time)

    if treatment_curve_names is not None:
        result.TreatmentCurves.Items = list(toolz.map(
            lambda sampled_quantity_name: create_stub_net_treatment_curve(
                sampled_quantity_name=sampled_quantity_name.value), treatment_curve_names))
    else:
        result.TreatmentCurves.Items = []

    if shmin is not None:
        if hasattr(shmin, 'unit'):
            result.Shmin = make_net_measurement(shmin)
        elif hasattr(shmin, 'Unit'):
            result.Shmin = shmin
        else:
            raise ValueError(f'Unrecognized shmin={shmin}. The value, `shmin`, must be a Python `unit` or'
                             f' a UnitsNet `Unit`.')

    if pnet is not None:
        if hasattr(pnet, 'unit'):
            result.Pnet = make_net_measurement(pnet)
        elif hasattr(pnet, 'Unit'):
            result.Pnet = pnet
        else:
            raise ValueError(f'Unrecognized shmin={pnet}. The value, `shmin`, must be a Python `unit` or'
                             f' a UnitsNet `Unit`.')

    if isip is not None:
        _set_net_isip(isip, result)

    return result


def create_stub_domain_object(object_id=None, name=None, display_name=None, stub_name=None, stub_spec=None):
    try:
        result = unittest.mock.MagicMock(name=stub_name, spec=stub_spec)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        result = unittest.mock.MagicMock(name=stub_name)
    if object_id is not None:
        result.ObjectId = Guid(object_id)
    if display_name is not None:
        result.DisplayName = display_name
    if name is not None:
        result.Name = name
    return result


def create_stub_net_subsurface_point(x=None, y=None, depth=None, xy_origin=None, depth_origin=None):
    try:
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point', spec=ISubsurfacePoint)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_subsurface_point = unittest.mock.MagicMock(name='stub_subsurface_point')
    if x is not None:
        stub_subsurface_point.X = make_net_measurement(x)
    if y is not None:
        stub_subsurface_point.Y = make_net_measurement(y)
    if depth is not None:
        stub_subsurface_point.Depth = make_net_measurement(depth)
    if xy_origin is not None:
        stub_subsurface_point.WellReferenceFrameXy = xy_origin
    if depth_origin is not None:
        stub_subsurface_point.DepthDatum = depth_origin
    return stub_subsurface_point


def create_stub_net_trajectory_array(magnitudes, unit):
    def make_stub_measurement_with_unit(measurement_unit):
        return make_measurement_dto(measurement_unit)

    result = toolz.pipe(magnitudes,
                        toolz.map(make_stub_measurement_with_unit(unit)),
                        toolz.map(make_net_measurement))
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
        time_points = create_30_second_time_points(start_time_point, len(values))
        samples = [StubSample(t, v) for (t, v) in zip(map(ndt.as_net_date_time, time_points), values)]
        stub_net_treatment_curve.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(name='stub_time_series',
                                                                                       return_value=samples)
    if project is not None:
        stub_net_treatment_curve.Stage.Well.Project = project

    return stub_net_treatment_curve


def create_stub_net_monitor(object_id=None, display_name=None, name=None, start=None, stop=None,
                            well_time_series_dto=None):
    stub_name = (f'stub_net_monitor_{display_name}' if display_name is not None else 'stub_net_monitor')
    try:
        result = unittest.mock.MagicMock(name=stub_name, spec=IMonitor)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        result = unittest.mock.MagicMock(name=stub_name)

    if display_name is not None:
        result.DisplayName = display_name

    if name is not None:
        result.Name = name

    if object_id is not None:
        result.ObjectId = Guid(object_id)

    if start is not None:
        result.StartTime = ndt.as_net_date_time(start)

    if stop is not None:
        result.StopTime = ndt.as_net_date_time(stop)

    if well_time_series_dto is not None:
        result.TimeSeries = create_stub_net_time_series(**well_time_series_dto)

    return result


def create_stub_net_time_series(object_id=None, name=None, display_name=None,
                                sampled_quantity_name=None, sampled_quantity_type=None,
                                data_points=(), project=None):
    stub_net_time_series_name = 'stub_net_time_series'
    stub_net_time_series = create_stub_domain_object(object_id=object_id,
                                                     name=name,
                                                     display_name=display_name,
                                                     stub_name=stub_net_time_series_name,
                                                     stub_spec=IWellSampledQuantityTimeSeries)

    if sampled_quantity_name is not None:
        stub_net_time_series.SampledQuantityName = sampled_quantity_name
    if sampled_quantity_type is not None:
        stub_net_time_series.SampledQuantityType = sampled_quantity_type
    stub_net_time_series.GetOrderedTimeSeriesHistory = unittest.mock.MagicMock(
        name='stub_time_series_data_points', return_value=data_points)
    if project is not None:
        stub_net_time_series.Well.Project = project

    return stub_net_time_series


def create_stub_net_well_trajectory(object_id=None, project=None,
                                    easting_magnitudes=None, northing_magnitudes=None, tvd_ss_magnitudes=None,
                                    inclination_magnitudes=None, azimuth_magnitudes=None, md_kb_magnitudes=None):
    try:
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory', spec=IWellTrajectory)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        stub_trajectory = unittest.mock.MagicMock(name='stub_trajectory')
    if object_id is not None:
        stub_trajectory.ObjectId = object_id

    if project is not None:
        stub_trajectory.Well.Project = project

    if easting_magnitudes is not None and project.project_units is not None:
        stub_eastings = create_stub_net_trajectory_array(easting_magnitudes, project.project_units.LENGTH)
        stub_trajectory.GetEastingArray = unittest.mock.MagicMock(name='stub_eastings', return_value=stub_eastings)

    if northing_magnitudes is not None and project.project_units is not None:
        stub_northings = create_stub_net_trajectory_array(northing_magnitudes,
                                                          project.project_units.LENGTH)
        stub_trajectory.GetNorthingArray = unittest.mock.MagicMock(name='stub_northings', return_value=stub_northings)

    if tvd_ss_magnitudes is not None and project.project_units is not None:
        stub_tvd_sss = create_stub_net_trajectory_array(tvd_ss_magnitudes, project.project_units.LENGTH)
        stub_trajectory.GetTvdArray = unittest.mock.MagicMock(name='stub_tvd_sss', return_value=stub_tvd_sss)

    if inclination_magnitudes is not None:
        stub_inclinations = create_stub_net_trajectory_array(inclination_magnitudes, units.Common.ANGLE)
        stub_trajectory.GetInclinationArray = unittest.mock.MagicMock(name='stub_inclinations',
                                                                      return_value=stub_inclinations)

    if azimuth_magnitudes is not None:
        stub_azimuths = create_stub_net_trajectory_array(azimuth_magnitudes, units.Common.ANGLE)
        stub_trajectory.GetAzimuthEastOfNorthArray = unittest.mock.MagicMock(name='stub_azimuths',
                                                                             return_value=stub_azimuths)

    if md_kb_magnitudes is not None and project.project_units is not None:
        stub_md_kbs = create_stub_net_trajectory_array(md_kb_magnitudes, project.project_units.LENGTH)
        stub_trajectory.GetMdKbArray = unittest.mock.MagicMock(name='stub_md_kbs', return_value=stub_md_kbs)

    return stub_trajectory


def get_mock_easting_array(stub_new_well_trajectory):
    return stub_new_well_trajectory.GetEastingArray


def get_mock_northing_array(stub_new_well_trajectory):
    return stub_new_well_trajectory.GetNorthingArray


def quantity_coordinate(raw_coordinates, i, stub_net_project):
    # The Pythonnet package has an open issue that the "Implicit Operator does not work from python"
    # (https://github.com/pythonnet/pythonnet/issues/253).
    #
    # One of the comments identifies a work-around from StackOverflow
    # (https://stackoverflow.com/questions/11544056/how-to-cast-implicitly-on-a-reflected-method-call/11563904).
    # This post states that "the trick is to realize that the compiler creates a special static method
    # called `op_Implicit` for your implicit conversion operator."
    result = [UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(c), stub_net_project.ProjectUnits.LengthUnit)
              for c in raw_coordinates[i]] if raw_coordinates else []
    return result


def _convert_locations_for_md_kb_values(locations_for_md_kb_values):
    if locations_for_md_kb_values is None:
        return {}

    def net_subsurface_point(ssp):
        return create_stub_net_subsurface_point(ssp.x, ssp.y, ssp.depth)

    def make_net_subsurface_points(points):
        return list(toolz.map(net_subsurface_point, points))

    def measurement_key_to_net_key(source_key):
        sample_measurements, frame, datum = source_key
        net_sample_measurements = toolz.pipe(sample_measurements,
                                             toolz.map(make_net_measurement),
                                             list)
        net_lengths = Array[UnitsNet.Length](net_sample_measurements)
        return net_lengths, frame, datum

    locations_with_net_keys = toolz.keymap(measurement_key_to_net_key, locations_for_md_kb_values)
    return toolz.valmap(make_net_subsurface_points, locations_with_net_keys)


def create_stub_net_well(object_id=None, name='', display_name='', ground_level_elevation_above_sea_level=None,
                         kelly_bushing_height_above_ground_level=None, uwi=None, locations_for_md_kb_values=None,
                         formation=None, stage_dtos=(), wellhead_location=None):
    try:
        result = unittest.mock.MagicMock(name=name, spec=IWell)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        result = unittest.mock.MagicMock(name=name)

    if object_id is not None:
        result.ObjectId = Guid(object_id)

    if name:
        result.Name = name

    if display_name:
        result.DisplayName = display_name

    if ground_level_elevation_above_sea_level is not None:
        result.GroundLevelElevationAboveSeaLevel = make_net_measurement(ground_level_elevation_above_sea_level)

    if kelly_bushing_height_above_ground_level is not None:
        result.KellyBushingHeightAboveGroundLevel = make_net_measurement(kelly_bushing_height_above_ground_level)

    if uwi:
        result.Uwi = uwi

    if formation:
        result.Formation = formation
    else:
        result.Formation = ''

    # Initialize the .NET `Wells.Items` property using `well_dtos`
    result.Stages.Items = [create_stub_net_stage(**stage_dto) for stage_dto in stage_dtos]

    if wellhead_location:
        # wellhead_location (whl) will be a list of 3 quantities (easting, northing, depth)
        whl = toolz.pipe(wellhead_location,
                         toolz.map(make_net_measurement),
                         list, )
        result.WellHeadLocation = whl

    locations_for_net_values = _convert_locations_for_md_kb_values(locations_for_md_kb_values)

    def get_location_for(md_kb_values, frame, datum):
        # return an empty list if nothing configured
        if not locations_for_net_values:
            return []

        def is_matching_args(to_test):
            to_test_samples, to_test_frame, to_test_datum = to_test
            if to_test_frame != frame:
                return False

            if to_test_datum != datum:
                return False

            each_equals = toolz.map(onq.equal_net_quantities, to_test_samples, md_kb_values)
            return all(each_equals)

        candidates = toolz.keyfilter(is_matching_args, locations_for_net_values)
        if len(candidates) == 0:
            return None
        elif len(candidates) > 1:
            raise ValueError(f'Multiple items matching {(md_kb_values, frame, datum)}.')

        return list(candidates.items())[0][1]

    result.GetLocationsForMdKbValues = unittest.mock.MagicMock(name='get_locations_for_md_kb_values')
    result.GetLocationsForMdKbValues.side_effect = get_location_for

    return result


def create_stub_net_project(name='', azimuth=None, curve_names=None, curves_physical_quantities=None,
                            data_frame_dtos=(), data_frame_ids=(), default_well_colors=None,
                            fluid_density=None, monitor_dtos=(), project_bounds=None, project_center=None,
                            project_units=None, samples=None, time_series_dtos=(), well_dtos=()):
    default_well_colors = default_well_colors if default_well_colors else [[]]
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
    if azimuth is not None:
        stub_net_project.Azimuth = make_net_measurement(azimuth)
    if fluid_density is not None:
        stub_net_project.FluidDensity = make_net_measurement(fluid_density)

    stub_net_project.Monitors.Items = [create_stub_net_monitor(**monitor_dto) for
                                       monitor_dto in monitor_dtos]

    stub_net_project.DataFrames.Items = [create_stub_net_data_frame(**data_frame_dto) for
                                         data_frame_dto in data_frame_dtos]

    try:
        plotting_settings = unittest.mock.MagicMock(name='stub_plotting_settings', spec=IPlottingSettings)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        plotting_settings = unittest.mock.MagicMock(name='stub_plotting_settings')
    plotting_settings.GetDefaultWellColors = unittest.mock.MagicMock(name='stub_default_well_colors',
                                                                     return_value=default_well_colors)
    stub_net_project.PlottingSettings = plotting_settings

    if project_bounds is not None:
        net_bounds = toolz.pipe(project_bounds,
                                toolz.map(make_net_measurement),
                                list,
                                )
        stub_net_project.GetProjectBounds = unittest.mock.MagicMock(name='stub_get_project_bounds',
                                                                    return_value=net_bounds)

    if project_center is not None:
        net_center = toolz.pipe(project_center,
                                toolz.map(make_net_measurement),
                                list,
                                )
        stub_net_project.GetProjectCenter = unittest.mock.MagicMock(name='stub_get_project_center',
                                                                    return_value=net_center)

    if project_units == units.UsOilfield:
        stub_net_project.ProjectUnits = UnitSystem.USOilfield()
    elif project_units == units.Metric:
        stub_net_project.ProjectUnits = UnitSystem.Metric()
    elif project_units is not None:
        stub_net_project.ProjectUnits = project_units

    # TODO: this code assumes that a caller initializes either `curve_names` or `time_series_dtos`.
    # Initialize the .NET `WellTimeSeriesList.Items` property using `time_series_dtos`
    if len(time_series_dtos) > 0:
        stub_net_project.WellTimeSeriesList.Items = [
            create_stub_net_time_series(**time_series_dto) for time_series_dto in time_series_dtos
        ]

    # Initialize the .NET `Wells.Items` property using `well_dtos`
    if len(well_dtos) > 0:
        stub_net_project.Wells.Items = [create_stub_net_well(**well_dto) for well_dto in well_dtos]

    # TODO: this code assumes that a caller initializes either `curve_names` or `time_series_dtos`.
    if len(curve_names) > 0:
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


def create_stub_net_project_object(object_id=None, name=None, display_name=None):
    """Create a stub implementation of an IProjectObject."""
    stub_net_project_object_name = 'stub_net_project_object'
    try:
        result = unittest.mock.MagicMock(name=stub_net_project_object_name, spec=IProjectObject)
    except TypeError:  # Raised in Python 3.8.6 and Pythonnet 2.5.1
        result = unittest.mock.MagicMock(name=stub_net_project_object_name)

    # To store a project object in a searchable project object collection, an object id is required and is
    # "automagically" generated. This code sets the `ObjectId` property to an ID supplied to this function or to a
    # "don't care" ID.
    result.ObjectId = Guid(object_id) if object_id is not None else Guid(_DONT_CARE_ID)

    if name is not None:
        result.Name = name

    result.DisplayName = display_name if display_name is not None else None

    return result


def create_stub_dom_project_object(object_id=None, name=None, display_name=None):
    """Create a stub wrapper for an IProjectObject."""
    stub_project_object_name = 'stub_project_object'
    result = create_stub_domain_object(object_id=object_id, name=name, display_name=display_name,
                                       stub_spec=IProjectObject)

    return result


@toolz.curry
def get_dtos_property(dtos, property_name, transform=toolz.identity):
    return toolz.pipe(
        dtos,
        toolz.map(toolz.get(property_name)),
        toolz.map(transform),
        list
    )