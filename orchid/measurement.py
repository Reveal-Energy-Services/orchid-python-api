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


import pathlib

import pint


# This is the single location to find the `pint.UnitRegistry`. The `pint` package considers units returned
# from different instances of `UnitRegistry` to be different. See the documentation at
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects for details.
units = pint.UnitRegistry()
"""
The registry of all known units. See the Pint tutorial, https://pint.readthedocs.io/en/stable/tutorial.html,
for general information on the registry. Specifically, see the section,
https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects, for the "perils" of using 
multiple registry instances.
"""

# Load additional, orchid-specific unit definitions and aliases.
units.load_definitions(str(pathlib.Path(__file__).parent.resolve().joinpath('orchid_units.txt')))

# Expose general types for use by type annotations
Quantity = units.Quantity
"""The type of a Pint measurement exposed for convenience."""
Unit = units.Unit
"""The type of Pint units of measure."""

# Register this instance of the registry as the application registry to support picking and unpickling of Pint
# Quantity and Unit instances.
pint.set_application_registry(units)
