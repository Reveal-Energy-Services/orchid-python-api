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

from behave import *
use_step_matcher("parse")
from hamcrest import assert_that, equal_to, close_to
import numpy as np
from scipy import integrate
import toolz.curried as toolz

import orchid.measurement as om
import orchid.native_treatment_curve_facade as ontc


@when('I query the stages for each well in the project')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stages_for_wells = [(w, w.stages) for w in context.project.wells]


# noinspection PyProtectedMember
def aggregate_stage_treatment(stage):
    stage_start_time = np.datetime64(stage.start_time)
    stage_end_time = np.datetime64(stage.stop_time)

    treatment_curves = stage.treatment_curves()
    pressure = treatment_curves[ontc.TREATING_PRESSURE].time_series()
    pressure.name = 'Treating Pressure'
    rate = treatment_curves[ontc.SLURRY_RATE].time_series()
    rate.name = 'Slurry Rate'
    concentration = treatment_curves[ontc.PROPPANT_CONCENTRATION].time_series()
    concentration.name = 'Proppant Concentration'

    def slurry_rate_per_min_to_per_second_conversion_factor():
        source_slurry_rate_unit = treatment_curves['Slurry Rate'].sampled_quantity_unit()
        target_slurry_rate_unit = f'{om.slurry_rate_volume_unit(source_slurry_rate_unit)}/s'
        local_result = om.get_conversion_factor(source_slurry_rate_unit, target_slurry_rate_unit)
        return local_result

    def slurry_rate_bbl_per_second_to_gal_per_second_conversion_factor():
        local_result = om.get_conversion_factor('bbl/s', 'gal/s')
        return local_result

    stage_rate = rate[stage_start_time:stage_end_time] * slurry_rate_per_min_to_per_second_conversion_factor()
    stage_fluid = integrate.trapz(stage_rate.values, (stage_rate.index - stage_start_time).seconds)

    stage_concentration = concentration[stage_start_time:stage_end_time]
    stage_proppant_rate = (stage_rate * slurry_rate_bbl_per_second_to_gal_per_second_conversion_factor() *
                           stage_concentration)
    stage_proppant = integrate.trapz(stage_proppant_rate.values, (stage_proppant_rate.index - stage_start_time).seconds)

    median_pressure = pressure[stage_start_time:stage_end_time].median()

    return stage_fluid, stage_proppant, median_pressure


@toolz.curry
def stage_treatment_details(project, well, stage):
    treatment_fluid_volume, treatment_proppant, median_treatment_pressure = aggregate_stage_treatment(stage)
    # TODO: Remove 'project_name' since it is no longer needed for subsequent tests
    return {'project_name': project.name,
            'well_name': well.name,
            'stage_number': stage.display_stage_number,
            'md_top': stage.md_top(project.unit('length')),
            'md_bottom': stage.md_bottom(project.unit('length')),
            'volume': treatment_fluid_volume,
            'proppant': treatment_proppant,
            'median': median_treatment_pressure}


def has_single_stage(well_stage_pair):
    # Since stages, the second argument to this function, is actually a map, once it is completely iterated,
    # it no longer produces items. This behavior is one of the breaking changes introduced in Python 3. (See
    # https://stackoverflow.com/questions/21715268/list-returned-by-map-function-disappears-after-one-use#:~:text=In%20Python%203%2C%20map%20returns,as%20though%20it%20were%20empty.&text=If%20you%20need%20to%20use,list%20instead%20of%20an%20iterator.)
    # Since an iterator *does not* support `len`, I must use the following code to determine if I have a
    # single stage.
    well, _ = well_stage_pair
    return toolz.count(well.stages) == 1


@when("I calculate the total fluid volume, proppant, and median treating pressure for each stage")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    details = []
    # The filter in the following code is based on a heuristic for
    for well, stages in toolz.filter(toolz.complement(has_single_stage), context.stages_for_wells):
        details.extend(map(stage_treatment_details(context.project, well), stages))
    context.stage_treatment_details = details


@then("I see {stage_count:d} stages for the project")
def step_impl(context, stage_count):
    """
    :param stage_count: The expected number of stages.
    :type context: behave.runner.Context
    """
    assert_that(len(context.stage_treatment_details), equal_to(stage_count))


# noinspection PyBDDParameters
@step("I see correct sample values for {index:d}, {well}, {stage:d}, {md_top:g}, and {md_bottom:g}")
def step_impl(context, index, well, stage, md_top, md_bottom):
    """
    Args:
        context (behave.runner.Context): Test context
        index (int): The index of the expected details
        well (str): The name of the well for the stage
        stage (int): The stage of interest
        md_top (float): The measured depth of the stage top
        md_bottom (float): The measured depth of the stage bottom
    """
    assert_that(context.stage_treatment_details[index]['well_name'], equal_to(well))
    assert_that(int(context.stage_treatment_details[index]['stage_number']), equal_to(stage))
    assert_that(context.stage_treatment_details[index]['md_top'].magnitude, close_to(float(md_top), 0.05))
    assert_that(context.stage_treatment_details[index]['md_bottom'].magnitude, close_to(float(md_bottom), 0.05))


# noinspection PyBDDParameters
@step("I see correct sample aggregate values for {index:d}, {volume:g}, {proppant:g} and {median:g}")
def step_impl(context, index, volume, proppant, median):
    """
    Args:
        context (behave.runner.Context): Test context
        index (int): The index of the expected details
        volume (float): The total volume of fluid pumped stage treatment
        proppant (float): The total quantity of proppant injected during stage treatment
        median (float0: The median treating pressure during stage treatment
    """
    # tolerances of 0.006 and 0.6 address "round half to even" of expected values
    assert_that(context.stage_treatment_details[index]['volume'], close_to(float(volume), 0.006))
    assert_that(context.stage_treatment_details[index]['proppant'], close_to(float(proppant), 0.6))
    assert_that(context.stage_treatment_details[index]['median'], close_to(float(median), 0.006))
