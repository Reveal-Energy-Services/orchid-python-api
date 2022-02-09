#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import argparse
import dataclasses as dc
import logging
import pathlib
from typing import Optional

import orchid
from orchid import (
    native_stage_adapter as nsa,
    native_well_adapter as nwa,
    net_quantity as onq,
    measurement as om,
    unit_system as units,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Factories import FractureDiagnosticsFactory
# noinspection PyUnresolvedReferences
from System import UInt32, Nullable
# noinspection PyUnresolvedReferences
from UnitsNet import Pressure


object_factory = FractureDiagnosticsFactory.Create()


@dc.dataclass(frozen=True)
class CreateStageDto:
    order_of_completion_on_well: int  # Must be non-negative
    connection_type: nsa.ConnectionType
    md_top: om.Quantity  # Must be length
    md_bottom: om.Quantity  # Must be length
    maybe_shmin: Optional[om.Quantity] = None  # If not None, must be pressure
    cluster_count: int = 0  # Must be non-negative

    def __post_init__(self):
        # See the
        # [StackOverflow post](https://stackoverflow.com/questions/54488765/validating-input-when-mutating-a-dataclass)
        assert self.order_of_completion_on_well >= 0, f'order_of_completion_on_well must be non-zero'
        assert self.md_top.check('[length]'), f'md_top must be a length'
        assert self.md_bottom.check('[length]'), f'md_bottom must be a length'
        if self.maybe_shmin is not None:
            assert self.maybe_shmin.check('[pressure]'), f'maybe_shmin must be a pressure if not `None`'
        assert self.cluster_count >= 0, f'cluster_count must be non-zero'


def create_stage(stage_dto: CreateStageDto, well: nwa.NativeWellAdapter):
    # Must supply the unit system for conversions
    native_md_top = onq.as_net_quantity(units.UsOilfield.LENGTH, stage_dto.md_top)
    native_md_bottom = onq.as_net_quantity(units.UsOilfield.LENGTH, stage_dto.md_bottom)
    native_shmin = (onq.as_net_quantity(units.UsOilfield.PRESSURE, stage_dto.maybe_shmin)
                    if stage_dto.maybe_shmin is not None
                    else None)
    native_stage = object_factory.CreateStage(UInt32(stage_dto.order_of_completion_on_well),
                                              well.dom_object,
                                              stage_dto.connection_type.value,
                                              native_md_top,
                                              native_md_bottom,
                                              native_shmin,
                                              UInt32(stage_dto.cluster_count))
    return nsa.NativeStageAdapter(native_stage)


def append_stages(project):
    # Find well to which to add stages
    candidate_well_name = 'Demo_4H'
    candidate_wells = list(project.wells().find_by_display_name(candidate_well_name))
    assert len(candidate_wells) == 1, (f'Expected single well named "{candidate_well_name}".'
                                       f' Found {len(candidate_wells)}.')
    target_well = candidate_wells[0]

    # Create an iterable of stages to append
    stages_to_append = [
        CreateStageDto(
            35,  # hard-coded to be one greater than largest `order_of_completion_on_well`
            nsa.ConnectionType.PLUG_AND_PERF,
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12603.3),
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12750.5)),
        CreateStageDto(
            36,
            nsa.ConnectionType.PLUG_AND_PERF,
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12396.8),
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12556.9),
            maybe_shmin=orchid.make_measurement(orchid.unit_system.UsOilfield.PRESSURE, 2.322)
        ),
        CreateStageDto(
            37,
            nsa.ConnectionType.PLUG_AND_PERF,
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12396.8),
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12556.9),
            cluster_count=7
        ),
    ]
    for stage_dto in stages_to_append:
        created_stage = create_stage(stage_dto, target_well)
        print(created_stage.name, created_stage.shmin if created_stage.shmin else 'None', created_stage.cluster_count)


def main(cli_args):
    """
    Add stages to an existing project and save changes back to disk.

    Args:
        cli_args: The command line arguments from `argparse.ArgumentParser`.
    """
    logging.basicConfig(level=logging.INFO)

    # Read Orchid project
    project = orchid.load_project(cli_args.input_project)

    append_stages(project)

    # Save project changes to specified .ifrac file
    target_path_name = cli_args.output_project
    orchid.save_project(project, target_path_name)
    if cli_args.verbosity >= 1:
        logging.info(f'Wrote changes to "{target_path_name}"')


def make_project_path_name(project_dir_name, project_file_name):
    """
    Make a path name to a project.

    Args:
        project_dir_name: The directory name of the project.
        project_file_name: The file name of the project.

    Returns:
        The path name to the .ifrac file for this project.
    """
    return str(project_dir_name.joinpath(project_file_name))


def make_target_file_name_from_source(source_file_name):
    """
    Make a file name for the changed project file name from the original project file name.

    Args:
        source_file_name: The file name of the project originally read.

    Returns:
        The project file name with a `.996` suffix inserted before the `.ifrac` suffix.
    """
    return ''.join([source_file_name.stem, '.996', source_file_name.suffix])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automatically pick leak off observations.")
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2], default=0,
                        help='Increase output verbosity. (Default: 0; that is, least output.)')

    parser.add_argument('input_project', help=f'Path name of project to read.')

    default_file_name_to_read = pathlib.Path('frankNstein_Bakken_UTM13_FEET.ifrac')
    default_project_path_name_to_read = make_project_path_name(orchid.training_data_path(),
                                                               default_file_name_to_read)
    default_file_name_to_write = make_target_file_name_from_source(default_file_name_to_read)
    default_project_path_name_to_write = make_project_path_name(orchid.training_data_path(),
                                                                default_file_name_to_write)
    parser.add_argument('-o', '--output_project', default=default_project_path_name_to_write,
                        help=f'Filename of project to write. (Default: {default_project_path_name_to_write}')

    args = parser.parse_args()
    main(args)

