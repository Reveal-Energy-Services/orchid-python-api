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

from hamcrest import assert_that, equal_to, is_, not_none
import dateutil.parser as dt_parser
import datetimerange as dtr
import toolz.curried as toolz

from tests import custom_matchers as tcm


@when("I query the monitor identified by {display_name} for the project for '{field}'")
def step_impl(context, display_name, field):
    """
    Args:
        context (behave.runner.Context): The testing context.
        field (str): The name of the field whose monitors are sought
        display_name (str): The name used by operations engineers to identify the monitor of interest.
    """
    context.monitor = toolz.get(display_name, context.project.monitors())
    assert_that(context.monitor, is_(not_none()))


# noinspection PyBDDParameters
@then("I see the {name}, {start_time}, and {stop_time} for the queried monitor")
def step_impl(context, name, start_time, stop_time):
    """
    Args:
        context (behave.runner.Context): The testing context.
        name: The name of the monitor (optional).
        start_time (str): The expected start time in ISO 8601 format
        stop_time (str): The expected stop time in ISO 8601 format
    """
    assert_that(context.monitor.name, equal_to(name))
    monitor_time_range = context.monitors.time_range
    expected_start = dt_parser.parse(start_time)
    expected_stop = dt_parser.parse(stop_time)
    expected_time_range = dtr.DateTimeRange(expected_start, expected_stop)
    assert_that(monitor_time_range, tcm.equal_to_time_range(expected_time_range))
