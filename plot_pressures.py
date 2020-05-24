#! py -3
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

import argparse

import orchid


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pathname', help="Path name of the project ('.ifrac') file.")

    # TODO Add options to control plotting better
    # I have chosen to hard-code data for now. My next set of commits will begin to parameterize the plotting
    # functions to allow for finer control in other situations.

    options = parser.parse_args()
    orchid.plot_pressures(options.pathname)
