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
from hamcrest import assert_that, has_length, equal_to
from toolz.curried import reduce


@when('I query the stages for each well in the project')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    def all_stages_for_well(well):
        return well.stages()

    context.stages = map(all_stages_for_well, context.project.wells())
    assert_that(len(list(context.stages)), equal_to(135))


@when("I calculate the total fluid volume, proppant, and median treating pressure for each stage")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'I calculate the total fluid volume, proppant,'
                              u' and median treating pressure for each stage')


@then("I see 135 stage")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'I calculate the total fluid volume, proppant,'
                              u' and median treating pressure for each stage')


@step("I see correct sample values for <WellName>, <Stage>, <MdTop>, <MdBottom>, <Volume>, <Proppant> and <Median>")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And I see correct sample values for'
                              u' <WellName>, <Stage>, <MdTop>, <MdBottom>, <Volume>, <Proppant> and <Median>')
