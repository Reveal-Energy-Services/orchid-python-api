#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

import pathlib

from behave import *
use_step_matcher("parse")

from hamcrest import assert_that, equal_to
import toolz.curried as toolz

import orchid


PROJECT_NAME_PATHNAME_MAP = {'Oasis_Crane_II': r'c:\Users\larry.jones\tmp\ifa-test-data\Crane_II.ifrac',
                             'Demo_Project': r'c:\Users\larry.jones\tmp\TrainingDataSet\Demo_Project.ifrac'}
FIELD_NAME_PATHNAME_MAP = {
    'Bakken': r'c:\src\Orchid.IntegrationTestData\frankNstein_Bakken_UTM13_FEET.ifrac',
    'Permian': r'c:\src\Orchid.IntegrationTestData\Project_frankNstein_Permian_UTM13_FEET.ifrac',
    'Montney': r'c:\src\Orchid.IntegrationTestData\Project-frankNstein_Montney_UTM13_METERS.ifrac'
}


@given("I have loaded a project from the file, '{filename}'")
def step_impl(context, filename):
    """
    :type context: behave.runner.Context
    :param filename: The name of the .ifrac file to be loaded.
    """
    project_pathname = str(pathlib.Path(__file__).joinpath(
        '..', '..', '..', '..', 'Orchid.IntegrationTestData', filename))
    if project_pathname not in context.loaded_projects:
        context.loaded_projects[project_pathname] = orchid.core.load_project(project_pathname)
    context.project = context.loaded_projects[project_pathname]


@given("I have loaded the project for the field, '{field_name}'")
def step_impl(context, field_name):
    """
    :type context: behave.runner.Context
    :param field_name: The name of the field of the project.
    """
    project_pathname = FIELD_NAME_PATHNAME_MAP[field_name]
    if project_pathname not in context.loaded_projects:
        context.loaded_projects[project_pathname] = orchid.core.load_project(project_pathname)
    context.project = context.loaded_projects[project_pathname]


@given('I have loaded the "{project_name}" project')
def step_impl(context, project_name):
    """
    :param project_name: Name of .ifrac project to load
    :type context: behave.runner.Context
    """
    project_pathname = PROJECT_NAME_PATHNAME_MAP[project_name]
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
@then("I see that the project, {project_name}, has {well_count:d} wells")
def step_impl(context, project_name, well_count):
    """
    :type context: behave.runner.Context
    :type project_name: str
    :param project_name: The name identifying the project of interest.
    :type well_count: int
    :param well_count: The number of wells in the project of interest.
    """
    context.execute_steps(f'When I query the project name')
    context.execute_steps(f'Then I see the text "{project_name}"')
    assert_that(len(list(context.actual_wells)), equal_to(well_count))


@then("I see the well details {well_name}, {display_name}, and {uwi} for {object_id}")
def step_impl(context, well_name, display_name, uwi, object_id):
    def actual_details_to_check(well):
        return well.name, well.display_name, well.uwi, str(well.object_id)

    def expected_details_to_check():
        return well_name, display_name, uwi, object_id

    tmp_to_test = toolz.pipe(toolz.map(actual_details_to_check, context.actual_wells),
                             toolz.filter(lambda d: d[0] == well_name),
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
