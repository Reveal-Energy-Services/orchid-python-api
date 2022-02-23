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
import enum
import logging
import pprint
from typing import Iterable

import orchid
from orchid import (
    native_well_adapter as nwa,
    net_fracture_diagnostics_factory as net_factory,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.Settings import Variant


object_factory = net_factory.create()


class StageCorrectionStatus(enum.Enum):
    # The values of these three members are the strings required by the low-level API
    CONFIRMED = "Confirmed"
    UNCONFIRMED = "Unconfirmed"
    NEW = ""


class StageQC:
    """Models the stage QC process."""

    _DEFAULT_CORRECTION_VARIANT = Variant.Create(StageCorrectionStatus.NEW.value)
    _TEXT_TO_STAGE_CORRECTION_STATUS = {
        StageCorrectionStatus.CONFIRMED.value: StageCorrectionStatus.CONFIRMED,
        StageCorrectionStatus.NEW.value: StageCorrectionStatus.NEW,
        StageCorrectionStatus.UNCONFIRMED.value: StageCorrectionStatus.UNCONFIRMED,
    }

    def __init__(self, stage):
        """
        Construct a `StageQC` instance for the specified `stage`.

        Args:
            stage: The stage of interest.
        """
        self._net_stage = stage.dom_object
        self._net_project = self._net_stage.Project

    def start_stop_time_confirmation(self) -> StageCorrectionStatus:
        """
        Calculate the stage start/stop time confirmation status using the low-level API.

        Returns:
            The start/stop time confirmation status for the QC of the stage of this instance.
        """
        project_user_data = self._net_project.ProjectUserData
        stage_qc_id = f'{str(self._net_stage.ObjectId)}|stage_start_stop_confirmation'
        net_status = project_user_data.GetValue(stage_qc_id, StageQC._DEFAULT_CORRECTION_VARIANT)
        status_text = net_status.ToString()
        result = StageQC._TEXT_TO_STAGE_CORRECTION_STATUS[status_text]

        return result


def log_status_for_stages(well: nwa.NativeWellAdapter, stage_display_numbers: Iterable[int]):
    """
    Log the stage QC statuses for `stage_display_numbers` of `well`.

    Args:
        well: The well of interest.
        stage_display_numbers: The display numbers of the stages of interest
    """
    stages = [well.stages().find_by_display_stage_number(display_number) for display_number in stage_display_numbers]
    statuses = {stage.display_name_with_well: StageQC(stage).start_stop_time_confirmation() for stage in stages}
    logging.info('Status for stages of interest')
    logging.info(pprint.pformat(statuses))


def main(cli_args):
    """
    Query stage QC start/stop time confirmation status values from an .ifrac file using the low-level API.

    Args:
        cli_args: The command line arguments from `argparse.ArgumentParser`.
    """
    logging.basicConfig(level=logging.INFO)

    # Read Orchid project
    project = orchid.load_project(cli_args.input_project)

    # Automatically pick the stages to illustrate different statuses.
    well_name = 'Demo_1H'
    candidate_wells = list(project.wells().find_by_name(well_name))
    # I actually expect exactly one well.
    assert len(candidate_wells) == 1, (f'Exactly one well with name, "{well_name}", expected.'
                                       f' Found {len(candidate_wells)}.')
    well = candidate_wells[0]

    # Log the status value for the specified stages (hard-coded values for known "interesting" stages)
    # noinspection PyTypeChecker
    log_status_for_stages(well, [1, 2, 3])


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automatically pick leak off observations.")
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2], default=0,
                        help='Increase output verbosity. (Default: 0; that is, least output.)')

    # The filename supplied on the command line *must* be a project with some statuses set to return
    # interesting results. The particular file,
    # `c:\src\Orchid.IntegrationTestData\frankNstein_Bakken_UTM13_FEET.stage-qc.ifrac`, contains:
    # - Demo_1H stage 1 start/stop time confirmation status: Confirmed
    # - Demo_1H stage 2 start/stop time confirmation status: Unknown
    # - Demo_1H stage 3 start/stop time confirmation status: New
    parser.add_argument('input_project', help=f'Path name of project to read.')

    args = parser.parse_args()
    main(args)
