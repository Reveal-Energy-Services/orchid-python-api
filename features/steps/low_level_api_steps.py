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

from hamcrest import assert_that, equal_to, is_, not_none, is_in
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
# noinspection PyUnresolvedReferences
import UnitsNet
#
#
# # noinspection PyBDDParameters
# @step("I create a stage attribute named '<{attr_name}>' for a(n) <{type_name}> value")
# def step_impl(context, attr_name, type_name):
#     """
#     Args:
#         context (behave.runner.Context): The test context.
#         attr_name (str): The name of the attribute to add.
#         type_name (str): The name of the type of the attribute.
#     """
#     type_name_to_net_type = {
#         'double': Double,
#         'integer': Int32,
#         'length_measurement': UnitsNet.Length,
#         'string': String,
#     }
#     to_add = Attribute[type_name_to_net_type[type_name]].Create(attr_name)
#     assert_that(to_add, is_(not_none()))
#     if 'stage_attributes' not in context:
#         context.stage_attributes = {}
#     context.stage_attributes[attr_name] = to_add
#
#
# # noinspection PyBDDParameters
# @step("I add the created attributes to the well, '{well}', of the project")
# def step_impl(context, well):
#     """
#     Args:
#         context (behave.runner.Context): The test context.
#         well (str): The well of interest.
#     """
#     to_add_to_well = cf.find_well_by_name_in_project(context, well)
#
#     with dnd.disposable(to_add_to_well.dom_object.ToMutable()) as mutable_well:
#         for attribute in context.stage_attributes.values():
#             mutable_well.AddStageAttribute(attribute)
#             assert_that(attribute, is_in(list(to_add_to_well.dom_object.StageAttributes.Items)))
#
#     for attribute_name in context.stage_attributes.keys():
#         candidate_attributes = list(toolz.filter(lambda a: a.Name == attribute_name,
#                                                  to_add_to_well.dom_object.StageAttributes.Items))
#         assert_that(len(candidate_attributes), equal_to(1))
#         # Beware: if one fails to include the `Name` attribute, the test will fail, but because the .NET implementation
#         # of `Attribute.ToString()` prints the name, the failure will seem to report that it expected the name and it
#         # **also** found the name.
#         assert_that(candidate_attributes[0], equal_to(context.stage_attributes[attribute_name]))
#
#
# # noinspection PyBDDParameters
# @step("I set the value of the stage length attribute of stage, {stage_no:d}, of '{well}' to the {length}")
# def step_impl(context, stage_no, well, length):
#     """
#     Args:
#         context (behave.runner.Context): The test context.
#         stage_no (int): The integer identifying the stage of interest.
#         well (str): The well of interest.
#         length (str): The value of the stage length attribute of stage to set.
#     """
#     stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
#     with dnd.disposable(stage.dom_object.ToMutable()) as mutable_stage:
#         expected_length = om.Quantity(length)
#         mutable_stage.SetAttribute(context.stage_attributes['My Stage Length'],
#                                    onq.as_net_quantity(opq.PhysicalQuantity.LENGTH, expected_length))
#
#
# # noinspection PyBDDParameters
# @step("I set the value of the sequence number attribute of stage, {stage_no:d}, of '{well}' to {global_seq_no:d}")
# def step_impl(context, stage_no, well, global_seq_no):
#     """
#     Args:
#         context (behave.runner.Context): The test context.
#         stage_no (int): The integer identifying the stage of interest.
#         well (str): The well of interest.
#         global_seq_no (int): The value of the global stage sequence number attribute.
#     """
#     stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
#     with dnd.disposable(stage.dom_object.ToMutable()) as mutable_stage:
#         mutable_stage.SetAttribute(context.stage_attributes['My Global Stage Sequence Number'], global_seq_no)
#
#
# # noinspection PyBDDParameters
# @then("I see the value of the stage length attribute of stage, {stage_no:d}, of '{well}' equals {length}")
# def step_impl(context, stage_no, well, length):
#     """
#     Args:
#         context (behave.runner.Context): The test context.
#         stage_no (int): The integer identifying the stage of interest.
#         well (str): The well of interest.
#         length (str): The value of the stage length attribute of stage to set.
#     """
#     stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
#     ignored_object = object()
#     _, actual_attribute_value = stage.dom_object.TryGetAttributeValue(context.stage_attributes['My Stage Length'],
#                                                                       ignored_object)
#     cf.assert_that_actual_measurement_close_to_expected(onq.as_measurement(units.UsOilfield.LENGTH,
#                                                                            option.maybe(actual_attribute_value)),
#                                                         length)
#
#
# # noinspection PyBDDParameters
# @step("I see the value of the sequence number attribute for stage, {stage_no:d}, of '{well}' equal to"
#       " {global_seq_no:d}")
# def step_impl(context, stage_no, well, global_seq_no):
#     """
#     Args:
#         context (behave.runner.Context): The test context.
#         stage_no (int): The integer identifying the stage of interest.
#         well (str): The well of interest.
#         global_seq_no (int): The value of the global stage sequence number attribute.
#     """
#     stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
#
#     ignored_object = object()
#     _, actual_attribute_value = stage.dom_object.TryGetAttributeValue(
#         context.stage_attributes['My Global Stage Sequence Number'], ignored_object)
#     assert_that(actual_attribute_value, equal_to(global_seq_no))


def _add_attribute_of_name_and_type_to_well(well, attribute_name, attribute_type):
    type_name_to_net_type = {
        'double': Double,
        'integer': Int32,
        'length': UnitsNet.Length,
        'string': String,
    }
    attribute = Attribute[type_name_to_net_type[attribute_type]].Create(attribute_name)
    assert_that(attribute, is_(not_none()))

    with dnd.disposable(well.dom_object.ToMutable()) as mutable_well:
        mutable_well.AddStageAttribute(attribute)
        assert_that(attribute, is_in(list(well.dom_object.StageAttributes.Items)))


@toolz.curry
def _set_stage_attribute(to_set_attribute, make_attribute_value_func, mutable_stage, attribute_value):
    mutable_stage.SetAttribute(to_set_attribute, make_attribute_value_func(attribute_value))


def _to_length_measurement(value):
    to_set_value = om.Quantity(value)
    onq.as_net_quantity(opq.PhysicalQuantity.LENGTH, to_set_value)


def _well_find_attributes_with_name(well, attribute_name):
    result = list(toolz.filter(lambda a: a.Name == attribute_name, well.dom_object.StageAttributes.Items))
    return result


@when("I add the attribute named '{attribute_name}' of type `{attribute_type}' to well, `{well}', of the project")
def step_impl(context, attribute_name, attribute_type, well):
    """
    Args:
        context (behave.runner.Context): The test context.
        attribute_name (str): The name of the stage attribute to add.
        attribute_type (str): The type of the stage attribute to add
        well (str): The name of the well to which to add the stage attribute.
    """
    to_add_to_well = cf.find_well_by_name_in_project(context, well)
    if len(_well_find_attributes_with_name(to_add_to_well, attribute_name)) == 0:
        _add_attribute_of_name_and_type_to_well(to_add_to_well, attribute_name, attribute_type)
        assert len(_well_find_attributes_with_name(to_add_to_well, attribute_name)) == 1,\
            f'Expected exactly one attribute named {attribute_name} in well, {to_add_to_well.name}'


# noinspection PyBDDParameters
@step("I set the attribute value of '{attribute_name}' of stage, {stage_no:d}, of '{well}' to the {attribute_value}")
def step_impl(context, attribute_name, stage_no, well, attribute_value):
    """
    Args:
        context (behave.runner.Context): The test context.
        attribute_name (str): The name of the stage attribute to set.
        stage_no (int): The number used by engineers to identify stages in a well.
        well (str): The name of the well to which to add the stage attribute.
        attribute_value (str): The value to which to set the stage attribute
    """
    well_with_attributes = cf.find_well_by_name_in_project(context, well)
    candidate_attributes = _well_find_attributes_with_name(well_with_attributes, attribute_name)
    assert len(candidate_attributes) == 1, (f'Expected single attribute of well {well},'
                                            f' but found {len(candidate_attributes)}')
    to_set_attribute = candidate_attributes[0]
    attribute_name_to_set_func = {
        'My Stage Length': _set_stage_attribute(to_set_attribute, _to_length_measurement),
        'My Global Stage Sequence Number': _set_stage_attribute(to_set_attribute, int),
    }

    stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    with dnd.disposable(stage.dom_object.ToMutable()) as mutable_stage:
        attribute_name_to_set_func[attribute_name](mutable_stage, attribute_value)


@then("I see the attribute value of '{attribute_name}' of stage, {stage_no}, of '{well}' equals {attribute_value}")
def step_impl(context, attribute_name, stage_no, well, attribute_value):
    """
    Args:
        context (behave.runner.Context):
        attribute_name (str):
        stage_no (str):
        well (str):
        attribute_value (str):
    """
    raise NotImplementedError(
        u'STEP: Then I see the attribute value of \'<attribute_name>\' of stage, <stage_no>, of \'<well>\' equals <attribute_value>')