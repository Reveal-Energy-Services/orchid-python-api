#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2025 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#


import random

# noinspection PyPackageRequirements
from behave import *
from hamcrest import assert_that, equal_to

import common_functions as cf

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

    return cf.find_data_frames_by_ignore_warnings(context, find_by_func, query_name)


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
