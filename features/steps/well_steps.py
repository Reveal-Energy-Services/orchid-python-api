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

import decimal

from hamcrest import assert_that, equal_to

import common_functions as cf

from orchid import (
    reference_origins as origins,
    unit_system as units,
)


def _assert_measurement_close_to(actual, expected):
    expected_magnitude = decimal.Decimal(expected.split(maxsplit=1)[0])
    # Tolerance determined empirically.
    magnitude_tolerance = decimal.Decimal((0, (4,), expected_magnitude.as_tuple()[-1]))
    cf.assert_that_actual_measurement_close_to_expected(actual, expected, tolerance=magnitude_tolerance)


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
    _assert_measurement_close_to(context.well_measurements['kb_above_ground'], kb_above_ground)
    _assert_measurement_close_to(context.well_measurements['ground_above_sea_level'], ground_above_sea_level)


@when("I sample the well subsurface locations for '{well}'")
def step_impl(context, well):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
    """
    context.selected_well = cf.find_well_by_name_in_project(context, well)


FRAME_TEXT_TO_FRAMES = {
    'Plane': origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
    'Project': origins.WellReferenceFrameXy.PROJECT,
    'Well': origins.WellReferenceFrameXy.WELL_HEAD,
}

DATUM_TEXT_TO_DEPTH_DATUM = {
    'Kelly': origins.DepthDatum.KELLY_BUSHING,
    'Ground': origins.DepthDatum.GROUND_LEVEL,
    'Sea': origins.DepthDatum.SEA_LEVEL,
}


def _measurement_text_to_measurement(measurement_text):
    magnitude_text, unit_text = measurement_text.split()
    magnitude = float(magnitude_text)
    if unit_text == 'ft':
        unit = units.UsOilfield.LENGTH
    elif unit_text == 'm':
        unit = units.Metric.LENGTH
    else:
        raise ValueError(f'Unrecognized unit, "{unit_text}".')

    result = units.make_measurement(unit, magnitude)
    return result


@then("I see the points {x}, {y}, and {depth} in project units at {md_kb} in {frame} and {datum}")
def step_impl(context, x, y, depth, md_kb, frame, datum):
    """
    Args:
        context (behave.runner.Context): The test context.
        x (str): The expected, sampled x-coordinate in project units.
        y (str): The expected, sampled y-coordinate in project units.
        depth (str): The expected, sampled depth coordinate in project units.
        md_kb (str): The measured depth from the Kelly Bushing at which I sample the trajectory.
        frame (str): The well reference frame for the location.
        datum (str): The depth datum for the location.
    """
    sample_md_kb_values = [_measurement_text_to_measurement(md_kb)]
    sample_frame = FRAME_TEXT_TO_FRAMES[frame]
    sample_datum = DATUM_TEXT_TO_DEPTH_DATUM[datum]

    actual_points = context.selected_well.locations_for_md_kb_values(sample_md_kb_values, sample_frame, sample_datum)

    assert_that(len(actual_points), equal_to(len(sample_md_kb_values)))
    actual_point = actual_points[0]
    _assert_measurement_close_to(actual_point.x, x)
    _assert_measurement_close_to(actual_point.y, y)
    _assert_measurement_close_to(actual_point.depth, depth)


@when("I sample the wellhead locations for {well}")
def step_impl(context, well):
    context.selected_well = cf.find_well_by_name_in_project(context, well)


@then("I see the points {easting}, {northing}, and {depth}")
def step_impl(context, easting, northing, depth):
    actual_points = context.selected_well.wellhead_location
    _assert_measurement_close_to(actual_points.easting, easting)
    _assert_measurement_close_to(actual_points.northing, northing)
    _assert_measurement_close_to(actual_points.depth, depth)
