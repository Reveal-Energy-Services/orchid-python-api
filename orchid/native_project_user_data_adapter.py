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

import dataclasses
import uuid

from orchid import net_stage_qc as nqc


# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Settings import IProjectUserData


@dataclasses.dataclass
class StageQC:
    stage_start_stop_confirmation: nqc.StageCorrectionStatus


class NativeProjectUserData:
    def __init__(self, net_project_user_data: IProjectUserData):
        pass

    def stage_qc(self):
        return {
            uuid.UUID('f1cfbb26-b492-4079-88ab-5798fcc76134'): StageQC(nqc.StageCorrectionStatus.CONFIRMED),
        }