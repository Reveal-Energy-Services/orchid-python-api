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

import dataclasses as dc

import pendulum as pdt
import parsy

# Utility parsers
comma = parsy.string(',') << parsy.whitespace.many()
equals = parsy.string('=')
integer = parsy.regex(r'\d+').map(int)
newline = parsy.string('\n')
left_brace = parsy.string('{')
left_paren = parsy.string('(')
right_brace = parsy.string('}')
right_paren = parsy.string(')')
single_quote = parsy.string("'")

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


@parsy.generate
def key_value_pair():
    yield parsy.regex(r'[\w_\d]+').desc('key')
    value = yield equals >> ((single_quote >> parsy.regex(r"[^']+") << single_quote) |
                             integer)
    return value


@dc.dataclass
class AddedStageDetails:
    stage_name: str
    shmin: str
    cluster_count: int
    global_stage_sequence_no: int
    start_time: str
    stop_time: str


@parsy.generate
def added_stage_details():
    yield parsy.string('INFO:root:CreatedStageDetails')
    yield left_paren
    stage_name = yield key_value_pair
    shmin = yield comma >> key_value_pair
    cluster_count = yield comma >> key_value_pair
    global_stage_sequence_no = yield comma >> key_value_pair
    start_time = yield (comma >> key_value_pair).map(pdt.parse).desc('start_time')
    stop_time = yield (comma >> key_value_pair).map(pdt.parse).desc('stop_time')
    yield right_paren

    return AddedStageDetails(stage_name=stage_name, shmin=shmin, cluster_count=cluster_count,
                             global_stage_sequence_no=global_stage_sequence_no,
                             start_time=start_time, stop_time=stop_time)


@parsy.generate
def get_added_stages():
    added_stages_details = yield (added_stage_details << newline).at_least(1)
    yield output_path_name
    yield newline

    return added_stages_details
