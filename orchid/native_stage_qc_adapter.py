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
    native_variant_adapter as nva,
    net_stage_qc as nqc,
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.Common import StageCorrectionStatus as NetStageCorrectionStatus
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Settings import Variant
# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import String


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
        return self._stage_id

    # Originally, I implemented this class to rely on the `NativeStageQCAdapter` class. However, I encountered a
    # problem I was unable to solve. In .NET, an instance of type `Enum` is a class. For classes that do not have an
    # obvious mapping to a Python type, Python.NET exposes them to Python as a wrapper around the .NET class instance
    # having all the methods and properties of the original .NET class (discovered through reflection). However,
    # for .NET `Enum` types, Python .NET appears to "hide" the .NET `Enum` class and instead expose the `Enum` members
    # as integral values. (I assume this solution was adopted *before* addition of the `enum` module to the standard
    # library.)
    #
    # Because the `Enum` class is *not* exposed by Python.NET, it is problematic to access the actual `Enum` type. One
    # can use `Type.GetType`, but for the `StageCorrectionStatus` class, one must specify the fully qualified assembly
    # name. This name includes assembly version information which the author believes to be problematic. (It was not
    # obvious to the author how to ensure calculation of the correct assembly version in a general way.) In addition,
    # one cannot evaluate expressions like `StageCorrectionStatus.NEW.GetType()` since Python understands that
    # `StageCorrectionStatus.NEW` is a (Python!) `int` which has no 'GetType()` method.
    #
    # My work-around is to hard-code references to the .NET `Variant` in this class. This solution is brittle in that
    # it assumes that variants returned from `IProjectUserData` for the key,
    # `<stage-oid>|stage_start_stop_time_confirmation`, will actually have type `StageCorrectionStatus`. I think this
    # assumption is safe, but it is brittle if changes occur in this area in Orchid.
    #
    # See the [Python.NET issue](https://github.com/pythonnet/pythonnet/issues/1220) for details.

    @property
    def start_stop_confirmation(self) -> nqc.StageCorrectionStatus:
        net_result = self.dom_object.GetValue(
            nqc.make_start_stop_confirmation_key(self._stage_id),
            Variant.Create.Overloads[NetStageCorrectionStatus](nqc.StageCorrectionStatus.NEW))
        # The following code fails at run-time with an error like the following. (The text of this error is actually
        # copied from a run of the `scratch.ipynb` Jupyter notebook.
        # >>> ---------------------------------------------------------------------------
        # >>> TypeError                                 Traceback (most recent call last)
        # >>> Input In [67], in <module>
        # >>> ----> 1 default_status_variant = Variant.Create.Overloads[Enum](StageCorrectionStatus.New)
        # >>>       2 default_status_variant.GetValue[StageCorrectionStatus]()
        # >>>
        # >>> TypeError: No method matches given arguments for Create: (<class 'int'>)
        return net_result.GetValue[NetStageCorrectionStatus]()

    @property
    def qc_notes(self):
        net_result = self.dom_object.GetValue(nqc.make_qc_notes_key(self._stage_id),
                                              nva.create_variant('non applicabitis',
                                                                 nva.PythonVariantTypes.STRING).dom_object)
        return nva.NativeVariantAdapter(net_result).value
