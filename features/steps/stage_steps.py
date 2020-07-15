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
import toolz.curried as toolz


# noinspection PyBDDParameters
@then("I see {stage_count:d} stages for well {well_name}")
def step_impl(context, stage_count, well_name):
    """
    :type context: behave.runner.Context
    :type stage_count: int
    :param stage_count: The number of stages for the well of interest
    :type well_name: str
    :param well_name: The name fo the well of interest
    """

    def actual_test_details(well):
        return well.name, toolz.count(well.stages)

    def expected_test_details():
        return well_name, stage_count

    candidates = list(toolz.pipe(toolz.map(actual_test_details, context.actual_wells),
                                 toolz.filter(lambda d: d[0] == well_name)))
    assert_that(len(candidates), equal_to(1))  # expect exactly one match

    assert_that(candidates[0], equal_to(expected_test_details()))
