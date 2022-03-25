#  Copyright (c) 2017-2022 Reveal Energy Services, Inc 
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

import dataclasses as dc
from collections import namedtuple
from typing import Iterable, Optional

import option
import pendulum as pdt
import toolz.curried as toolz

import orchid.base
from orchid import (
    dot_net_dom_access as dna,
    dom_project_object as dpo,
    searchable_stages as oss,
    measurement as om,
    native_stage_adapter as nsa,
    native_subsurface_point as nsp,
    native_trajectory_adapter as nta,
    net_fracture_diagnostics_factory as fdf,
    net_quantity as onq,
    reference_origins as origins,
    unit_system as units,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell
# noinspection PyUnresolvedReferences
import UnitsNet
# noinspection PyUnresolvedReferences
from System import Array, UInt32

WellHeadLocation = namedtuple('WellHeadLocation',
                              ['easting', 'northing', 'depth'])


_object_factory = fdf.create()


def replace_no_uwi_with_text(uwi):
    return uwi if uwi else 'No UWI'


@dc.dataclass
class CreateStageDto:
    stage_no: int  # Must be greater than 0
    stage_type: nsa.ConnectionType
    md_top: om.Quantity  # Must be length
    md_bottom: om.Quantity  # Must be length
    cluster_count: int = 0  # Must be non-negative
    # WARNING: one need supply neither a start time nor a stop time; however, not supplying this data can
    # produce unexpected behavior for the `global_stage_sequence_number` property. For example, one can
    # generate duplicate values for the `global_stage_sequence_number`. This unexpected behavior is a known
    # issue with Orchid.
    #
    # Note supplying no value (an implicit `None`) results in the largest possible .NET time range.
    maybe_time_range: Optional[pdt.Period] = None
    # WARNING: one **must** currently supply an ISIP for each stage; otherwise, Orchid fails to correctly load
    # the project saved with the added stages.
    maybe_isip: Optional[om.Quantity] = None  # The actual value must be a pressure
    maybe_shmin: Optional[om.Quantity] = None  # If not None, must be pressure

    def __post_init__(self):
        if self.stage_no < 1:
            raise ValueError(f'Expected `stage_no` greater than 0. Found {self.stage_no}')

        if not units.is_length_unit(self.md_top):
            raise ValueError(f'Expected `md_top` to be a length measurement.'
                             f' Found {self.md_top:~P}')

        if not units.is_length_unit(self.md_bottom):
            raise ValueError(f'Expected `md_bottom` to be a length measurement.'
                             f' Found {self.md_bottom:~P}')

        if self.cluster_count < 0:
            raise ValueError(f'Expected `cluster_count` to be non-negative.'
                             f' Found {self.cluster_count}')

        if self.maybe_isip is None:
            raise TypeError(f'Expected `maybe_isip` to be supplied. Found'
                            f' `{self.maybe_isip}`')

        if not units.is_pressure_unit(self.maybe_isip):
            raise ValueError(f'Expected `maybe_isip` to be a pressure measurement.'
                             f' Found {self.maybe_isip:~P}')

        if self.maybe_shmin is not None:
            if not units.is_pressure_unit(self.maybe_shmin):
                raise ValueError(f'Expected `maybe_shmin` to be a pressure measurement.'
                                 f' Found {self.maybe_shmin:~P}')

    @property
    def order_of_completion_on_well(self):
        """Return the order (beginning at zero) in which this stage was completed on its well."""
        return self.stage_no - 1


class NativeWellAdapter(dpo.DomProjectObject):
    """Adapts a native IWell to python."""

    def __init__(self, net_well: IWell):
        """
        Constructs an instance adapting a .NET IWell.

        Args:
            net_well: The .NET well to be adapted.
        """
        super().__init__(net_well, orchid.base.constantly(net_well.Project))

    trajectory = dna.transformed_dom_property('trajectory', 'The trajectory of the adapted .NET well.',
                                              nta.NativeTrajectoryAdapterIdentified)
    uwi = dna.transformed_dom_property('uwi', 'The UWI of the adapted .', replace_no_uwi_with_text)

    # The formation property **does not** check when a `None` value is passed from Orchid.
    # Although it is possible, it is very unlikely to occur from IWell.Formation.
    formation = dna.dom_property('formation', 'The production formation the well is landed')

    @property
    def ground_level_elevation_above_sea_level(self) -> om.Quantity:
        return onq.as_measurement(self.expect_project_units.LENGTH,
                                  option.maybe(self.dom_object.GroundLevelElevationAboveSeaLevel))

    @property
    def kelly_bushing_height_above_ground_level(self) -> om.Quantity:
        return onq.as_measurement(self.expect_project_units.LENGTH,
                                  option.maybe(self.dom_object.KellyBushingHeightAboveGroundLevel))

    @property
    def wellhead_location(self):
        dom_whl = self.dom_object.WellHeadLocation
        result = toolz.pipe(dom_whl,
                            toolz.map(option.maybe),
                            toolz.map(onq.as_measurement(self.expect_project_units.LENGTH)),
                            list, )
        return WellHeadLocation(*result)

    def stages(self) -> oss.SearchableStages:
        """
        Return a `spo.SearchableProjectObjects` instance of all the stages for this project.

        Returns:
            An `spo.SearchableProjectObjects` for all the stages of this project.
        """
        return oss.SearchableStages(nsa.NativeStageAdapter, self.dom_object.Stages.Items)

    def locations_for_md_kb_values(self,
                                   md_kb_values: Iterable[om.Quantity],
                                   well_reference_frame_xy: origins.WellReferenceFrameXy,
                                   depth_origin: origins.DepthDatum) -> Iterable[nsp.SubsurfacePoint]:
        sample_at = Array[UnitsNet.Length](toolz.map(onq.as_net_quantity(self.expect_project_units.LENGTH),
                                                     md_kb_values))
        result = toolz.pipe(
            self.dom_object.GetLocationsForMdKbValues(sample_at, well_reference_frame_xy, depth_origin),
            toolz.map(nsp.make_subsurface_point(self.expect_project_units.LENGTH)),
            list,
        )
        return result

    def add_stage(self, create_stage_dto: CreateStageDto):
        created_stage = self._create_stage(create_stage_dto)

    def create_stage(self, create_stage_dto: CreateStageDto) -> nsa.NativeStageAdapter:
        """
        Create a stage with the using the properties of this class on `well`.

        Although this is a public method, the author intends it to only be called in the implementation of
        the methods, `NativeWellAdapter.add_stage()` and `NativeWellAdapter.add_stages()`.

        Args:
            create_stage_dto: The details to be used to create the stage on this well.

        Returns:
            The newly created stage. Remember that, at this point in time, the specified `well`
            is **unaware** of this newly added stage.
        """
        project_units = self.expect_project_units(f'Expected to find project units for well'
                                                  f' with name={self.name},'
                                                  f' display_name={self.display_name},'
                                                  f' and object_id={self.object - id}')
        net_md_top = onq.as_net_quantity(project_units.LENGTH)
        net_md_bottom = onq.as_net_quantity(project_units.LENGTH)
        net_shmin = onq.as_net_quantity(project_units.PRESSURE)
        net_stage_without_time_range = _object_factory.CreateStage(
            UInt32(create_stage_dto.order_of_completion_on_self),
            create_stage_dto.stage_type,
            create_stage_dto.md_top,
            create_stage_dto.md_bottom, )

        result = None
        return result
