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

Feature: Adapted IWell DOM API
  As a data engineer,
  I want to access Orchid wells conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get well measurements in project units
    Given I have loaded the project for the field, '<field>'
    When I query the well measurements for <well>
    Then I see measurements for <kb_above_ground> and <ground_above_sea_level>

    Examples: Bakken
      | field  | well    | kb_above_ground | ground_above_sea_level |
      | Bakken | Demo_1H | 0 ft            | 0 ft                   |
      | Bakken | Demo_2H | 0 ft            | 0 ft                   |
      | Bakken | Demo_3H | 0 ft            | 0 ft                   |
      | Bakken | Demo_4H | 0 ft            | 0 ft                   |

    Examples: Montney
      | field   | well    | kb_above_ground | ground_above_sea_level |
      | Montney | Hori_01 | 10 m            | 718 m                  |
      | Montney | Hori_02 | 10 m            | 718 m                  |
      | Montney | Hori_03 | 10 m            | 718 m                  |
      | Montney | Vert_01 | 10 m            | 718 m                  |

  Scenario Outline: Get subsurface locations in project units along the well trajectory
    Given I have loaded the project for the field, '<field>'
    When I sample the well subsurface locations for '<well>'
    Then I see the points <x>, <y>, and <depth> in project units at <md_kb> in <frame> and <datum>

    Examples: Bakken
      | field  | well    | md_kb        | frame   | datum | x             | y            | depth        |
      | Bakken | Demo_1H | 350.4 ft     | Well    | Kelly | 1.002 ft      | -0.5727 ft   | 350.4 ft     |
      | Bakken | Demo_1H | 2880. ft     | Well    | Kelly | 20.51 ft      | 52.04 ft     | 2877. ft     |
      | Bakken | Demo_1H | 1.297e+04 ft | Well    | Kelly | -1990. ft     | 1314. ft     | 1.077e+04 ft |
      | Bakken | Demo_1H | 1.853e+04 ft | Well    | Kelly | -7547. ft     | 1324. ft     | 1.072e+04 ft |
      | Bakken | Demo_2H | 2943. ft     | Plane   | Kelly | 1.989e+06 ft  | 1.750e+07 ft | 2943. ft     |
      | Bakken | Demo_2H | 3496. ft     | Plane   | Kelly | 1.989e+06 ft  | 1.750e+07 ft | 3495. ft     |
      | Bakken | Demo_2H | 7739. ft     | Plane   | Kelly | 1.990e+06 ft  | 1.750e+07 ft | 7712. ft     |
      | Bakken | Demo_2H | 1.091e+04 ft | Plane   | Kelly | 1.989e+06 ft  | 1.750e+07 ft | 1.074e+04 ft |
      | Bakken | Demo_3H | 756.1 ft     | Well    | Kelly | 5.000e-3 ft   | 0.000 ft     | 756.2 ft     |
      | Bakken | Demo_3H | 5893. ft     | Well    | Kelly | 8.203 ft      | -24.55 ft    | 5892. ft     |
      | Bakken | Demo_3H | 6283. ft     | Well    | Kelly | 14.05 ft      | -23.66 ft    | 6282. ft     |
      | Bakken | Demo_3H | 2.065e+04 ft | Well    | Kelly | -9910. ft     | 719.3 ft     | 1.074e+04 ft |
      | Bakken | Demo_4H | 3799. ft     | Project | Sea   | -1.306e+04 ft | 3.537e+04 ft | 3798. ft     |
      | Bakken | Demo_4H | 7971. ft     | Project | Sea   | -1.283e+04 ft | 3.493e+04 ft | 7930. ft     |
      | Bakken | Demo_4H | 9654. ft     | Project | Sea   | -1.275e+04 ft | 3.473e+04 ft | 9600. ft     |
      | Bakken | Demo_4H | 1.422e+04 ft | Project | Sea   | -1.630e+04 ft | 3.460e+04 ft | 1.075e+04 ft |

    Examples: Montney
      | field   | well    | md_kb   | frame   | datum  | x           | y           | depth    |
      | Montney | Hori_01 | 467.3 m | Project | Sea    | -653.4 m    | 355.0 m     | -263.2 m |
      | Montney | Hori_01 | 814.8 m | Project | Sea    | -656.0 m    | 344.2 m     | 83.88 m  |
      | Montney | Hori_01 | 2595. m | Project | Sea    | -478.6 m    | 128.0 m     | 1692. m  |
      | Montney | Hori_01 | 3062. m | Project | Sea    | -112.2 m    | -161.2 m    | 1695. m  |
      | Montney | Hori_02 | 1026. m | Well    | Ground | -19.34 m    | -32.18 m    | -421.9 m |
      | Montney | Hori_02 | 1889. m | Well    | Ground | -15.00 m    | -32.30 m    | 441.0 m  |
      | Montney | Hori_02 | 3968. m | Well    | Ground | 1243. m     | -926.9 m    | 1098. m  |
      | Montney | Hori_02 | 4096. m | Well    | Ground | 1344. m     | -1006. m    | 1099. m  |
      | Montney | Hori_03 | 358.8 m | Plane   | Ground | 6.566e+05 m | 6.179e+06 m | -1089. m |
      | Montney | Hori_03 | 1018. m | Plane   | Ground | 6.566e+05 m | 6.179e+06 m | -429.7 m |
      | Montney | Hori_03 | 3668. m | Plane   | Ground | 6.578e+05 m | 6.179e+06 m | 974.4 m  |
      | Montney | Hori_03 | 4439. m | Plane   | Ground | 6.584e+05 m | 6.178e+06 m | 977.4 m  |
      | Montney | Vert_01 | 360.0 m | Plane   | Ground | 6.590e+05 m | 6.178e+06 m | -1086. m |
      | Montney | Vert_01 | 462.1 m | Plane   | Ground | 6.590e+05 m | 6.178e+06 m | -983.9 m |
      | Montney | Vert_01 | 1158. m | Plane   | Ground | 6.590e+05 m | 6.178e+06 m | -288.0 m |
      | Montney | Vert_01 | 2640. m | Plane   | Ground | 6.590e+05 m | 6.178e+06 m | 1194. m  |

  Scenario Outline: Get wellhead locations in project units for different wells
    Given I have loaded the project for the field, '<field>'
    When I sample the well subsurface locations for '<well>'
    Then I see the points <easting>, <northing>, and <depth>

    Examples: Bakken
      | field  | well    | easting       | northing       | depth  |
      | Bakken | Demo_1H | 1989427.13 ft | 17496710.27 ft | 0.0 ft |
      | Bakken | Demo_2H | 1989404.16 ft | 17496644.65 ft | 0.0 ft |
      | Bakken | Demo_3H | 1990381.85 ft | 17495906.46 ft | 0.0 ft |

    Examples: Montney
      | field   | well    | easting       | northing       | depth |
      | Montney | Hori_01 | 656587.37 m   | 6179346.351 m  | 0.0 m |
      | Montney | Hori_03 | 656590.37 m   | 6179349.351 m  | 0.0 m |
      | Montney | Vert_01 | 659044.57 m   | 6177836.623 m  | 0.0 m |