#  Copyright 2017-2021 Reveal Energy Services, Inc
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

# noinspection PyPackageRequirements
from behave import *
use_step_matcher("parse")

from hamcrest import assert_that, equal_to, close_to
import toolz.curried as toolz

from common_functions import (
    find_stage_no_in_well,
    find_well_by_name_in_stages_for_wells,
    find_stage_by_stage_no
)

from orchid import (
    native_stage_adapter as nsa,
    reference_origins as origins,
    unit_system as units,
)


# noinspection PyBDDParameters
@then("I see {stage_count:d} stages for well {well}")
def step_impl(context, stage_count, well):
    """
    Args:
        context (behave.runner.Context): The context of the test.
        stage_count (int): The number of stages for the well of interest.
        well (str): The name of the well of interest.
    """

    def actual_test_details(well_adapter):
        return well_adapter.name, toolz.count(well_adapter.stages)

    def expected_test_details():
        return well, stage_count

    candidates = list(toolz.pipe(toolz.map(actual_test_details, context.actual_wells),
                                 toolz.filter(lambda d: d[0] == well)))
    # Expect exactly one match
    assert_that(len(candidates), equal_to(1),
                f'Expected 1 stage for well {well} in field {context.field}. Found {len(candidates)}.')

    assert_that(candidates[0], equal_to(expected_test_details()),
                f'Candidate well and stage failed for field {context.field}.')


def get_stages(well_stages_pair):
    return well_stages_pair[1]


@toolz.curry
def find_stage(display_name_with_well, all_stages):
    def has_display_name_with_well(stage_to_test):
        return stage_to_test.display_name_with_well == display_name_with_well

    candidates = list(toolz.pipe(all_stages,
                                 toolz.filter(has_display_name_with_well)))
    assert len(candidates) == 1, f'Expected 1 stage with "{display_name_with_well}". Found {len(candidates)}.'
    return candidates[0]


def assert_measurement_equal(actual, expected):
    expected_magnitude_text, expected_unit = expected.split()
    expected_magnitude = float(expected_magnitude_text)
    assert_that(actual.magnitude, close_to(expected_magnitude, 6e-2))
    assert_that(units.abbreviation(actual.unit), equal_to(expected_unit))


# noinspection PyBDDParameters
@then("I see the correct {stage_no:d}, {name_with_well}, {md_top}, {md_bottom} and {cluster_count:d}")
def step_impl(context, stage_no, name_with_well, md_top, md_bottom, cluster_count):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The displayed stage number of the stage of interest
        name_with_well (str): The display name with the well of the stage of interest.
        md_top (str): The measured depth of the stage top.
        md_bottom (str): The measured depth of the stage bottom.
        cluster_count (int): The number of clusters for the stage.

    """
    stage_of_interest = find_stage_with_name(context, name_with_well)

    assert_that(stage_of_interest.display_stage_number, equal_to(stage_no))
    assert_measurement_equal(stage_of_interest.md_top(context.project.project_units.LENGTH), md_top)
    assert_measurement_equal(stage_of_interest.md_bottom(context.project.project_units.LENGTH), md_bottom)
    assert_that(stage_of_interest.cluster_count, equal_to(cluster_count))


def find_stage_with_name(context, name_with_well):
    stages_of_interest = toolz.pipe(context.stages_for_wells.values(),
                                    toolz.concat,
                                    toolz.filter(lambda s: s.display_name_with_well == name_with_well),
                                    list)
    assert len(stages_of_interest) == 1, \
        f'Expected 1 stage with name with well: {name_with_well}. Found {len(stages_of_interest)}.'
    stage_of_interest = toolz.nth(0, stages_of_interest)
    return stage_of_interest


# noinspection PyBDDParameters
@step("I see additional data {stage:d}, {name_with_well}, {easting}, {northing}, {tvdss} and {length}")
def step_impl(context, stage, name_with_well, easting, northing, tvdss, length):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage (int): The displayed stage number
        name_with_well (str): The display name with the well of the stage of interest
        easting (str): The x-coordinate of the stage center in project coordinates and in project length units.
        northing (str): The y-coordinate of the stage center in project coordinates and in project length units.
        tvdss (str): The total vertical depth of the stage center relative to sea level and in project length units.
        length (str): The length of the stage in project length units.
    """
    stage_of_interest = find_stage_with_name(context, name_with_well)

    in_length_unit = context.project.project_units.LENGTH
    assert_measurement_equal(stage_of_interest.center_location_easting(in_length_unit,
                                                                       origins.WellReferenceFrameXy.PROJECT),
                             easting)
    assert_measurement_equal(stage_of_interest.center_location_northing(in_length_unit,
                                                                        origins.WellReferenceFrameXy.PROJECT),
                             northing)
    assert_measurement_equal(stage_of_interest.center_location_tvdss(in_length_unit), tvdss)
    assert_measurement_equal(stage_of_interest.stage_length(in_length_unit), length)


# noinspection PyBDDParameters
@step("I see basic data {well}, {stage_no:d}, {name_without_well}, {order:d}, {global_stage_no:d}, and {connection}")
def step_impl(context, well, stage_no, name_without_well, order, global_stage_no, connection):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number.
        name_without_well (str): The name of the stage **without** the well name.
        order (int): The order of stage completion for this well.
        global_stage_no (int): The global stage sequence number.
        connection (str): The name of the formation connection type of this stage.
    """
    well_of_interest = find_well_by_name_in_stages_for_wells(context, well)
    stage_of_interest = find_stage_by_stage_no(context, stage_no, well_of_interest)

    message = f'Failure for field {context.field}, well {well}, and stage_no {stage_no}.'

    assert_that(stage_of_interest.display_name_without_well, equal_to(name_without_well), message)
    assert_that(stage_of_interest.order_of_completion_on_well, equal_to(order), message)
    assert_that(stage_of_interest.global_stage_sequence_number, equal_to(global_stage_no), message)

    def connection_name_to_type(connection_name):
        name_to_type_map = {'PlugAndPerf': nsa.ConnectionType.PLUG_AND_PERF,
                            'SlidingSleeve': nsa.ConnectionType.SLIDING_SLEEVE,
                            'SinglePointEntry': nsa.ConnectionType.SINGLE_POINT_ENTRY,
                            'OpenHole': nsa.ConnectionType.OPEN_HOLE}
        return name_to_type_map[connection_name]

    assert_that(stage_of_interest.stage_type, equal_to(connection_name_to_type(connection)))


def reference_frame_from_frame_name(frame):
    frame_reference_frame_map = {'State Plane': origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                 'Project': origins.WellReferenceFrameXy.PROJECT,
                                 'Well Head': origins.WellReferenceFrameXy.WELL_HEAD}
    reference_frame = frame_reference_frame_map[frame]
    return reference_frame


# noinspection PyBDDParameters
@step("I see stage bottom location {well}, {stage_no:d}, {frame}, {x}, {y}, and {depth}")
def step_impl(context, well, stage_no, frame, x, y, depth):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of interest.
        frame (str): The well reference frame in which the measurements are made.
        x (str): The x-coordinate (easting) of the stage top subsurface location.
        y (str): The y-coordinate (northing) of the stage top subsurface location.
        depth (str): The depth (TVDSS) of the stage top subsurface location.
    """
    stage_of_interest = find_stage_no_in_well(context, stage_no, well)
    subsurface_location = stage_of_interest.bottom_location(context.project.project_units.LENGTH,
                                                            reference_frame_from_frame_name(frame),
                                                            origins.DepthDatum.KELLY_BUSHING)

    assert_equal_location_measurements(subsurface_location, x, y, depth)


def assert_equal_location_measurements(subsurface_location, x, y, depth):
    assert_measurement_equal(subsurface_location.x, x)
    assert_measurement_equal(subsurface_location.y, y)
    assert_measurement_equal(subsurface_location.depth, depth)


# noinspection PyBDDParameters
@step("I see stage cluster count {well}, {stage_no:d}, and {cluster_count:d}")
def step_impl(context, well, stage_no, cluster_count):
    """
    Args:
        context (behave.runner.Context): The test context
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of interest.
        cluster_count (int) in the stage of interest.
    """
    stage_of_interest = find_stage_no_in_well(context, stage_no, well)
    actual_cluster_count = stage_of_interest.cluster_count

    assert_that(actual_cluster_count, equal_to(cluster_count))


# noinspection PyBDDParameters
@step("I see stage cluster location {well}, {stage_no:d}, {cluster_no:d}, {frame}, {x}, {y}, and {depth}")
def step_impl(context, well, stage_no, cluster_no, frame, x, y, depth):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of the stage of interest.
        cluster_no (str): The cluster number whose location is sought.
        frame (str): The well reference frame in which the measurements are made.
        x (str): The x-coordinate (easting) of the stage top subsurface location.
        y (str): The y-coordinate (northing) of the stage top subsurface location.
        depth (str): The depth (TVDSS) of the stage top subsurface location.
    """
    stage_of_interest = find_stage_no_in_well(context, stage_no, well)
    subsurface_location = stage_of_interest.cluster_location(context.project.project_units.LENGTH,
                                                             cluster_no,
                                                             reference_frame_from_frame_name(frame),
                                                             origins.DepthDatum.KELLY_BUSHING)

    assert_equal_location_measurements(subsurface_location, x, y, depth)


# noinspection PyBDDParameters
@step("I see stage top location {well}, {stage_no:d}, {frame}, {x}, {y}, and {depth}")
def step_impl(context, well, stage_no, frame, x, y, depth):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of interest.
        frame (str): The well reference frame in which the measurements are made.
        x (str): The x-coordinate (easting) of the stage top subsurface location.
        y (str): The y-coordinate (northing) of the stage top subsurface location.
        depth (str): The depth (TVDSS) of the stage top subsurface location.
    """
    stage_of_interest = find_stage_no_in_well(context, stage_no, well)
    subsurface_location = stage_of_interest.top_location(context.project.project_units.LENGTH,
                                                         reference_frame_from_frame_name(frame),
                                                         origins.DepthDatum.KELLY_BUSHING)

    assert_equal_location_measurements(subsurface_location, x, y, depth)


@step("I see additional treatment data for samples {well}, {stage_no:d}, {shmin}, {isip}, and {pnet}")
def step_impl(context, well, stage_no, shmin, isip, pnet):
    stage_of_interest = find_stage_no_in_well(context, stage_no, well)
    # TODO: Change scenario to specify requested units instead of assuming project units.
    if context.field == 'Bakken':
        pressure_units = units.UsOilfield.PRESSURE
    elif context.field == 'Montney':
        pressure_units = units.Metric.PRESSURE
    else:
        raise ValueError(f'Field Name: {context.field} not recognized')

    actual_shmin = stage_of_interest.shmin_in_pressure_unit(pressure_units)
    actual_isip = stage_of_interest.isip_in_pressure_unit(pressure_units)
    actual_pnet = stage_of_interest.pnet_in_pressure_unit(pressure_units)

    assert_measurement_equal(actual_shmin, shmin)
    assert_measurement_equal(actual_isip, isip)
    assert_measurement_equal(actual_pnet, pnet)


# noinspection PyBDDParameters
@step("I see measurements in project units for samples {well}, {stage_no:d}, {shmin}, {isip}, and {pnet}")
def step_impl(context, well, stage_no, shmin, isip, pnet):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of interest.
        shmin (str): The expected minimum horizontal stress in project units.
        isip (str): The expected instantaneous shut-in pressure in project units.
        pnet (str): The net pressure for the stage in project units.
    """
    stage_of_interest = find_stage_no_in_well(context, stage_no, well)
    actual_shmin = stage_of_interest.shmin
    actual_isip = stage_of_interest.isip
    actual_pnet = stage_of_interest.pnet

    assert_measurement_equal(actual_shmin, shmin)
    assert_measurement_equal(actual_isip, isip)
    assert_measurement_equal(actual_pnet, pnet)
