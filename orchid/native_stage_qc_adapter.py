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

import deal

from orchid import (
    dot_net_dom_access as dna,
    net_stage_qc as nqc
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Settings import Variant
# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import String


def _project_user_data_contains_stage_id(stage_id, native_project_user_data):
    return (native_project_user_data.Contains(nqc.make_start_stop_confirmation_key(stage_id)) or
            native_project_user_data.Contains(nqc.make_qc_notes_key(stage_id)))


class NativeStageQCAdapter(dna.DotNetAdapter):
    @deal.pre(lambda _, stage_id, adaptee: _project_user_data_contains_stage_id(stage_id, adaptee),
              message='`stage_id` must be in project user data')
    @deal.pre(lambda _, stage_id, _adaptee: stage_id is not None,
              message='`stage_id` is required')
    def __init__(self, stage_id, adaptee):
        super().__init__(adaptee)
        self._stage_id = stage_id

    @property
    def stage_id(self):
        return self._stage_id

    @property
    def start_stop_confirmation(self):
        return None

    @property
    def qc_notes(self):
        return None
