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


import orchid.dot_net_dom_access as dna


class NativeWellTimeSeriesAdapter(dna.DotNetAdapter):
    def __init__(self, native_well_time_series):
        super().__init__(native_well_time_series)

    display_name = dna.dom_property('display_name', 'The display name of the .NET well time series.')
