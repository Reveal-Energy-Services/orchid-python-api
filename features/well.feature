#  Copyright 2017-2022 Reveal Energy Services, Inc
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
      | field  | well    | md_kb        | frame   | datum  | x             | y            | depth        |
      | Bakken | Demo_1H | 350.4 ft     | Project | Kelly  | -1.299e+04 ft | 3.555e+04 ft | 350.4 ft     |
      | Bakken | Demo_1H | 2880. ft     | Project | Kelly  | -1.297e+04 ft | 3.560e+04 ft | 2877. ft     |
      | Bakken | Demo_1H | 1.297e+04 ft | Project | Kelly  | -1.498e+04 ft | 3.686e+04 ft | 1.077e+04 ft |
      | Bakken | Demo_1H | 1.853e+04 ft | Project | Kelly  | -2.054e+04 ft | 3.687e+04 ft | 1.072e+04 ft |
      | Bakken | Demo_2H | 2943. ft     | Well    | Sea    | 10.03 ft      | -1.229 ft    | 2943. ft     |
      | Bakken | Demo_2H | 3496. ft     | Well    | Sea    | 16.51 ft      | 17.80 ft     | 3495. ft     |
      | Bakken | Demo_2H | 7739. ft     | Well    | Sea    | 218.4 ft      | 398.7 ft     | 7712. ft     |
      | Bakken | Demo_2H | 1.091e+04 ft | Well    | Sea    | 54.92 ft      | 695.7 ft     | 1.074e+04 ft |
      | Bakken | Demo_3H | 756.1 ft     | Plane   | Ground | 1.990e+06 ft  | 1.750e+07 ft | 756.2 ft     |
      | Bakken | Demo_3H | 5893. ft     | Plane   | Ground | 1.990e+06 ft  | 1.750e+07 ft | 5892. ft     |
      | Bakken | Demo_3H | 6283. ft     | Plane   | Ground | 1.990e+06 ft  | 1.750e+07 ft | 6282. ft     |
      | Bakken | Demo_3H | 2.065e+04 ft | Plane   | Ground | 1.980e+06 ft  | 1.750e+07 ft | 1.074e+04 ft |
      | Bakken | Demo_4H | 3799. ft     | Project | Ground | -1.306e+04 ft | 3.537e+04 ft | 3799. ft     |
      | Bakken | Demo_4H | 7971. ft     | Project | Ground | -1.283e+04 ft | 3.493e+04 ft | 7930. ft     |
      | Bakken | Demo_4H | 9654. ft     | Project | Ground | -1.275e+04 ft | 3.473e+04 ft | 9600. ft     |
      | Bakken | Demo_4H | 1.422e+04 ft | Project | Ground | -1.630e+04 ft | 3.460e+04 ft | 1.075e+04 ft |

    Examples: Montney
      | field   | well    | md_kb   | frame   | datum  | x           | y           | depth    |
      | Montney | Hori_01 | 467.3 m | Plane   | Kelly  | 6.565e+05 m | 6.179e+06 m | 464.8 m  |
      | Montney | Hori_01 | 814.8 m | Plane   | Kelly  | 6.565e+05 m | 6.179e+06 m | 811.9 m  |
      | Montney | Hori_01 | 2595. m | Plane   | Kelly  | 6.567e+05 m | 6.179e+06 m | 2420. m  |
      | Montney | Hori_01 | 3062. m | Plane   | Kelly  | 6.571e+05 m | 6.179e+06 m | 2423. m  |
      | Montney | Hori_02 | 1026. m | Well    | Ground | -19.34 m    | -32.18 m    | 1014. m  |
      | Montney | Hori_02 | 1889. m | Well    | Ground | -15.00 m    | -32.30 m    | 1877. m  |
      | Montney | Hori_02 | 3968. m | Well    | Ground | 1243. m     | -926.9 m    | 2534. m  |
      | Montney | Hori_02 | 4096. m | Well    | Ground | 1344. m     | -1006. m    | 2535. m  |
      | Montney | Hori_03 | 358.8 m | Project | Sea    | -605.7 m    | 351.7 m     | -370.5 m |
      | Montney | Hori_03 | 1018. m | Project | Sea    | -599.0 m    | 351.0 m     | 288.4 m  |
      | Montney | Hori_03 | 3668. m | Project | Sea    | 562.7 m     | -302.7 m    | 1692. m  |
      | Montney | Hori_03 | 4439. m | Project | Sea    | 1172. m     | -774.2 m    | 1695. m  |
      | Montney | Vert_01 | 360.0 m | Well    | Sea    | 0.000 m     | 0.000 m     | -368.0 m |
      | Montney | Vert_01 | 462.1 m | Well    | Sea    | 0.000 m     | 0.000 m     | -265.9 m |
      | Montney | Vert_01 | 1158. m | Well    | Sea    | 0.000 m     | 0.000 m     | 430.0 m  |
      | Montney | Vert_01 | 2640. m | Well    | Sea    | 0.000 m     | 0.000 m    | 1912. m  |

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
