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

Feature: Low-level DOM API (project)
  As a data engineer,
  I want to access Orchid projects conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get the name of a project
    Given I have loaded a project from the file, '<filename>'
    When I query the project name
    Then I see the text "<project>"
    Examples:
      | filename                                       | project                                 |
      | frankNstein_Bakken_UTM13_FEET.ifrac            | frankNstein_Bakken_UTM13_FEET           |
      | Project_frankNstein_Permian_UTM13_FEET.ifrac   | Project_frankNstein_subset02_UTM13_FEET |
      | Project-frankNstein_Montney_UTM13_METERS.ifrac | Project-frankNstein                     |

  Scenario Outline: Get project measurements in project units
    Given I have loaded the project for the field, '<field>'
    When I query the project measurements
    Then I see project measurements <fluid_density>, <azimuth>, <center_x>, and <center_y>

    Examples: Bakken
      | field  | fluid_density | azimuth   | center_x   | center_y   |
      | Bakken | 63.20 lb/ft^3 | 50.00 deg | 1.990e6 ft | 17.50e6 ft |

    Examples: Montney
      | field   | fluid_density | azimuth   | center_x  | center_y  |
      | Montney | 1012 kg/m^3   | 90.00 deg | 657.2e3 m | 6.179e6 m |

  Scenario Outline: Get project bounds in project units
    Given I have loaded the project for the field, '<field>'
    When I query the project bounds
    Then I see project bounds <min_x>, <max_x>, <min_y>, <max_y>, <min_depth>, and <max_depth>,

    Examples: Bakken
      | field  | min_x      | max_x      | min_y       | max_y       | min_depth | max_depth |
      | Bakken | 1979381 ft | 1990412 ft | 17495687 ft | 17498048 ft | 0 ft       | 10773 ft  |

    Examples: Montney
      | field   | min_x    | max_x    | min_y     | max_y     | min_depth | max_depth |
      | Montney | 656540 m | 659106 m | 6177242 m | 6179349 m | -728.0 m  | 1972 m    |

    Examples: Permian
      | field   | min_x      | max_x      | min_y       | max_y       | min_depth | max_depth |
      | Permian | 2141174 ft | 2142179 ft | 11664081 ft | 11669346 ft | -2872 ft  | 11749 ft  |

  Scenario Outline: Get the well counts from a project
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    Then I see that the project, <project>, has <well count> wells

    Examples: Bakken
      | field   | project                                 | well count |
      | Bakken  | frankNstein_Bakken_UTM13_FEET           | 4          |
      | Permian | Project_frankNstein_subset02_UTM13_FEET | 4          |
      | Montney | Project-frankNstein                     | 4          |

  Scenario Outline: Get the wells from a project
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    Then I see the well details <well>, <display name>, and <uwi> for <object id>

    Examples: Bakken
      | field  | well    | display name | uwi    | object id                            |
      | Bakken | Demo_1H | Demo_1H      | No UWI | ce9290bd-f9f1-45c2-b8c8-77b672ec0c43 |
      | Bakken | Demo_2H | Demo_2H      | No UWI | 22afba22-6be4-460d-9b83-a43b8b1eec11 |
      | Bakken | Demo_3H | Demo_3H      | No UWI | 5af7a14e-b7c9-4662-ba95-5ce3a0c39f60 |
      | Bakken | Demo_4H | Demo_4H      | No UWI | 9fe727b0-5fd1-4240-b475-51c1363edb0d |

    Examples: Permian
      | field   | well | display name | uwi    | object id                            |
      | Permian | C1   | C1           | No UWI | 5d11747e-b121-4bdb-8ff6-a3131aafa8e1 |
      | Permian | C2   | C2           | No UWI | 8d5ae42a-28aa-4e1f-9947-3b5511ac3143 |
      | Permian | C3   | C3           | No UWI | d44f70be-b77b-4da6-80d1-5edc76d98839 |
      | Permian | P1   | P1           | No UWI | 918a9c53-63a9-405d-bd03-f43422e0a4c4 |

    Examples: Montney
      | field   | well    | display name | uwi    | object id                            |
      | Montney | Hori_01 | Hori_01      | No UWI | c5eeddd4-62a8-4ab6-a630-bccd7ea629af |
      | Montney | Hori_02 | Hori_02      | No UWI | 1b1689dc-d46f-433f-ada8-a6fb58380954 |
      | Montney | Hori_03 | Hori_03      | No UWI | 40bd58a0-28f5-4af1-8f39-f40c3ebcb8c8 |
      | Montney | Vert_01 | Vert_01      | No UWI | 7f38537e-293b-4b88-8b85-099b28e43c6e |

  Scenario Outline: Sample the well time series for a project
    Given I have loaded the project for the field, '<field>'
    When I query the project well time series
    Then I see the samples <index>, <qty_name>, <time>, and <value> for <name>

    Examples: Bakken
      | field  | name                | index  | qty_name | time                         | value       |
      | Bakken | MonitorData-Demo_1H | 0      | Pressure | 2018-05-27T18:46:21.0000000Z | 12.84 psi   |
      | Bakken | MonitorData-Demo_1H | 6078   | Pressure | 2018-05-29T21:25:50.0000000Z | 12.8 psi    |
      | Bakken | MonitorData-Demo_1H | 24489  | Pressure | 2018-06-05T06:51:51.0000000Z | 13.24 psi   |
      | Bakken | MonitorData-Demo_1H | 35902  | Pressure | 2018-06-09T05:59:28.0000000Z | 3072.1 psi  |
      | Bakken | MonitorData-Demo_1H | 47331  | Pressure | 2018-06-13T05:14:55.0000000Z | 5643.42 psi |
      | Bakken | MonitorData-Demo_1H | 56567  | Pressure | 2018-06-16T10:13:32.0000000Z | 4267.47 psi |
      | Bakken | MonitorData-Demo_1H | 94551  | Pressure | 2018-06-29T14:47:28.0000000Z | 3471.16 psi |
      | Bakken | MonitorData-Demo_1H | 114594 | Pressure | 2018-07-07T03:13:05.0000000Z | -7999 psi   |
      | Bakken | MonitorData-Demo_2H | 0      | Pressure | 2018-05-27T18:46:21.0000000Z | 13.21 psi   |
      | Bakken | MonitorData-Demo_2H | 1105   | Pressure | 2018-05-28T03:59:18.0000000Z | 12.42 psi   |
      | Bakken | MonitorData-Demo_2H | 14475  | Pressure | 2018-06-01T19:24:46.0000000Z | 12.75 psi   |
      | Bakken | MonitorData-Demo_2H | 18418  | Pressure | 2018-06-03T04:16:20.0000000Z | 12.52 psi   |
      | Bakken | MonitorData-Demo_2H | 33263  | Pressure | 2018-06-08T07:59:47.0000000Z | 2882.93 psi |
      | Bakken | MonitorData-Demo_2H | 83966  | Pressure | 2018-06-25T22:34:44.0000000Z | 3424.57 psi |
      | Bakken | MonitorData-Demo_2H | 87110  | Pressure | 2018-06-27T00:46:44.0000000Z | 3231.8 psi  |
      | Bakken | MonitorData-Demo_2H | 114594 | Pressure | 2018-07-07T03:13:05.0000000Z | -7999 psi   |
      | Bakken | MonitorData-Demo_3H | 0      | Pressure | 2018-06-07T16:35:02.0000000Z | 1628.97 psi |
      | Bakken | MonitorData-Demo_3H | 9872   | Pressure | 2018-06-11T02:53:53.0000000Z | 1278.02 psi |
      | Bakken | MonitorData-Demo_3H | 38744  | Pressure | 2018-06-21T03:38:08.0000000Z | 900.61 psi  |
      | Bakken | MonitorData-Demo_3H | 47718  | Pressure | 2018-06-24T06:28:34.0000000Z | 904.48 psi  |
      | Bakken | MonitorData-Demo_3H | 58806  | Pressure | 2018-06-28T02:55:59.0000000Z | 1399.29 psi |
      | Bakken | MonitorData-Demo_3H | 58869  | Pressure | 2018-06-28T03:27:29.0000000Z | 1964.85 psi |
      | Bakken | MonitorData-Demo_3H | 62026  | Pressure | 2018-06-29T05:46:52.0000000Z | 2716.76 psi |
      | Bakken | MonitorData-Demo_3H | 62757  | Pressure | 2018-06-29T11:52:22.0000000Z | 2677.54 psi |
      | Bakken | MonitorData-Demo_4H | 0      | Pressure | 2018-05-27T18:46:21.0000000Z | 13.22 psi   |
      | Bakken | MonitorData-Demo_4H | 3864   | Pressure | 2018-05-29T02:58:48.0000000Z | 12.48 psi   |
      | Bakken | MonitorData-Demo_4H | 19189  | Pressure | 2018-06-03T10:41:50.0000000Z | 13.19 psi   |
      | Bakken | MonitorData-Demo_4H | 25197  | Pressure | 2018-06-05T12:45:51.0000000Z | 13.3 psi    |
      | Bakken | MonitorData-Demo_4H | 65166  | Pressure | 2018-06-19T09:53:18.0000000Z | 4995.46 psi |
      | Bakken | MonitorData-Demo_4H | 81490  | Pressure | 2018-06-25T01:56:42.0000000Z | 2887.48 psi |
      | Bakken | MonitorData-Demo_4H | 87675  | Pressure | 2018-06-27T05:29:14.0000000Z | 3743.04 psi |
      | Bakken | MonitorData-Demo_4H | 114594 | Pressure | 2018-07-07T03:13:05.0000000Z | -7999 psi   |

    Examples: Montney
      | field   | name               | index       | qty_name    | time                         | value         |
      | Montney | Hori_01-Downhole-0 | 0           | Pressure    | 2018-04-05T10:01:07.0000000Z | 20665.11 kPa |
      | Montney | Hori_01-Downhole-0 | 14848       | Pressure    | 2018-04-05T14:16:39.0000000Z | 18562.68 kPa |
      | Montney | Hori_01-Downhole-0 | 67025       | Pressure    | 2018-04-06T05:11:54.0000000Z | 15446.07 kPa |
      | Montney | Hori_01-Downhole-0 | 138193      | Pressure    | 2018-04-07T01:34:01.0000000Z | 27726.53 kPa |
      | Montney | Hori_01-Downhole-0 | 196604      | Pressure    | 2018-04-07T18:18:33.0000000Z | 27965.21 kPa |
      | Montney | Hori_01-Downhole-0 | 252497      | Pressure    | 2018-04-08T10:17:31.0000000Z | 27131.21 kPa |
      | Montney | Hori_01-Downhole-0 | 256716      | Pressure    | 2018-04-08T11:30:10.0000000Z | 34203.43 kPa |
      | Montney | Hori_01-Downhole-0 | 325041      | Pressure    | 2018-04-09T07:06:53.0000000Z | 26835 kPa    |
      | Montney | Hori_01-Downhole-0 | 0           | Temperature | 2018-04-05T10:01:07.0000000Z | -11.79 degC    |
      | Montney | Hori_01-Downhole-0 | 21207       | Temperature | 2018-04-05T16:05:12.0000000Z | 1.48 degC      |
      | Montney | Hori_01-Downhole-0 | 131030      | Temperature | 2018-04-06T23:31:32.0000000Z | -0.99 degC     |
      | Montney | Hori_01-Downhole-0 | 144783      | Temperature | 2018-04-07T03:27:25.0000000Z | -9.48 degC     |
      | Montney | Hori_01-Downhole-0 | 275515      | Temperature | 2018-04-08T16:53:34.0000000Z | -1012 degC    |
      | Montney | Hori_01-Downhole-0 | 276326      | Temperature | 2018-04-08T17:07:14.0000000Z | 11.61 degC     |
      | Montney | Hori_01-Downhole-0 | 321067      | Temperature | 2018-04-09T05:57:57.0000000Z | -0.67 degC     |
      | Montney | Hori_01-Downhole-0 | 325041      | Temperature | 2018-04-09T07:06:53.0000000Z | -0.83 degC     |
      | Montney | Hori_02-Downhole-0 | 0           | Pressure    | 2018-04-05T09:26:03.0000000Z | 16136.97 kPa |
      | Montney | Hori_02-Downhole-0 | 57362       | Pressure    | 2018-04-06T01:34:42.0000000Z | 15442.79 kPa |
      | Montney | Hori_02-Downhole-0 | 75454       | Pressure    | 2018-04-06T06:41:19.0000000Z | 15317.41 kPa |
      | Montney | Hori_02-Downhole-0 | 77095       | Pressure    | 2018-04-06T07:08:44.0000000Z | 15308.05 kPa |
      | Montney | Hori_02-Downhole-0 | 230565      | Pressure    | 2018-04-08T02:21:39.0000000Z | 15575.36 kPa |
      | Montney | Hori_02-Downhole-0 | 242309      | Pressure    | 2018-04-08T05:39:08.0000000Z | 15178.11 kPa |
      | Montney | Hori_02-Downhole-0 | 311658      | Pressure    | 2018-04-09T01:12:25.0000000Z | 13830.99 kPa |
      | Montney | Hori_02-Downhole-0 | 332477      | Pressure    | 2018-04-09T07:04:03.0000000Z | 13540.6 kPa  |
      | Montney | Hori_02-Downhole-0 | 0           | Temperature | 2018-04-05T09:26:03.0000000Z | -12.7 degC     |
      | Montney | Hori_02-Downhole-0 | 14635       | Temperature | 2018-04-05T13:33:38.0000000Z | 3.64 degC      |
      | Montney | Hori_02-Downhole-0 | 118229      | Temperature | 2018-04-06T18:44:06.0000000Z | 1.8 degC       |
      | Montney | Hori_02-Downhole-0 | 119021      | Temperature | 2018-04-06T18:57:21.0000000Z | 1.74 degC      |
      | Montney | Hori_02-Downhole-0 | 136730      | Temperature | 2018-04-06T23:56:35.0000000Z | -1.48 degC     |
      | Montney | Hori_02-Downhole-0 | 154389      | Temperature | 2018-04-07T04:53:40.0000000Z | -10.14 degC    |
      | Montney | Hori_02-Downhole-0 | 283266      | Temperature | 2018-04-08T17:13:06.0000000Z | 6.45 degC      |
      | Montney | Hori_02-Downhole-0 | 332477      | Temperature | 2018-04-09T07:04:03.0000000Z | 1.65 degC      |
      | Montney | Hori_03-Downhole-0 | 0           | Pressure    | 2018-04-05T10:00:19.0000000Z | 13434.1 kPa  |
      | Montney | Hori_03-Downhole-0 | 17858       | Pressure    | 2018-04-05T15:04:57.0000000Z | 13413.82 kPa |
      | Montney | Hori_03-Downhole-0 | 94644       | Pressure    | 2018-04-06T12:57:11.0000000Z | 13301.95 kPa |
      | Montney | Hori_03-Downhole-0 | 98895       | Pressure    | 2018-04-06T14:10:13.0000000Z | 13297.05 kPa |
      | Montney | Hori_03-Downhole-0 | 105291      | Pressure    | 2018-04-06T15:59:17.0000000Z | 13288.75 kPa |
      | Montney | Hori_03-Downhole-0 | 124265      | Pressure    | 2018-04-06T21:22:16.0000000Z | 13691.07 kPa |
      | Montney | Hori_03-Downhole-0 | 157027      | Pressure    | 2018-04-07T06:41:22.0000000Z | 26739.18 kPa |
      | Montney | Hori_03-Downhole-0 | 323523      | Pressure    | 2018-04-09T07:02:35.0000000Z | 26358.15 kPa |
      | Montney | Hori_03-Downhole-0 | 0           | Temperature | 2018-04-05T10:00:19.0000000Z | -3.44 degC     |
      | Montney | Hori_03-Downhole-0 | 3925        | Temperature | 2018-04-05T11:07:46.0000000Z | -4.49 degC     |
      | Montney | Hori_03-Downhole-0 | 9783        | Temperature | 2018-04-05T12:47:32.0000000Z | 0.84 degC      |
      | Montney | Hori_03-Downhole-0 | 47158       | Temperature | 2018-04-05T23:24:29.0000000Z | -11.73 degC    |
      | Montney | Hori_03-Downhole-0 | 88961       | Temperature | 2018-04-06T11:20:08.0000000Z | -10.15 degC    |
      | Montney | Hori_03-Downhole-0 | 170895      | Temperature | 2018-04-07T10:35:40.0000000Z | -5.32 degC     |
      | Montney | Hori_03-Downhole-0 | 246659      | Temperature | 2018-04-08T08:06:47.0000000Z | -3.09 degC     |
      | Montney | Hori_03-Downhole-0 | 323523      | Temperature | 2018-04-09T07:02:35.0000000Z | -3.65 degC     |
      | Montney | Vert_01-Downhole-0 | 0           | Pressure    | 2018-04-05T10:24:12.0000000Z | 19459.03 kPa |
      | Montney | Vert_01-Downhole-0 | 6652        | Pressure    | 2018-04-05T12:19:34.0000000Z | 19061.51 kPa |
      | Montney | Vert_01-Downhole-0 | 90175       | Pressure    | 2018-04-06T12:16:56.0000000Z | 16491.47 kPa |
      | Montney | Vert_01-Downhole-0 | 134841      | Pressure    | 2018-04-07T01:09:16.0000000Z | 25115.39 kPa |
      | Montney | Vert_01-Downhole-0 | 211515      | Pressure    | 2018-04-07T23:10:44.0000000Z | 16361.86 kPa |
      | Montney | Vert_01-Downhole-0 | 222007      | Pressure    | 2018-04-08T02:11:20.0000000Z | 15895.58 kPa |
      | Montney | Vert_01-Downhole-0 | 300671      | Pressure    | 2018-04-09T00:49:23.0000000Z | 14088.72 kPa |
      | Montney | Vert_01-Downhole-0 | 322124      | Pressure    | 2018-04-09T06:59:16.0000000Z | 13859.02 kPa |
      | Montney | Vert_01-Downhole-0 | 0           | Temperature | 2018-04-05T10:24:12.0000000Z | -6.38 degC     |
      | Montney | Vert_01-Downhole-0 | 34549       | Temperature | 2018-04-05T20:20:56.0000000Z | -7.49 degC     |
      | Montney | Vert_01-Downhole-0 | 89295       | Temperature | 2018-04-06T12:01:51.0000000Z | -5.73 degC     |
      | Montney | Vert_01-Downhole-0 | 111788      | Temperature | 2018-04-06T18:30:28.0000000Z | -0.88 degC     |
      | Montney | Vert_01-Downhole-0 | 209284      | Temperature | 2018-04-07T22:32:44.0000000Z | 3.11 degC      |
      | Montney | Vert_01-Downhole-0 | 232331      | Temperature | 2018-04-08T05:10:26.0000000Z | 2.11 degC      |
      | Montney | Vert_01-Downhole-0 | 300439      | Temperature | 2018-04-09T00:44:44.0000000Z | 7.68 degC      |
      | Montney | Vert_01-Downhole-0 | 322124      | Temperature | 2018-04-09T06:59:16.0000000Z | 3.61 degC      |

  Scenario: Get the default well colors from a project
    Given I have loaded the project for the field, 'Montney'
    When I query the project default well colors
    Then I see the colors
      | red   | green | blue  |
      | 0.0   | 0.447 | 0.741 |
      | 0.85  | 0.325 | 0.098 |
      | 0.929 | 0.694 | 0.125 |
      | 0.494 | 0.184 | 0.556 |
      | 0.466 | 0.674 | 0.188 |
      | 0.301 | 0.745 | 0.933 |
      | 0.635 | 0.078 | 0.184 |
      | 0.0   | 0.447 | 0.741 |
      | 0.85  | 0.325 | 0.098 |
      | 0.929 | 0.694 | 0.125 |
      | 0.494 | 0.184 | 0.556 |
      | 0.466 | 0.674 | 0.188 |
      | 0.301 | 0.745 | 0.933 |
      | 0.635 | 0.078 | 0.184 |
