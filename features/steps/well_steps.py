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

import common_functions as cf


@when("I query the well measurements for {well}")
def step_impl(context, well):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
    """
    context.selected_well = cf.find_well_by_name_in_project(context, well)

    context.well_measurements = {
        'kb_above_ground': context.selected_well.kelly_bushing_height_above_ground_level,
        'ground_above_sea_level': context.selected_well.ground_level_elevation_above_sea_level,
    }


@then("I see measurements for {kb_above_ground} and {ground_above_sea_level}")
def step_impl(context, kb_above_ground, ground_above_sea_level):
    """
    Args:
        context (behave.runner.Context): The test context.
        kb_above_ground (str): The expected measurement (text) of kelly bushing height above ground level.
        ground_above_sea_level (str): The expected measurement (text) of ground level elevation above sea level.
    """
    cf.assert_measurement_close_to(context.well_measurements['kb_above_ground'], kb_above_ground)
    cf.assert_measurement_close_to(context.well_measurements['ground_above_sea_level'], ground_above_sea_level)


@when("I sample the well subsurface locations for '{well}'")
def step_impl(context, well):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
    """
    raise NotImplementedError(u'STEP: When I sample the well subsurface locations')


@then(
    "I see the points {x}, {y}, and {depth} in project units for {well} at {mdkb} in {frame} and {datum}")
def step_impl(context, x, y, depth, well, mdkb, frame, datum):
    """
    Args:
        context (behave.runner.Context):
        x (str):
        y (str):
        depth (str):
        well (str):
        mdkb (str):
        frame (str):
        datum (str):
    """
    raise NotImplementedError(
        u'STEP: Then I see the points <x>, <y>, and <depth> in project units for <well> at <mdkb> in <frame> and <datum>')
