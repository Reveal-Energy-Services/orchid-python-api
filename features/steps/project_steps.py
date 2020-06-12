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

from behave import *
use_step_matcher("parse")

from hamcrest import assert_that, equal_to

import orchid


PROJECT_NAME_PATHNAME_MAP = {'Oasis_Crane_II': r'c:\Users\larry.jones\tmp\ifa-test-data\Crane_II.ifrac'}


@given('I have loaded the "{project_name}" project')
def step_impl(context, project_name):
    """
    :param project_name: Name of .ifrac project to load
    :type context: behave.runner.Context
    """
    project_pathname = PROJECT_NAME_PATHNAME_MAP[project_name]
    context.project = orchid.core.load_project(project_pathname)


@when("I query the project name")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.actual_project_name = context.project.name()


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
    context.actual_wells = context.project.wells()


@then("I see the well information")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert_that(len(context.actual_wells), equal_to(len(context.table.rows)))
    for (actual, expected) in zip(context.actual_wells, context.table):
        assert_that(actual.name(), equal_to(expected['name']))
        assert_that(actual.display_name(), equal_to(expected['display_name']))
        assert_that(actual.uwi(), equal_to(expected['uwi']))


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
