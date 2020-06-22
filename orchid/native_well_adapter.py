#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

from typing import Iterable

# noinspection PyUnresolvedReferences
import orchid
import orchid.dot_net as odn
import orchid.native_stage_adapter as nsa
import orchid.native_trajectory_adapter as nta

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell


def replace_no_uwi_with_text(uwi):
    return uwi if uwi else 'No UWI'


class NativeWellAdapter:
    """Adapts a native IWell to python."""
    def __init__(self, native_well: IWell):
        """
        Constructs an instance adapting a .NET IWell.
        :param native_well: The .NET well to be adapted.
        """
        self._adaptee = native_well

    name = odn.dom_property('name', 'The name of the adapted .NET well.')
    display_name = odn.dom_property('display_name', 'The display name of the adapted .NET well.')
    trajectory = odn.transformed_dom_property('trajectory', 'The trajectory of the adapted .NET well.',
                                              nta.NativeTrajectoryAdapter)
    uwi = odn.transformed_dom_property('uwi', 'The UWI of the adapted .', replace_no_uwi_with_text)

    def stages(self) -> Iterable[nsa.NativeStageAdapter]:
        """
        Return an iterator of NativeStageAdapters
        :return: An iterator over the NativeStageAdapters.
        """
        return map(nsa.NativeStageAdapter, self._adaptee.Stages.Items)

    # def trajectory(self) -> nta.NativeTrajectoryAdapter:
    #     """
    #     Returns the trajectory of the adapted IWell
    #     :return: The trajectory of the adapted .NET well.
    #     """
    #     return nta.NativeTrajectoryAdapter(self._adaptee.Trajectory)
