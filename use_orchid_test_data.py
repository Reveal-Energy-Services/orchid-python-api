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


def main(test_data_dir: str, example_dir: str) -> None:
    """
    Change the placeholder integration test data directory to the specified directory.

    Args:
        test_data_dir: The directory containing the installed Orchid test data.
        example_dir: The directory containing the Orchid Python API examples.
    """
    print(f'Change directory of examples in {example_dir} to {test_data_dir}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Change the integration test directories in the example files.')
    parser.add_argument('--example-dir', default='.',
                        help='Directory containing the Orchid Python API examples (default: current directory)')
    parser.add_argument('test_data_dir', help='Directory of installed Orchid test data.')

    args = parser.parse_args()
    main(args.test_data_dir, args.example_dir)
