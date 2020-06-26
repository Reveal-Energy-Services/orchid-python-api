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
import pandas as pd
from scipy import integrate
import toolz.curried as toolz

import orchid.time_series


@when('I query the stages for each well in the project')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stages_for_wells = [(w, w.stages) for w in context.project.wells]


# noinspection PyProtectedMember
def aggregate_stage_treatment(stage):
    stage_start_time = np.datetime64(orchid.time_series._as_datetime(stage._adaptee.StartTime))
    stage_end_time = np.datetime64(orchid.time_series._as_datetime(stage._adaptee.StopTime))

    treatment_curves_df = orchid.time_series.deprecated_transform_net_treatment(stage._adaptee.TreatmentCurves.Items)

    time_base = np.timedelta64(1, 's')
    nrows = treatment_curves_df.shape[0];

    # print(f'{stage.Well.Name}-{stage.DisplayStageNumber}')

    d = {
        't': treatment_curves_df.index.values,
        'dt': (treatment_curves_df.index.values - stage_start_time) / np.timedelta64(1, 's'),
        'p': treatment_curves_df['Treating Pressure'],
        'r': treatment_curves_df['Slurry Rate'] / 60.0,
        'c': (42 * treatment_curves_df['Slurry Rate'] / 60.0) * treatment_curves_df['Proppant Concentration'],
    }
    df = pd.DataFrame(data=d)
    df = df[(df['t'] >= stage_start_time) & (df['t'] <= stage_end_time)]
    result = df.iloc[:, 2:].apply(lambda x: integrate.trapz(x, df['dt']))
    if stage._adaptee.DisplayStageNumber == 1:
        print(f'Stage: {stage._adaptee.DisplayStageNumber}')
        print(f'  Duration: ({stage_start_time}, {stage_end_time}), '
              f'Sample count: {len(df)}, Fluid volume: {result.r}')

    return result.r, result.c, df['p'].median()


@toolz.curry
def stage_treatment_details(project, well, stage):
    treatment_fluid_volume, treatment_proppant, median_treatment_pressure = aggregate_stage_treatment(stage)
    return {'project_name': project.name,
            'well_name': well.name,
            'stage_number': stage.display_stage_number,
            'md_top': stage.md_top(project.unit('length')),
            'md_bottom': stage.md_bottom(project.unit('length')),
            'total_fluid_volume': treatment_fluid_volume,
            'treatment_proppant': treatment_proppant,
            'median_treating_pressure': median_treatment_pressure}


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
        # tolerance 0.006 addresses half-even rounding of expected values
        assert_that(context.stage_treatment_details[sample_index]['total_fluid_volume'],
                    close_to(float(expected_details['Volume']), 0.006))
        # assert_that(context.stage_treatment_details[sample_index]['treatment_proppant'],
        #             equal_to(float(expected_details['Proppant'])))
        # assert_that(context.stage_treatment_details[sample_index]['median_treating_pressure'],
        #             equal_to(float(expected_details['Median'])))
