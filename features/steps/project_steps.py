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

from dateutil import parser as dup
from hamcrest import assert_that, equal_to, is_, not_none
import toolz.curried as toolz

import orchid

import common_functions as cf


FIELD_NAME_PATHNAME_MAP = {
    'Bakken': str(orchid.training_data_path().joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')),
    'Permian': str(orchid.training_data_path().joinpath('Project_frankNstein_Permian_UTM13_FEET.ifrac')),
    'Montney': str(orchid.training_data_path().joinpath('Project-frankNstein_Montney_UTM13_METERS.ifrac'))
}


@given("I have loaded a project from the file, '{filename}'")
def step_impl(context, filename):
    """
    :type context: behave.runner.Context
    :param filename: The name of the .ifrac file to be loaded.
    """
    project_pathname = str(orchid.training_data_path().joinpath(filename))
    if project_pathname not in context.loaded_projects:
        context.loaded_projects[project_pathname] = orchid.core.load_project(project_pathname)
    context.project = context.loaded_projects[project_pathname]


@given("I have loaded the project for the field, '{field}'")
def step_impl(context, field):
    """
    :type context: behave.runner.Context
    :param field: The name of the field of the project.
    """
    context.field = field
    project_pathname = FIELD_NAME_PATHNAME_MAP[field]
    if project_pathname not in context.loaded_projects:
        context.loaded_projects[project_pathname] = orchid.core.load_project(project_pathname)
    context.project = context.loaded_projects[project_pathname]


@when("I query the project name")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.actual_project_name = context.project.name


@then('I see the text "{expected_project_name}"')
def step_impl(context, expected_project_name):
    """
    :param expected_project_name: The expected name of the project.
    :type context: behave.runner.Context
    """
    assert_that(context.actual_project_name, equal_to(expected_project_name))


@when("I query the project wells")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.actual_wells = context.project.wells


# noinspection PyBDDParameters
@then("I see that the project, {project}, has {well_count:d} wells")
def step_impl(context, project, well_count):
    """
    Args:
        context (behave.runner.Context): The test context.
        project (str): The name identifying the project of interest.
        well_count (int): The number of wells in the project of interest.
    """
    context.execute_steps(f'When I query the project name')
    context.execute_steps(f'Then I see the text "{project}"')
    assert_that(len(list(context.actual_wells)), equal_to(well_count))


@then("I see the well details {well}, {display_name}, and {uwi} for {object_id}")
def step_impl(context, well, display_name, uwi, object_id):
    def actual_details_to_check(well_adapter):
        return well_adapter.name, well_adapter.display_name, well_adapter.uwi, str(well_adapter.object_id)

    def expected_details_to_check():
        return well, display_name, uwi, object_id

    tmp_to_test = toolz.pipe(toolz.map(actual_details_to_check, context.actual_wells),
                             toolz.filter(lambda d: d[0] == well),
                             toolz.first)

    actual_to_test = tmp_to_test
    if tmp_to_test[2] == '':
        actual_to_test = (tmp_to_test[0], tmp_to_test[1], None, str(tmp_to_test[3]))

    assert_that(actual_to_test, equal_to(expected_details_to_check()))


@when("I query the project default well colors")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.actual_default_well_colors = context.project.default_well_colors()


@then("I see the colors")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert_that(len(context.actual_default_well_colors), equal_to(len(context.table.rows)))
    for (actual, expected) in zip(context.actual_default_well_colors, context.table):
        for component_index, component_name in zip(range(3), ['red', 'green', 'blue']):
            assert_that(actual[component_index], equal_to(float(expected[component_name])))


@when("I query the project bounds")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):  The test context.
    """
    min_x, max_x, min_y, max_y, min_depth, max_depth = context.project.project_bounds()
    context.project_bounds = {
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y,
        'min_depth': min_depth,
        'max_depth': max_depth,
    }


@then("I see project bounds {min_x}, {max_x}, {min_y}, {max_y}, {min_depth}, and {max_depth},")
def step_impl(context, min_x, max_x, min_y, max_y, min_depth, max_depth):
    """
    Args:
        context (behave.runner.Context): The test context.
        min_x (str): The project's minimum x-coordinate (in project units and relative to the absolute state plane).
        max_x (str): The project's maximum y-coordinate.
        min_y (str): The project's minimum y-coordinate.
        max_y (str): The project's maximum y-coordinate.
        min_depth (str): The project's minimum (total vertical) depth coordinate.
        max_depth (str): The project's maximum depth coordinate.
    """

    cf.assert_that_actual_measurement_close_to_expected(context.project_bounds['min_x'], min_x)
    cf.assert_that_actual_measurement_close_to_expected(context.project_bounds['max_x'], max_x)
    cf.assert_that_actual_measurement_close_to_expected(context.project_bounds['min_y'], min_y)
    cf.assert_that_actual_measurement_close_to_expected(context.project_bounds['max_y'], max_y)
    cf.assert_that_actual_measurement_close_to_expected(context.project_bounds['min_depth'], min_depth)
    cf.assert_that_actual_measurement_close_to_expected(context.project_bounds['max_depth'], max_depth)


@when("I query the project measurements")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    context.project_measurements = {
        'fluid_density': context.project.fluid_density,
        'azimuth': context.project.azimuth,
        'center_x': context.project.project_center().x,
        'center_y': context.project.project_center().y,
    }


@then("I see project measurements {fluid_density}, {azimuth}, {center_x}, and {center_y}")
def step_impl(context, fluid_density, azimuth, center_x, center_y):
    """
    Args:
        context (behave.runner.Context): The test context.
        fluid_density (str): The fluid density measurement in project units.
        azimuth (str): The azimuth in project units.
        center_x (str): The x-coordinate of the project center in project units.
        center_y (str): The y-coordinate of the project center in project units.
    """

    cf.assert_that_actual_measurement_close_to_expected(context.project_measurements['fluid_density'], fluid_density)
    cf.assert_that_actual_measurement_close_to_expected(context.project_measurements['azimuth'], azimuth)
    cf.assert_that_actual_measurement_close_to_expected(context.project_measurements['center_x'], center_x)
    cf.assert_that_actual_measurement_close_to_expected(context.project_measurements['center_y'], center_y)


@when("I query the project well time series")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    context.monitor_curves = context.project.monitor_curves()
    assert_that(context.monitor_curves, is_(not_none()))


# noinspection PyBDDParameters
@then("I see the samples {index:d}, {qty_name}, {time}, and {value} for {name}")
def step_impl(context, index, qty_name, time, value, name):
    """
    Args:
        context (behave.runner.Context): The test context
        index (int): The index of the well time series sample of interest.
        qty_name (str): The phenomenon type of sample of interest.
        time (str): The time of the sample of interest
        value (str): The measured value of the sample of interest.
        name (str): The name of the sampled time series curve.
    """
    def is_candidate(curve_to_test):
        return curve_to_test.name == name and curve_to_test.sampled_quantity_name == qty_name

    candidate_curves = list(toolz.filter(is_candidate, context.monitor_curves))
    assert_that(len(candidate_curves), equal_to(1),
                f'Expected 1 curve with name, {name}, and sampled quantity_name, {qty_name}.' +
                f' Found {len(candidate_curves)}')

    curve = candidate_curves[0]
    actual_quantity_name = curve.sampled_quantity_name
    assert_that(actual_quantity_name, equal_to(qty_name))

    samples = curve.time_series()

    actual_sample_time = samples.index[index]
    expected_sample_time = dup.parse(time)
    assert_that(actual_sample_time, equal_to(expected_sample_time))

    actual_sample_magnitude = samples[actual_sample_time]
    actual_sample_measurement = orchid.make_measurement(curve.sampled_quantity_unit(), actual_sample_magnitude)
    cf.assert_that_actual_measurement_close_to_expected(actual_sample_measurement, value)
