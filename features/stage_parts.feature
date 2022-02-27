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

Feature: High-level DOM API (stage part)
  As a data engineer,
  I want to access Orchid stage parts conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get the identifying information for each stage part in a project
    Given I have loaded the project for the field, '<field>'
    When I query the stage parts for well, <well>, and stage, <stage_no>, of the project
    Then I see <part_no>, <name>, <display_name>, <display_name_with_well>, and <display_name_without_well>

    Examples: Bakken
      | field  | well    | stage_no | part_no | name     | display_name | display_name_with_well | display_name_without_well |
      | bakken | Demo_1H | 1        | 0       | Stage-1  | Stage-1      | Demo_1H-Stage-1        | Stage-1                   |
      | bakken | Demo_1H | 9        | 0       | Stage-9  | Stage-9      | Demo_1H-Stage-9        | Stage-9                   |
      | bakken | Demo_1H | 31       | 0       | Stage-31 | Stage-31     | Demo_1H-Stage-31       | Stage-31                  |
      | bakken | Demo_1H | 50       | 0       | Stage-50 | Stage-50     | Demo_1H-Stage-50       | Stage-50                  |
      | bakken | Demo_2H | 1        | 0       | Stage-1  | Stage-1      | Demo_2H-Stage-1        | Stage-1                   |
      | bakken | Demo_2H | 15       | 0       | Stage-15 | Stage-15     | Demo_2H-Stage-15       | Stage-15                  |
      | bakken | Demo_2H | 42       | 0       | Stage-42 | Stage-42     | Demo_2H-Stage-42       | Stage-42                  |
      | bakken | Demo_2H | 50       | 0       | Stage-50 | Stage-50     | Demo_2H-Stage-50       | Stage-50                  |
      | bakken | Demo_4H | 1        | 0       | Stage-1  | Stage-1      | Demo_4H-Stage-1        | Stage-1                   |
      | bakken | Demo_4H | 18       | 0       | Stage-18 | Stage-18     | Demo_4H-Stage-18       | Stage-18                  |
      | bakken | Demo_4H | 28       | 0       | Stage-28 | Stage-28     | Demo_4H-Stage-28       | Stage-28                  |
      | bakken | Demo_4H | 35       | 0       | Stage-35 | Stage-35     | Demo_4H-Stage-35       | Stage-35                  |

    Examples: Montney
      | field   | well    | stage_no | part_no | name     | display_name | display_name_with_well | display_name_without_well |
      | montney | Hori_01 | 1        | 0       | Stage-1  | Stage-1      | Hori_01-Stage-1        | Stage-1                   |
      | montney | Hori_01 | 4        | 0       | Stage-4  | Stage-4      | Hori_01-Stage-4        | Stage-4                   |
      | montney | Hori_01 | 11       | 0       | Stage-11 | Stage-11     | Hori_01-Stage-11       | Stage-11                  |
      | montney | Hori_01 | 15       | 0       | Stage-15 | Stage-15     | Hori_01-Stage-15       | Stage-15                  |
      | montney | Hori_02 | 1        | 0       | Stage-1  | Stage-1      | Hori_02-Stage-1        | Stage-1                   |
      | montney | Hori_02 | 14       | 0       | Stage-14 | Stage-14     | Hori_02-Stage-14       | Stage-14                  |
      | montney | Hori_02 | 21       | 0       | Stage-21 | Stage-21     | Hori_02-Stage-21       | Stage-21                  |
      | montney | Hori_02 | 29       | 0       | Stage-29 | Stage-29     | Hori_02-Stage-29       | Stage-29                  |
      | montney | Hori_03 | 1        | 0       | Stage-1  | Stage-1      | Hori_03-Stage-1        | Stage-1                   |
      | montney | Hori_03 | 13       | 0       | Stage-13 | Stage-13     | Hori_03-Stage-13       | Stage-13                  |
      | montney | Hori_03 | 19       | 0       | Stage-19 | Stage-19     | Hori_03-Stage-19       | Stage-19                  |
      | montney | Hori_03 | 28       | 0       | Stage-28 | Stage-28     | Hori_03-Stage-28       | Stage-28                  |
      | montney | Vert_01 | 1        | 0       | Stage-1  | Stage-1      | Vert_01-Stage-1        | Stage-1                   |
      | montney | Vert_01 | 2        | 0       | Stage-2  | Stage-2      | Vert_01-Stage-2        | Stage-2                   |
      | montney | Vert_01 | 3        | 0       | Stage-3  | Stage-3      | Vert_01-Stage-3        | Stage-3                   |
      | montney | Vert_01 | 4        | 0       | Stage-4  | Stage-4      | Vert_01-Stage-4        | Stage-4                   |

  Scenario Outline: Get the details for each stage part in a project
    Given I have loaded the project for the field, '<field>'
    When I query the stage parts for well, <well>, and stage, <stage_no>, of the project
    Then I see <part_no>, <start_time>, <stop_time>, and <isip>

    Examples: Bakken
      | field  | well    | stage_no | part_no | start_time               | stop_time                | isip         |
      | bakken | Demo_1H | 1        | 0       | 2018-06-06T13:37:13.273Z | 2018-06-06T16:55:21.743Z | 4748.924 psi |
      | bakken | Demo_1H | 9        | 0       | 2018-06-12T12:40:58.000Z | 2018-06-12T15:12:32.000Z | 5085.0 psi   |
      | bakken | Demo_1H | 31       | 0       | 2018-06-21T11:52:55.268Z | 2018-06-21T13:34:13.070Z | 5240.0 psi   |
      | bakken | Demo_1H | 50       | 0       | 2018-06-28T12:43:08.378Z | 2018-06-28T13:52:37.360Z | 5177.0 psi   |
      | bakken | Demo_2H | 1        | 0       | 2018-06-06T06:57:39.072Z | 2018-06-06T09:11:00.113Z | 4778.533 psi |
      | bakken | Demo_2H | 15       | 0       | 2018-06-16T10:44:37.148Z | 2018-06-16T12:56:20.218Z | 5125.056 psi |
      | bakken | Demo_2H | 42       | 0       | 2018-06-25T02:33:37.584Z | 2018-06-25T03:46:23.825Z | 5200.0 psi   |
      | bakken | Demo_2H | 50       | 0       | 2018-06-29T23:48:10.173Z | 2018-06-30T01:24:49.306Z | 5324.0 psi   |
      | bakken | Demo_4H | 1        | 0       | 2018-06-06T09:43:37.053Z | 2018-06-06T11:56:26.370Z | 4800.49 psi  |
      | bakken | Demo_4H | 18       | 0       | 2018-06-19T16:18:05.559Z | 2018-06-19T18:51:50.449Z | 5199.172 psi |
      | bakken | Demo_4H | 28       | 0       | 2018-06-26T07:30:49.713Z | 2018-06-26T09:43:52.708Z | 5150.0 psi   |
      | bakken | Demo_4H | 35       | 0       | 2018-06-28T18:30:42.187Z | 2018-06-28T20:32:57.209Z | 5178.0 psi   |

    Examples: Montney
      | field   | well    | stage_no | part_no | start_time               | stop_time                | isip     |
      | montney | Hori_01 | 1        | 0       | 2018-04-06T18:09:28.000Z | 2018-04-06T21:14:58.000Z | 69.2 kPa |
      | montney | Hori_01 | 4        | 0       | 2018-04-08T03:45:00.000Z | 2018-04-08T07:16:00.000Z | 32.0 kPa |
      | montney | Hori_01 | 11       | 0       | 2018-04-12T03:03:28.000Z | 2018-04-12T05:29:28.000Z | 30.6 kPa |
      | montney | Hori_01 | 15       | 0       | 2018-04-19T19:47:22.000Z | 2018-04-19T22:41:54.000Z | 28.9 kPa |
      | montney | Hori_02 | 1        | 0       | 2018-04-06T10:40:00.000Z | 2018-04-06T13:30:00.000Z | 31.3 kPa |
      | montney | Hori_02 | 14       | 0       | 2018-04-15T08:16:00.000Z | 2018-04-15T10:06:00.000Z | 32.1 kPa |
      | montney | Hori_02 | 21       | 0       | 2018-04-17T12:18:30.000Z | 2018-04-17T13:35:55.000Z | 34.5 kPa |
      | montney | Hori_02 | 29       | 0       | 2018-04-19T10:13:14.000Z | 2018-04-19T11:21:07.000Z | 34.1 kPa |
      | montney | Hori_03 | 1        | 0       | 2018-04-06T21:29:15.000Z | 2018-04-07T00:29:35.000Z | 30.0 kPa |
      | montney | Hori_03 | 13       | 0       | 2018-04-15T14:16:00.000Z | 2018-04-15T18:00:45.000Z | 29.4 kPa |
      | montney | Hori_03 | 19       | 0       | 2018-04-17T10:28:29.000Z | 2018-04-17T12:01:05.000Z | 31.7 kPa |
      | montney | Hori_03 | 28       | 0       | 2018-04-20T11:31:35.000Z | 2018-04-20T12:50:34.000Z | 31.7 kPa |
      | montney | Vert_01 | 1        | 0       | 2018-04-06T13:59:00.000Z | 2018-04-06T16:44:00.000Z | 33.5 kPa |
      | montney | Vert_01 | 2        | 0       | 2018-04-10T03:20:00.000Z | 2018-04-10T06:38:00.000Z | 33.1 kPa |
      | montney | Vert_01 | 3        | 0       | 2018-04-10T12:37:14.000Z | 2018-04-10T15:24:41.000Z | 32.1 kPa |
      | montney | Vert_01 | 4        | 0       | 2018-04-10T18:41:50.000Z | 2018-04-10T20:29:35.000Z | 32.2 kPa |

