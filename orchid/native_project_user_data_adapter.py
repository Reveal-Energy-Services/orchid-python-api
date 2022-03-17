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
from typing import Callable, Union
import uuid

import toolz.curried as toolz

from orchid import (
    dot_net_dom_access as dna,
    dot_net_disposable as dnd,
    net_stage_qc as nqc,
)


# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Settings import IProjectUserData, Variant


class NativeProjectUserData(dna.DotNetAdapter):
    """Adapts a .NET `IProjectUserData` instance to Python."""

    # TODO: Add code to `SdkAdapter` to allow handling `GetValue` and .NET `StageCorrectionStatus`
    # Python.NET has a [known issue](https://github.com/pythonnet/pythonnet/issues/1220) with its
    # handling of .NET Enum types. The Python.NET team has repaired this issue; however, the repair
    # is targeted for Python.NET 3. The team has specifically stated that they will *not* backport
    # this fix to the 2.5 version. Because .NET `StageCorrectionStatus` is a .NET `Enum` type, we
    # *cannot* construct a .NET `Variant` of type .NET `StageCorrectionStatus`.
    #
    # Our work-around for this issue is to implement this class in terms of the the JSON available
    # from the `IProjectUserData.ToJson`. This choice further requires hard-coding the logic used
    # by `StartStopTimeEditorViewModel` default `Variant` logic for QC notes and for start stop
    # confirmation.

    def __init__(self, adaptee: IProjectUserData):
        super().__init__(adaptee)

    def stage_qc_notes(self, stage_id: uuid.UUID) -> str:
        """
        Calculate the QC notes for the specified stage.

        Args:
            stage_id: The object ID of the stage of interest.

        Returns:
            The requested QC notes.
        """
        key_func = nqc.make_qc_notes_key
        transform_func = toolz.identity
        default_result = ''

        return self._extract_value_for_stage_id(stage_id, key_func, default_result, transform_func)

    def stage_start_stop_confirmation(self, stage_id: uuid.UUID) -> nqc.StageCorrectionStatus:
        """
        Calculate the start stop confirmation for the specified stage.

        Args:
            stage_id: The object ID of the stage of interest.

        Returns:
            The requested start stop confirmation.
        """
        key_func = nqc.make_start_stop_confirmation_key
        transform_func = nqc.StageCorrectionStatus
        default_result = nqc.StageCorrectionStatus.NEW

        return self._extract_value_for_stage_id(stage_id, key_func, default_result, transform_func)

    def _extract_value_for_stage_id(self,
                                    stage_id: uuid.UUID,
                                    key_func: Callable[[uuid.UUID], str],
                                    default_result: Union[str, nqc.StageCorrectionStatus],
                                    transform_func: Callable[[str], Union[str, nqc.StageCorrectionStatus]]):
        project_user_data_json = json.loads(self.dom_object.ToJson())
        confirmation_key = key_func(stage_id)
        # TODO: Replace hard-coded "copy" of logic
        # Hard-coded logic for QC notes default value from `StartStopTimeEditorViewModel`:
        # return .NET `StageCorrectionStatus.New` if either of stage ID or of start stop
        # confirmation is unavailable.
        result = default_result
        if confirmation_key in project_user_data_json:
            actual_value_type = toolz.get_in([confirmation_key, 'Type'], project_user_data_json)
            assert actual_value_type == 'System.String', (f'Expected, "System.String",'
                                                          f' but found "{actual_value_type}".')
            text_status = toolz.get_in([confirmation_key, 'Value'], project_user_data_json)
            result = transform_func(text_status)
        return result

    def set_stage_qc_notes(self, stage_id, to_notes):
        with dnd.disposable(self.dom_object.ToMutable()) as mutable_pud:
            mutable_pud.SetValue(nqc.make_qc_notes_key(stage_id), Variant.Create.Overloads[str](to_notes))
