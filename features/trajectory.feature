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

Feature: Low-level trajectory API (DOM API)
  As a data engineer,
  I want to access trajectory information conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get the trajectory easting, northing, and TVDSS in project units
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    When I query the trajectory for well "<well>"
    And I query the easting, northing, and TVDSS arrays in the project reference frame in project units
    Then I see the initial trajectory details <easting>, <northing>, and <tvdss> values at <index>

    Examples: Bakken
      | field  | well    | index | easting   | northing | tvdss     |
      | Bakken | Demo_1H | 0     | -12994 ft | 35549 ft | 0.0000 ft |
      | Bakken | Demo_1H | 252   | -23010 ft | 36879 ft | 10705 ft  |
      | Bakken | Demo_1H | 146   | -13280 ft | 36870 ft | 10770 ft  |
      | Bakken | Demo_1H | 174   | -15903 ft | 36872 ft | 10751 ft  |
      | Bakken | Demo_1H | 99    | -12732 ft | 36547 ft | 8609.4 ft |
      | Bakken | Demo_1H | 185   | -16947 ft | 36880 ft | 10739 ft  |
      | Bakken | Demo_2H | 0     | -13017 ft | 35483 ft | 0.0000 ft |
      | Bakken | Demo_2H | 245   | -23024 ft | 36105 ft | 10712 ft  |
      | Bakken | Demo_2H | 203   | -19077 ft | 36105 ft | 10732 ft  |
      | Bakken | Demo_2H | 154   | -14420 ft | 36141 ft | 10766 ft  |
      | Bakken | Demo_2H | 155   | -14512 ft | 36142 ft | 10766 ft  |
      | Bakken | Demo_2H | 241   | -22682 ft | 36095 ft | 10714 ft  |
      | Bakken | Demo_3H | 0     | -12039 ft | 34745 ft | 0.0000 ft |
      | Bakken | Demo_3H | 233   | -22849 ft | 35477 ft | 10728 ft  |
      | Bakken | Demo_3H | 121   | -12638 ft | 35145 ft | 10768 ft  |
      | Bakken | Demo_3H | 19    | -12037 ft | 34727 ft | 3785.1 ft |
      | Bakken | Demo_3H | 213   | -21007 ft | 35450 ft | 10741 ft  |
      | Bakken | Demo_3H | 53    | -12021 ft | 34724 ft | 6987.8 ft |
      | Bakken | Demo_4H | 0     | -13044 ft | 35392 ft | 0.0000 ft |
      | Bakken | Demo_4H | 256   | -23040 ft | 34636 ft | 10716 ft  |
      | Bakken | Demo_4H | 53    | -13037 ft | 35364 ft | 4820.3 ft |
      | Bakken | Demo_4H | 14    | -13042 ft | 35390 ft | 1294.7 ft |
      | Bakken | Demo_4H | 144   | -13383 ft | 34594 ft | 10763 ft  |
      | Bakken | Demo_4H | 140   | -13224 ft | 34576 ft | 10761 ft  |

    Examples: Permian
      | field   | well | index | easting     | northing   | tvdss      |
      | Permian | C1   | 0     | -60.137 ft  | -0.9075 ft | -2872.0 ft |
      | Permian | C1   | 527   | -391.31 ft  | -4713.0 ft | 11727 ft   |
      | Permian | C1   | 506   | -387.02 ft  | -2731.0 ft | 11746 ft   |
      | Permian | C1   | 316   | -190.85 ft  | -37.164 ft | 7097.6 ft  |
      | Permian | C1   | 355   | -195.47 ft  | -39.288 ft | 8072.6 ft  |
      | Permian | C1   | 419   | -205.74 ft  | -70.320 ft | 9672.1 ft  |
      | Permian | C2   | 0     | -19.881 ft  | -0.2875 ft | -2872.0 ft |
      | Permian | C2   | 527   | -65.280 ft  | -4856.2 ft | 11452 ft   |
      | Permian | C2   | 525   | -72.042 ft  | -4687.6 ft | 11442 ft   |
      | Permian | C2   | 487   | -130.077 ft | -1103.9 ft | 11452 ft   |
      | Permian | C2   | 331   | -46.124 ft  | 65.843 ft  | 7473.1 ft  |
      | Permian | C2   | 240   | -36.545 ft  | 60.606 ft  | 5198.2 ft  |
      | Permian | C3   | 0     | 59.974 ft   | 0.8925 ft  | -2872.0 ft |
      | Permian | C3   | 530   | 529.25 ft   | -5170.0 ft | 11447 ft   |
      | Permian | C3   | 478   | 427.90 ft   | -475.20 ft | 11432 ft   |
      | Permian | C3   | 374   | 197.17 ft   | 35.921 ft  | 8547.8 ft  |
      | Permian | C3   | 182   | 150.80 ft   | 18.434 ft  | 3748.4 ft  |
      | Permian | C3   | 132   | 130.82 ft   | 12.055 ft  | 2498.6 ft  |
      | Permian | P1   | 0     | 20.046 ft   | 0.3025 ft  | -2872.0 ft |
      | Permian | P1   | 535   | 229.53 ft   | -5114.5 ft | 11650 ft   |
      | Permian | P1   | 478   | 172.42 ft   | -259.50 ft | 11526 ft   |
      | Permian | P1   | 410   | 114.31 ft   | 92.342 ft  | 9446.8 ft  |
      | Permian | P1   | 57    | 66.378 ft   | 28.362 ft  | 623.33 ft  |
      | Permian | P1   | 519   | 214.53 ft   | -3659.3 ft | 11636 ft   |

    Examples: Montney
      | field   | well    | index | easting   | northing  | tvdss       |
      | Montney | Hori_01 | 0     | -615.05 m | 376.68 m  | -728.00 m   |
      | Montney | Hori_01 | 101   | -545.28 m | 203.34 m  | 1678.0 m    |
      | Montney | Hori_01 | 13    | -645.92 m | 362.27 m  | -368.34 m   |
      | Montney | Hori_01 | 22    | -657.97 m | 347.51 m  | -134.85 m   |
      | Montney | Hori_01 | 84    | -649.13 m | 339.62 m  | 1513.82 m   |
      | Montney | Hori_01 | 91    | -618.31 m | 297.64 m  | 1599.48 m   |
      | Montney | Hori_02 | 0     | -615.05 m | 376.68 m  | -728.00 m   |
      | Montney | Hori_02 | 211   | 1897.8 m  | -1526.1 m | 1819.4 m    |
      | Montney | Hori_02 | 150   | 508.83 m  | -454.41 m | 1813.0 m    |
      | Montney | Hori_02 | 109   | -384.80 m | 226.86 m  | 1805.0 m    |
      | Montney | Hori_02 | 194   | 1530.4 m  | -1246.0 m | 1816.5 m    |
      | Montney | Hori_02 | 18    | -634.65 m | 345.16 m  | -236.66 m   |
      | Montney | Hori_03 | 0     | -612.05 m | 379.68 m  | -728.00 m   |
      | Montney | Hori_03 | 201   | 1893.5 m  | -1335.1 m | 1699.0 m    |
      | Montney | Hori_03 | 88    | -543.26 m | 338.53 m  | 1587.7 m    |
      | Montney | Hori_03 | 167   | 1127.3 m  | -738.75 m | 1694.3 m    |
      | Montney | Hori_03 | 173   | 1264.4 m  | -848.18 m | 1695.9 m    |
      | Montney | Hori_03 | 10    | -608.25 m | 359.36 m  | -459.65 m   |
      | Montney | Vert_01 | 0     | 1842.2 m  | -1133.0 m | -728.0000 m |
      | Montney | Vert_01 | 101   | 1842.2 m  | -1133.0 m | 1972.0 m    |
      | Montney | Vert_01 | 95    | 1842.2 m  | -1133.0 m | 1702.4 m    |
      | Montney | Vert_01 | 78    | 1842.2 m  | -1133.0 m | 1457.0 m    |
      | Montney | Vert_01 | 29    | 1842.2 m  | -1133.0 m | 79.690 m    |
      | Montney | Vert_01 | 42    | 1842.2 m  | -1133.0 m | 458.39 m    |

  Scenario Outline: Get the trajectory inclination and azimuth in degrees and MDKB in project units
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    When I query the trajectory for well "<well>"
    And I query the inclination and azimuth arrays and the MDKB arrays in the project reference frame in project units
    Then I see the additional trajectory details <inclination>, <azimuth>, and <mdkb> values at <index>

    Examples: Bakken
      | field  | well    | index |  inclination | azimuth    | mdkb      |
      | Bakken | Demo_1H | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_1H | 252   |  0.0000 deg  | 0.0000 deg | 21000 ft  |
      | Bakken | Demo_1H | 146   |  0.0000 deg  | 0.0000 deg | 11266 ft  |
      | Bakken | Demo_1H | 174   |  0.0000 deg  | 0.0000 deg | 13890 ft  |
      | Bakken | Demo_1H | 99    |  0.0000 deg  | 0.0000 deg | 8697.0 ft |
      | Bakken | Demo_1H | 185   |  0.0000 deg  | 0.0000 deg | 14934 ft  |
      | Bakken | Demo_2H | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_2H | 245   |  0.0000 deg  | 0.0000 deg | 20980 ft  |
      | Bakken | Demo_2H | 203   |  0.0000 deg  | 0.0000 deg | 17032 ft  |
      | Bakken | Demo_2H | 154   |  0.0000 deg  | 0.0000 deg | 12373 ft  |
      | Bakken | Demo_2H | 155   |  0.0000 deg  | 0.0000 deg | 12465 ft  |
      | Bakken | Demo_2H | 241   |  0.0000 deg  | 0.0000 deg | 20639 ft  |
      | Bakken | Demo_3H | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_3H | 233   |  0.0000 deg  | 0.0000 deg | 21550 ft  |
      | Bakken | Demo_3H | 121   |  0.0000 deg  | 0.0000 deg | 11274 ft  |
      | Bakken | Demo_3H | 19    |  0.0000 deg  | 0.0000 deg | 3786.0 ft |
      | Bakken | Demo_3H | 213   |  0.0000 deg  | 0.0000 deg | 19708 ft  |
      | Bakken | Demo_3H | 53    |  0.0000 deg  | 0.0000 deg | 6989.0 ft |
      | Bakken | Demo_4H | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_4H | 256   |  0.0000 deg  | 0.0000 deg | 20967 ft  |
      | Bakken | Demo_4H | 53    |  0.0000 deg  | 0.0000 deg | 4821.0 ft |
      | Bakken | Demo_4H | 14    |  0.0000 deg  | 0.0000 deg | 1294.8 ft |
      | Bakken | Demo_4H | 144   |  0.0000 deg  | 0.0000 deg | 11298 ft  |
      | Bakken | Demo_4H | 140   |  0.0000 deg  | 0.0000 deg | 11138 ft  |

    Examples: Permian
      | field   | well | index |  inclination | azimuth     | mdkb      |
      | Permian | C1   | 0     |  0.0000 deg  | 0.0000 deg  | 0.0000 ft |
      | Permian | C1   | 527   |  90.830 deg  | 179.09 deg  | 16960 ft  |
      | Permian | C1   | 506   |  90.290 deg  | 177.29 deg  | 14977 ft  |
      | Permian | C1   | 316   |  0.6500 deg  | 268.20 deg  | 7975.0 ft |
      | Permian | C1   | 355   |  0.4400 deg  | 178.74 deg  | 8950.0 ft |
      | Permian | C1   | 419   |  2.3500 deg  | 188.58 deg  | 10550 ft  |
      | Permian | C2   | 0     |  0.0000 deg  | 0.0000 deg  | 0.0000 ft |
      | Permian | C2   | 527   |  87.0500 deg | 177.65 deg  | 16912 ft  |
      | Permian | C2   | 525   |  86.0800 deg | 177.84 deg  | 16743 ft  |
      | Permian | C2   | 487   |  88.0700 deg | 179.42 deg  | 13157 ft  |
      | Permian | C2   | 331   |  1.2700 deg  | 307.58 deg  | 8350.0 ft |
      | Permian | C2   | 240   |  0.4200 deg  | 259.07 deg  | 6075.0 ft |
      | Permian | C3   | 0     |  0.0000 deg  | 0.0000 deg  | 0.0000 ft |
      | Permian | C3   | 530   |  89.790 deg  | 177.13 deg  | 17273 ft  |
      | Permian | C3   | 478   |  82.120 deg  | 159.86 deg  | 12568 ft  |
      | Permian | C3   | 374   |  1.6100 deg  | 105.03 deg  | 9425.0 ft |
      | Permian | C3   | 182   |  1.1100 deg  | 109.20 deg  | 4625.0 ft |
      | Permian | C3   | 132   |  0.8300 deg  | 65.04 deg   | 3375.0 ft |
      | Permian | P1   | 0     |  0.0000 deg  | 0.0000 deg  | 0.0000 ft |
      | Permian | P1   | 535   |  89.480 deg  | 176.22 deg  | 17391 ft  |
      | Permian | P1   | 478   |  52.370 deg  | 180.59 deg  | 12507 ft  |
      | Permian | P1   | 410   |  2.0600 deg  | 171.93 deg  | 10325 ft  |
      | Permian | P1   | 57    |  1.0400 deg  | 20.4800 deg | 1500.0 ft |
      | Permian | P1   | 519   |  90.120 deg  | 180.83 deg  | 15935 ft  |

    Examples: Montney
      | field   | well    | index |  inclination | azimuth    | mdkb     |
      | Montney | Hori_01 | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 m |
      | Montney | Hori_01 | 101   |  69.800 deg  | 138.90 deg | 2492.6 m |
      | Montney | Hori_01 | 13    |  6.5000 deg  | 233.90 deg | 361.68 m |
      | Montney | Hori_01 | 22    |  2.5000 deg  | 194.70 deg | 596.00 m |
      | Montney | Hori_01 | 84    |  18.900 deg  | 146.40 deg | 2246.0 m |
      | Montney | Hori_01 | 91    |  36.200 deg  | 139.70 deg | 2346.8 m |
      | Montney | Hori_02 | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 m |
      | Montney | Hori_02 | 211   |  90.300 deg  | 128.10 deg | 5570.0 m |
      | Montney | Hori_02 | 150   |  86.500 deg  | 128.20 deg | 3815.1 m |
      | Montney | Hori_02 | 109   |  83.300 deg  | 122.40 deg | 2690.6 m |
      | Montney | Hori_02 | 194   |  89.900 deg  | 126.50 deg | 5108.0 m |
      | Montney | Hori_02 | 18    |  2.4000 deg  | 191.30 deg | 493.08 m |
      | Montney | Hori_03 | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 m |
      | Montney | Hori_03 | 201   |  90.300 deg  | 127.90 deg | 5353.0 m |
      | Montney | Hori_03 | 88    |  30.500 deg  | 101.40 deg | 2327.8 m |
      | Montney | Hori_03 | 167   |  88.600 deg  | 127.90 deg | 4381.7 m |
      | Montney | Hori_03 | 173   |  90.400 deg  | 128.60 deg | 4557.2 m |
      | Montney | Hori_03 | 10    |  4.2000 deg  | 165.70 deg | 269.31 m |
      | Montney | Vert_01 | 0     |  0.0000 deg  | 0.0000 deg | 0.0000 m |
      | Montney | Vert_01 | 101   |  0.0000 deg  | 0.0000 deg | 2700.0 m |
      | Montney | Vert_01 | 95    |  0.0000 deg  | 0.0000 deg | 2430.4 m |
      | Montney | Vert_01 | 78    |  0.0000 deg  | 0.0000 deg | 2185.0 m |
      | Montney | Vert_01 | 29    |  0.0000 deg  | 0.0000 deg | 807.69 m |
      | Montney | Vert_01 | 42    |  0.0000 deg  | 0.0000 deg | 1186.4 m |
