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

Feature: Low-level DOM API
  As a data engineer,
  I sometimes need to access Orchid projects using Python.NET and the .NET API
  In order to meet deadlines

  Scenario Outline: Create stage attribute using the .NET API
    Given I have loaded the project for the field, '<field>'
    When I add the attribute named '<attribute_name>' of type `<attribute_type>' to well, `<well>', of the project
    And I set the attribute value of '<attribute_name>' of stage, <stage_no>, of '<well>' to <attribute_value>
    Then I see the attribute value of '<attribute_name>' of stage, <stage_no>, of '<well>' equals <attribute_value>

#    Examples: Bakken stage length
#      | field  | well    | stage_no | attribute_name  | attribute_type | attribute_value |
#      | Bakken | Demo_1H | 1        | My Stage Length | length         | 50.66 ft        |
#      | Bakken | Demo_1H | 50       | My Stage Length | length         | 147.11 ft       |
#      | Bakken | Demo_1H | 4        | My Stage Length | length         | 147.22 ft       |
#      | Bakken | Demo_2H | 1        | My Stage Length | length         | 147.22 ft       |
#      | Bakken | Demo_2H | 50       | My Stage Length | length         | 75.08 ft        |
#      | Bakken | Demo_2H | 35       | My Stage Length | length         | 147.15 ft       |
#      | Bakken | Demo_2H | 13       | My Stage Length | length         | 148.05 ft       |
#      | Bakken | Demo_4H | 1        | My Stage Length | length         | 148.05 ft       |
#      | Bakken | Demo_4H | 35       | My Stage Length | length         | 65.93 ft        |
#      | Bakken | Demo_4H | 29       | My Stage Length | length         | 225.00 ft       |
#      | Bakken | Demo_4H | 6        | My Stage Length | length         | 245.00 ft       |

    Examples: Bakken global stage sequence number
      | field  | well    | stage_no | attribute_name                  | attribute_type | attribute_value |
      | Bakken | Demo_1H | 1        | My Global Stage Sequence Number | integer        | 4               |
#      | Bakken | Demo_1H | 50       | My Global Stage Sequence Number | integer        | 128             |
#      | Bakken | Demo_1H | 4        | My Global Stage Sequence Number | integer        | 10              |
#      | Bakken | Demo_2H | 1        | My Global Stage Sequence Number | integer        | 2               |
#      | Bakken | Demo_2H | 50       | My Global Stage Sequence Number | integer        | 136             |
#      | Bakken | Demo_2H | 35       | My Global Stage Sequence Number | integer        | 97              |
#      | Bakken | Demo_2H | 13       | My Global Stage Sequence Number | integer        | 28              |
#      | Bakken | Demo_4H | 1        | My Global Stage Sequence Number | integer        | 3               |
#      | Bakken | Demo_4H | 35       | My Global Stage Sequence Number | integer        | 129             |
#      | Bakken | Demo_4H | 29       | My Global Stage Sequence Number | integer        | 114             |
#      | Bakken | Demo_4H | 6        | My Global Stage Sequence Number | integer        | 15              |

#    Examples: Montney stage length
#      | field   | well    | stage_no | attribute_name  | attribute_type | attribute_value |
#      | Montney | Hori_01 | 1        | My Stage Length | length         | 174.5 m         |
#      | Montney | Hori_01 | 15       | My Stage Length | length         | 175.5 m         |
#      | Montney | Hori_01 | 6        | My Stage Length | length         | 174.5 m         |
#      | Montney | Hori_01 | 11       | My Stage Length | length         | 174.5 m         |
#      | Montney | Hori_02 | 1        | My Stage Length | length         | 39.0 m          |
#      | Montney | Hori_02 | 29       | My Stage Length | length         | 72.0 m          |
#      | Montney | Hori_02 | 14       | My Stage Length | length         | 72.5 m          |
#      | Montney | Hori_02 | 22       | My Stage Length | length         | 72.5 m          |
#      | Montney | Hori_03 | 1        | My Stage Length | length         | 75.5 m          |
#      | Montney | Hori_03 | 28       | My Stage Length | length         | 75.5 m          |
#      | Montney | Hori_03 | 12       | My Stage Length | length         | 75.5 m          |
#      | Montney | Hori_03 | 21       | My Stage Length | length         | 75.5 m          |
#      | Montney | Vert_01 | 1        | My Stage Length | length         | 35.5 m          |
#      | Montney | Vert_01 | 2        | My Stage Length | length         | 35.5 m          |
#      | Montney | Vert_01 | 3        | My Stage Length | length         | 35.5 m          |
#      | Montney | Vert_01 | 4        | My Stage Length | length         | 35.5 m          |

#    Examples: Montney global stage sequence number
#      | field   | well    | stage_no | attribute_name                  | attribute_type | attribute_value |
#      | Montney | Hori_01 | 1        | My Global Stage Sequence Number | integer        | 4               |
#      | Montney | Hori_01 | 15       | My Global Stage Sequence Number | integer        | 73              |
#      | Montney | Hori_01 | 6        | My Global Stage Sequence Number | integer        | 12              |
#      | Montney | Hori_01 | 11       | My Global Stage Sequence Number | integer        | 24              |
#      | Montney | Hori_02 | 1        | My Global Stage Sequence Number | integer        | 1               |
#      | Montney | Hori_02 | 29       | My Global Stage Sequence Number | integer        | 70              |
#      | Montney | Hori_02 | 14       | My Global Stage Sequence Number | integer        | 43              |
#      | Montney | Hori_02 | 22       | My Global Stage Sequence Number | integer        | 59              |
#      | Montney | Hori_03 | 1        | My Global Stage Sequence Number | integer        | 4               |
#      | Montney | Hori_03 | 28       | My Global Stage Sequence Number | integer        | 76              |
#      | Montney | Hori_03 | 12       | My Global Stage Sequence Number | integer        | 42              |
#      | Montney | Hori_03 | 21       | My Global Stage Sequence Number | integer        | 60              |
#      | Montney | Vert_01 | 1        | My Global Stage Sequence Number | integer        | 2               |
#      | Montney | Vert_01 | 2        | My Global Stage Sequence Number | integer        | 14              |
#      | Montney | Vert_01 | 3        | My Global Stage Sequence Number | integer        | 16              |
#      | Montney | Vert_01 | 4        | My Global Stage Sequence Number | integer        | 18              |
