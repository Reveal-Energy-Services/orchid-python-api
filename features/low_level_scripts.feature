#  Copyright (c) 2017-2022 Reveal Energy Services, Inc
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

Feature: Low-level example scripts
  As a data engineer,
  I want to access Orchid projects using the low-level API exemplified by scripts
  In order to complete my work in a timely manner

  Scenario Outline: Automatically pick observations
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script
    Then I see that <observation_count> observations were picked

    Examples:
      | script_file_name             | observation_count |
      | auto_pick.py                 | 120               |
      | auto_pick_iterate_example.py | 120               |

  Scenario Outline: Automatically pick observations and create stage attributes
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script
    Then I see that <observation_count> observations were picked
    And I see that <attribute_count> attributes were created for each stage of each well

    Examples: auto_pick_and_create_stage_attributes
      | script_file_name                        | observation_count | attribute_count |
      | auto_pick_and_create_stage_attribute.py | 120               | 2               |

  Scenario Outline: Add stages
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script
    And I see the following added stages
      | stage_name | shmin        | clusters | global_seq_no | stage_time_range                                |
      | Stage-36   | 8144.498 psi | 0        | 0             | 2018-06-06T05:34:03.684/2018-06-06T07:19:35.560 |
      | Stage-37   | 2.322 psi    | 0        | 0             | 2018-06-15T14:11:40.450/2018-06-15T15:10:11.200 |
      | Stage-38   | 8041.893 psi | 7        | 0             | 2018-06-28T23:35:54.379/2018-06-29T01:18:05.840 |

    Examples: auto_pick_and_create_stage_attributes
      | script_file_name |
      | add_stages.py    |
