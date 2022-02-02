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

#    Examples: Montney
#      | field   | display_name       | index  | qty_name    | time                         | value        |
#      | Montney | Hori_01-Downhole-0 | 0      | Pressure    | 2018-04-05T10:01:07.0000000Z | 20665.11 kPa |
#      | Montney | Hori_01-Downhole-0 | 14848  | Pressure    | 2018-04-05T14:16:39.0000000Z | 18562.68 kPa |
#      | Montney | Hori_01-Downhole-0 | 67025  | Pressure    | 2018-04-06T05:11:54.0000000Z | 15446.07 kPa |
#      | Montney | Hori_01-Downhole-0 | 138193 | Pressure    | 2018-04-07T01:34:01.0000000Z | 27726.53 kPa |
#      | Montney | Hori_01-Downhole-0 | 196604 | Pressure    | 2018-04-07T18:18:33.0000000Z | 27965.21 kPa |
#      | Montney | Hori_01-Downhole-0 | 252497 | Pressure    | 2018-04-08T10:17:31.0000000Z | 27131.21 kPa |
#      | Montney | Hori_01-Downhole-0 | 256716 | Pressure    | 2018-04-08T11:30:10.0000000Z | 34203.43 kPa |
#      | Montney | Hori_01-Downhole-0 | 325041 | Pressure    | 2018-04-09T07:06:53.0000000Z | 26835 kPa    |
#      | Montney | Hori_01-Downhole-0 | 0      | Temperature | 2018-04-05T10:01:07.0000000Z | -11.79 degC  |
#      | Montney | Hori_01-Downhole-0 | 21207  | Temperature | 2018-04-05T16:05:12.0000000Z | 1.48 degC    |
#      | Montney | Hori_01-Downhole-0 | 131030 | Temperature | 2018-04-06T23:31:32.0000000Z | -0.99 degC   |
#      | Montney | Hori_01-Downhole-0 | 144783 | Temperature | 2018-04-07T03:27:25.0000000Z | -9.48 degC   |
#      | Montney | Hori_01-Downhole-0 | 275515 | Temperature | 2018-04-08T16:53:34.0000000Z | -1012 degC   |
#      | Montney | Hori_01-Downhole-0 | 276326 | Temperature | 2018-04-08T17:07:14.0000000Z | 11.61 degC   |
#      | Montney | Hori_01-Downhole-0 | 321067 | Temperature | 2018-04-09T05:57:57.0000000Z | -0.67 degC   |
#      | Montney | Hori_01-Downhole-0 | 325041 | Temperature | 2018-04-09T07:06:53.0000000Z | -0.83 degC   |
#      | Montney | Hori_02-Downhole-0 | 0      | Pressure    | 2018-04-05T09:26:03.0000000Z | 16136.97 kPa |
#      | Montney | Hori_02-Downhole-0 | 57362  | Pressure    | 2018-04-06T01:34:42.0000000Z | 15442.79 kPa |
#      | Montney | Hori_02-Downhole-0 | 75454  | Pressure    | 2018-04-06T06:41:19.0000000Z | 15317.41 kPa |
#      | Montney | Hori_02-Downhole-0 | 77095  | Pressure    | 2018-04-06T07:08:44.0000000Z | 15308.05 kPa |
#      | Montney | Hori_02-Downhole-0 | 230565 | Pressure    | 2018-04-08T02:21:39.0000000Z | 15575.36 kPa |
#      | Montney | Hori_02-Downhole-0 | 242309 | Pressure    | 2018-04-08T05:39:08.0000000Z | 15178.11 kPa |
#      | Montney | Hori_02-Downhole-0 | 311658 | Pressure    | 2018-04-09T01:12:25.0000000Z | 13830.99 kPa |
#      | Montney | Hori_02-Downhole-0 | 332477 | Pressure    | 2018-04-09T07:04:03.0000000Z | 13540.6 kPa  |
#      | Montney | Hori_02-Downhole-0 | 0      | Temperature | 2018-04-05T09:26:03.0000000Z | -12.7 degC   |
#      | Montney | Hori_02-Downhole-0 | 14635  | Temperature | 2018-04-05T13:33:38.0000000Z | 3.64 degC    |
#      | Montney | Hori_02-Downhole-0 | 118229 | Temperature | 2018-04-06T18:44:06.0000000Z | 1.8 degC     |
#      | Montney | Hori_02-Downhole-0 | 119021 | Temperature | 2018-04-06T18:57:21.0000000Z | 1.74 degC    |
#      | Montney | Hori_02-Downhole-0 | 136730 | Temperature | 2018-04-06T23:56:35.0000000Z | -1.48 degC   |
#      | Montney | Hori_02-Downhole-0 | 154389 | Temperature | 2018-04-07T04:53:40.0000000Z | -10.14 degC  |
#      | Montney | Hori_02-Downhole-0 | 283266 | Temperature | 2018-04-08T17:13:06.0000000Z | 6.45 degC    |
#      | Montney | Hori_02-Downhole-0 | 332477 | Temperature | 2018-04-09T07:04:03.0000000Z | 1.65 degC    |
#      | Montney | Hori_03-Downhole-0 | 0      | Pressure    | 2018-04-05T10:00:19.0000000Z | 13434.1 kPa  |
#      | Montney | Hori_03-Downhole-0 | 17858  | Pressure    | 2018-04-05T15:04:57.0000000Z | 13413.82 kPa |
#      | Montney | Hori_03-Downhole-0 | 94644  | Pressure    | 2018-04-06T12:57:11.0000000Z | 13301.95 kPa |
#      | Montney | Hori_03-Downhole-0 | 98895  | Pressure    | 2018-04-06T14:10:13.0000000Z | 13297.05 kPa |
#      | Montney | Hori_03-Downhole-0 | 105291 | Pressure    | 2018-04-06T15:59:17.0000000Z | 13288.75 kPa |
#      | Montney | Hori_03-Downhole-0 | 124265 | Pressure    | 2018-04-06T21:22:16.0000000Z | 13691.07 kPa |
#      | Montney | Hori_03-Downhole-0 | 157027 | Pressure    | 2018-04-07T06:41:22.0000000Z | 26739.18 kPa |
#      | Montney | Hori_03-Downhole-0 | 323523 | Pressure    | 2018-04-09T07:02:35.0000000Z | 26358.15 kPa |
#      | Montney | Hori_03-Downhole-0 | 0      | Temperature | 2018-04-05T10:00:19.0000000Z | -3.44 degC   |
#      | Montney | Hori_03-Downhole-0 | 3925   | Temperature | 2018-04-05T11:07:46.0000000Z | -4.49 degC   |
#      | Montney | Hori_03-Downhole-0 | 9783   | Temperature | 2018-04-05T12:47:32.0000000Z | 0.84 degC    |
#      | Montney | Hori_03-Downhole-0 | 47158  | Temperature | 2018-04-05T23:24:29.0000000Z | -11.73 degC  |
#      | Montney | Hori_03-Downhole-0 | 88961  | Temperature | 2018-04-06T11:20:08.0000000Z | -10.15 degC  |
#      | Montney | Hori_03-Downhole-0 | 170895 | Temperature | 2018-04-07T10:35:40.0000000Z | -5.32 degC   |
#      | Montney | Hori_03-Downhole-0 | 246659 | Temperature | 2018-04-08T08:06:47.0000000Z | -3.09 degC   |
#      | Montney | Hori_03-Downhole-0 | 323523 | Temperature | 2018-04-09T07:02:35.0000000Z | -3.65 degC   |
#      | Montney | Vert_01-Downhole-0 | 0      | Pressure    | 2018-04-05T10:24:12.0000000Z | 19459.03 kPa |
#      | Montney | Vert_01-Downhole-0 | 6652   | Pressure    | 2018-04-05T12:19:34.0000000Z | 19061.51 kPa |
#      | Montney | Vert_01-Downhole-0 | 90175  | Pressure    | 2018-04-06T12:16:56.0000000Z | 16491.47 kPa |
#      | Montney | Vert_01-Downhole-0 | 134841 | Pressure    | 2018-04-07T01:09:16.0000000Z | 25115.39 kPa |
#      | Montney | Vert_01-Downhole-0 | 211515 | Pressure    | 2018-04-07T23:10:44.0000000Z | 16361.86 kPa |
#      | Montney | Vert_01-Downhole-0 | 222007 | Pressure    | 2018-04-08T02:11:20.0000000Z | 15895.58 kPa |
#      | Montney | Vert_01-Downhole-0 | 300671 | Pressure    | 2018-04-09T00:49:23.0000000Z | 14088.72 kPa |
#      | Montney | Vert_01-Downhole-0 | 322124 | Pressure    | 2018-04-09T06:59:16.0000000Z | 13859.02 kPa |
#      | Montney | Vert_01-Downhole-0 | 0      | Temperature | 2018-04-05T10:24:12.0000000Z | -6.38 degC   |
#      | Montney | Vert_01-Downhole-0 | 34549  | Temperature | 2018-04-05T20:20:56.0000000Z | -7.49 degC   |
#      | Montney | Vert_01-Downhole-0 | 89295  | Temperature | 2018-04-06T12:01:51.0000000Z | -5.73 degC   |
#      | Montney | Vert_01-Downhole-0 | 111788 | Temperature | 2018-04-06T18:30:28.0000000Z | -0.88 degC   |
#      | Montney | Vert_01-Downhole-0 | 209284 | Temperature | 2018-04-07T22:32:44.0000000Z | 3.11 degC    |
#      | Montney | Vert_01-Downhole-0 | 232331 | Temperature | 2018-04-08T05:10:26.0000000Z | 2.11 degC    |
#      | Montney | Vert_01-Downhole-0 | 300439 | Temperature | 2018-04-09T00:44:44.0000000Z | 7.68 degC    |
#      | Montney | Vert_01-Downhole-0 | 322124 | Temperature | 2018-04-09T06:59:16.0000000Z | 3.61 degC    |
