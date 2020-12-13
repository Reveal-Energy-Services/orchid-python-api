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

from collections import namedtuple

from hamcrest import assert_that, equal_to, close_to


# The following functions are not custom matchers as defined by the `pyhamcrest` package; however, they
# provide similar functionality by implementing common test code.


ScalarQuantity = namedtuple('ScalarQuantity', ['magnitude', 'unit'])
SubsurfaceLocation = namedtuple('SubsurfaceLocation', ['x', 'y', 'depth'])


def assert_that_scalar_quantities_close_to(actual, expected, tolerance):
    assert_that(actual.unit, equal_to(expected.unit))
    assert_that(actual.magnitude, close_to(expected.magnitude, tolerance))


def assert_that_net_quantities_close_to(actual, expected, tolerance):
    def get_net_unit(net_quantity):
        raise NotImplementedError
    assert_that(get_net_unit(actual), equal_to(get_net_unit(expected)))
    assert_that(actual.Value, close_to(expected.Value, tolerance))
