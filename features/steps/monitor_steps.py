#  Copyright (c) 2017-2022 Reveal Energy Services, Inc
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

import uuid

from hamcrest import assert_that, equal_to, is_, not_none
import pendulum

import orchid

import common_functions as cf

from tests import custom_matchers as tcm


@when("I query the monitor identified by display name, {display_name}, for the project for '{field}'")
def step_impl(context, display_name, field):
    """
    Args:
        context (behave.runner.Context): The testing context.
        field (str): The name of the field whose monitors are sought
        display_name (str): The value used by data scientists to identify a single monitor of interest.
    """
    candidates = list(context.project.monitors().find_by_display_name(display_name))
    assert_that(len(candidates), equal_to(1))
    context.monitor = candidates[0]


@when("I query the monitor identified by object ID, {object_id}, for the project for '{field}'")
def step_impl(context, object_id, field):
    """
    Args:
        context (behave.runner.Context): The testing context.
        field (str): The name of the field whose monitors are sought
        object_id (str): The value used by data scientists to identify a single monitor of interest.
    """
    context.monitor = context.project.monitors().find_by_object_id(uuid.UUID(object_id))
    assert_that(context.monitor, is_(not_none()))


# noinspection PyBDDParameters
@then("I see the {name}, {start_time}, and {stop_time} for the queried monitor")
def step_impl(context, name, start_time, stop_time):
    """
    Args:
        context (behave.runner.Context): The testing context
        name: The name of the monitor (optional)
        start_time (str): The expected start time in ISO 8601 format
        stop_time (str): The expected stop time in ISO 8601 format
    """
    assert_that(context.monitor.name, equal_to(name))
    monitor_time_range = context.monitor.time_range
    expected_start = pendulum.parse(start_time)
    expected_stop = pendulum.parse(stop_time)
    expected_time_range = pendulum.Period(expected_start, expected_stop)
    assert_that(monitor_time_range, tcm.equal_to_time_range(expected_time_range))


@then("I see the {object_id}, {start_time} and {stop_time} for the queried monitor")
def step_impl(context, object_id, start_time, stop_time):
    """
    Args:
        context (behave.runner.Context): The test context
        object_id (str): The value that identifies a single monitor object
        start_time (str):  The start time of this monitor
        stop_time (str):  The stop time of this monitor
    """
    actual = context.monitor

    assert_that(actual.object_id, equal_to(uuid.UUID(object_id)))
    assert_that(actual.time_range, tcm.equal_to_time_range(pendulum.Period(pendulum.parse(start_time),
                                                                           pendulum.parse(stop_time))))


@when("I query the monitor time series with {display_name}")
def step_impl(context, display_name):
    """
    Args:
        context (behave.runner.Context): The test context
        display_name (str): The display name that identifies the monitor of interest.
    """
    candidate_monitors = list(context.project.monitors().find_by_display_name(display_name))
    assert_that(len(candidate_monitors), equal_to(1),
                f'Expected single monitor with {display_name}. Found {len(candidate_monitors)}.')

    context.monitor = candidate_monitors[0]


@then("I see the samples {index:d}, {qty_name}, {time}, and {value} for the monitor time series")
def step_impl(context, index, qty_name, time, value):
    """
    Args:
        context (behave.runner.Context): The test context
        index (int): The index of the well time series sample of interest.
        qty_name (str): The phenomenon type of sample of interest.
        time (str): The time of the sample of interest
        value (str): The measured value of the sample of interest.
    """
    # curve = context.monitor.time_series()
    # actual_quantity_name = curve.sampled_quantity_name
    # assert_that(actual_quantity_name, equal_to(qty_name))
    #
    # samples = curve.data_points()
    #
    # actual_sample_time = samples.index[index]
    # expected_sample_time = pendulum.parse(time)
    # assert_that(actual_sample_time, equal_to(expected_sample_time))
    #
    # actual_sample_magnitude = samples[actual_sample_time]
    # actual_sample_measurement = orchid.make_measurement(curve.sampled_quantity_unit(), actual_sample_magnitude)
    # cf.assert_that_actual_measurement_close_to_expected(actual_sample_measurement, value)
    pass
