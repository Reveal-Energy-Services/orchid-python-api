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

import decimal

from hamcrest import assert_that, equal_to
import dateutil.parser

from orchid import (native_treatment_curve_adapter as tca,
                    unit_system as units)

import common_functions as cf


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
    stage_of_interest = cf.find_stage_no_in_well(context, stage_no, well)
    treatment_curves = stage_of_interest.treatment_curves()
    curve_name = {'pressure': tca.TreatmentCurveTypes.TREATING_PRESSURE,
                  'proppant': tca.TreatmentCurveTypes.SURFACE_PROPPANT_CONCENTRATION,
                  'slurry': tca.TreatmentCurveTypes.SLURRY_RATE}[curve_type]
    actual_treatment_curve = treatment_curves[curve_name]
    actual_time_stamp = actual_treatment_curve.time_series().index[index].to_pydatetime()
    expected_time_stamp = dateutil.parser.parse(timestamp)
    assert_that(actual_time_stamp, equal_to(expected_time_stamp))
    actual_time_series_value = actual_treatment_curve.time_series()[index]
    actual_value_magnitude = decimal.Decimal(actual_time_series_value)
    actual_value_unit = actual_treatment_curve.sampled_quantity_unit()
    actual_value = units.make_measurement(actual_value_unit, actual_value_magnitude)
    cf.assert_that_actual_measurement_close_to_expected(actual_value, value)
