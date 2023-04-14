#  Copyright (c) 2017-2023 Reveal Energy Services, Inc
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

from hamcrest import assert_that, equal_to

import common_functions as cf

from orchid import (
    net_stage_qc as nqc,
)


use_step_matcher("parse")


@step("I change the specified stage correction status")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context with the loaded project available via `project`
    """
    # TODO: reduce common code by introducing lambda (last two lines)
    for row in context.table:
        well = row['well']
        stage_no = int(row['stage_no'])
        stage_object_id = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well).object_id
        project_user_data = context.project.user_data

        to_corrected_status = nqc.CorrectionStatus[row['to_correction_status'].upper()]
        project_user_data.set_stage_start_stop_confirmation(stage_object_id, to_corrected_status)

        to_qc_notes = row['to_qc_notes']
        project_user_data.set_stage_qc_notes(stage_object_id, to_qc_notes)


@then("I see the changed stage correction status")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context): The test context with the loaded project available via `project`
    """
    # TODO: reduce common code by introducing lambda (last two lines)
    for row in context.table:
        well = row['well']
        stage_no = int(row['stage_no'])
        stage_object_id = cf.find_stage_by_stage_no_in_well_of_project(context, stage_no, well).object_id
        project_user_data = context.project.user_data

        to_corrected_status = nqc.CorrectionStatus[row['to_correction_status'].upper()]
        assert_that(project_user_data.stage_start_stop_confirmation(stage_object_id), equal_to(to_corrected_status))

        to_qc_notes = row['to_qc_notes']
        assert_that(project_user_data.stage_qc_notes(stage_object_id), equal_to(to_qc_notes))
