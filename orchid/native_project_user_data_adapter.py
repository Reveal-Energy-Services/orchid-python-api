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

import uuid

import deal

from orchid import (
    dot_net_dom_access as dna,
    native_stage_qc_adapter as qca,
)


# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Settings import IProjectUserData


class NativeProjectUserData(dna.DotNetAdapter):
    """Adapts a .NET `IProjectUserData` instance to Python."""
    def __init__(self, adaptee: IProjectUserData):
        super().__init__(adaptee)

    def stage_qc(self, stage_id: uuid.UUID) -> qca.NativeStageQCAdapter:
        """
        Creates a `NativeStageQCAdapter` for the specified stage

        Args:
            stage_id: The object ID of the stage of interest

        Returns:
            The newly created `NativeStageQCAdapter` for the specified stage
        """
        try:
            return qca.NativeStageQCAdapter(stage_id, self.dom_object)
        except deal.PreContractError as pce:
            if pce.message == '`stage_id` must be in project user data':
                return None
            else:
                raise
