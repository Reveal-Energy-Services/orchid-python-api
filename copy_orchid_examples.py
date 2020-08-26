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


def main(target_dir: str) -> None:
    """
    Copy the Orchid Python API examples into the specified, `target_dir`.
    Args:
        target_dir: The target for the examples.
    """
    print(f'Copying examples to {target_dir}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy Orchid Python API examples to specified directory.')
    parser.add_argument('--target-dir', default='.',
                        help='Directory into which to copy the Orchid Python API examples '
                             '(default: current directory)')

    args = parser.parse_args()
    main(args.target_dir)
