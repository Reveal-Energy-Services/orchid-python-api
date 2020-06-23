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
import numpy as np

from hamcrest import assert_that, has_length


@when('I query the trajectory for well "{well_name}"')
def step_impl(context, well_name):
    """
    :param well_name: Name of the well of interest
    :type context: behave.runner.Context
    """
    actual_wells = list(context.project.wells_by_name(well_name))
    # noinspection PyTypeChecker
    assert_that(actual_wells, has_length(1))
    actual_well = actual_wells[0]
    context.trajectory = actual_well.trajectory


@when('I query the easting and northing arrays in the project reference frame in project units')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.easting_array = context.trajectory.get_easting_array('project')
    context.northing_array = context.trajectory.get_northing_array('project')


@then('I see {count:d} values in each array')
def step_impl(context, count):
    """
    :param count: The number of expected values in the easting and northing arrays
    :type context: behave.runner.Context
    """
    assert_that(context.easting_array, has_length(count))
    assert_that(context.northing_array, has_length(count))


@then('I see correct <easting> and <northing> values for specific points')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected_eastings = np.array([float(r['easting']) for r in context.table])
    expected_northings = np.array([float(r['northing']) for r in context.table])
    sample_indices = np.array([int(i['index']) for i in context.table])
    # Relative tolerance of 0.001 determined empirically. Expected data was rounded to 6 significant figures
    np.testing.assert_allclose(context.easting_array[sample_indices], expected_eastings, rtol=0.001)
    np.testing.assert_allclose(context.northing_array[sample_indices], expected_northings, rtol=0.001)
