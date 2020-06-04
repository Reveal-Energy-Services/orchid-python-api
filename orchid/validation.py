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

"""This module contains common functions used to validate arguments."""


# TODO: Any better functional support?
# I'd really like to compose these functions but the `functional` library appears dead.
# Consider the `functionally` package. Although not updated since 2012, contains many
# higher-level functions familiar from other libraries. Don't think we expose this to
# consumers, but may be useful internally.


def arg_not_none(_, arg) -> bool:
    """
    Tests if the single argument is not None

    :param _: Ignored (typically mapped to `self` for bound methods)
    :param arg: The argument to be tested
    :return: True if arg is not None; otherwise, false.
    """
    return arg is not None


def arg_neither_empty_nor_all_whitespace(_, arg: str) -> bool:
    """
    Tests if the single argument is not None

    :param _: Ignored (typically mapped to `self` for bound methods)
    :param arg: The argument to be tested
    :return: True if arg is neither an empty string nor a string consisting only of whitespace.
    """
    return len(arg.strip()) > 0
