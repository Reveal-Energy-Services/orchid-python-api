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

import deal
import numpy as np

import orchid.validation

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import (WellReferenceFrameXy, DepthDatum, IWell)

# noinspection PyUnresolvedReferences
import UnitsNet


class NativeTrajectoryAdapter:
    def __init__(self, native_trajectory):
        self._adaptee = native_trajectory
        self._reference_frame_text_net_map = {'absolute': WellReferenceFrameXy.AbsoluteStatePlane,
                                              'project': WellReferenceFrameXy.Project,
                                              'well_head': WellReferenceFrameXy.WellHead}

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    @deal.pre(lambda _, reference_frame: reference_frame in ['absolute', 'project', 'well_head'])
    def get_easting_array(self, reference_frame: str) -> np.array:
        """
        Calculates the eastings of this trajectory in the specified `reference_frame` measured in `length_units`
        :param reference_frame: The reference from for the easting coordinates. Valid values are 'absolute' (
        absolute state plane), 'project', and 'well_head'.
        """
        net_reference_frame = self._reference_frame_text_net_map[reference_frame]
        project_length_unit = self._adaptee.Well.Project.ProjectUnits.LengthUnit
        raw_eastings = self._adaptee.GetEastingArray(net_reference_frame)
        return np.array([e.As(project_length_unit) for e in raw_eastings])

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    @deal.pre(lambda _, reference_frame: reference_frame in ['absolute', 'project', 'well_head'])
    def get_northing_array(self, reference_frame: str) -> np.array:
        """
        Calculates the northings of this trajectory in the specified `reference_frame` measured in `length_units`
        :param reference_frame: The reference from for the easting coordinates. Valid values are 'absolute' (
        absolute state plane), 'project', and 'well_head'.
        """
        net_reference_frame = self._reference_frame_text_net_map[reference_frame]
        project_length_unit = self._adaptee.Well.Project.ProjectUnits.LengthUnit
        raw_northings = self._adaptee.GetNorthingArray(net_reference_frame)
        return np.array([e.As(project_length_unit) for e in raw_northings])
