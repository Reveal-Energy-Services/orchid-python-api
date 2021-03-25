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


from orchid import (
    dot_net_dom_access as dna,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IMonitor


class NativeMonitorAdapter(dna.DotNetAdapter):
    """Adapts a native IMonitor to python."""
    def __init__(self, net_monitor: IMonitor):
        """
        Constructs an instance adapting a .NET IMonitor.

        Args:
            net_monitor: The .NET monitor to be adapted.
        """
        super().__init__(net_monitor, dna.constantly(net_monitor.Project))
