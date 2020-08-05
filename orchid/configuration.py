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

import logging
import os
import pathlib
import re
from typing import Dict

import toolz.curried as toolz
import yaml

_logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    pass


@toolz.curry
def sort_installations(candidate_pattern, user_friendly_pattern, path):
    match_result = re.match(candidate_pattern, path.name)
    if not match_result:
        raise ConfigurationError(f'Expected directories matching {user_friendly_pattern} but found, "{str(path)}".')

    sortable_version = match_result.groups()
    return sortable_version


def python_api() -> Dict[str, str]:
    """
    Calculate the configuration for the Python API.

        Returns: The Python API configuration.

        BEWARE: The returned configuration will not have an 'directory' key if Orchid is neither installed
        nor configured with `$HOME/.orchid/python.yaml`.
    """

    # My general intent is that an actual user need not provide *any* configuration. Specifically,
    # I assume that the Orchid application is installed in the "standard" location,
    # `$ProgramFiles/Reveal Energy Services, Inc/Orchid/<version-specific-directory>`
    standard_orchid_dir = pathlib.Path(os.environ['ProgramFiles']).joinpath('Reveal Energy Services, Inc',
                                                                            'Orchid')

    candidate_pattern = re.compile(r'Orchid-(\d{4})\.([1234])\.(\d+).(\d+)$')
    candidates = list(toolz.map(
        str,
        sorted(standard_orchid_dir.glob('Orchid*'),
               key=sort_installations(candidate_pattern,
                                      '"Orchid-(major).(minor).(patch).(build)" (all integers)'), reverse=True)))
    _logger.debug(f'candidates={candidates}')
    default = {}
    if len(candidates) > 0:
        default = {'directory': toolz.first(candidates)}
    _logger.debug(f'default configuration={default}')

    # This code looks for the configuration file, `python_api.yaml`, in the `.orchid` sub-directory in the
    # user-specific home directory.
    custom = {}
    custom_config_path = pathlib.Path.home().joinpath('.orchid', 'python_api.yaml')
    if custom_config_path.exists():
        with custom_config_path.open('r') as in_stream:
            custom = yaml.full_load(in_stream)
    _logger.debug(f'custom configuration={custom}')

    result = toolz.merge(default, custom)
    _logger.debug(f'result configuration={result}')
    return result
