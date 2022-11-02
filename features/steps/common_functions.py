#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
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
import warnings

from hamcrest import assert_that, equal_to

import pint
import toolz.curried as toolz

import orchid

# noinspection PyUnresolvedReferences
from tests import (custom_matchers as tcm)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime


def assert_that_actual_measurement_close_to_expected(actual, expected_text, tolerance=None, reason=''):
    expected = parse_measurement(expected_text)

    # Allow error of +/- 1 in last significant figure of expected value.
    expected_magnitude_text = expected_text.split(maxsplit=1)[0]
    tolerance = (decimal.Decimal((0, (1,), decimal.Decimal(expected_magnitude_text).as_tuple()[-1]))
                 if tolerance is None
                 else tolerance)
    tcm.assert_that_measurements_close_to(actual, expected, tolerance=tolerance, reason=reason)


def parse_measurement(measurement_text):
    try:
        result = orchid.unit_registry.Quantity(measurement_text)
    except pint.errors.OffsetUnitCalculusError:
        # Unit most likely temperature
        magnitude_text, unit = measurement_text.split(maxsplit=1)
        result = orchid.unit_registry.Quantity(float(magnitude_text), unit)
    except pint.errors.UndefinedUnitError:
        expected_magnitude_text, expected_unit_text = measurement_text.split(maxsplit=1)
        if expected_unit_text == 'bpm':
            result = orchid.unit_registry.Quantity(f'{expected_magnitude_text} oil_bbl/min')
        else:
            raise
    return result


def assert_that_actual_measurement_magnitude_close_to_expected(actual: float,
                                                               expected_text: str,
                                                               tolerance:  decimal.Decimal = None,
                                                               reason: str = ''):
    expected = parse_measurement(expected_text)

    # Allow error of +/- 1 in last significant figure of expected value.
    expected_magnitude_text = expected_text.split(maxsplit=1)[0]
    tolerance = (decimal.Decimal((0, (1,), decimal.Decimal(expected_magnitude_text).as_tuple()[-1]))
                 if tolerance is None
                 else tolerance)
    tcm.assert_that_measurements_close_to(actual * expected.units, expected, tolerance=tolerance, reason=reason)


def assert_that_net_date_times_are_equal(actual: DateTime, expected: DateTime):
    assert_that(actual, tcm.equal_to_net_date_time(expected))


def find_stage_by_stage_no(context, stage_no, well_of_interest):
    candidate = toolz.pipe(
        context.stages_for_wells[well_of_interest],
        lambda stages: stages.find_by_display_stage_number(stage_no),
    )
    assert_that(candidate is not None,
                f'Failure for field "{context.field}", well "{well_of_interest.name}", and stage_no {stage_no}.')
    return candidate


def find_part_by_part_no_in_stage_no_in_well_of_project(context, part_no, stage_no, well_name):
    """
    Return the part with `part_no` in stage , `stage_no`, in well named, `well_name`, of loaded project.
    Args:
        context: The test context (expected to contain the loaded project)
        part_no (int): The number used by engineers to identify the stage part of interest.
        stage_no (int): The number used by engineers to identify the stage of interest.
        well_name (str): The name used by engineers to identify the well of interest.

    Returns:
        The part with `part_no` in stage , `stage_no`, in well named, `well_name`, of loaded project.
    """
    stage_of_interest = find_stage_by_stage_no_in_well_of_project(context, stage_no, well_name)
    result = stage_of_interest.stage_parts().find_by_part_number(part_no)
    assert result is not None, (f'Expected part number, {part_no}, in stage number, {stage_no},'
                                f' in well named, {well_name}, of loaded project. Found none.')

    return result


def find_stage_by_stage_no_in_well_of_project(context, stage_no, well_name):
    """
    Return the stage number, `stage_no`, in well named, `well_name`, of loaded project.
    Args:
        context: The test context (expected to contain the loaded project)
        stage_no: The number used by engineers to identify the stage of interest.
        well_name: The name used by engineers to identify the well of interest.

    Returns:
        The stage of the well named, `well_name`. If no such stage is present, raises an `AssertionError`.
    """
    well_of_interest = find_well_by_name_in_project(context, well_name)
    result = well_of_interest.stages().find_by_display_stage_number(stage_no)
    assert result is not None, f'Expected stage number, {stage_no}, in well named, {well_name}, of loaded project.' \
                               ' Found none.'

    return result


def find_well_by_name_in_project(context, well_name):
    """
    Return the single well, named `well_name`, of the loaded project.
    Args:
        context: The test context (expected to contain the loaded project).
        well_name: The name of the well of interest.

    Returns:
        The single well named, `well_name`, in the loaded project.

    Raises:
        AssertionError if no such well exists or more than one well exists.
    """
    assert context.project is not None, f'Expected loaded project to be available in `context`. Found none.'
    candidates = list(context.project.wells().find_by_name(well_name))
    assert len(candidates) == 1, f'Found {len(candidates)} wells with name, {well_name}. Expected exactly 1.'

    return candidates[0]


def find_well_by_name_in_stages_for_wells(context, name):
    candidates = toolz.pipe(context.stages_for_wells,
                            toolz.keyfilter(lambda w: w.name == name))
    assert_that(toolz.count(candidates), equal_to(1), f'Failure for field "{context.field}" and well "{name}".')
    result = toolz.nth(0, candidates)
    return result


def find_stage_no_in_well(context, stage_no, well):
    well_of_interest = find_well_by_name_in_stages_for_wells(context, well)
    stage_of_interest = find_stage_by_stage_no(context, stage_no, well_of_interest)
    return stage_of_interest


def find_stage_no_in_well_of_project(context, stage_no, well):
    """
    Find the stage identified by `stage_no` in the well named, `well`, in the project in `context`
    Args:
        context: The test context (containing the project)
        stage_no: The number used by an engineer to identify a stage in a well.
        well: The name of the well of interest.

    Returns:
        The stage identified by `stage_no` in `well` of the project.

    Raises:
        AssertionError: Raised if
        - No such stage exists or more than one stage exists in the well
        - No such well exists or more than one well exists in the project.
    """
    candidate_wells = list(context.project.wells().find_by_name(well))
    assert_that(len(candidate_wells), equal_to(1), f'Failure for field "{context.field}" and well "{well}".')
    well_for_interest = candidate_wells[0]

    result = well_for_interest.stages().find_by_display_stage_number(stage_no)
    return result


def find_data_frames_by_ignore_warnings(context, find_by_func, find_by_value):
    # TODO: Remove catching warnings if we change the integration test data file,
    #  "c:\src\Orchid.IntegrationTestData\05PermianProjectQ3_2022_DataFrames.ifrac"
    #
    # I currently ignore these warnings only for this single project because it is the only project in the
    # integration test data that has duplicate object IDs in data frames. I ignore it because I do not want printing
    # the warning to act as a "false positive" for a developer investigating another issue, seeing this expected
    # warning and wondering (or investigating) the issue.
    with warnings.catch_warnings(record=False):
        if context.project.name == 'PermianProjectQ3_2022':
            warnings.simplefilter("ignore")
        return find_by_func(context.project.data_frames(), find_by_value)
