#  Copyright 2017-2020 Reveal Energy Services, Inc 
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

from behave import *
use_step_matcher("parse")

from hamcrest import assert_that, equal_to
import toolz.curried as toolz


# noinspection PyBDDParameters
@then("I see {stage_count:d} stages for well {well}")
def step_impl(context, stage_count, well):
    """
    Args:
        context (behave.runner.Context): The context of the test.
        stage_count (int): The number of stages for the well of interest.
        well (str): The name of the well of interest.
    """
    def actual_test_details(well_adapter):
        return well_adapter.name, toolz.count(well_adapter.stages)

    def expected_test_details():
        return well, stage_count

    candidates = list(toolz.pipe(toolz.map(actual_test_details, context.actual_wells),
                                 toolz.filter(lambda d: d[0] == well)))
    assert_that(len(candidates), equal_to(1))  # expect exactly one match

    assert_that(candidates[0], equal_to(expected_test_details()))
