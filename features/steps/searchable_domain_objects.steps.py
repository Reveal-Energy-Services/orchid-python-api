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


# noinspection PyPackageRequirements
from behave import *
use_step_matcher("parse")


@when("I query the loaded project for the data frame named '{name}' with {surrounding} whitespace")
def step_impl(context, name, surrounding):
    """
    Args:
        context (behave.runner.Context):
        name (str):
        surrounding (str):
    """
    raise NotImplementedError(
        u'STEP: When I query the loaded project for the data frame named \'<name>\' with <surrounding> whitespace')


@then("I see a single data frame named '{name}' with no surrounding whitespace")
def step_impl(context, name):
    """
    Args:
        context (behave.runner.Context):
        name (str):
    """
    raise NotImplementedError(u'STEP: Then I see a single data frame named \'<name>\' with no surrounding whitespace')


@when("I query the loaded project for the data frame with display name '{name}' and {surrounding} whitespace")
def step_impl(context, name, surrounding):
    """
    Args:
        context (behave.runner.Context):
        name (str):
        surrounding (str):
    """
    raise NotImplementedError(
        u'STEP: When I query the loaded project for the data frame with display name \'<name>\' and <surrounding> whitespace')


@then("I see a single data frame with display name '{name}' and no surrounding whitespace")
def step_impl(context, name):
    """
    Args:
        context (behave.runner.Context):
        name (str):
    """
    raise NotImplementedError(
        u'STEP: Then I see a single data frame with display name \'<name>\' and no surrounding whitespace')