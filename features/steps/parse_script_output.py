#  Copyright 2017-2021 Reveal Energy Services, Inc 
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

"""
Common functions for parsing the output of the low-level example script integration tests.
"""

import parsy

# Utility parsers
newline = parsy.string('\n')
left_brace = parsy.string('{')
right_brace = parsy.string('}')
integer = parsy.regex(r'\d+').map(int)

# Single-line parsers
project_name = parsy.string("INFO:root:native_project.Name='frankNstein_Bakken_UTM13_FEET'")
observation_set_items = parsy.string("INFO:root:len(native_project.ObservationSets.Items)=2")
parent_well_observations = parsy.string("INFO:root:observation_set.Name='ParentWellObservations'")
get_observations = parsy.string("INFO:root:len(observation_set.GetObservations())=") >> parsy.regex(r'\d+').map(int)
auto_picked_observation_set = parsy.string("INFO:root:observation_set.Name='Auto-picked Observation Set3'")
output_path_name = (parsy.string('INFO:root:Wrote changes to') >>
                    parsy.regex(r' "c:\\src\\Orchid.IntegrationTestData\\frankNstein_Bakken_UTM13_FEET.\d{3}.ifrac"'))
unique_attribute_count_per_stage_per_well_equals = parsy.string(r'INFO:root:Unique counts of'
                                                                r' attributes per stage per well=')


# Parser generators
@parsy.generate
def attribute_count_per_stage_per_well():
    yield unique_attribute_count_per_stage_per_well_equals
    yield left_brace
    attribute_per_stage_per_well_count = yield integer
    yield right_brace

    return attribute_per_stage_per_well_count


@parsy.generate
def get_second_observations_count():
    yield project_name
    yield newline >> observation_set_items
    yield newline >> parent_well_observations
    yield newline >> get_observations
    yield newline >> auto_picked_observation_set
    get_observations_count = yield newline >> get_observations
    yield (newline >> attribute_count_per_stage_per_well).optional()
    yield newline >> output_path_name
    yield newline

    return get_observations_count


@parsy.generate
def get_attribute_count_for_each_stage_and_well():
    yield project_name
    yield newline >> observation_set_items
    yield newline >> parent_well_observations
    yield newline >> get_observations
    yield newline >> auto_picked_observation_set
    yield newline >> get_observations
    attribute_count_for_each_stage_and_well = yield newline >> attribute_count_per_stage_per_well
    yield newline >> output_path_name
    yield newline

    return attribute_count_for_each_stage_and_well
