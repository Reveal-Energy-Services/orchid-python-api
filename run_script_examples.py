#! /usr/bin/env python
#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
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
import subprocess
import sys
from typing import Optional, Sequence

import examples


def run_script_examples() -> None:
    """
    Run the Orchid Python API script examples.
    """

    example_script_names = examples.ordered_script_names()
    if not example_script_names:
        print(f'No example scripts matching "{example_script_names}"')
        return

    for example_script_name in example_script_names:
        subprocess.call(f'python {example_script_name}')


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
