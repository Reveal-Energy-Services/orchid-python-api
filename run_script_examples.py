#! /usr/bin/env python
#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2024 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


import argparse
import subprocess
import sys
from typing import Optional, Sequence

import examples

import orchid


def run_script_examples() -> None:
    """
    Run the Orchid Python API script examples.
    """

    example_script_names = examples.ordered_script_names()
    if not example_script_names:
        print(f'No example scripts matching "{example_script_names}"')
        return

    for example_script_name in example_script_names:
        # Treat `stage_qc_results.py` specially
        if example_script_name != 'stage_qc_results.py':
            subprocess.call(f'{sys.executable} {example_script_name}')
        else:
            verbosity = '-v2'
            ifrac_filename = 'frankNstein_Bakken_UTM13_FEET.ifrac'
            read_only_command_line = (f'{sys.executable} {example_script_name} {verbosity}'
                                      f' --read-only {orchid.training_data_path().joinpath(ifrac_filename)}')
            print()
            print('Demonstrate reading stage QC results')
            print(read_only_command_line)
            subprocess.call(read_only_command_line)

            read_write_command_line = (f'{sys.executable} {example_script_name} {verbosity}'
                                       f' {orchid.training_data_path().joinpath(ifrac_filename)}')
            print()
            print('Demonstrate reading and writing stage QC results')
            print(read_write_command_line)
            subprocess.call(read_write_command_line)


def main(cli_args: Optional[Sequence[str]] = None):
    """
    Entry point for copy Orchid examples utility.
    Args:
        cli_args: The command line arguments.
    """
    cli_args = cli_args if cli_args else sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Run Orchid Python API script examples in current directory')

    args = parser.parse_args(cli_args)
    run_script_examples()


if __name__ == '__main__':
    main(sys.argv[1:])
