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

# noinspection PyPackageRequirements
from behave import *

use_step_matcher("parse")

from hamcrest import assert_that, equal_to
import pendulum as pdt
import toolz.curried as toolz

import common_functions as cf

from orchid import (
    native_stage_adapter as nsa,
    net_date_time as ndt,
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
        return well_adapter.name, toolz.count(well_adapter.stages())

    def expected_test_details():
        return well, stage_count

    candidate_wells = list(context.actual_wells.find_by_name(well))
    # Expect exactly one match
    assert_that(len(candidate_wells), equal_to(1),
                f'Expected 1 stage for well, {well} in field, {context.field}'
                f' but found {len(candidate_wells)}.')

    well_to_test = candidate_wells[0]
    actual_details_to_test = actual_test_details(well_to_test)
    assert_that(actual_details_to_test, equal_to(expected_test_details()),
                f'Candidate well and stage failed for field {context.field}.')


def get_stages(well_stages_pair):
    return well_stages_pair[1]


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
    actual = stage_of_interest.md_top(context.project.project_units.LENGTH)
    cf.assert_that_actual_measurement_close_to_expected(actual, md_top)
    actual1 = stage_of_interest.md_bottom(context.project.project_units.LENGTH)
    cf.assert_that_actual_measurement_close_to_expected(actual1, md_bottom)
    assert_that(stage_of_interest.cluster_count, equal_to(cluster_count))


def find_stage_with_name(context, name_with_well):
    stages_of_interest = toolz.pipe(context.stages_for_wells.values(),
                                    toolz.map(lambda stages: stages.find_by_display_name_with_well(name_with_well)),
                                    toolz.concat,
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
    actual = stage_of_interest.center_location_easting(in_length_unit,
                                                       origins.WellReferenceFrameXy.PROJECT)
    cf.assert_that_actual_measurement_close_to_expected(actual, easting)
    actual1 = stage_of_interest.center_location_northing(in_length_unit,
                                                         origins.WellReferenceFrameXy.PROJECT)
    cf.assert_that_actual_measurement_close_to_expected(actual1, northing)
    actual2 = stage_of_interest.center_location_tvdss(in_length_unit)
    cf.assert_that_actual_measurement_close_to_expected(actual2, tvdss)
    actual3 = stage_of_interest.stage_length(in_length_unit)
    cf.assert_that_actual_measurement_close_to_expected(actual3, length)


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
    well_of_interest = cf.find_well_by_name_in_stages_for_wells(context, well)
    stage_of_interest = cf.find_stage_by_stage_no(context, stage_no, well_of_interest)

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
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
    subsurface_location = stage_of_interest.bottom_location(context.project.project_units.LENGTH,
                                                            reference_frame_from_frame_name(frame),
                                                            origins.DepthDatum.KELLY_BUSHING)

    assert_equal_location_measurements(subsurface_location, x, y, depth)


def assert_equal_location_measurements(subsurface_location, x, y, depth):
    cf.assert_that_actual_measurement_close_to_expected(subsurface_location.x, x)
    cf.assert_that_actual_measurement_close_to_expected(subsurface_location.y, y)
    cf.assert_that_actual_measurement_close_to_expected(subsurface_location.depth, depth)


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
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
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
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
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
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
    subsurface_location = stage_of_interest.top_location(context.project.project_units.LENGTH,
                                                         reference_frame_from_frame_name(frame),
                                                         origins.DepthDatum.KELLY_BUSHING)

    assert_equal_location_measurements(subsurface_location, x, y, depth)


@step("I see additional treatment data for samples {well}, {stage_no:d}, {shmin}, {isip}, and {pnet}")
def step_impl(context, well, stage_no, shmin, isip, pnet):
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
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

    cf.assert_that_actual_measurement_close_to_expected(actual_shmin, shmin)
    cf.assert_that_actual_measurement_close_to_expected(actual_isip, isip)
    cf.assert_that_actual_measurement_close_to_expected(actual_pnet, pnet)


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
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
    actual_shmin = stage_of_interest.shmin
    actual_isip = stage_of_interest.isip
    actual_pnet = stage_of_interest.pnet

    cf.assert_that_actual_measurement_close_to_expected(actual_shmin, shmin)
    cf.assert_that_actual_measurement_close_to_expected(actual_isip, isip)
    cf.assert_that_actual_measurement_close_to_expected(actual_pnet, pnet)


# noinspection PyBDDParameters
@then("I see the correct {well}, {stage_no:d}, and {center_mdkb}")
def step_impl(context, well, stage_no, center_mdkb):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of interest.
        center_mdkb (str): The measured depth of the stage center relative to the kelly bushing.
    """
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
    actual = stage_of_interest.center_location_mdkb(context.project.project_units.LENGTH)
    cf.assert_that_actual_measurement_close_to_expected(actual, center_mdkb)


@then("I see the correct {well}, {stage_no:d}, {start_time}, and {stop_time}")
def step_impl(context, well, stage_no, start_time, stop_time):
    """
    Args:
        context (behave.runner.Context): The
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of interest.
        start_time (str): The start time of the stage.
        stop_time (str): The stop time of the stage.
    """
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
    actual_start_time = stage_of_interest.start_time
    assert_that(actual_start_time, equal_to(pdt.parse(start_time)))
    actual_stop_time = stage_of_interest.stop_time
    assert_that(actual_stop_time, equal_to(pdt.parse(stop_time)))


@step("I change the start time of stage {stage_no:d} of {well} {to_start}")
def step_impl(context, stage_no, well, to_start):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The number used by engineers to identifying stages in a well.
        well (str): The well containing the stage whose start time is to be changed.
        to_start (str): The new start time of the stage.
    """
    stage_of_interest = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    stage_of_interest.start = pdt.parse(to_start)


@step("I change the stop time of stage {stage_no:d} of {well} {to_stop}")
def step_impl(context, stage_no, well, to_stop):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The number used by engineers to identifying stages in a well.
        well (str): The well containing the stage whose stop time is to be changed.
        to_stop (str): The new stop time of the stage.
    """
    stage_of_interest = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    stage_of_interest.stop = pdt.parse(to_stop)


@then("I see the changed {to_start} and {to_stop} for well, {well} and stage, {stage_no:d}")
def step_impl(context, to_start, to_stop, well, stage_no):
    """
    Args:
        context (behave.runner.Context): The test context.
        to_start (str): The new start time of the stage.
        to_stop (str): The new stop time of the stage.
        stage_no (int): The number used by engineers to identifying stages in a well.
        well (str): The well containing the stage whose stop time is to be changed.
    """
    stage_of_interest = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    assert_that(stage_of_interest.start_time, equal_to(pdt.parse(to_start)))
    assert_that(stage_of_interest.stop_time, equal_to(pdt.parse(to_stop)))
