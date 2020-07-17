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

import os
import pathlib

import yaml


def python_api():
    """
    Calculate the configuration for the Python API.

    :return: The Python API configuration.
    """

    # My general intent is that an actual user need not provide *any* configuration. Specifically, I assume
    # that the user has installed the `orchid` package (Python API) with the Orchid application itself.
    # Further, I assume that the Orchid application is installed in the "standard" location for user-specific
    # code; that is, `AppData/Local` of the users "home" directory. This location is identified by the
    # environment variable, `LOCALAPPDATA`, which is set by Windows.
    config = {'directory': pathlib.Path(os.environ['LOCALAPPDATA']).joinpath('Reveal')}
    custom = {}

    # This code looks for the configuration file, `python_api.yaml`, in the parent directory of the package.
    # This choice works great for a developer, but I'm less clear that it would work for a data scientist at
    # a customer. (Because it would depend on where the Python package is installed.)
    # custom_config_path = pathlib.Path(__file__).joinpath('..', '..', 'python_api.yaml')
    custom_config_path = pathlib.Path.home().joinpath('.orchid', 'python_api.yaml')
    if custom_config_path.exists():
        with custom_config_path.open('r') as in_stream:
            custom = yaml.full_load(in_stream)

    config.update(custom)
    return config
