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


"""
Low-level example of creating a multi-picking event.
"""

import argparse
import logging
import pathlib

import clr
import orchid
from orchid import (
    dot_net_disposable as dnd,
    net_fracture_diagnostics_factory as net_factory,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import (MonitorExtensions, Leakoff, Observation)
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Factories.Implementations import LeakoffCurves
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import (
    ScriptAdapter,
)
# noinspection PyUnresolvedReferences
from System import (Array, Double, DateTime, String)
# noinspection PyUnresolvedReferences
from System.IO import (FileStream, FileMode, FileAccess, FileShare)
# noinspection PyUnresolvedReferences
import UnitsNet

clr.AddReference('Orchid.Math')
clr.AddReference('System.Collections')
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IStagePart
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.MultiPickingObservation import Classification as MultiPickingObservationClassification
# noinspection PyUnresolvedReferences
from Orchid.Math import Interpolation
# noinspection PyUnresolvedReferences
from System import DateTime
# noinspection PyUnresolvedReferences
from System.Collections.Generic import List


object_factory = net_factory.create()


def multi_pick_observations(native_project, native_monitor):
    """
        Multi-pick observations for each treatment stage of `native_project` observed by `native_monitor`.
    Args:
        native_project: The `IProject` whose observations are sought.
        native_monitor: The `IMonitor` whose observations we automatically pick.

    Returns:

    """
    observation_set = object_factory.CreateObservationSet(native_project, 'Multi-pick Observation Set')

    # Arbitrarily select well, 'Demo_1H'
    monitored_well = [well for well in native_project.Wells.Items if well.Name == 'Demo_1H'][0]
    # Arbitrarily select stages and classifications. All stages are visible with a single stage part.
    monitored_stage_numbers = {
        37: MultiPickingObservationClassification.Spacer,
        38: MultiPickingObservationClassification.DiverterDrop,
        44: MultiPickingObservationClassification.Chemical,
        16: MultiPickingObservationClassification.RateChange,
        33: MultiPickingObservationClassification.BadData,
    }
    monitored_stages = [stage for stage in monitored_well.Stages.Items if
                        stage.DisplayStageNumber in monitored_stage_numbers]
    for stage in monitored_stages:
        if is_stage_visible_to_monitor(native_monitor, stage):
            stage_parts = stage.Parts
            for part in stage_parts:
                # Create multi-pick observation
                picked_observation = object_factory.CreateMultiPickingEventObservation(
                    part, part.StartTime, monitored_stage_numbers[stage.DisplayStageNumber],
                    f'auto-pick: {monitored_stage_numbers[stage.DisplayStageNumber]}')

                # Add picked observation to observation set
                with dnd.disposable(observation_set.ToMutable()) as mutable_observation_set:
                    mutable_observation_set.AddEvent(picked_observation)

    # Add observation set to project
    project_with_observation_set = native_project  # An alias to better communicate intent
    with dnd.disposable(native_project.ToMutable()) as mutable_project:
        mutable_project.AddObservationSet(observation_set)

    return project_with_observation_set


def is_stage_visible_to_monitor(native_monitor, stage):
    """
    Determine if the stage treatment is visible to the specified monitor.

    Args:
        native_monitor: The .NET `IMonitor` that may "see" the stage treatment.
        stage: The stage of interest.

    Returns:
        True if the stage is being treated while the monitor is actively monitoring pressures.
    """
    return (stage.StartTime.Ticks > native_monitor.StartTime.Ticks and
            stage.StopTime.Ticks < native_monitor.StopTime.Ticks)


def main(cli_args):
    """
    Save project with automatically picked observations from original project read from disk.

    Args:
        cli_args: The command line arguments from `argparse.ArgumentParser`.
    """
    logging.basicConfig(level=logging.INFO)

    # Read Orchid project
    project = orchid.load_project(cli_args.input_project)
    native_project = project.dom_object

    # Automatically pick the observations for a specific monitor
    monitor_name = 'Demo_3H - MonitorWell'
    candidate_monitors = list(project.monitors().find_by_display_name(monitor_name))
    # I actually expect one or more monitors, but I only need one (arbitrarily the first one)
    assert len(candidate_monitors) > 0, (f'One or monitors with display name, "{monitor_name}", expected.'
                                         f' Found {len(candidate_monitors)}.')
    native_monitor = candidate_monitors[0].dom_object
    multi_pick_observations(native_project, native_monitor)

    # Log changed project data if requested
    if cli_args.verbosity >= 2:
        logging.info(f'{native_project.Name=}')
        logging.info(f'{len(native_project.ObservationSets.Items)=}')
        for observation_set in native_project.ObservationSets.Items:
            logging.info(f'{observation_set.Name=}')
            logging.info(f'{len(observation_set.LeakOffObservations.Items)=}')
            logging.info(f'{len(observation_set.MultiPickingObservations.Items)=}')

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
        The project file name with a `.992` suffix inserted before the `.ifrac` suffix.
    """
    return ''.join([source_file_name.stem, '.992', source_file_name.suffix])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a multi-picking event observation.")
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

