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

"""
Expose constants to the Orchid Python API.

The .NET stage QC "class" implementation depends upon a number of constants. This module exposes those constants to the
Orchid Python API.
"""

import enum
import uuid

import toolz.curried as toolz

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.Common import StageCorrectionStatus as NetStageCorrectionStatus


# The .NET Variant type does not seem to support a "no value" type. In .NET, this idea would typically be
# communicated by a `null` value; however, returning `null` has its own issues.
NOT_AVAILABLE = 'N/A'


class StageCorrectionStatus(enum.Enum):
    CONFIRMED = NetStageCorrectionStatus.Confirmed
    NEW = NetStageCorrectionStatus.New
    UNCONFIRMED = NetStageCorrectionStatus.Unconfirmed


class StageQCTags(enum.Enum):
    QC_NOTES = 'stage_qc_notes'
    START_STOP_CONFIRMATION = 'stage_start_stop_confirmation'


def make_key(stage_id: uuid.UUID, tag: StageQCTags) -> str:
    return f'{str(stage_id)}|{tag.value}'


make_start_stop_confirmation_key = toolz.flip(make_key)(StageQCTags.START_STOP_CONFIRMATION)
make_qc_notes_key = toolz.flip(make_key)(StageQCTags.QC_NOTES)
