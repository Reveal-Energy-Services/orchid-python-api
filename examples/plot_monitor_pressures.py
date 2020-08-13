#! /usr/bin/env python
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

import argparse

import orchid


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pathname', help="Path name of the project ('.ifrac') file.")

    # TODO Add options to control plotting better
    # I have chosen to hard-code data for now. My next set of commits will begin to parameterize the plotting
    # functions to allow for finer control in other situations.

    options = parser.parse_args()
    orchid.plot_monitor_pressures(options.pathname)
