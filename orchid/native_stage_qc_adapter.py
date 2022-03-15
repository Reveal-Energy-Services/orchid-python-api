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

import json

import deal
import toolz.curried as toolz

from orchid import (
    dot_net_dom_access as dna,
    net_stage_qc as nqc,
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.Common import StageCorrectionStatus as NetStageCorrectionStatus


def _project_user_data_contains_stage_id(stage_id, native_project_user_data):
    return (native_project_user_data.Contains(nqc.make_start_stop_confirmation_key(stage_id)) or
            native_project_user_data.Contains(nqc.make_qc_notes_key(stage_id)))


class NativeStageQCAdapter(dna.DotNetAdapter):
    """
    This class adapts the .NET IProjectUserData instance to synthesize a stage QC class.

    Note that the DOM *does not* contain a stage QC class because this class is *not* considered part of the domain,
    but, instead, is considered part of the ImageFRAC workflow.

    Despite this intention, our customer has asked for access to this information for their business purposes.
    """

    @deal.pre(lambda _, stage_id, adaptee: _project_user_data_contains_stage_id(stage_id, adaptee),
              message='`stage_id` must be in project user data')
    @deal.pre(lambda _, stage_id, _adaptee: stage_id is not None,
              message='`stage_id` is required')
    def __init__(self, stage_id, adaptee):
        super().__init__(adaptee)
        self._stage_id = stage_id

    @property
    def stage_id(self):
        """
        Determines the object ID that identifies the stage of interest.

        Returns:
            Returns the object ID for this instance.
        """
        return self._stage_id

    @property
    def start_stop_confirmation(self) -> nqc.StageCorrectionStatus:
        """
        Calculate the stage start stop confirmation of the stage of interest.

        Returns:
            The `StageCorrectionStatus` for the stage of interest.
        """
        project_user_data_json = self.dom_object.ToJson()
        user_data_json = json.loads(project_user_data_json)
        try:
            start_stop_confirmation_json = toolz.get(nqc.make_start_stop_confirmation_key(self._stage_id),
                                                     user_data_json)
            assert start_stop_confirmation_json['Type'] == 'System.String', (f'Expected start stop confirmation'
                                                                             f' for stage, {self._stage_id},'
                                                                             f' of type string.'
                                                                             f' Found {start_stop_confirmation_json}')

            start_stop_confirmation_json_value = start_stop_confirmation_json['Value']
            return nqc.StageCorrectionStatus(start_stop_confirmation_json_value )
        except KeyError:
            return None

    @property
    def qc_notes(self):
        project_user_data_json = self.dom_object.ToJson()
        user_data_json = json.loads(project_user_data_json)
        try:
            qc_notes_json = toolz.get(nqc.make_qc_notes_key(self._stage_id), user_data_json)
            assert qc_notes_json['Type'] == 'System.String', (f'Expected QC notes for stage, {self._stage_id},'
                                                              f' of type string. Found {qc_notes_json}')

            return qc_notes_json['Value']
        except KeyError:
            return ''


