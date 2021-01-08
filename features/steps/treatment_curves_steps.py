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

import decimal

from hamcrest import assert_that, equal_to, close_to

from orchid import (native_treatment_curve_adapter as ntc,
                    unit_system as units)

from common_functions import find_stage_no_in_well


# noinspection PyBDDParameters
@then("I see correct curve samples for {well}, {stage_no:d}, {curve_type}, {index:d}, {timestamp}, and {value}")
def step_impl(context, well, stage_no, curve_type, index, timestamp, value):
    """
    Args:
        context (behave.runner.Context): The test context.
        well (str): The name of the well of interest.
        stage_no (int): The displayed stage number of interest.
        curve_type (str): The (predefined) type of curve.
        index (int): The index of the curve sample.
        timestamp (str): The time stamp of the curve sample.
        value (str): The value of the curve sample.
    """
    # TODO: Uncomment the slurry rate and proppant concentration integration tests.
    stage_of_interest = find_stage_no_in_well(context, stage_no, well)
    treatment_curves = stage_of_interest.treatment_curves()
    curve_name = {'pressure': ntc.TreatmentCurveTypes.TREATING_PRESSURE,
                  'proppant': ntc.TreatmentCurveTypes.SURFACE_PROPPANT_CONCENTRATION,
                  'slurry': ntc.TreatmentCurveTypes.SLURRY_RATE}
    actual_treatment_curve = treatment_curves[curve_name[curve_type]]
    actual_value = actual_treatment_curve.time_series()[timestamp]
    same_actual_value = actual_treatment_curve.time_series()[index]
    assert_that(actual_value, equal_to(same_actual_value))
    expected_value_text, raw_expected_unit = value.split(maxsplit=1)
    # Encoding for unicode superscript 3
    expected_unit = raw_expected_unit.replace('^3', '\u00b3')
    assert_that(units.abbreviation(actual_treatment_curve.sampled_quantity_unit()), equal_to(expected_unit))
    expected_value = decimal.Decimal(expected_value_text)
    _, _, expected_exponent = expected_value.as_tuple()
    calculated_max_error = decimal.Decimal((0, (1,), expected_exponent))
    assert_that(decimal.Decimal(actual_value), close_to(expected_value, calculated_max_error))
