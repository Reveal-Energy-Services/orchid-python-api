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

  Scenario Outline: Get the easting and northing trajectories in project units
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    When I query the trajectory for well "<well>"
    And I query the easting and northing arrays in the project reference frame in project units
    Then I see correct <easting>, <northing>, <tvdss>, <inclination>, <azimuth>, and <mdkb> values at <index>

    Examples: Bakken
      | field  | well    | index | easting   | northing | tvdss     | inclination | azimuth    | mdkb      |
      | Bakken | Demo_1H | 0     | -12994 ft | 35549 ft | 0.0000 ft | 0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_1H | 252   | -23010 ft | 36879 ft | 10705 ft  | 0.0000 deg  | 0.0000 deg | 21000 ft  |
      | Bakken | Demo_1H | 146   | -13280 ft | 36837 ft | 10770 ft  | 0.0000 deg  | 0.0000 deg | 11266 ft  |
      | Bakken | Demo_1H | 174   | -15903 ft | 36872 ft | 10751 ft  | 0.0000 deg  | 0.0000 deg | 13890 ft  |
      | Bakken | Demo_1H | 99    | -12732 ft | 36547 ft | 8609.4 ft | 0.0000 deg  | 0.0000 deg | 8697.0 ft |
      | Bakken | Demo_1H | 185   | -16947 ft | 36880 ft | 10739 ft  | 0.0000 deg  | 0.0000 deg | 14934 ft  |
      | Bakken | Demo_2H | 0     | -13017 ft | 35483 ft | 0.0000 ft | 0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_2H | 245   | -23024 ft | 36105 ft | 10712 ft  | 0.0000 deg  | 0.0000 deg | 20980 ft  |
      | Bakken | Demo_2H | 203   | -19077 ft | 36105 ft | 10732 ft  | 0.0000 deg  | 0.0000 deg | 17032 ft
      | Bakken | Demo_2H | 154   | -14420 ft | 36141 ft | 10766 ft  | 0.0000 deg  | 0.0000 deg | 12373 ft  |
      | Bakken | Demo_2H | 155   | -14512 ft | 36142 ft | 10766 ft  | 0.0000 deg  | 0.0000 deg | 12465 ft  |
      | Bakken | Demo_2H | 241   | -22682 ft | 36095 ft | 10714 ft  | 0.0000 deg  | 0.0000 deg | 20639 ft  |
      | Bakken | Demo_3H | 0     | -12039 ft | 34745 ft | 0.0000 ft | 0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_3H | 233   | -22849 ft | 35477 ft | 10728 ft  | 0.0000 deg  | 0.0000 deg | 21550 ft  |
      | Bakken | Demo_3H | 121   | -12638 ft | 35145 ft | 10768 ft  | 0.0000 deg  | 0.0000 deg | 11274 ft  |
      | Bakken | Demo_3H | 19    | -12037 ft | 34727 ft | 3785.1 ft | 0.0000 deg  | 0.0000 deg | 3786.0 ft |
      | Bakken | Demo_3H | 213   | -21007 ft | 35450 ft | 10741 ft  | 0.0000 deg  | 0.0000 deg | 19708 ft  |
      | Bakken | Demo_3H | 53    | -12021 ft | 34724 ft | 6987.8 ft | 0.0000 deg  | 0.0000 deg | 6989.0 ft |
      | Bakken | Demo_4H | 0     | -13044 ft | 35392 ft | 0.0000 ft | 0.0000 deg  | 0.0000 deg | 0.0000 ft |
      | Bakken | Demo_4H | 256   | -23040 ft | 34636 ft | 10716 ft  | 0.0000 deg  | 0.0000 deg | 20967 ft  |
      | Bakken | Demo_4H | 53    | -13037 ft | 35364 ft | 4820.3 ft | 0.0000 deg  | 0.0000 deg | 4821.0 ft |
      | Bakken | Demo_4H | 14    | -13042 ft | 35390 ft | 1294.7 ft | 0.0000 deg  | 0.0000 deg | 1294.8 ft |
      | Bakken | Demo_4H | 144   | -13383 ft | 34594 ft | 10763 ft  | 0.0000 deg  | 0.0000 deg | 11298 ft  |
      | Bakken | Demo_4H | 140   | -13224 ft | 34576 ft | 10761 ft  | 0.0000 deg  | 0.0000 deg | 11138 ft  |

#    Examples: Permian
#      | field   | well | index | easting | northing |
#      | Permian | C1   | 0     | -60.14  | -0.91    |
#      | Permian | C1   | 527   | -391.31 | -4712.97 |
#      | Permian | C1   | 506   | -387.02 | -2731.01 |
#      | Permian | C1   | 316   | -190.85 | -37.16   |
#      | Permian | C1   | 355   | -195.47 | -39.29   |
#      | Permian | C1   | 419   | -205.74 | -70.32   |
#      | Permian | C2   | 0     | -19.88  | -0.29    |
#      | Permian | C2   | 527   | -65.28  | -4856.17 |
#      | Permian | C2   | 525   | -72.04  | -4687.58 |
#      | Permian | C2   | 487   | -130.08 | -1103.93 |
#      | Permian | C2   | 331   | -46.12  | 65.84    |
#      | Permian | C2   | 240   | -36.54  | 60.61    |
#      | Permian | C3   | 0     | 59.97   | 0.89     |
#      | Permian | C3   | 530   | 529.25  | -5169.96 |
#      | Permian | C3   | 478   | 427.90  | -475.20  |
#      | Permian | C3   | 374   | 197.17  | 35.92    |
#      | Permian | C3   | 182   | 150.80  | 18.43    |
#      | Permian | C3   | 132   | 130.82  | 12.05    |
#      | Permian | P1   | 0     | 20.04   | 0.30     |
#      | Permian | P1   | 535   | 229.52  | -5114.54 |
#      | Permian | P1   | 478   | 172.42  | -259.50  |
#      | Permian | P1   | 410   | 114.31  | 92.34    |
#      | Permian | P1   | 57    | 66.38   | 28.36    |
#      | Permian | P1   | 519   | 214.53  | -3659.28 |
#
#    Examples: Montney
#      | field   | well    | index | easting  | northing  |
#      | Montney | Hori_01 | 0     | -615.050 | 376.682   |
#      | Montney | Hori_01 | 101   | -545.283 | 203.339   |
#      | Montney | Hori_01 | 13    | -645.919 | 362.269   |
#      | Montney | Hori_01 | 22    | -657.965 | 347.512   |
#      | Montney | Hori_01 | 84    | -649.134 | 339.618   |
#      | Montney | Hori_01 | 91    | -618.307 | 297.645   |
#      | Montney | Hori_02 | 0     | -615.050 | 376.682   |
#      | Montney | Hori_02 | 211   | 1897.803 | -1526.118 |
#      | Montney | Hori_02 | 150   | 508.827  | -454.406  |
#      | Montney | Hori_02 | 109   | -384.796 | 226.856   |
#      | Montney | Hori_02 | 194   | 1530.445 | -1245.970 |
#      | Montney | Hori_02 | 18    | -634.650 | 345.162   |
#      | Montney | Hori_03 | 0     | -612.050 | 379.682   |
#      | Montney | Hori_03 | 201   | 1893.489 | -1335.094 |
#      | Montney | Hori_03 | 88    | -543.260 | 338.535   |
#      | Montney | Hori_03 | 167   | 1127.349 | -738.748  |
#      | Montney | Hori_03 | 173   | 1264.479 | -848.186  |
#      | Montney | Hori_03 | 10    | -608.251 | 359.357   |
#      | Montney | Vert_01 | 0     | 1842.150 | -1133.046 |
#      | Montney | Vert_01 | 101   | 1842.150 | -1133.046 |
#      | Montney | Vert_01 | 95    | 1842.150 | -1133.046 |
#      | Montney | Vert_01 | 78    | 1842.150 | -1133.046 |
#      | Montney | Vert_01 | 29    | 1842.150 | -1133.046 |
#      | Montney | Vert_01 | 42    | 1842.150 | -1133.046 |
