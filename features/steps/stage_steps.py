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

from behave import *
use_step_matcher("parse")

from hamcrest import assert_that, equal_to, close_to
import toolz.curried as toolz

import orchid.physical_quantity as opq
import orchid.reference_origin as oro


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
    assert_that(len(candidates), equal_to(1))  # expect exactly one match

    assert_that(candidates[0], equal_to(expected_test_details()))


def get_stages(well_stages_pair):
    return well_stages_pair[1]


@toolz.curry
def find_stage(selector_func, not_1_message_func, all_stages):
    candidates = list(toolz.pipe(all_stages,
                                 toolz.filter(selector_func)))
    assert len(candidates) == 1, f'Expected 1 stage with "{not_1_message_func()}". Found {len(candidates)}.'
    return candidates[0]


def assert_measurement_equal(actual, expected):
    expected_magnitude_text, expected_unit = expected.split()
    expected_magnitude = float(expected_magnitude_text)
    assert_that(actual.magnitude, close_to(expected_magnitude, 6e-2))
    assert_that(actual.unit, equal_to(expected_unit))


# noinspection PyBDDParameters
@then("I see the correct {stage:d}, {display_name_with_well}, {md_top}, {md_bottom} and {cluster_count:d}")
def step_impl(context, stage, display_name_with_well, md_top, md_bottom, cluster_count):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage (int): The displayed stage number of the stage of interest
        display_name_with_well (str): The display name with the well of the stage of interest
        md_top (str): The measured depth of the stage top.
        md_bottom (str): The measured depth of the stage bottom.
        cluster_count (int): The number of clusters for the stage.
    """

    def has_display_name_with_well(stage_to_test):
        return stage_to_test.display_name_with_well == display_name_with_well

    def not_1_message():
        return display_name_with_well

    stage_of_interest = toolz.pipe(context.stages_for_wells,
                                   toolz.map(get_stages),
                                   toolz.concat,
                                   toolz.partial(find_stage, has_display_name_with_well, not_1_message))

    assert_that(stage_of_interest.display_stage_number, equal_to(stage))
    assert_measurement_equal(stage_of_interest.md_top(context.project.unit(str(opq.PhysicalQuantity.LENGTH))),
                             md_top)
    assert_measurement_equal(stage_of_interest.md_bottom(context.project.unit(str(opq.PhysicalQuantity.LENGTH))),
                             md_bottom)
    assert_that(stage_of_interest.cluster_count, equal_to(cluster_count))


# noinspection PyBDDParameters
@step("I see the correct additional stage data {display_name_with_well}, {x}, {y}, {tvdss} and {stage_length}")
def step_impl(context, display_name_with_well, x, y, tvdss, stage_length):
    """
    Args:
        context (behave.runner.Context): The test context.
        display_name_with_well (str): The display name with the well of the stage of interest
        x (str): The x-coordinate of the stage center in project coordinates and in project length units.
        y (str): The y-coordinate of the stage center in project coordinates and in project length units.
        tvdss (str): The total vertical depth of the stage center relative to sea level and in project length units.
        stage_length (str): The length of the stage in project length units.
    """

    def has_display_name_with_well(stage_to_test):
        return stage_to_test.display_name_with_well == display_name_with_well

    def not_1_message():
        return display_name_with_well

    stage_of_interest = toolz.pipe(context.stages_for_wells,
                                   toolz.map(get_stages),
                                   toolz.concat,
                                   toolz.partial(find_stage, has_display_name_with_well, not_1_message))

    assert_measurement_equal(
        stage_of_interest.center_location_x(context.project.unit(opq.PhysicalQuantity.LENGTH.value.name),
                                            oro.WellReferenceFrameXy.PROJECT),
        x)
    assert_measurement_equal(
        stage_of_interest.center_location_y(context.project.unit( opq.PhysicalQuantity.LENGTH.value.name),
                                            oro.WellReferenceFrameXy.PROJECT),
        y)
    assert_measurement_equal(
        stage_of_interest.center_location_tvdss(context.project.unit(opq.PhysicalQuantity.LENGTH.value.name)),
        tvdss)
    assert_measurement_equal(
        stage_of_interest.stage_length(context.project.unit(opq.PhysicalQuantity.LENGTH.value.name)),
        stage_length)
