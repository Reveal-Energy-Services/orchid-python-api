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

import dataclasses as dc
import pathlib
import re
import shutil
import subprocess
import sys

from hamcrest import assert_that, equal_to, is_, not_none
import parsy
import pendulum as pdt
import toolz.curried as toolz

import orchid

import parse_script_output as pso


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
@when("I execute the script")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    training_data_dir = pathlib.Path(orchid.configuration.training_data_path())
    training_data_path = training_data_dir.joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')
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
    # `context.script_process.stdout` contains an empty string.
    # script_output = context.script_process.stdout
    script_output = context.script_process.stderr
    actual_observations_count = pso.get_second_observations_count.parse(script_output)
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
    # `context.script_process.stdout` contains an empty string.
    # script_output = context.script_process.stdout
    script_output = context.script_process.stderr
    actual_attributes_count_per_stage_per_well = pso.get_attribute_count_for_each_stage_and_well.parse(script_output)
    try:
        assert_that(actual_attributes_count_per_stage_per_well, equal_to(attribute_count),
                    (f'Expected second observation count to' f' equal {attribute_count}.'
                     f' Found {actual_attributes_count_per_stage_per_well}'))
    except AssertionError:
        print(f'Output:\n{script_output}')
        raise


@dc.dataclass
class AddedStageDetails:
    """Models details of an added stage output by the `add_stages.py` low-level example script."""
    stage_name: str = 'Stage-36'
    shmin: str = '8144.498 psi'
    cluster_count: int = 0
    global_stage_sequence_no: int = 0
    start_time: pdt.DateTime = pdt.from_format('2018-06-06T05:34:03:684000+00:00', 'YYYY-MM-DDTHH:mm:ss:SSSSSSZ')
    stop_time: pdt.DateTime = pdt.from_format('2018-06-06T07:19:35:560000+00:00', 'YYYY-MM-DDTHH:mm:ss:SSSSSSZ')


def _parse_added_stage_details(details_text):
    pattern = re.compile(r"INFO:root:CreatedStageDetails\(name='(Stage-\d{2})', shmin='(\d+.\d+ psi)',"
                         r" cluster_count=(\d+), global_stage_sequence_no=(\d+),"
                         r" start_time='([^']+)', stop_time='([^']+)'\)")
    match = re.match(pattern, details_text)
    assert_that(match, is_(not_none()))
    # Groups are inside unescaped parentheses of the pattern. The zeroth group is the entire match; the first group
    # is the stage name, and so on. See
    # [Python help on regular expressions](https://docs.python.org/3.8/library/re.html) for details. Note that I used
    # the [Pythex website](https://pythex.org/) to test my regular expression.
    time_stamp_format = 'YYYY-MM-DDTHH:mm:ss.SSSSSSZ'
    start_time = pdt.from_format(match.group(5), time_stamp_format)
    stop_time = pdt.from_format(match.group(6), time_stamp_format)
    return AddedStageDetails(stage_name=match.group(1), shmin=match.group(2),
                             cluster_count=int(match.group(3)), global_stage_sequence_no=int(match.group(4)),
                             start_time=start_time, stop_time=stop_time)


@step("I see the following added stages")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context
    """
    # TODO: I believe the following, commented out code, is correct.
    # However, at run-time, `context.script_process.stderr` has the output text (from the Python logger) and
    # `context.script_process.stdout` contains an empty string.
    # script_output = context.script_process.stdout
    script_output = context.script_process.stderr
    script_lines = script_output.split('\n')
    expected_added_stage_details = context.table

    # One line for each stage plus two lines for output file path.
    assert_that(len(script_lines), equal_to(len(expected_added_stage_details.rows) + 2))

    for expected_details_row, actual_details_text in zip(expected_added_stage_details.rows, script_lines[:-1]):
        actual_details = _parse_added_stage_details(actual_details_text)
        assert_that(actual_details.stage_name, equal_to(expected_details_row['stage_name']))
        assert_that(actual_details.shmin, equal_to(expected_details_row['shmin']))
        assert_that(actual_details.cluster_count, equal_to(int(expected_details_row['clusters'])))
        assert_that(actual_details.global_stage_sequence_no, equal_to(int(expected_details_row['global_seq_no'])))
        expected_stage_time_range = pdt.parse(expected_details_row['stage_time_range'])
        assert_that(actual_details.start_time, equal_to(expected_stage_time_range.start))
        assert_that(actual_details.stop_time, equal_to(expected_stage_time_range.end))
