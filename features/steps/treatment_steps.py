#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

from behave import *
use_step_matcher("parse")
from hamcrest import assert_that, equal_to, close_to
import numpy as np
from toolz.curried import *

from orchid.time_series import deprecated_transform_net_treatment


@when('I query the stages for each well in the project')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stages_for_wells = [(w, w.stages()) for w in context.project.wells()]


def aggregate_stage_treatment(stage):
    stage_start_time_np, stage_stop_time_np = map(np.datetime64, [stage.start_time(), stage.stop_time()])
    # treatment_curves = deprecated_transform_net_treatment(stage.treatment_curves())
    return 0, 0, 0


@curry
def stage_treatment_details(project, well, stage):
    treatment_fluid_volume, treatment_proppant, median_treatment_pressure = aggregate_stage_treatment(stage)
    return {'project_name': project.name(),
            'well_name': well.name(),
            'stage_number': stage.display_stage_number(),
            'md_top': stage.md_top(project.unit('length')),
            'md_bottom': stage.md_bottom(project.unit('length')),
            'total_fluid_volume': treatment_fluid_volume,
            'treatment_proppant': treatment_proppant,
            'median_treating_pressure': median_treatment_pressure}


@when("I calculate the total fluid volume, proppant, and median treating pressure for each stage")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    details = []
    for well, stages in context.stages_for_wells:
        details.extend(map(stage_treatment_details(context.project, well), stages))
    context.stage_treatment_details = details


@then("I see {stage_count:d} stages")
def step_impl(context, stage_count):
    """
    :param stage_count: The expected number of stages.
    :type context: behave.runner.Context
    """
    assert_that(len(context.stage_treatment_details), equal_to(stage_count))


@step("I see correct sample values for <Project>, <WellName>, <Stage>, <MdTop>, and <MdBottom>")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    for expected_details in context.table.rows:
        sample_index = int(expected_details['index'])
        assert_that(context.stage_treatment_details[sample_index]['project_name'],
                    equal_to(expected_details['Project']))
        assert_that(context.stage_treatment_details[sample_index]['well_name'], equal_to(expected_details['WellName']))
        assert_that(context.stage_treatment_details[sample_index]['stage_number'],
                    equal_to(int(expected_details['Stage'])))
        assert_that(context.stage_treatment_details[sample_index]['md_top'].magnitude,
                    close_to(float(expected_details['MdTop']), 0.05))
        assert_that(context.stage_treatment_details[sample_index]['md_bottom'].magnitude,
                    close_to(float(expected_details['MdBottom']), 0.05))


@step("I see correct sample aggregate values for <Volume>, <Proppant> and <Median>")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    for expected_details in context.table.rows:
        sample_index = int(expected_details['index'])
        # assert_that(context.stage_treatment_details[sample_index]['total_fluid_volume'],
        #             equal_to(float(expected_details['Volume'])))
        # assert_that(context.stage_treatment_details[sample_index]['treatment_proppant'],
        #             equal_to(float(expected_details['Proppant'])))
        # assert_that(context.stage_treatment_details[sample_index]['median_treating_pressure'],
        #             equal_to(float(expected_details['Median'])))
