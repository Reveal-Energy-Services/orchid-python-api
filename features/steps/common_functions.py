#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


import decimal

from hamcrest import assert_that, equal_to, close_to

import toolz.curried as toolz

from orchid import (unit_system as units)


def assert_measurement_close_to(actual, expected):
    expected_magnitude_text, expected_unit = expected.split()
    expected_magnitude = decimal.Decimal(expected_magnitude_text)
    magnitude_tolerance = decimal.Decimal((0, (6,), expected_magnitude.as_tuple()[-1] - 1))
    assert_that(decimal.Decimal(actual.magnitude), close_to(expected_magnitude, magnitude_tolerance))
    assert_that(units.abbreviation(actual.unit), equal_to(expected_unit))


@toolz.curry
def has_well_name(well_name, candidate_well):
    return candidate_well.name == well_name


def find_well_by_name_in_project(context, name):
    candidates = toolz.pipe(context.project.wells,
                            toolz.filter(has_well_name(name)),
                            list)
    assert_that(toolz.count(candidates), equal_to(1), f'Failure for field "{context.field}" and well "{name}".')
    result = toolz.first(candidates)
    return result


def find_well_by_name_in_stages_for_wells(context, name):
    candidates = toolz.pipe(context.stages_for_wells,
                            toolz.keyfilter(has_well_name(name)))
    assert_that(toolz.count(candidates), equal_to(1), f'Failure for field "{context.field}" and well "{name}".')
    result = toolz.nth(0, candidates)
    return result


def find_stage_by_stage_no(context, stage_no, well_of_interest):
    @toolz.curry
    def has_stage_no(displayed_stage_no, candidate_stage):
        return candidate_stage.display_stage_number == displayed_stage_no

    candidates = toolz.pipe(context.stages_for_wells[well_of_interest],
                            toolz.filter(has_stage_no(stage_no)),
                            list)
    assert_that(toolz.count(candidates), equal_to(1),
                f'Failure for field "{context.field}", well "{well_of_interest.name}", and stage_no {stage_no}.')
    result = toolz.nth(0, candidates)
    return result


def find_stage_no_in_well(context, stage_no, well):
    well_of_interest = find_well_by_name_in_stages_for_wells(context, well)
    stage_of_interest = find_stage_by_stage_no(context, stage_no, well_of_interest)
    return stage_of_interest
