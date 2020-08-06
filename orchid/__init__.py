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

from .dot_net import prepare_imports
prepare_imports()

# High-level API
from .core import load_project
from .core import plot_monitor_pressures
from .core import plot_monitor_pressure_curve
from .core import plot_trajectories
from .core import plot_treatment

# Helpful constants
from .native_treatment_curve_facade import (PROPPANT_CONCENTRATION, SLURRY_RATE, TREATING_PRESSURE)

# Helpful functions
from .measurement import (get_conversion_factor, slurry_rate_volume_unit, proppant_concentration_mass_unit)
