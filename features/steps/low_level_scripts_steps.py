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

import pathlib
import re
import shutil
import subprocess
import sys

from hamcrest import assert_that, equal_to
import toolz.curried as toolz

import orchid


# noinspection PyBDDParameters
@given("I have copied the low-level script, '<{script_file_name}>', to the repository root")
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
    except AssertionError:
        script_error = script_process.stderr
        print(script_error)
        raise


# noinspection PyBDDParameters
@then("I see that <{observation_count:d}> observations were picked")
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
    script_lines = script_output.split()
    pattern = re.compile(r'len\(observation_set.GetObservations\(\)\)=(\d+)$')
    candidate_get_observations_matches = toolz.pipe(
        script_lines,
        toolz.map(lambda l: re.search(pattern, l)),
        toolz.filter(lambda m: m is not None),
        list,
    )
    try:
        assert_that(len(candidate_get_observations_matches), equal_to(2),
                    f'Expected exactly two matches in output. Found {candidate_get_observations_matches}')
        to_test_count = int(candidate_get_observations_matches[-1].group(1))
        assert_that(to_test_count, equal_to(observation_count), (f'Expected second observation count to'
                                                                 f' equal {observation_count}. Found {to_test_count}'))
    except AssertionError:
        print(f'Output:\n{script_output}')
        raise


# noinspection PyBDDParameters
@step("I see that <{attribute_count:d}> attributes were created for each stage of each well")
def step_impl(context, attribute_count):
    """
    Args:
        context (behave.runner.Context): The test context
        attribute_count (int): The number of attributes added to each stage of each well
    """
    # script_output = script_process.stdout
    # print(script_output)
    raise NotImplementedError(f"STEP: Then I see that <{attribute_count}> attributes were added"
                              f" for each stage and well")