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

Feature: Adapted IMonitor DOM API
  As a data engineer,
  I want to access Orchid monitors conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get monitor identified by object ID
    Given I have loaded the project for the field, '<field>'
    When I query the monitor identified by object ID, <object_id>, for the project for '<field>'
    Then I see the <object_id>, <start_time> and <stop_time> for the queried monitor

    Examples: Bakken
      | field  | object_id                            | start_time                   | stop_time                    |
      | Bakken | 5b68d8c4-a578-44e7-bc08-b1d83483c4ec | 2018-06-06T06:57:39.0728704Z | 2018-06-08T18:41:57.6818816Z |
      | Bakken | 4116e3d3-b1ba-4063-b41e-467c5c00eb20 | 2018-06-08T10:01:14.0478464Z | 2018-06-12T08:31:14.5422336Z |
      | Bakken | 8fab7763-8cad-42f4-8d44-899f2e8691bc | 2018-06-08T14:30:09.6954368Z | 2018-06-12T12:40:58.0000000Z |
      | Bakken | 8660a506-e2a3-4427-8a03-d20e60c214df | 2018-06-12T02:58:49.9896192Z | 2018-06-16T10:44:37.1484416Z |
      | Bakken | 9d702765-5696-4b38-a54c-84813898f907 | 2018-06-16T04:46:26.0778752Z | 2018-06-19T01:00:07.3059072Z |
      | Bakken | 182fa5d0-5695-40e8-ad59-ed18e796ee9c | 2018-06-16T08:05:09.6496640Z | 2018-06-19T04:36:34.6289024Z |
      | Bakken | c1d35d86-a8a1-4e46-a303-f2f1011a399f | 2018-06-18T21:54:39.0344192Z | 2018-06-22T18:31:17.2888192Z |
      | Bakken | be89b07b-e37f-4222-9759-acd5682dc7a0 | 2018-06-22T13:05:04.2663552Z | 2018-06-25T08:51:22.6538112Z |
      | Bakken | 14607f23-95f4-4405-b34b-daa0f924c2be | 2018-06-22T16:24:09.5910656Z | 2018-06-25T11:39:06.6796928Z |
      | Bakken | 6777b2fe-7575-4fed-a82a-bb0b0085152d | 2018-06-25T05:46:56.1804160Z | 2018-06-29T00:10:52.0385792Z |
      | Bakken | 5e51285b-6ac9-4a23-a360-f56399e4fe6b | 2018-06-28T12:43:08.3789056Z | 2018-07-07T03:13:05.0000000Z |
      | Bakken | 44e7ad1c-f6b9-411c-84c3-fa903b1a516c | 2018-06-28T18:30:42.1874944Z | 2018-07-07T03:13:05.0000000Z |
      | Bakken | 6b024601-ef74-4a82-ae4a-2a91648cae07 | 2018-06-07T16:35:02.0000000Z | 2018-06-29T11:52:22.0000000Z |

    Examples: Montney
      | field   | object_id                            | start_time                   | stop_time                    |
      | Montney | ad002ac7-c2e5-44d4-b3cc-fca9ad84d10e | 2018-04-06T16:44:00.0000000Z | 2018-04-10T03:20:00.0000000Z |
      | Montney | 34fbef8a-ba84-4437-bfe4-0b78a3e12199 | 2018-04-06T13:30:00.0000000Z | 2018-04-09T22:06:00.0000000Z |

  Scenario Outline: Get monitor identified by display name
    Given I have loaded the project for the field, '<field>'
    When I query the monitor identified by display name, <display_name>, for the project for '<field>'
    Then I see the <name>, <start_time>, and <stop_time> for the queried monitor

    Examples: Bakken
      | field  | display_name          | name    | start_time                   | stop_time                    |
      | Bakken | Demo_2H - stage 1     | Demo_2H | 2018-06-06T06:57:39.0728704Z | 2018-06-08T18:41:57.6818816Z |
      | Bakken | Demo_4H - stage 6     | Demo_4H | 2018-06-08T10:01:14.0478464Z | 2018-06-12T08:31:14.5422336Z |
      | Bakken | Demo_1H - stage 8     | Demo_1H | 2018-06-08T14:30:09.6954368Z | 2018-06-12T12:40:58.0000000Z |
      | Bakken | Demo_2H - stage 14    | Demo_2H | 2018-06-12T02:58:49.9896192Z | 2018-06-16T10:44:37.1484416Z |
      | Bakken | Demo_4H - stage 15    | Demo_4H | 2018-06-16T04:46:26.0778752Z | 2018-06-19T01:00:07.3059072Z |
      | Bakken | Demo_1H - stage 22    | Demo_1H | 2018-06-16T08:05:09.6496640Z | 2018-06-19T04:36:34.6289024Z |
      | Bakken | Demo_2H - stage 29    | Demo_2H | 2018-06-18T21:54:39.0344192Z | 2018-06-22T18:31:17.2888192Z |
      | Bakken | Demo_4H - stage 25    | Demo_4H | 2018-06-22T13:05:04.2663552Z | 2018-06-25T08:51:22.6538112Z |
      | Bakken | Demo_1H - stage 36    | Demo_1H | 2018-06-22T16:24:09.5910656Z | 2018-06-25T11:39:06.6796928Z |
      | Bakken | Demo_2H - stage 43    | Demo_2H | 2018-06-25T05:46:56.1804160Z | 2018-06-29T00:10:52.0385792Z |
      | Bakken | Demo_1H - stage 50    | Demo_1H | 2018-06-28T12:43:08.3789056Z | 2018-07-07T03:13:05.0000000Z |
      | Bakken | Demo_4H - stage 35    | Demo_4H | 2018-06-28T18:30:42.1874944Z | 2018-07-07T03:13:05.0000000Z |
      | Bakken | Demo_3H - MonitorWell | Demo_3H | 2018-06-07T16:35:02.0000000Z | 2018-06-29T11:52:22.0000000Z |

    Examples: Montney
      | field   | display_name          | name    | start_time                   | stop_time                    |
      | Montney | Vert_01 - 0 - stage 1 | Vert_01 | 2018-04-06T16:44:00.0000000Z | 2018-04-10T03:20:00.0000000Z |
      | Montney | Hori_02 - 0 - stage 1 | Hori_02 | 2018-04-06T13:30:00.0000000Z | 2018-04-09T22:06:00.0000000Z |

  Scenario Outline: Sample the well time series for a monitor
    Given I have loaded the project for the field, '<field>'
    When I query the monitor time series with <display_name>
    Then I see the samples <index>, <qty_name>, <time>, and <value> for the monitor time series

    Examples: Bakken
      | field  | display_name          | index  | qty_name | time                         | value       |
      | Bakken | Demo_1H - stage 22    | 0      | Pressure | 2018-05-27T18:46:21.0000000Z | 12.84 psi   |
      | Bakken | Demo_1H - stage 50    | 6078   | Pressure | 2018-05-29T21:25:50.0000000Z | 12.8 psi    |
      | Bakken | Demo_1H - stage 22    | 24489  | Pressure | 2018-06-05T06:51:51.0000000Z | 13.24 psi   |
      | Bakken | Demo_1H - stage 8     | 35902  | Pressure | 2018-06-09T05:59:28.0000000Z | 3072.1 psi  |
      | Bakken | Demo_1H - stage 36    | 47331  | Pressure | 2018-06-13T05:14:55.0000000Z | 5643.42 psi |
      | Bakken | Demo_1H - stage 50    | 56567  | Pressure | 2018-06-16T10:13:32.0000000Z | 4267.47 psi |
      | Bakken | Demo_1H - stage 36    | 94551  | Pressure | 2018-06-29T14:47:28.0000000Z | 3471.16 psi |
      | Bakken | Demo_1H - stage 8     | 114594 | Pressure | 2018-07-07T03:13:05.0000000Z | -7999 psi   |
      | Bakken | Demo_2H - stage 29    | 0      | Pressure | 2018-05-27T18:46:21.0000000Z | 13.21 psi   |
      | Bakken | Demo_2H - stage 14    | 1105   | Pressure | 2018-05-28T03:59:18.0000000Z | 12.42 psi   |
      | Bakken | Demo_2H - stage 1     | 14475  | Pressure | 2018-06-01T19:24:46.0000000Z | 12.75 psi   |
      | Bakken | Demo_2H - stage 29    | 18418  | Pressure | 2018-06-03T04:16:20.0000000Z | 12.52 psi   |
      | Bakken | Demo_2H - stage 1     | 33263  | Pressure | 2018-06-08T07:59:47.0000000Z | 2882.93 psi |
      | Bakken | Demo_2H - stage 14    | 83966  | Pressure | 2018-06-25T22:34:44.0000000Z | 3424.57 psi |
      | Bakken | Demo_2H - stage 43    | 87110  | Pressure | 2018-06-27T00:46:44.0000000Z | 3231.8 psi  |
      | Bakken | Demo_2H - stage 43    | 114594 | Pressure | 2018-07-07T03:13:05.0000000Z | -7999 psi   |
      | Bakken | Demo_3H - MonitorWell | 0      | Pressure | 2018-06-07T16:35:02.0000000Z | 1628.97 psi |
      | Bakken | Demo_3H - MonitorWell | 9872   | Pressure | 2018-06-11T02:53:53.0000000Z | 1278.02 psi |
      | Bakken | Demo_3H - MonitorWell | 38744  | Pressure | 2018-06-21T03:38:08.0000000Z | 900.61 psi  |
      | Bakken | Demo_3H - MonitorWell | 47718  | Pressure | 2018-06-24T06:28:34.0000000Z | 904.48 psi  |
      | Bakken | Demo_3H - MonitorWell | 58806  | Pressure | 2018-06-28T02:55:59.0000000Z | 1399.29 psi |
      | Bakken | Demo_3H - MonitorWell | 58869  | Pressure | 2018-06-28T03:27:29.0000000Z | 1964.85 psi |
      | Bakken | Demo_3H - MonitorWell | 62026  | Pressure | 2018-06-29T05:46:52.0000000Z | 2716.76 psi |
      | Bakken | Demo_3H - MonitorWell | 62757  | Pressure | 2018-06-29T11:52:22.0000000Z | 2677.54 psi |
      | Bakken | Demo_4H - stage 35    | 0      | Pressure | 2018-05-27T18:46:21.0000000Z | 13.22 psi   |
      | Bakken | Demo_4H - stage 25    | 3864   | Pressure | 2018-05-29T02:58:48.0000000Z | 12.48 psi   |
      | Bakken | Demo_4H - stage 6     | 19189  | Pressure | 2018-06-03T10:41:50.0000000Z | 13.19 psi   |
      | Bakken | Demo_4H - stage 35    | 25197  | Pressure | 2018-06-05T12:45:51.0000000Z | 13.3 psi    |
      | Bakken | Demo_4H - stage 15    | 65166  | Pressure | 2018-06-19T09:53:18.0000000Z | 4995.46 psi |
      | Bakken | Demo_4H - stage 15    | 81490  | Pressure | 2018-06-25T01:56:42.0000000Z | 2887.48 psi |
      | Bakken | Demo_4H - stage 25    | 87675  | Pressure | 2018-06-27T05:29:14.0000000Z | 3743.04 psi |
      | Bakken | Demo_4H - stage 6     | 114594 | Pressure | 2018-07-07T03:13:05.0000000Z | -7999 psi   |

    Examples: Montney
      | field   | display_name         | index  | qty_name | time                         | value        |
      | Montney | Hori_02 - 0 - stage 1 | 0      | Pressure | 2018-04-05T09:26:03.0000000Z | 16136.97 kPa |
      | Montney | Hori_02 - 0 - stage 1 | 57362  | Pressure | 2018-04-06T01:34:42.0000000Z | 15442.79 kPa |
      | Montney | Hori_02 - 0 - stage 1 | 75454  | Pressure | 2018-04-06T06:41:19.0000000Z | 15317.41 kPa |
      | Montney | Hori_02 - 0 - stage 1 | 77095  | Pressure | 2018-04-06T07:08:44.0000000Z | 15308.05 kPa |
      | Montney | Hori_02 - 0 - stage 1 | 230565 | Pressure | 2018-04-08T02:21:39.0000000Z | 15575.36 kPa |
      | Montney | Hori_02 - 0 - stage 1 | 242309 | Pressure | 2018-04-08T05:39:08.0000000Z | 15178.11 kPa |
      | Montney | Hori_02 - 0 - stage 1 | 311658 | Pressure | 2018-04-09T01:12:25.0000000Z | 13830.99 kPa |
      | Montney | Hori_02 - 0 - stage 1 | 332477 | Pressure | 2018-04-09T07:04:03.0000000Z | 13540.6 kPa  |
      | Montney | Vert_01 - 0 - stage 1 | 0      | Pressure | 2018-04-05T10:24:12.0000000Z | 19459.03 kPa |
      | Montney | Vert_01 - 0 - stage 1 | 6652   | Pressure | 2018-04-05T12:19:34.0000000Z | 19061.51 kPa |
      | Montney | Vert_01 - 0 - stage 1 | 90175  | Pressure | 2018-04-06T12:16:56.0000000Z | 16491.47 kPa |
      | Montney | Vert_01 - 0 - stage 1 | 134841 | Pressure | 2018-04-07T01:09:16.0000000Z | 25115.39 kPa |
      | Montney | Vert_01 - 0 - stage 1 | 211515 | Pressure | 2018-04-07T23:10:44.0000000Z | 16361.86 kPa |
      | Montney | Vert_01 - 0 - stage 1 | 222007 | Pressure | 2018-04-08T02:11:20.0000000Z | 15895.58 kPa |
      | Montney | Vert_01 - 0 - stage 1 | 300671 | Pressure | 2018-04-09T00:49:23.0000000Z | 14088.72 kPa |
      | Montney | Vert_01 - 0 - stage 1 | 322124 | Pressure | 2018-04-09T06:59:16.0000000Z | 13859.02 kPa |
