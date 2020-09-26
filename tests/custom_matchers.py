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

from hamcrest import assert_that, equal_to, close_to


# The following functions are not custom matchers as defined by the `pyhamcrest` package; however, they
# provide similar functionality by implementing common test code.


def assert_that_scalar_quantities_close_to(actual_x, expected_x, tolerance):
    assert_that(actual_x.unit, equal_to(expected_x.unit))
    assert_that(actual_x.magnitude, close_to(expected_x.magnitude, tolerance))
