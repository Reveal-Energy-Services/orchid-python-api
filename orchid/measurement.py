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

"""This module contains functions and classes supporting the (Python) Measurement 'class.'"""

import collections


Measurement = collections.namedtuple('measurement', ['magnitude', 'unit'], module=__name__)


def make_measurement(magnitude, unit):
    """
    Construct a measurement.
    :param magnitude: The magnitude of the measurement.
    :param unit: The abbreviation of the unit of measurement.
    :return: The constructed (Python) measurement.
    """
    return Measurement(magnitude, unit)
