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

from collections import namedtuple
import decimal
import math

from hamcrest import assert_that, equal_to
import toolz.curried as toolz

from orchid import (
    measurement as om,
    native_treatment_calculations as calcs,
)

import common_functions as cf


StageAggregates = namedtuple('StageAggregates', ['stage', 'pumped_volume', 'proppant_mass', 'median_treating_pressure'])


@when('I query the stages for each well in the project')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    searchable_wells = context.project.wells()
    context.stages_for_wells = toolz.pipe(
        searchable_wells.all_object_ids(),
        toolz.map(lambda oid: searchable_wells.find_by_object_id(oid)),
        lambda ws: toolz.reduce(
            lambda so_far, update_value: toolz.assoc(so_far, update_value, update_value.stages), ws, {})
    )


@when("I calculate the total pumped volume, proppant mass, and median treating pressure for each stage")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    def calculate_treatment_aggregates(for_stage):
        start_time = for_stage.start_time
        stop_time = for_stage.stop_time
        aggregates = StageAggregates(for_stage, calcs.pumped_fluid_volume(for_stage, start_time, stop_time),
                                     calcs.total_proppant_mass(for_stage, start_time, stop_time),
                                     calcs.median_treating_pressure(for_stage, start_time, stop_time))
        return aggregates

    def calculate_all_treatment_aggregates(for_stages):
        return list(toolz.map(calculate_treatment_aggregates, for_stages))

    result = toolz.valmap(calculate_all_treatment_aggregates, context.stages_for_wells)
    context.aggregates_for_stages_for_wells = result


# noinspection PyBDDParameters
@step("I see correct sample values for {well}, {index:d}, {stage_no:d}, {volume}, {proppant} and {median}")
def step_impl(context, well, index, stage_no, volume, proppant, median):
    """
    Args:
        context (behave.runner.Context):
        well (str): The name of the well whose stages were sampled.
        index (int): The expected index of the sampled stage.
        stage_no (int): The expected displayed stage number of the sampled stage.
        volume (str): A measurement of the expected pumped fluid volume of the sampled stage.
        proppant (str): A measurement of the expected total proppant mass of the sampled stage.
        median (str): A measurement of the expected median treating pressure of the sampled stage.
    """
    @toolz.curry
    def has_well_name(well_name, well_adapter):
        return well_adapter.name == well_name

    @toolz.curry
    def has_stage_no(number, stage_aggregate):
        return stage_aggregate.stage.display_stage_number == number

    aggregates_for_well = toolz.keyfilter(has_well_name(well), context.aggregates_for_stages_for_wells)
    assert len(aggregates_for_well) == 1, f'Expected 1 aggregate for well {well} for field {context.field}.'

    aggregates_for_stages = toolz.pipe(aggregates_for_well.values(),
                                       toolz.first)
    assert len(aggregates_for_stages) > 0, 'Expected at least 1 aggregate for well. Found 0.'
    aggregates_for_stage = toolz.nth(index, aggregates_for_stages)

    assert_that(aggregates_for_stage.stage.display_stage_number, equal_to(stage_no))

    def assert_message(well_name, ndx, quantity_name):
        return f'{well_name} {ndx} {quantity_name}'
    assert_message_quantity_name = toolz.partial(assert_message, well, index)

    assert_expected_measurement(aggregates_for_stage.pumped_volume.measurement,
                                volume,
                                assert_message_quantity_name('pumped volume'))

    assert_expected_measurement(aggregates_for_stage.proppant_mass.measurement,
                                proppant,
                                assert_message_quantity_name('proppant_mass'))

    assert_expected_measurement(aggregates_for_stage.median_treating_pressure.measurement,
                                median,
                                assert_message_quantity_name('median treating pressure'))


def assert_expected_measurement(actual, expected_text, message):
    expected_magnitude_text, expected_units_text = expected_text.split(maxsplit=1)
    expected_magnitude = decimal.Decimal(expected_magnitude_text)
    if not math.isnan(expected_magnitude):
        cf.assert_that_actual_measurement_close_to_expected(actual, expected_text, reason=message)
    else:
        assert_that(math.isnan(actual.magnitude), reason=message)
        expected_units = om.registry.Unit(expected_units_text)
        assert_that(actual.units, equal_to(expected_units), reason=message)
