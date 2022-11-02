#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#


import random
import warnings

# noinspection PyPackageRequirements
from behave import *
from hamcrest import assert_that, equal_to

use_step_matcher("parse")


@when("I query the loaded project for the data frame named '{name}' with {surrounding} whitespace")
def step_impl(context, name, surrounding):
    """
    Args:
        context (behave.runner.Context): The test context.
        name (str): The name of the data frame.
        surrounding (str): The kind of whitespace surrounding the data frame name in the query.
    """
    context.queried_domain_objects = _query_project_objects_by_find_func(context, name, surrounding,
                                                                         lambda src, qn: list(src.find_by_name(qn)))


def _query_project_objects_by_find_func(context, name, surrounding, find_by_func):
    if surrounding == 'no':
        query_name = name
    elif surrounding == 'leading':
        query_name = ' ' * random.choice(range(1, 3 + 1)) + name
    elif surrounding == 'trailing':
        query_name = name + ' ' * random.choice(range(1, 3 + 1))
    elif surrounding == 'leading and trailing':
        query_name = ' ' * random.choice(range(1, 3 + 1)) + name + ' ' * random.choice(range(1, 3 + 1))
    else:
        raise ValueError(f'Unexpected surrounding text: "{surrounding}"')

    # TODO: Remove catching warnings if we change the integration test data file,
    #  "c:\src\Orchid.IntegrationTestData\05PermianProjectQ3_2022_DataFrames.ifrac"
    #
    # I currently ignore these warnings only for this single project because it is the only project in the
    # integration test data that has duplicate object IDs in data frames. I ignore it because I do not want printing
    # the warning to act as a "false positive" for a developer investigating another issue, seeing this expected
    # warning and wondering (or investigating) the issue.
    with warnings.catch_warnings(record=False):
        if context.project.name == 'PermianProjectQ3_2022':
            warnings.simplefilter("ignore")
        return find_by_func(context.project.data_frames(), query_name)


@then("I see a single data frame named '{name}' with no surrounding whitespace")
def step_impl(context, name):
    """
    Args:
        context (behave.runner.Context): The text context.
        name (str): The expected data frame name.
    """
    assert_that(len(context.queried_domain_objects), equal_to(1))

    assert_that(context.queried_domain_objects[0].name, equal_to(name))


@when("I query the loaded project for the data frame with display name '{display_name}' and {surrounding} whitespace")
def step_impl(context, display_name, surrounding):
    """
    Args:
        context (behave.runner.Context): The test context.
        display_name (str): The display name of the data frame.
        surrounding (str): The kind of whitespace surrounding the data frame name in the query.
    """
    context.queried_domain_objects = _query_project_objects_by_find_func(
        context, display_name, surrounding, lambda src, qn: list(src.find_by_display_name(qn)))


@then("I see a single data frame with display name '{display_name}' and no surrounding whitespace")
def step_impl(context, display_name):
    """
    Args:
        context (behave.runner.Context): The text context.
        display_name (str): The expected data frame display name.
    """
    assert_that(len(context.queried_domain_objects), equal_to(1))

    assert_that(context.queried_domain_objects[0].display_name, equal_to(display_name))
