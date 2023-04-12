#  Copyright 2017-2023 Reveal Energy Services, Inc
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
import pathlib
from typing import List
import uuid

import numpy as np
import pendulum as pdt
import parsy


WROTE_CHANGES_TO = 'Wrote changes to'

LEAK_OFF_COUNT = 'LeakOffObservations'
MULTI_PICKING = 'Multi-pick Observation Set'
MULTI_PICK_COUNT = 'MultiPickingObservations'
PARENT_WELLS = 'ParentWellObservations'


# If you need to test the regular expressions used in this parse, consider using [Pythex](https://pythex.org/)


# Utility parsers
colon = parsy.string(':') << parsy.whitespace.many()
comma = parsy.string(',') << parsy.whitespace.many()
dash = parsy.string('-')
dot = parsy.string('.')
double_quote = parsy.string('"')
equals = parsy.string('=')
float_parser = parsy.regex(r'\d+\.\d*').map(float)
greater_than = parsy.string('>')
hex_digits = parsy.regex(r'[\da-fA-F]+')
hex_literal = parsy.string('0x') >> hex_digits
integer = parsy.regex(r'\d+').map(int)
newline = parsy.string('\n')
left_brace = parsy.string('{')
left_paren = parsy.string('(')
less_than = parsy.string('<')
right_brace = parsy.string('}')
right_paren = parsy.string(')')
single_quote = parsy.string("'")

# Single-line parsers
single_quoted_text = (single_quote >> parsy.regex(r"[^']+") << single_quote)
double_quoted_text = (double_quote >> parsy.regex(r"[^']+") << double_quote)

auto_picked_observation_set = parsy.string("INFO:root:observation_set.Name='Auto-picked Observation Set3'")
get_leak_off_observations = (parsy.string(f"INFO:root:len(dne.as_list(observation_set.{LEAK_OFF_COUNT}.Items))=") >>
                             parsy.regex(r'\d+').map(int))
get_multi_pick_observations = (parsy.string(f"INFO:root:len(dne.as_list(observation_set.{MULTI_PICK_COUNT}.Items))=") >>
                               parsy.regex(r'\d+').map(int))
get_observations = (parsy.string("INFO:root:len(dne.as_list(observation_set.GetLeakOffObservations()))=") >>
                    parsy.regex(r'\d+').map(int))
multi_picked_observation_set = parsy.string(f"INFO:root:observation_set.Name='{MULTI_PICKING}'")
observation_set_items = parsy.string("INFO:root:len(observation_sets_items)=2")
oid_parser = parsy.string('UUID') >> left_paren >> single_quoted_text.map(uuid.UUID) << right_paren
parent_well_observations = parsy.string(f"INFO:root:observation_set.Name='{PARENT_WELLS}'")
project_name = parsy.string("INFO:root:native_project.Name='frankNstein_Bakken_UTM13_FEET'")
python_var_name = parsy.regex(r'[\w_\d]+')
python_attribute_name = (python_var_name << dot.optional()).many().map(lambda ns: '.'.join(ns))
rfc_date_time_text = parsy.regex(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\+|-)\d{2}:\d{2}')
rfc_date_time = rfc_date_time_text.map(pdt.parse)
unique_attribute_count_per_stage_per_well_equals = parsy.string(
    r'INFO:root:Unique counts of attributes per stage per well=')
uuid_parser = (hex_digits + dash  # 8 digit block
               + hex_digits + dash  # 4 digit block
               + hex_digits + dash  # 4 digit block
               + hex_digits + dash  # 4 digit block
               + hex_digits  # 12 digit block
               ).map(uuid.UUID)
# The next three parsers are based on a recipe from
# [The Regular Expression Cookbook]https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s18.html)
drive_letter = parsy.regex(r'[a-zA-Z]:\\')
folders = parsy.regex(r'(?:[^\\/:*?"<>|\r\n]+\\)*')
filename = parsy.regex(r'[^\\/:*?"<>|\r\n]*')
get_output_path_name = (parsy.string(f'INFO:root:{WROTE_CHANGES_TO} ') >>
                        double_quote >>
                        parsy.seq(drive_letter, folders, filename)
                        .combine(lambda d, fs, fn: ''.join([d, fs, fn]))
                        .map(pathlib.Path) <<
                        double_quote)


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
    yield newline >> get_output_path_name
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
    yield newline >> get_output_path_name
    yield newline

    return attribute_count_for_each_stage_and_well


@parsy.generate
def key_value_pair():
    yield python_var_name.desc('key')
    value = yield equals >> (single_quoted_text | integer)
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
    yield get_output_path_name
    yield newline

    return added_stages_details


@dc.dataclass
class BriefOrchidObject:
    object_id: uuid.UUID
    class_name: str


@parsy.generate
def brief_orchid_object():
    oid = yield oid_parser
    yield colon
    class_name = yield (less_than >> python_attribute_name
                        << parsy.string(' object at ')
                        << hex_literal
                        << greater_than)

    return BriefOrchidObject(object_id=oid, class_name=class_name)


@parsy.generate
def brief_orchid_objects():
    yield parsy.whitespace.optional()
    yield left_brace
    brief_objects = yield (brief_orchid_object << comma.optional()).many()
    yield right_brace
    # TODO: Consider replacing all `newline` parsers with `whitespace`
    # The step, "I see all time series in the project", passes in a development environment but fails in the build
    # pipeline. When it fails, the next character in the input stream is `\r`. Larry, the author, has never seen a
    # carriage return character in all his testing locally, but his environment for testing is
    # - `bash`
    # - `PyCharm`
    # - A `poetry` virtual environment running under `Powershell` (and usually Powershell Core).
    # Larry's working hypothesis is that the build environment is truly a Windows environment in which a "newline" is
    # not a single character but the string `\r\n`. In debug output of the failures in the build environment, one sees
    # the Windows newline in the representation of the `behave` `context.text`.
    #
    # Another alternative would be to switch the parsing package from `parsy` to `pyparsing`. I believe that
    # `pyparsing`, by default, ignores whitespace.
    #
    # A final option would be to change the implementation altogether in one of two ways. Either complete forget parsing
    # or, the best option, stop testing the output of scripts (which, by it's nature, can produce these kinds of
    # issues, and move to integration tests of the .NET API).
    yield parsy.whitespace.optional()
    return brief_objects


@parsy.generate
def all_times_series_in_project():
    yield parsy.whitespace.optional()
    yield parsy.string('All time series in project')
    yield parsy.whitespace.optional()
    brief_objects = yield brief_orchid_objects

    return brief_objects


@parsy.generate
def all_monitors_in_project():
    yield parsy.string('All monitors in project')
    yield parsy.whitespace.optional()
    brief_objects = yield brief_orchid_objects

    return brief_objects


@parsy.generate
def monitor_of_interest():
    yield parsy.string('Monitor of interest:')
    yield parsy.whitespace.optional()
    yield parsy.string('- Object ID: ')
    object_id = yield uuid_parser
    yield parsy.whitespace.optional()
    yield parsy.string('- Display Name: Demo_2H - stage 1')
    yield parsy.whitespace.optional()

    return object_id


@parsy.generate
def monitor_time_series_of_interest():
    yield parsy.string('Object ID of monitor time series of interest: ')
    object_id = yield uuid_parser
    yield parsy.whitespace.optional()

    return object_id


@dc.dataclass
class TimeSeriesSample:
    sample_time: pdt.DateTime
    sample_value: float


@parsy.generate
def monitor_time_series_sample():
    sample_time = yield rfc_date_time
    yield parsy.whitespace
    yield parsy.whitespace.many()
    sample_value = yield float_parser

    return TimeSeriesSample(sample_time=sample_time, sample_value=sample_value)


@dc.dataclass
class AboutTimeSeriesSample:
    name: str
    dtype: np.dtype


@dc.dataclass
class TimeSeriesSamples:
    samples: List[TimeSeriesSample]
    about: AboutTimeSeriesSample


@parsy.generate
def about_monitor_time_series_samples():
    yield parsy.string('Name: ')
    name = yield parsy.regex('[^,]+')
    yield parsy.seq(comma, parsy.whitespace.many())
    yield parsy.string('dtype: ')
    dtype = yield python_var_name.map(np.dtype)
    yield parsy.whitespace.optional()

    return AboutTimeSeriesSample(name=name, dtype=dtype)


@parsy.generate
def monitor_time_series_samples():
    yield parsy.string('Head of time series')
    samples = yield (parsy.whitespace >> monitor_time_series_sample).many()
    yield parsy.whitespace
    about_time_series_samples = yield about_monitor_time_series_samples

    return TimeSeriesSamples(samples=samples, about=about_time_series_samples)


@parsy.generate
def get_observations_counts():
    yield project_name
    yield newline >> observation_set_items
    yield newline >> parent_well_observations
    parent_leak_off_counts = yield newline >> get_leak_off_observations
    parent_multi_pick_counts = yield newline >> get_multi_pick_observations
    yield newline >> multi_picked_observation_set
    multi_leak_off_counts = yield newline >> get_leak_off_observations
    multi_multi_pick_counts = yield newline >> get_multi_pick_observations
    output_path_name = yield newline >> get_output_path_name
    yield newline

    return {
        PARENT_WELLS: {LEAK_OFF_COUNT: parent_leak_off_counts,
                       MULTI_PICK_COUNT: parent_multi_pick_counts},
        MULTI_PICKING: {LEAK_OFF_COUNT: multi_leak_off_counts,
                        MULTI_PICK_COUNT: multi_multi_pick_counts},
        WROTE_CHANGES_TO: output_path_name,
    }
