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
import shutil


# # noinspection PyBDDParameters
@given("I have copied the low-level script, '<script_file_name>', to the repository root")
def step_impl(context, script_file_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        script_file_name (str): The file name of the script to copy.
    """
    raise NotImplementedError(f"STEP: Given I have copied the low-level script, '<{script_file_name}>',"
                              f" to the repository root")


# noinspection PyBDDParameters
@when("I execute the script")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    raise NotImplementedError(u'STEP: When I execute the script')


# noinspection PyBDDParameters
@then("I see that <{picked_observation_count:d}> observations were picked")
def step_impl(context, picked_observation_count):
    """
    Args:
        context (behave.runner.Context): The test context.
        picked_observation_count (int): The number of picked observations.
    """
    raise NotImplementedError(f"STEP: Then I see that <{picked_observation_count}> observations were picked")


# noinspection PyBDDParameters
@step("I see that <{attribute_count:d}> attributes were created for each stage of each well")
def step_impl(context, attribute_count):
    """
    Args:
        context (behave.runner.Context): The test context
        attribute_count (int): The number of attributes added to each stage of each well
    """
    raise NotImplementedError(u'STEP: And I see that <{attribute_count}> attributes were created'
                              u' for each stage of each well')