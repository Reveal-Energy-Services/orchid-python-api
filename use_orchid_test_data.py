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
import glob
import pathlib
import re
import shutil
import sys
import tempfile
from typing import Optional, Sequence


def sed_inplace(filename, pattern: str, repl: str):
    """
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.

    This implementation was copied from [StackOverflow](
    https://stackoverflow.com/questions/4427542/how-to-do-sed-like-text-replace-with-python/31499114)
    retrieved on 26-Aug-2020.
    """
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                print()
                print(f'Transforming: "{filename}"')
                transformed_line = pattern_compiled.sub(repl, line)
                if transformed_line != line:
                    # `end=''` removes automatic newline
                    print(f'  Before: "{line}"', end='')
                    print(f'  After:  "{transformed_line}"', end='')
                tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


def change_examples_test_dir(test_data_dir: str, examples_dir: str) -> None:
    """
    Change the placeholder integration test data directory to the specified directory.

    Args:
        test_data_dir: The directory containing the installed Orchid test data.
        examples_dir: The directory containing the Orchid Python API examples.
    """
    for example_path in glob.glob(str(pathlib.Path(examples_dir).joinpath('*.ipynb'))):
        sed_inplace(example_path, r'\path\to', test_data_dir)
        print(f'Change test data directory(ies) of "{example_path}" to "{test_data_dir}".')


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
