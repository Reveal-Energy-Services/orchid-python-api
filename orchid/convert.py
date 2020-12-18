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

from typing import Union

import toolz.curried as toolz

from orchid import (measurement as om,
                    net_quantity as onq,
                    unit_system as units)


def to_unit(source_measurement: om.Measurement, target_unit: Union[units.UsOilfield, units.Metric]):
    """
    Convert a `Measurement` instance to the same measurement in `target_unit`.

    Args:
        source_measurement: The Measurement instance to convert.
        target_unit: The units to which I convert `source_measurement`.
    """
    if source_measurement.unit == target_unit:
        return source_measurement

    result = toolz.pipe(onq.as_net_quantity_in_different_unit(source_measurement, target_unit),
                        toolz.curry(onq.as_measurement))

    return result
