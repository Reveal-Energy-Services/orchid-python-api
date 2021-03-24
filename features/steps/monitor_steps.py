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

from hamcrest import assert_that, equal_to
import dateutil.parser as dt_parser


@when("I query the monitor start and stop times for '{field}'")
def step_impl(context, field):
    """
    Args:
        context (behave.runner.Context):
        field (str): The name of the field whose monitor start and stop times are sought
    """
    context.monitors = context.project.monitors


@then("I see the {start} and {stop} times for the monitor at {index}")
def step_impl(context, start, stop, index):
    """
    Args:
        context (behave.runner.Context):
        start (str): The expected start time in ISO 8601 format.
        stop (str): The expected stop time in ISO 8601 format.
        index (str): The index of the monitor of interest.
    """
    monitor_time_range = context.monitors.time_range()
    expected_start = dt_parser.parse(start)
    assert_that(monitor_time_range.start, equal_to(expected_start))
    expected_stop = dt_parser.parse(start)
    assert_that(monitor_time_range.stop, equal_to(expected_stop))
