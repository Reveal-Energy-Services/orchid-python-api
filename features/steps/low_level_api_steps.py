#  Copyright (c) 2017-2025 KAPPA
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
    net_fracture_diagnostics_factory as net_factory
)

import common_functions as cf

# noinspection PyUnresolvedReferences
from System import Double, Int32, String
# noinspection PyUnresolvedReferences
import UnitsNet

object_factory = net_factory.create()

def _add_attribute_of_name_and_type_to_well(well, attribute_name, attribute_type):
    type_name_to_net_type = {
        'double': Double,
        'integer': Int32,
        'length': UnitsNet.Length,
        'string': String,
    }

    if attribute_type == 'double':
        default = 0.0
    elif attribute_type == 'integer':
        default = -1
    elif attribute_type == 'length':
        default = UnitsNet.Length.FromFeet(UnitsNet.QuantityValue.op_Implicit(0.0))
    else:
        default = ''

    attribute = object_factory.CreateAttribute[type_name_to_net_type[attribute_type]](attribute_name, default)
    assert_that(attribute, is_(not_none()))

    with dnd.disposable(well.dom_object.ToMutable()) as mutable_well:
        mutable_well.AddStageAttribute(attribute)
        assert_that(attribute, is_in(list(well.dom_object.StageAttributes.Items)))


@toolz.curry
def _set_stage_attribute(to_set_attribute, make_attribute_value_func, mutable_stage, attribute_value):
    mutable_stage.SetAttribute(to_set_attribute, make_attribute_value_func(attribute_value))


def _to_length_measurement(value):
    to_set_value = om.Quantity(value)
    result = onq.as_net_quantity(opq.PhysicalQuantity.LENGTH, to_set_value)
    return result


def _to_length_unit(value):
    length_measurement = om.Quantity(value)
    if length_measurement.units == om.registry('ft'):
        return units.UsOilfield.LENGTH
    elif length_measurement.units == om.registry('m'):
        return units.Metric.LENGTH


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
@step("I set the attribute value of '{attribute_name}' of stage, {stage_no:d}, of '{well}' to {attribute_value}")
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

    # This expression seems superfluous. I'm a little unclear myself.
    # Here's my working hypothesis. The function, `_set_stage_attribute`,
    # is passed an actual second argument named,
    # `make_attribute_value_func`, that is of type, `Callable`.
    # `_set_stage_attribute` calls `make_attribute_value_func` with the
    # argument `actual_attribute`. The actual value of this argument is
    # supplied by a `behave` example and is of type `str`. If
    # `make_attribute_value_func == int`, the `str` value is converted,
    # but to a **Python** `int`. The attribute; however, expects a value of
    # type, `System.Int32`, so it throws an exception.
    #
    # My first change was to supply the value, `Int32.Parse`, as the actual
    # value of the `make_attribute_value_func` argument. This function will
    # convert a `str` value to a value of type, `System.Int32`. My hypothesis
    # is that the call to the method, `SetAttribute`, because it is made
    # through Python.NET, results in converting the `Int32` value to a
    # Python `int` again raising the exception.
    #
    # Consequently, the implementation of `str_to_net_int32` has this
    # unusual implementation of converting a `str` to a Python `int` (by
    # calling `int`) and then invoking `Int32` to convert the Python `int`
    # to a .NET `System.Int32`. I'm unclear why this result appears to be
    # passed **unchanged** to the method `SetAttribute`.
    str_to_net_int32 = toolz.compose(Int32, int)

    attribute_name_to_set_func = {
        'My Stage Length': _set_stage_attribute(to_set_attribute, _to_length_measurement),
        'My Global Stage Sequence Number': _set_stage_attribute(to_set_attribute, str_to_net_int32),
    }

    stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    with dnd.disposable(stage.dom_object.ToMutable()) as mutable_stage:
        attribute_name_to_set_func[attribute_name](mutable_stage, attribute_value)


# noinspection PyBDDParameters
@then("I see the attribute value of '{attribute_name}' of stage, {stage_no:d}, of '{well}' equals {attribute_value}")
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
    to_query_attribute = candidate_attributes[0]

    stage = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well)
    ignored_object = object()
    is_attribute_present, actual_attribute_value = stage.dom_object.TryGetAttributeValue(to_query_attribute,
                                                                                         ignored_object)
    assert_that(is_attribute_present, equal_to(True))

    if attribute_name == 'My Stage Length':
        cf.assert_that_actual_measurement_close_to_expected(onq.as_measurement(_to_length_unit(attribute_value),
                                                                               option.maybe(actual_attribute_value)),
                                                            attribute_value)
    elif attribute_name == 'My Global Stage Sequence Number':
        assert_that(actual_attribute_value, equal_to(int(attribute_value)))
    else:
        raise NotImplementedError(f'Unexpected attribute_name "{attribute_name}".')
