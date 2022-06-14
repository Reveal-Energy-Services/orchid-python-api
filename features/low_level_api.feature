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
#    When I create a stage attribute named '<My Stage Length>' for a(n) <length_measurement> value
#    And I create a stage attribute named '<My Global Stage Sequence Number>' for a(n) <integer> value
#    And I add the created attributes to the well, '<well>', of the project
    And I set the attribute value of '<attribute_name>' of stage, <stage_no>, of '<well>' to the <attribute_value>
#    And I set the value of the stage length attribute of stage, <stage_no>, of '<well>' to the <length>
#    And I set the value of the sequence number attribute of stage, <stage_no>, of '<well>' to <global_seq_no>
#    Then I see the value of the stage length attribute of stage, <stage_no>, of '<well>' equals <length>
#    And I see the value of the sequence number attribute for stage, <stage_no>, of '<well>' equal to <global_seq_no>
    Then I see the attribute value of '<attribute_name>' of stage, <stage_no>, of '<well>' equals <attribute_value>

    Examples: Bakken stage length
      | field  | well    | stage_no | attribute_name  | attribute_type | attribute_value |
      | Bakken | Demo_1H | 1        | My Stage Length | length         | 50.66 ft        |

    Examples: Bakken global stage sequence number
      | field  | well    | stage_no | attribute_name                  | attribute_type | attribute_value |
      | Bakken | Demo_1H | 1        | My Global Stage Sequence Number | integer        | 4               |

    Examples: Montney stage length
      | field   | well    | stage_no | attribute_name  | attribute_type | attribute_value |
      | Montney | Hori_01 | 1        | My Stage Length | length         | 174.5 m         |

    Examples: Montney global stage sequence number
      | field   | well    | stage_no | attribute_name                  | attribute_type | attribute_value |
      | Montney | Hori_01 | 1        | My Global Stage Sequence Number | integer        | 4               |

#    Examples: Bakken
#      | field  | well    | stage_no | length    | global_seq_no |
#      | Bakken | Demo_1H | 1        | 50.66 ft  | 4             |
#      | Bakken | Demo_1H | 50       | 147.11 ft | 128           |
#      | Bakken | Demo_1H | 4        | 147.22 ft | 10            |
#      | Bakken | Demo_2H | 1        | 147.22 ft | 2             |
#      | Bakken | Demo_2H | 50       | 75.08 ft  | 136           |
#      | Bakken | Demo_2H | 35       | 147.15 ft | 97            |
#      | Bakken | Demo_2H | 13       | 148.05 ft | 28            |
#      | Bakken | Demo_4H | 1        | 148.05 ft | 3             |
#      | Bakken | Demo_4H | 35       | 65.93 ft  | 129           |
#      | Bakken | Demo_4H | 29       | 225.00 ft | 114           |
#      | Bakken | Demo_4H | 6        | 245.00 ft | 15            |
#
#    Examples: Montney
#      | field   | well    | stage_no | length  | global_seq_no |
#      | Montney | Hori_01 | 1        | 174.5 m | 3             |
#      | Montney | Hori_01 | 15       | 175.5 m | 73            |
#      | Montney | Hori_01 | 6        | 174.5 m | 12            |
#      | Montney | Hori_01 | 11       | 174.5 m | 24            |
#      | Montney | Hori_02 | 1        | 39.0 m  | 1             |
#      | Montney | Hori_02 | 29       | 72.0 m  | 70            |
#      | Montney | Hori_02 | 14       | 72.5 m  | 43            |
#      | Montney | Hori_02 | 22       | 72.5 m  | 59            |
#      | Montney | Hori_03 | 1        | 75.5 m  | 4             |
#      | Montney | Hori_03 | 28       | 75.5 m  | 76            |
#      | Montney | Hori_03 | 12       | 75.5 m  | 42            |
#      | Montney | Hori_03 | 21       | 75.5 m  | 60            |
#      | Montney | Vert_01 | 1        | 35.5 m  | 2             |
#      | Montney | Vert_01 | 2        | 35.5 m  | 14            |
#      | Montney | Vert_01 | 3        | 35.5 m  | 16            |
#      | Montney | Vert_01 | 4        | 35.5 m  | 18            |