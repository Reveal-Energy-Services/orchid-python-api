#  Copyright 2017-2020 Reveal Energy Services, Inc 
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

import toolz.curried as toolz

import orchid.native_treatment_calculations as calcs

StageAggregates = namedtuple('StageAggregates', ['stage', 'pumped_volume', 'proppant_mass', 'median_treating_pressure'])


@when('I query the stages for each well in the project')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stages_for_wells = {w: list(w.stages) for w in context.project.wells}


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
@step("I see correct sample values for {well}, {index:d}, {stage:d}, {volume}, {proppant} and {median}")
def step_impl(context, well, index, stage, volume, proppant, median):
    """
    Args:
        context (behave.runner.Context):
        well (str): The name of the well whose stages were sampled.
        index (int): The expected index of the sampled stage.
        stage (int): The expected displayed stage number of the sampled stage.
        volume (str): A measurement of the expected pumped fluid volume of the sampled stage.
        proppant (str): A measurement of the expected total proppant mass of the sampled stage.
        median (str): A measurement of the expected median treating pressure of the sampled stage.
    """
    aggregates_for_well = toolz.keyfilter(lambda w: w.name == well, context.aggregates_for_stages_for_wells)
    assert(len(aggregates_for_well) == 1)
