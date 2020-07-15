# Created by larry.jones at 6/10/2020
Feature: Low-level trajectory API (DOM API)
  As a data engineer,
  I want to access trajectory information conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get the easting and northing trajectories in project units
    Given I have loaded the project for the field, '<field name>'
    When I query the project wells
    When I query the trajectory for well "<well name>"
    And I query the easting and northing arrays in the project reference frame in project units
    Then I see correct <easting> and <northing> values at <index>

    Examples: Bakken
      | field name | well name | index | easting  | northing  |
      | Bakken     | Demo_1H   | 0     | -12994   | 35549     |
      | Bakken     | Demo_1H   | 252   | -23010   | 36879     |
      | Bakken     | Demo_1H   | 146   | -13280   | 36870     |
      | Bakken     | Demo_1H   | 174   | -15903   | 36872     |
      | Bakken     | Demo_1H   | 99    | -12732   | 36547     |
      | Bakken     | Demo_1H   | 185   | -16947   | 36880     |
      | Bakken     | Demo_2H   | 0     | -13017   | 35483     |
      | Bakken     | Demo_2H   | 245   | -23024   | 36105     |
      | Bakken     | Demo_2H   | 203   | -19077   | 36105     |
      | Bakken     | Demo_2H   | 154   | -14420   | 36141     |
      | Bakken     | Demo_2H   | 155   | -14512   | 36142     |
      | Bakken     | Demo_2H   | 241   | -22683   | 36095     |
      | Bakken     | Demo_3H   | 0     | -12039   | 34745     |
      | Bakken     | Demo_3H   | 233   | -22849   | 35477     |
      | Bakken     | Demo_3H   | 121   | -12638   | 35145     |
      | Bakken     | Demo_3H   | 19    | -12037   | 34727     |
      | Bakken     | Demo_3H   | 213   | -21008   | 35450     |
      | Bakken     | Demo_3H   | 53    | -12021   | 34724     |
      | Bakken     | Demo_4H   | 0     | -13044   | 35392     |
      | Bakken     | Demo_4H   | 256   | -23040   | 34637     |
      | Bakken     | Demo_4H   | 53    | -13037   | 35364     |
      | Bakken     | Demo_4H   | 14    | -13042   | 35390     |
      | Bakken     | Demo_4H   | 144   | -13383   | 34595     |
      | Bakken     | Demo_4H   | 140   | -13224   | 34576     |

    Examples: Permian
      | field name | well name | index | easting  | northing  |
      | Permian    | C1        | 0     | -60.14   | -0.91     |
      | Permian    | C1        | 527   | -391.31  | -4712.97  |
      | Permian    | C1        | 506   | -387.02  | -2731.01  |
      | Permian    | C1        | 316   | -190.85  | -37.16    |
      | Permian    | C1        | 355   | -195.47  | -39.29    |
      | Permian    | C1        | 419   | -205.74  | -70.32    |
      | Permian    | C2        | 0     | -19.88   | -0.29     |
      | Permian    | C2        | 527   | -65.28   | -4856.17  |
      | Permian    | C2        | 525   | -72.04   | -4687.58  |
      | Permian    | C2        | 487   | -130.08  | -1103.93  |
      | Permian    | C2        | 331   | -46.12   | 65.84     |
      | Permian    | C2        | 240   | -36.54   | 60.61     |
      | Permian    | C3        | 0     | 59.97    | 0.89      |
      | Permian    | C3        | 530   | 529.25   | -5169.96  |
      | Permian    | C3        | 478   | 427.90   | -475.20   |
      | Permian    | C3        | 374   | 197.17   | 35.92     |
      | Permian    | C3        | 182   | 150.80   | 18.43     |
      | Permian    | C3        | 132   | 130.82   | 12.05     |
      | Permian    | P1        | 0     | 20.04    | 0.30      |
      | Permian    | P1        | 535   | 229.52   | -5114.54  |
      | Permian    | P1        | 478   | 172.42   | -259.50   |
      | Permian    | P1        | 410   | 114.31   | 92.34     |
      | Permian    | P1        | 57    | 66.38    | 28.36     |
      | Permian    | P1        | 519   | 214.53   | -3659.28  |

    Examples: Montney
      | field name | well name | index | easting  | northing  |
      | Montney    | Hori_01   | 0     | -615.050 | 376.682   |
      | Montney    | Hori_01   | 101   | -545.283 | 203.339   |
      | Montney    | Hori_01   | 13    | -645.919 | 362.269   |
      | Montney    | Hori_01   | 22    | -657.965 | 347.512   |
      | Montney    | Hori_01   | 84    | -649.134 | 339.618   |
      | Montney    | Hori_01   | 91    | -618.307 | 297.645   |
      | Montney    | Hori_02   | 0     | -615.050 | 376.682   |
      | Montney    | Hori_02   | 211   | 1897.803 | -1526.118 |
      | Montney    | Hori_02   | 150   | 508.827  | -454.406  |
      | Montney    | Hori_02   | 109   | -384.796 | 226.856   |
      | Montney    | Hori_02   | 194   | 1530.445 | -1245.970 |
      | Montney    | Hori_02   | 18    | -634.650 | 345.162   |
      | Montney    | Hori_03   | 0     | -612.050 | 379.682   |
      | Montney    | Hori_03   | 201   | 1893.489 | -1335.094 |
      | Montney    | Hori_03   | 88    | -543.260 | 338.535   |
      | Montney    | Hori_03   | 167   | 1127.349 | -738.748  |
      | Montney    | Hori_03   | 173   | 1264.479 | -848.186  |
      | Montney    | Hori_03   | 10    | -608.251 | 359.357   |
      | Montney    | Vert_01   | 0     | 1842.150 | -1133.046 |
      | Montney    | Vert_01   | 101   | 1842.150 | -1133.046 |
      | Montney    | Vert_01   | 95    | 1842.150 | -1133.046 |
      | Montney    | Vert_01   | 78    | 1842.150 | -1133.046 |
      | Montney    | Vert_01   | 29    | 1842.150 | -1133.046 |
      | Montney    | Vert_01   | 42    | 1842.150 | -1133.046 |
