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
import logging
import pathlib
import pprint
from typing import Optional

import orchid
from orchid import (
    dot_net_disposable as dnd,
    native_stage_adapter as nsa,
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


def create_stage(
        # 1 more than the maximum of `order_of_completion_on_well` for all stages on `target_well`
        order_of_completion_on_well: int,
        well: object,
        connection_type: nsa.ConnectionType,
        md_top: om.Quantity,
        md_bottom: om.Quantity,
        *,
        # Remember that passing `None`, the default value, results in Orchid calculating a shmin value from
        # the `FracGradient` property of the well.
        maybe_shmin: Optional[om.Quantity] = None,
        cluster_count: int = 0):
    native_md_top = onq.as_net_quantity(units.UsOilfield.LENGTH, md_top)  # Must supply the unit system for conversion
    native_md_bottom = onq.as_net_quantity(units.UsOilfield.LENGTH, md_bottom)
    shmin = onq.as_net_quantity(units.UsOilfield.PRESSURE, maybe_shmin) if maybe_shmin is not None else None
    native_stage = object_factory.CreateStage(UInt32(order_of_completion_on_well),
                                              well.dom_object,
                                              connection_type.value,
                                              native_md_top,
                                              native_md_bottom,
                                              shmin,
                                              UInt32(cluster_count))
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
        create_stage(
            35,  # hard-coded to be one greater than largest `order_of_completion_on_well`
            target_well, nsa.ConnectionType.PLUG_AND_PERF,
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12603.3),
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12750.5)),
        create_stage(
            36,
            target_well, nsa.ConnectionType.PLUG_AND_PERF,
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12396.8),
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12556.9),
            maybe_shmin=orchid.make_measurement(orchid.unit_system.UsOilfield.PRESSURE, 2.322)
        ),
        create_stage(
            37,
            target_well, nsa.ConnectionType.PLUG_AND_PERF,
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12396.8),
            orchid.make_measurement(orchid.unit_system.UsOilfield.LENGTH, 12556.9),
            cluster_count=7
        ),
    ]
    pprint.pprint([(s.name, s.shmin if s.shmin else 'None', s.cluster_count) for s in stages_to_append])


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

