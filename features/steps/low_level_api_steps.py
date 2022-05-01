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


# noinspection PyBDDParameters
@step("I create a stage attribute named '{attr_name}' for a(n) {type_name} value")
def step_impl(context, attr_name, type_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        attr_name (str): The name of the attribute to add.
        type_name (str): The name of the type of the attribute.
    """
    raise NotImplementedError(f'STEP: I create a stage attribute named "{attr_name}" for a(n) {type_name} value')


# noinspection PyBDDParameters
@step("I add the created attributes to the well, '{well}', of the project")
def step_impl(context, well):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The well of interest.
    """
    raise NotImplementedError(f"STEP: And I add the created attributes to the well, '{well}', of the project")


# noinspection PyBDDParameters
@step("I set the value of the stage length attribute of stage, {stage_no:d}, of '{well}' to the {length}")
def step_impl(context, stage_no, well, length):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The integer identifying the stage of interest.
        well (str): The well of interest.
        length (str): The value of the stage length attribute of stage to set.
    """
    raise NotImplementedError(f"STEP: And I set the value of the stage length attribute of stage, {stage_no},"
                              f" of '{well}' to the {length}")


# noinspection PyBDDParameters
@step("I set the value of the sequence number attribute of stage, {stage_no}, of '{well}' to {global_seq_no:d}")
def step_impl(context, stage_no, well, global_seq_no):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The integer identifying the stage of interest.
        well (str): The well of interest.
        global_seq_no (int): The value of the global stage sequence number attribute.
    """
    raise NotImplementedError(f"STEP: And I set the value of the sequence number attribute of stage, {stage_no},"
                              f" of '{well}' to {global_seq_no}")


# noinspection PyBDDParameters
@then("I see the value of the stage length attribute of stage, {stage_no:d}, of '{well}' equals {length}")
def step_impl(context, stage_no, well, length):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The integer identifying the stage of interest.
        well (str): The well of interest.
        length (str): The value of the stage length attribute of stage to set.
    """
    raise NotImplementedError(f"STEP: Then I see the value of the stage length attribute of stage, {stage_no},"
                              f" of '{well}' equals {length}")


# noinspection PyBDDParameters
@step("I see the value of the sequence number attribute for stage, {stage_no:d}, of '{well}' equal to {global_seq_no}")
def step_impl(context, stage_no, well, global_seq_no):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The integer identifying the stage of interest.
        well (str): The well of interest.
        global_seq_no (int): The value of the global stage sequence number attribute.
    """
    raise NotImplementedError(
        f"STEP: And I see the value of the sequence number attribute for stage, {stage_no},"
        f" of '{well}' equal to {global_seq_no}")