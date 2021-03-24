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

Feature: Adapted IMonitor DOM API
  As a data engineer,
  I want to access Orchid monitors conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get monitor start and stop times
    Given I have loaded the project for the field, '<field>'
    When I query the monitor start and stop times for '<field>'
    Then I see the <start> and <stop> times for the monitor at <index>

    Examples: Bakken
      | field  | index | start                        | stop                         |
      | Bakken | 0     | 2018-06-06T06:57:39.0728704Z | 2018-06-08T18:41:57.6818816Z |
      | Bakken | 1     | 2018-06-08T10:01:14.0478464Z | 2018-06-12T08:31:14.5422336Z |
      | Bakken | 2     | 2018-06-08T14:30:09.6954368Z | 2018-06-12T12:40:58.0000000Z |
      | Bakken | 3     | 2018-06-12T02:58:49.9896192Z | 2018-06-16T10:44:37.1484416Z |
      | Bakken | 4     | 2018-06-16T04:46:26.0778752Z | 2018-06-19T01:00:07.3059072Z |
      | Bakken | 5     | 2018-06-16T08:05:09.6496640Z | 2018-06-19T04:36:34.6289024Z |
      | Bakken | 6     | 2018-06-18T21:54:39.0344192Z | 2018-06-22T18:31:17.2888192Z |
      | Bakken | 7     | 2018-06-22T13:05:04.2663552Z | 2018-06-25T08:51:22.6538112Z |
      | Bakken | 8     | 2018-06-22T16:24:09.5910656Z | 2018-06-25T11:39:06.6796928Z |
      | Bakken | 9     | 2018-06-25T05:46:56.1804160Z | 2018-06-29T00:10:52.0385792Z |
      | Bakken | 10    | 2018-06-28T12:43:08.3789056Z | 2018-07-07T03:13:05.0000000Z |
      | Bakken | 11    | 2018-06-28T18:30:42.1874944Z | 2018-07-07T03:13:05.0000000Z |
      | Bakken | 12    | 2018-06-07T16:35:02.0000000Z | 2018-06-29T11:52:22.0000000Z |

    Examples: Montney
      | field   | index | start                        | stop                         |
      | Montney | 0     | 2018-04-06T16:44:00.0000000Z | 2018-04-10T03:20:00.0000000Z |
      | Montney | 1     | 2018-04-06T13:30:00.0000000Z | 2018-04-09T22:06:00.0000000Z |
