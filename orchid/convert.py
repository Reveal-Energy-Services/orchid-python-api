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

from typing import Union

import toolz.curried as toolz

from orchid import (
    measurement as om,
    net_quantity as onq,
    unit_system as units,
)


@toolz.curry
def to_unit(target_unit: Union[units.UsOilfield, units.Metric], source_measurement: om.Measurement):
    """
    Convert a `Measurement` instance to the same measurement in `target_unit`.

    The order of arguments allows easier conversion of a sequence of `Measurement` instances (with the same
    unit) to another unit. For example, if client code wished to convert a sequence of force measurements from
    US oilfield units to metric units (that is, pound-force to Newtons). Code to perform this conversion might
    be similar to the following:

    > make_metric_force = to_unit(units.Metric.FORCE)
    > metric_force_measurements = [make_metric_force(f) for f in us_oilfield_force_measurements]
    > # alternatively,
    > # metric_force_measurements = toolz.map(make_metric_force, us_oilfield_force_measurements)

    Args:
        source_measurement: The Measurement instance to convert.
        target_unit: The units to which I convert `source_measurement`.
    """
    if source_measurement.unit == target_unit:
        return source_measurement

    result = toolz.pipe(onq.as_net_quantity_in_different_unit(source_measurement, target_unit),
                        onq.obs_as_measurement(target_unit.value.physical_quantity))

    return result
