#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

import os
import os.path

import yaml


def python_api():
    config = {'directory': os.path.join(os.environ['LOCALAPPDATA'], 'Reveal')}
    custom = {}

    if os.path.exists('python_api.yaml'):
        with open('python_api.yaml', 'r') as in_stream:
            custom = yaml.full_load(in_stream)

    config.update(custom)
    return config
