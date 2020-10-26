#  Copyright 2017-2020 Reveal Energy Services, Inc 
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

Feature: Low-level stages API (DOM)
  As a data engineer,
  I want to access treatment information for stages conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Perform a pad analysis for a well treatment
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I calculate the total fluid volume, proppant, and median treating pressure for each stage
    Then I see 135 stages for the project
    And I see correct sample values for <index>, <well>, <stage>, <md_top>, and <md_bottom>
    And I see correct sample aggregate values for <index>, <volume>, <proppant> and <median>

    Examples: Bakken
      | field  | index | well    | stage | md_top  | md_bottom | volume  | proppant | median  |
      | Bakken | 0     | Demo_1H | 1     | 20883.3 | 20934.0   | 3668.30 | 139702   | 6164.04 |
      | Bakken | 134   | Demo_4H | 35    | 11260.0 | 11485.0   | 8294.68 | 135936   | 6442.86 |
      | Bakken | 78    | Demo_2H | 29    | 15313.9 | 15461.9   | 6164.56 | 222663   | 7631.72 |
      | Bakken | 9     | Demo_1H | 10    | 19127.4 | 19274.6   | 8667.34 | 220929   | 8271.64 |
      | Bakken | 25    | Demo_1H | 26    | 15986.6 | 16133.8   | 6502.47 | 208507   | 7983.54 |
      | Bakken | 56    | Demo_2H | 7     | 19656.7 | 19804.7   | 8407.48 | 205751   | 8240.48 |
      | Bakken | 3     | Demo_1H | 4     | 20358.3 | 20410.3   | 4055.97 | 233982   | 6516.33 |

  Scenario Outline: Calculate basic information to support stage tool tips
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    Then I see the correct <stage>, <name_with_well>, <md_top>, <md_bottom> and <cluster_count>

    Examples: Bakken
      | field  | stage | name_with_well   | md_top      | md_bottom   | cluster_count |
      | Bakken | 1     | Demo_1H-Stage-1  | 20883.34 ft | 20934.0 ft  | 2             |
      | Bakken | 50    | Demo_1H-Stage-50 | 11275.52 ft | 11422.62 ft | 4             |
      | Bakken | 9     | Demo_1H-Stage-9  | 19323.68 ft | 19470.9 ft  | 4             |
      | Bakken | 33    | Demo_1H-Stage-33 | 14612.48 ft | 14759.7 ft  | 4             |
      | Bakken | 1     | Demo_2H-Stage-1  | 20839 ft    | 20914.08 ft | 8             |
      | Bakken | 50    | Demo_2H-Stage-50 | 11169.53 ft | 11316.68 ft | 4             |
      | Bakken | 21    | Demo_2H-Stage-21 | 16893.08 ft | 17041.13 ft | 4             |
      | Bakken | 8     | Demo_2H-Stage-8  | 19459.28 ft | 19607.33 ft | 4             |
      | Bakken | 1     | Demo_3H-Stage-1  | 11200 ft    | 21500 ft    | 4             |
      | Bakken | 1     | Demo_4H-Stage-1  | 20835 ft    | 20900.93 ft | 8             |
      | Bakken | 35    | Demo_4H-Stage-35 | 11260 ft    | 11485 ft    | 6             |
      | Bakken | 7     | Demo_4H-Stage-7  | 19446.5 ft  | 19691.5 ft  | 6             |
      | Bakken | 26    | Demo_4H-Stage-26 | 13860.5 ft  | 14105.5 ft  | 6             |

    Examples: Montney
      | field   | stage | name_with_well   | md_top   | md_bottom | cluster_count |
      | Montney | 1     | Hori_01-Stage-1  | 5395 m   | 5569.5 m  | 1             |
      | Montney | 15    | Hori_01-Stage-15 | 2595.5 m | 2771 m    | 1             |
      | Montney | 8     | Hori_01-Stage-8  | 3996 m   | 4170.5 m  | 1             |
      | Montney | 2     | Hori_01-Stage-2  | 5196 m   | 5370.5 m  | 1             |
      | Montney | 1     | Hori_02-Stage-1  | 5456.5 m | 5495.5 m  | 1             |
      | Montney | 29    | Hori_02-Stage-29 | 2768.5 m | 2840.5 m  | 1             |
      | Montney | 8     | Hori_02-Stage-8  | 4784.5 m | 4857 m    | 1             |
      | Montney | 14    | Hori_02-Stage-14 | 4208.5 m | 4281 m    | 1             |
      | Montney | 1     | Hori_03-Stage-1  | 5238 m   | 5313.5 m  | 1             |
      | Montney | 28    | Hori_03-Stage-28 | 2538 m   | 2613.5 m  | 1             |
      | Montney | 9     | Hori_03-Stage-9  | 4438 m   | 4513.5 m  | 1             |
      | Montney | 20    | Hori_03-Stage-20 | 3338 m   | 3413.5 m  | 1             |
      | Montney | 1     | Vert_01-Stage-1  | 2495 m   | 2530.5 m  | 1             |
      | Montney | 2     | Vert_01-Stage-2  | 2445 m   | 2480.5 m  | 1             |
      | Montney | 3     | Vert_01-Stage-3  | 2395 m   | 2430.5 m  | 1             |
      | Montney | 4     | Vert_01-Stage-4  | 2345 m   | 2380.5 m  | 1             |

  Scenario Outline: Calculate additional information to support stage tool tips
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see additional data <stage>, <name_with_well>, <easting>, <northing>, <tvdss> and <length>

    Examples: Bakken
      | field  | stage | name_with_well   | easting      | northing    | tvdss       | length      |
      | Bakken | 1     | Demo_1H-Stage-1  | -22918.59 ft | 36877.27 ft | 10707.32 ft | 50.66 ft    |
      | Bakken | 50    | Demo_1H-Stage-50 | -13363.32 ft | 36868.75 ft | 10770.12 ft | 147.11 ft   |
      | Bakken | 9     | Demo_1H-Stage-9  | -21408.04 ft | 36880.20 ft | 10719.38 ft | 147.22 ft   |
      | Bakken | 33    | Demo_1H-Stage-33 | -16699.31 ft | 36878.51 ft | 10740.07 ft | 147.22 ft   |
      | Bakken | 1     | Demo_2H-Stage-1  | -22920.25 ft | 36102.40 ft | 10711.98 ft | 75.08 ft    |
      | Bakken | 50    | Demo_2H-Stage-50 | -13291.11 ft | 36157.69 ft | 10767.44 ft | 147.15 ft   |
      | Bakken | 21    | Demo_2H-Stage-21 | -19012.26 ft | 36106.84 ft | 10731.78 ft | 148.05 ft   |
      | Bakken | 8     | Demo_2H-Stage-8  | -21577.64 ft | 36083.34 ft | 10727.67 ft | 148.05 ft   |
      | Bakken | 1     | Demo_3H-Stage-1  | -17651.57 ft | 35498.61 ft | 10756.04 ft | 10300.00 ft |
      | Bakken | 1     | Demo_4H-Stage-1  | -22941.22 ft | 34633.37 ft | 10717.32 ft | 65.93 ft    |
      | Bakken | 35    | Demo_4H-Stage-35 | -13456.91 ft | 34600.45 ft | 10765.60 ft | 225.00 ft   |
      | Bakken | 7     | Demo_4H-Stage-7  | -21643.18 ft | 34607.90 ft | 10722.36 ft | 245.00 ft   |
      | Bakken | 26    | Demo_4H-Stage-26 | -16066.09 ft | 34600.48 ft | 10754.28 ft | 245.00 ft   |

    Examples: Montney
      | field   | stage | name_with_well   | easting   | northing   | tvdss     | length  |
      | Montney | 1     | Hori_01-Stage-1  | 1798.47 m | -1645.40 m | 1715.62 m | 174.5 m |
      | Montney | 15    | Hori_01-Stage-15 | -411.39 m | 70.92 m    | 1690.61 m | 175.5 m |
      | Montney | 8     | Hori_01-Stage-8  | 695.63 m  | -785.57 m  | 1705.04 m | 174.5 m |
      | Montney | 2     | Hori_01-Stage-2  | 1640.41 m | -1524.58 m | 1714.82 m | 174.5 m |
      | Montney | 1     | Hori_02-Stage-1  | 1823.90 m | -1468.04 m | 1819.17 m | 39.0 m  |
      | Montney | 29    | Hori_02-Stage-29 | -294.27 m | 158.02 m   | 1806.98 m | 72.0 m  |
      | Montney | 8     | Hori_02-Stage-8  | 1302.97 m | -1070.91 m | 1820.75 m | 72.5 m  |
      | Montney | 14    | Hori_02-Stage-14 | 846.41 m  | -720.02 m  | 1817.50 m | 72.5 m  |
      | Montney | 1     | Hori_03-Stage-1  | 1832.20 m | -1288.07 m | 1698.90 m | 75.5 m  |
      | Montney | 28    | Hori_03-Stage-28 | -335.48 m | 311.16 m   | 1689.96 m | 75.5 m  |
      | Montney | 9     | Hori_03-Stage-9  | 1200.95 m | -797.29 m  | 1695.73 m | 75.5 m  |
      | Montney | 20    | Hori_03-Stage-20 | 328.02 m  | -128.77 m  | 1691.35 m | 75.5 m  |
      | Montney | 1     | Vert_01-Stage-1  | 1842.15 m | -1133.05 m | 1784.75 m | 35.5 m  |
      | Montney | 2     | Vert_01-Stage-2  | 1842.15 m | -1133.05 m | 1734.75 m | 35.5 m  |
      | Montney | 3     | Vert_01-Stage-3  | 1842.15 m | -1133.05 m | 1684.75 m | 35.5 m  |
      | Montney | 4     | Vert_01-Stage-4  | 1842.15 m | -1133.05 m | 1634.75 m | 35.5 m  |
