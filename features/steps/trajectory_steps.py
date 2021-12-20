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

from behave import *
use_step_matcher("parse")

import toolz.curried as toolz
import numpy as np

from hamcrest import assert_that, has_length, close_to

from orchid import (
    measurement as om,
    reference_origins as origins,
)

import common_functions as cf


@when('I query the trajectory for well "{well}"')
def step_impl(context, well):
    """
    :param well: Name of the well of interest
    :type context: behave.runner.Context
    """
    # Remember the `well` to correctly calculate the delta for `close_to` in trajectory step
    context.well = well
    actual_wells = list(context.project.wells().find_by_name(well))
    # noinspection PyTypeChecker
    assert_that(actual_wells, has_length(1))
    actual_well = actual_wells[0]
    context.trajectory = actual_well.trajectory


@then('I see {count:d} values in each array')
def step_impl(context, count):
    """
    :param count: The number of expected values in the easting and northing arrays
    :type context: behave.runner.Context
    """
    assert_that(context.easting_array, has_length(count))
    assert_that(context.northing_array, has_length(count))


def close_to_delta(well_to_test):
    """
    Calculate the delta value to be used in a `close_to` comparison of trajectory points.
    :param well_to_test: The name of the well used to calculate the appropriate delta.
    :return: The value to be used as the third argument to `close_to` based on the well name.
    """
    def is_bakken_well(to_test):
        return to_test in set(toolz.map(lambda d: f'Demo_{d}H', [1, 2, 3, 4]))

    def is_permian_well(to_test):
        return to_test in set(toolz.map(lambda d: f'C{d}', [1, 2, 3])).union(['P1'])

    def is_montney_well(to_test):
        return to_test in set(toolz.map(lambda d: f'Hori_0{d}', [1, 2, 3])).union(['Vert_01'])

    result = 0.0
    # Delta of magnitude 6 accounts for half-even rounding
    if is_bakken_well(well_to_test):
        result = 6e-1
    elif is_permian_well(well_to_test):
        result = 6e-3
    elif is_montney_well(well_to_test):
        result = 6e-4
    return result


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


@step("I query the easting, northing, and TVDSS arrays in the project reference frame in project units")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    context.easting_array = context.trajectory.get_easting_array(origins.WellReferenceFrameXy.PROJECT)
    context.northing_array = context.trajectory.get_northing_array(origins.WellReferenceFrameXy.PROJECT)
    context.tvd_ss_array = context.trajectory.get_tvd_ss_array()


# noinspection PyBDDParameters
@then("I see correct {easting}, {northing}, and {tvdss} values at {index:d}")
def step_impl(context, easting, northing, tvdss, index):
    """
    Args:
        context (behave.runner.Context): The test context.
        easting (str): The trajectory item easting.
        northing (str): The trajectory item northing.
        tvdss (str): The trajectory item TVDSS.
        index (int): The index of the trajectory item.
    """
    cf.assert_that_actual_measurement_magnitude_close_to_expected(context.easting_array[index], easting)
    cf.assert_that_actual_measurement_magnitude_close_to_expected(context.northing_array[index], northing)
    cf.assert_that_actual_measurement_magnitude_close_to_expected(context.tvd_ss_array[index], tvdss)


@step("I query the inclination and azimuth arrays and the MDKB arrays in the project reference frame in project units")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context.
    """
    context.inclination_array = context.trajectory.get_inclination_array()
    context.azimuth_array = context.trajectory.get_azimuth_east_of_north_array()
    context.mdb_kb_array = context.trajectory.get_mk_kb_array()


# noinspection PyBDDParameters
@then("I see correct {inclination}, {azimuth}, and {mdkb} values at {index:d}")
def step_impl(context, inclination, azimuth, mdkb, index):
    """
    Args:
        context (behave.runner.Context): The test context.
        inclination (str): The trajectory item inclination.
        azimuth (str): The trajectory item azimuth.
        mdkb (str): The trajectory item TVDSS.
        index (int): The index of the trajectory item.
    """
    cf.assert_that_actual_measurement_magnitude_close_to_expected(context.inclination_array[index], inclination)
    cf.assert_that_actual_measurement_magnitude_close_to_expected(context.azimuth_array[index], azimuth)
    cf.assert_that_actual_measurement_magnitude_close_to_expected(context.md_kb_array[index], mdkb)
