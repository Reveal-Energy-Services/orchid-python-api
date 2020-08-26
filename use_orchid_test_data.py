#! /usr/bin/env python
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


import argparse
import sys
from typing import Optional, Sequence


def change_examples_test_dir(test_data_dir: str, examples_dir: str) -> None:
    """
    Change the placeholder integration test data directory to the specified directory.

    Args:
        test_data_dir: The directory containing the installed Orchid test data.
        examples_dir: The directory containing the Orchid Python API examples.
    """
    print(f'Change directory of examples in "{examples_dir}" to "{test_data_dir}".')


def main(cli_args: Optional[Sequence[str]] = None):
    """
    Entry point for use Orchid test data utility.
    Args:
        cli_args: The command line arguments.
    """
    cli_args = cli_args if cli_args else sys.argv[1:]

    parser = argparse.ArgumentParser(description='Change the Orchid Python API examples in a directory to use the '
                                                 'Orchid test data found in the specified directory')
    parser.add_argument('-e', '--examples-dir', default='.',
                        help='The directory containing the Orchid Python API examples (default: current directory)')
    # REMEMBER: positional arguments *do not* transform '-' into '_'
    parser.add_argument('test_data_dir',
                        help='The directory containing the Orchid Python API test data to use')

    args = parser.parse_args(cli_args)
    change_examples_test_dir(args.test_data_dir, args.examples_dir)


if __name__ == '__main__':
    main(sys.argv[1:])
