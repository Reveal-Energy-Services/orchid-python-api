#  Copyright (c) 2017-2025 KAPPA
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

import common_functions as cf


@when("I query the stage parts for well, {well}, and stage, {stage_no:d}, of the project")
def step_impl(context, well, stage_no):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name used to identify the well (assumed unique).
        stage_no (int): The stage number that identifies the stage of interest.
    """
    candidate_wells = list(context.project.wells().find_by_name(well))
    assert len(candidate_wells) == 1, f'Expected exactly one well named, {well}. Found {len(candidate_wells)}.'
    context.well_of_interest = candidate_wells[0]

    context.stage_of_interest = context.well_of_interest.stages().find_by_display_stage_number(stage_no)

    context.stage_parts_of_interest = context.stage_of_interest.stage_parts()


@then("I see {part_no:d}, {name}, {display_name}, {display_name_with_well}, and {display_name_without_well}")
def step_impl(context, part_no, name, display_name, display_name_with_well, display_name_without_well):
    """
    Args:
        context (behave.runner.Context): The test context
        name (str): The name of the stage part.
        part_no (int): The number of the stage part.
        display_name (str): The value identifying this stage part displayed to users.
        display_name_with_well (str): The value identifying this stage part, including the well, displayed to users.
        display_name_without_well (str): The value identifying this stage part, without the well, displayed to users.
    """
    sut = context.stage_parts_of_interest.find_by_part_number(part_no)
    assert_that(sut.name, equal_to(name))
    assert_that(sut.display_name, equal_to(display_name))
    assert_that(sut.display_name_with_well, equal_to(display_name_with_well))
    assert_that(sut.display_name_without_well, equal_to(display_name_without_well))


# noinspection PyBDDParameters
@then("I see {part_no:d}, {start_time}, {stop_time}, and {isip}")
def step_impl(context, part_no, start_time, stop_time, isip):
    """
    Args:
        context (behave.runner.Context): The test context.
        part_no (int): The number of the stage part.
        start_time (str): The start time of this stage part.
        stop_time (str): The stop time of this stage part.
        isip (str): The instantaneous shut-in pressure of this stage part.
    """
    sut = context.stage_parts_of_interest.find_by_part_number(part_no)
    assert_that(sut.start_time, equal_to(pdt.parse(start_time)))
    assert_that(sut.stop_time, equal_to(pdt.parse(stop_time)))
    cf.assert_that_actual_measurement_close_to_expected(sut.isip, isip)


@step("I see the changed {to_start} and {to_stop} for well, {well}, stage, {stage_no:d}, and part, {part_no:d}")
def step_impl(context, to_start, to_stop, well, stage_no, part_no):
    """
    Args:
        context (behave.runner.Context):
        to_start (str): The expected start time of the part of interest.
        to_stop (str): The expected stop time of the part of interest.
        well (str): The name of the well of interest.
        stage_no (int): The displayed number of the stage of interest.
        part_no (int): The number of the stage part of interest.
    """
    part_of_interest = cf.find_part_by_part_no_in_stage_no_in_well_of_project(context, part_no, stage_no, well)
    assert_that(part_of_interest.start_time, equal_to(pdt.parse(to_start)))
    assert_that(part_of_interest.stop_time, equal_to(pdt.parse(to_stop)))
