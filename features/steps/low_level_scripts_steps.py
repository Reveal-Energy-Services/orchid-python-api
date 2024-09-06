#  Copyright (c) 2017-2024 KAPPA
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

import pathlib
import shutil
import subprocess
import sys

from hamcrest import assert_that, equal_to, is_, not_none
import parsy
import pendulum as pdt
import toolz.curried as toolz

import orchid

import parse_script_output as pso

# noinspection PyPackageRequirements
from behave import *

use_step_matcher("parse")


class ExtendedParseError(Exception):
    """An error providing better error information to diagnose issues."""

    def __str__(self):
        indent = '  '
        # noinspection PyUnresolvedReferences
        return ('\n'
                f'{indent}Consumed:'
                f'\n{indent * 2}{repr(self.__context__.stream[self.__context__.index - 64:self.__context__.index])}'
                '\n'
                f'{indent}Parsing:'
                f'\n{indent * 2}{repr(self.__context__.stream[self.__context__.index:])}\n')


# noinspection PyBDDParameters
@given("I have copied the low-level script, '{script_file_name}', to the repository root")
def step_impl(context, script_file_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        script_file_name (str): The file name of the script to copy.
    """
    repository_root = pathlib.Path()
    low_level_example_scripts_dirname = repository_root.joinpath('orchid_python_api', 'examples', 'low_level')
    to_copy_path_name = low_level_example_scripts_dirname.joinpath(script_file_name)
    shutil.copy(to_copy_path_name, repository_root)
    script_path = repository_root.joinpath(script_file_name)
    assert_that(script_path.exists(), f'Script, {str(script_path.absolute())}, does not exist.')
    context.script_path = script_path


# noinspection PyBDDParameters
@when("I execute the script using project version {ifrac_version}")
def step_impl(context, ifrac_version):
    """
    Args:
        context (behave.runner.Context):
        ifrac_version (str): The value identifying the version of the `.ifrac` file.
    """
    training_data_dir = pathlib.Path(orchid.configuration.training_data_path())
    version_suffix = f'.{ifrac_version}' if ifrac_version != 'v2' else ''
    training_data_path = training_data_dir.joinpath(f'frankNstein_Bakken_UTM13_FEET{version_suffix}.ifrac')
    command_line = [sys.executable, str(context.script_path), '-v2', str(training_data_path)]
    script_process = subprocess.run(command_line, capture_output=True, text=True)
    try:
        assert_that(script_process.returncode, equal_to(0), f'{" ".join(command_line)}'
                                                            f' returns {script_process.returncode}')
        context.script_process = script_process
        pathlib.Path(context.script_path).unlink()
    except AssertionError:
        script_error = script_process.stderr
        print(script_error)
        raise


# noinspection PyBDDParameters
@then("I see that {observation_count:d} observations were picked")
def step_impl(context, observation_count):
    """
    Args:
        context (behave.runner.Context): The test context.
        observation_count (int): The number of observations that were picked.
    """
    # TODO: I believe the following, commented out code, is correct.
    # However, at run-time, `context.script_process.stderr` has the output text (from the Python logger) and
    # `context.script_process.stdout` contains an empty string. Based on the behavior of the `monitor_time_series`
    # script, I believe this anomaly results from using the Python logger (perhaps it is configured to pipe standard
    # output to standard error).
    # script_output = context.script_process.stdout
    script_output = context.script_process.stderr
    try:
        actual_observations_count = pso.get_second_observations_count.parse('\n'.join(script_output.split('\n')[1:]))  # Remove first log which only shows orchid path
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe
    try:
        assert_that(actual_observations_count, equal_to(observation_count),
                    (f'Expected second observation count to' f' equal {observation_count}.'
                     f' Found {actual_observations_count}'))
    except AssertionError:
        print(f'Output:\n{script_output}')
        raise


# noinspection PyBDDParameters
@step("I see that {attribute_count:d} attributes were created for each stage of each well")
def step_impl(context, attribute_count):
    """
    Args:
        context (behave.runner.Context): The test context
        attribute_count (int): The number of attributes added to each stage of each well
    """
    # TODO: I believe the following, commented out code, is correct.
    # However, at run-time, `context.script_process.stderr` has the output text (from the Python logger) and
    # `context.script_process.stdout` contains an empty string. Based on the behavior of the `monitor_time_series`
    # script, I believe this anomaly results from using the Python logger (perhaps it is configured to pipe standard
    # output to standard error).
    # script_output = context.script_process.stdout
    script_output = context.script_process.stderr
    try:
        actual_attributes_count_per_stage_per_well = \
            pso.get_attribute_count_for_each_stage_and_well.parse('\n'.join(script_output.split('\n')[1:]))  # Remove first log which only shows orchid path
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe
    try:
        assert_that(actual_attributes_count_per_stage_per_well, equal_to(attribute_count),
                    (f'Expected second observation count to' f' equal {attribute_count}.'
                     f' Found {actual_attributes_count_per_stage_per_well}'))
    except AssertionError:
        print(f'Output:\n{script_output}')
        raise


@step("I see the following added stages")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    # TODO: I believe the following, commented out code, is correct.
    # However, at run-time, `context.script_process.stderr` has the output text (from the Python logger) and
    # `context.script_process.stdout` contains an empty string. Based on the behavior of the `monitor_time_series`
    # script, I believe this anomaly results from using the Python logger (perhaps it is configured to pipe standard
    # output to standard error).
    # script_output = context.script_process.stdout
    script_output = context.script_process.stderr
    try:
        actual_added_stages_details = pso.get_added_stages.parse('\n'.join(script_output.split('\n')[1:]))  # Remove first log which only shows orchid path
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe
    expected_added_stage_details = context.table

    assert_that(len(actual_added_stages_details), equal_to(len(expected_added_stage_details.rows)))

    for expected_details_row, actual_details in zip(expected_added_stage_details.rows, actual_added_stages_details):
        assert_that(actual_details.stage_name, equal_to(expected_details_row['stage_name']))
        assert_that(actual_details.cluster_count, equal_to(int(expected_details_row['clusters'])))
        assert_that(actual_details.global_stage_sequence_no, equal_to(int(expected_details_row['global_seq_no'])))
        expected_stage_time_range = pdt.parse(expected_details_row['stage_time_range'])
        assert_that(actual_details.start_time, equal_to(expected_stage_time_range.start))
        assert_that(actual_details.stop_time, equal_to(expected_stage_time_range.end))


def sections(all_output):
    return all_output.split('\n\n')


@then("I see all time series in the project")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    script_output = context.script_process.stdout
    # Sections are separated by an empty line.
    raw_sections = sections(script_output)
    # The time series are in the first section.
    all_time_series_in_project_output = raw_sections[0]
    try:
        actual_time_series_in_project = pso.all_times_series_in_project.parse(all_time_series_in_project_output)
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe
    try:
        expected_time_series_in_project = pso.brief_orchid_objects.parse(context.text)
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe

    assert_that(actual_time_series_in_project, equal_to(expected_time_series_in_project))


@step("I see all monitors in the project")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    script_output = context.script_process.stdout
    # Sections are separated by an empty line.
    raw_sections = sections(script_output)
    # The monitors are in the second section.
    all_monitors_in_project = raw_sections[1]
    try:
        actual_monitors_in_project = pso.all_monitors_in_project.parse(all_monitors_in_project)
        expected_monitors_in_project = pso.brief_orchid_objects.parse(context.text)
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe

    assert_that(actual_monitors_in_project, equal_to(expected_monitors_in_project))


@step("I see the monitor of interest")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    script_output = context.script_process.stdout
    # Sections are separated by an empty line.
    raw_sections = sections(script_output)
    # The monitor time series are in the third section.
    monitor_of_interest_output = raw_sections[2]
    try:
        actual_monitors_of_interest = pso.monitor_of_interest.parse(monitor_of_interest_output)
        expected_monitors_of_interest = pso.monitor_of_interest.parse(context.text)
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe

    assert_that(actual_monitors_of_interest, equal_to(expected_monitors_of_interest))


@step("I see the object ID of the monitor time series")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    script_output = context.script_process.stdout
    # Sections are separated by an empty line.
    raw_sections = sections(script_output)
    # The monitor time series are in the fourth section.
    monitor_time_series_of_interest_output = raw_sections[3]
    try:
        actual_monitor_time_series_of_interest = pso.monitor_time_series_of_interest.parse(
            monitor_time_series_of_interest_output)
        expected_monitor_time_series_of_interest = pso.monitor_time_series_of_interest.parse(context.text)
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe

    assert_that(actual_monitor_time_series_of_interest, equal_to(expected_monitor_time_series_of_interest))


@step("I see the first few time series samples for the monitor")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    script_output = context.script_process.stdout
    # Sections are separated by an empty line.
    raw_sections = sections(script_output)
    # The time series samples are in the fifth section
    time_series_samples_output = raw_sections[4]
    try:
        actual_time_series_samples = pso.monitor_time_series_samples.parse(time_series_samples_output)
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe

    assert_that(len(actual_time_series_samples.samples), equal_to(len(context.table.rows)))
    for actual_samples, expected_samples in zip(actual_time_series_samples.samples, context.table.rows):
        assert_that(actual_samples,
                    equal_to(pso.TimeSeriesSample(pdt.parse(expected_samples['sample_time']),
                                                  float(expected_samples['sample_value']))))


@step("I see the time series name and data type")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    script_output = context.script_process.stdout
    # Sections are separated by an empty line.
    raw_sections = sections(script_output)
    # The time series samples are in the fifth section
    time_series_samples_output = raw_sections[4]
    try:
        actual_time_series_samples = pso.monitor_time_series_samples.parse(time_series_samples_output)
        expected_about_time_series_samples = pso.about_monitor_time_series_samples.parse(context.text)

        assert_that(actual_time_series_samples.about.name, equal_to(expected_about_time_series_samples.name))
        assert_that(actual_time_series_samples.about.dtype, equal_to(expected_about_time_series_samples.dtype))
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe


@then('I see that the "{set_name}" set has observations')
def step_impl(context, set_name):
    """
    Args:
        context (behave.runner.Context): The test context containing the expected observation counts.
        set_name (str): The name of the observation set.
    """
    # TODO: I believe the following, commented out code, is correct.
    # However, at run-time, `context.script_process.stderr` has the output text (from the Python logger) and
    # `context.script_process.stdout` contains an empty string. Based on the behavior of the `monitor_time_series`
    # script, I believe this anomaly results from using the Python logger (perhaps it is configured to pipe standard
    # output to standard error).
    # script_output = context.script_process.stdout
    script_output = context.script_process.stderr
    try:
        actual_results = pso.get_observations_counts.parse('\n'.join(script_output.split('\n')[1:]))  # Remove first log which only shows orchid path
    except parsy.ParseError as pe:
        raise ExtendedParseError from pe
    expected_observation_counts = context.table

    assert_that(len(actual_results[set_name]),
                equal_to(len(expected_observation_counts.headings)), f'{pso.PARENT_WELLS} columns')
    assert_that(len(actual_results[set_name]),
                equal_to(len(expected_observation_counts.headings)), f'{pso.MULTI_PICKING} columns')

    assert_that(toolz.get_in([set_name, pso.LEAK_OFF_COUNT], actual_results),
                equal_to(int(expected_observation_counts.rows[0]['leak_off_count'])),
                f'Leak off count for {set_name}')
    assert_that(toolz.get_in([set_name, pso.MULTI_PICK_COUNT], actual_results),
                equal_to(int(expected_observation_counts.rows[0]['multi_pick_count'])),
                f'Multi-pick count for {set_name}')

    context.save_project_path = actual_results[pso.WROTE_CHANGES_TO]


@step("I can successfully load the file after saving")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): Test context (contains saved project path)
    """
    loaded_project = orchid.load_project(str(context.save_project_path))
    assert_that(loaded_project, is_(not_none()))
