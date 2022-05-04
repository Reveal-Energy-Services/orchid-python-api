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

from hamcrest import assert_that, equal_to, is_, not_none
import option
import toolz.curried as toolz


from orchid import (
    dot_net_disposable as dnd,
    measurement as om,
    net_quantity as onq,
    physical_quantity as opq,
    unit_system as units,
)

import common_functions as cf

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Factories.Implementations import Attribute
# noinspection PyUnresolvedReferences
from System import Double, Int32, String


# noinspection PyBDDParameters
@step("I create a stage attribute named '<{attr_name}>' for a(n) <{type_name}> value")
def step_impl(context, attr_name, type_name):
    """
    Args:
        context (behave.runner.Context): The test context.
        attr_name (str): The name of the attribute to add.
        type_name (str): The name of the type of the attribute.
    """
    type_name_to_net_type = {
        'double': Double,
        'integer': Int32,
        'string': String,
    }
    to_add = Attribute[type_name_to_net_type[type_name]].Create(attr_name)
    assert_that(to_add, is_(not_none()))
    if 'stage_attributes' not in context:
        context.stage_attributes = {}
    context.stage_attributes[attr_name] = to_add


# noinspection PyBDDParameters
@step("I add the created attributes to the well, '{well}', of the project")
def step_impl(context, well):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The well of interest.
    """
    to_add_to_well = cf.find_well_by_name_in_project(context, well)

    with dnd.disposable(to_add_to_well.dom_object.ToMutable()) as mutable_well:
        for attribute in context.stage_attributes.values():
            mutable_well.AddStageAttribute(attribute)

    for attribute_name in context.stage_attributes.keys():
        candidate_attributes = list(toolz.filter(lambda a: a.Name == attribute_name,
                                                 to_add_to_well.dom_object.StageAttributes.Items))
        assert_that(len(candidate_attributes), equal_to(1))
        # Beware: if one fails to include the `Name` attribute, the test will fail, but because the .NET implementation
        # of `Attribute.ToString()` prints the name, the failure will seem to report that it expected the name and it
        # **also** found the name.
        print(candidate_attributes[0] == context.stage_attributes[attribute_name])
        assert_that(candidate_attributes[0], equal_to(context.stage_attributes[attribute_name]))


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
    stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    with dnd.disposable(stage.dom_object.ToMutable()) as mutable_stage:
        expected_length = om.Quantity(length)
        mutable_stage.SetAttribute(context.stage_attributes['My Stage Length'],
                                   onq.as_net_quantity(opq.PhysicalQuantity.LENGTH, expected_length))


# noinspection PyBDDParameters
@step("I set the value of the sequence number attribute of stage, {stage_no:d}, of '{well}' to {global_seq_no:d}")
def step_impl(context, stage_no, well, global_seq_no):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The integer identifying the stage of interest.
        well (str): The well of interest.
        global_seq_no (int): The value of the global stage sequence number attribute.
    """
    stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    with dnd.disposable(stage.dom_object.ToMutable()) as mutable_stage:
        mutable_stage.SetAttribute(context.stage_attributes['My Global Stage Sequence Number'], global_seq_no)


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
    stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    ignored_object = object()
    _, actual_attribute_value = stage.dom_object.TryGetAttributeValue(context.stage_attributes['My Stage Length'],
                                                                      ignored_object)
    cf.assert_that_actual_measurement_close_to_expected(onq.as_measurement(units.UsOilfield.LENGTH,
                                                                           option.maybe(actual_attribute_value)),
                                                        length)


# noinspection PyBDDParameters
@step("I see the value of the sequence number attribute for stage, {stage_no:d}, of '{well}' equal to"
      " {global_seq_no:d}")
def step_impl(context, stage_no, well, global_seq_no):
    """
    Args:
        context (behave.runner.Context): The test context.
        stage_no (int): The integer identifying the stage of interest.
        well (str): The well of interest.
        global_seq_no (int): The value of the global stage sequence number attribute.
    """
    stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)

    ignored_object = object()
    _, actual_attribute_value = stage.dom_object.TryGetAttributeValue(
        context.stage_attributes['My Global Stage Sequence Number'], ignored_object)
    assert_that(actual_attribute_value, equal_to(global_seq_no))
