#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#


import orchid.dot_net_dom_access as dna


class NativeWellTimeSeriesAdapter(dna.DotNetAdapter):
    def __init__(self, native_well_time_series):
        super().__init__(native_well_time_series)

    display_name = dna.dom_property('display_name', 'The display name of the .NET well time series.')
