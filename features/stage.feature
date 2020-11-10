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

Feature: Low-level DOM API (stage)
  As a data engineer,
  I want to access Orchid projects conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get the stage counts for each well in a project
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    Then I see <stage count> stages for well <well>

    Examples: Bakken
      | field  | well    | stage count |
      | Bakken | Demo_1H | 50          |
      | Bakken | Demo_2H | 50          |
      | Bakken | Demo_3H | 1           |
      | Bakken | Demo_4H | 35          |

    Examples: Permian
      | field   | well | stage count |
      | Permian | C1   | 25          |
      | Permian | C2   | 29          |
      | Permian | C3   | 31          |
      | Permian | P1   | 1           |

    Examples: Montney
      | field   | well    | stage count |
      | Montney | Hori_01 | 15          |
      | Montney | Hori_02 | 29          |
      | Montney | Hori_03 | 28          |
      | Montney | Vert_01 | 4           |

  Scenario Outline: Calculate additional basic stage information
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see basic data <well>, <stage_no>, <name_without_well>, <order>, <global_stage_no>, and <connection>

    Examples: Bakken
      | field  | well    | stage_no | name_without_well | order | global_stage_no | connection  |
      | Bakken | Demo_1H | 1        | Stage-1           | 0     | 4               | PlugAndPerf |
      | Bakken | Demo_1H | 50       | Stage-50          | 49    | 128             | PlugAndPerf |
      | Bakken | Demo_1H | 4        | Stage-4           | 3     | 10              | PlugAndPerf |
      | Bakken | Demo_2H | 1        | Stage-1           | 0     | 2               | PlugAndPerf |
      | Bakken | Demo_2H | 50       | Stage-50          | 49    | 136             | PlugAndPerf |
      | Bakken | Demo_2H | 35       | Stage-35          | 34    | 97              | PlugAndPerf |
      | Bakken | Demo_2H | 13       | Stage-13          | 12    | 28              | PlugAndPerf |
      | Bakken | Demo_3H | 1        | Stage-1           | 0     | 1               | PlugAndPerf |
      | Bakken | Demo_4H | 1        | Stage-1           | 0     | 3               | PlugAndPerf |
      | Bakken | Demo_4H | 35       | Stage-35          | 34    | 129             | PlugAndPerf |
      | Bakken | Demo_4H | 29       | Stage-29          | 28    | 114             | PlugAndPerf |
      | Bakken | Demo_4H | 6        | Stage-6           | 5     | 15              | PlugAndPerf |

    Examples: Montney
      | field   | well    | stage_no | name_without_well | order | global_stage_no | connection  |
      | Montney | Hori_01 | 1        | Stage-1           | 0     | 3               | PlugAndPerf |
      | Montney | Hori_01 | 15       | Stage-15          | 14    | 73              | PlugAndPerf |
      | Montney | Hori_01 | 6        | Stage-6           | 5     | 12              | PlugAndPerf |
      | Montney | Hori_01 | 11       | Stage-11          | 10    | 24              | PlugAndPerf |
      | Montney | Hori_02 | 1        | Stage-1           | 0     | 1               | PlugAndPerf |
      | Montney | Hori_02 | 29       | Stage-29          | 28    | 70              | PlugAndPerf |
      | Montney | Hori_02 | 14       | Stage-14          | 13    | 43              | PlugAndPerf |
      | Montney | Hori_02 | 22       | Stage-22          | 21    | 59              | PlugAndPerf |
      | Montney | Hori_03 | 1        | Stage-1           | 0     | 4               | PlugAndPerf |
      | Montney | Hori_03 | 28       | Stage-28          | 27    | 76              | PlugAndPerf |
      | Montney | Hori_03 | 12       | Stage-12          | 11    | 42              | PlugAndPerf |
      | Montney | Hori_03 | 21       | Stage-21          | 20    | 60              | PlugAndPerf |
      | Montney | Vert_01 | 1        | Stage-1           | 0     | 2               | PlugAndPerf |
      | Montney | Vert_01 | 2        | Stage-2           | 1     | 14              | PlugAndPerf |
      | Montney | Vert_01 | 3        | Stage-3           | 2     | 16              | PlugAndPerf |
      | Montney | Vert_01 | 4        | Stage-4           | 3     | 18              | PlugAndPerf |

  Scenario Outline: Calculate the location top for a stage
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see stage top location <well>, <stage_no>, <frame>, <x>, <y>, and <depth>

    Examples: Bakken
      | field  | well    | stage_no | frame       | x             | y              | depth          |
      | Bakken | Demo_1H | 1        | Well Head   | -9899.14 ft   | 1327.94 ft     | 1327.94 ft     |
      | Bakken | Demo_1H | 50       | Well Head   | -295.65 ft    | 1320.65 ft     | 1320.65 ft     |
      | Bakken | Demo_1H | 4        | State Plane | 1980052.61 ft | 17498020.42 ft | 17498020.42 ft |
      | bakken | Demo_1H | 38       | Project     | -15644.53 ft  | 36875.19 ft    | 36875.19 ft    |
      | Bakken | Demo_2H | 1        | Project     | -22882.73 ft  | 36101.34 ft    | 36101.34 ft    |
      | Bakken | Demo_2H | 50       | State Plane | 1989203.51 ft | 17497324.76 ft | 17497324.76 ft |
      | Bakken | Demo_2H | 38       | Well Head   | -2567.44 ft   | 667.26 ft      | 667.26 ft      |
      | Bakken | Demo_2H | 19       | State Plane | 1983088.30 ft | 17497264.42 ft | 17497264.42 ft |
      | Bakken | Demo_3H | 1        | State Plane | 1989848.04 ft | 17496270.86 ft | 17496270.86 ft |
      | Bakken | Demo_4H | 1        | Well Head   | -9863.91 ft   | -759.13 ft     | -759.13 ft     |
      | Bakken | Demo_4H | 35       | Project     | -13344.88 ft  | 34590.82 ft    | 34590.82 ft    |
      | Bakken | Demo_4H | 8        | State Plane | 1981194.48 ft | 17495772.14 ft | 17495772.14 ft |
      | Bakken | Demo_4H | 33       | State Plane | 1988534.51 ft | 17495772.51 ft | 17495772.51 ft |

    Examples: Montney
      | field   | well    | stage_no | frame       | x           | y            | depth        |
      | Montney | Hori_01 | 1        | Well Head   | 2344.53 m   | -1968.70 m   | -1968.70 m   |
      | Montney | Hori_01 | 15       | Project     | -478.23 m   | 127.63 m     | 127.63 m     |
      | Montney | Hori_01 | 7        | Project     | 785.50 m    | -853.64 m    | -853.64 m    |
      | Montney | Hori_01 | 10       | State Plane | 657510.84 m | 6178480.55 m | 6178480.55 m |
      | Montney | Hori_02 | 1        | Well Head   | 2423.59 m   | -1832.70 m   | -1832.70 m   |
      | Montney | Hori_02 | 29       | Project     | -322.66 m   | 180.15 m     | 180.15 m     |
      | Montney | Hori_02 | 10       | State Plane | 658324.33 m | 6178037.58 m | 6178037.58 m |
      | Montney | Hori_02 | 26       | Project     | -91.15 m    | 8.58 m       | 8.58 m       |
      | Montney | Hori_03 | 1        | Project     | 1802.08 m   | -1265.32 m   | -1265.32 m   |
      | Montney | Hori_03 | 28       | Well Head   | 239.64 m    | -60.86 m     | -60.86 m     |
      | Montney | Hori_03 | 6        | Project     | 1406.83 m   | -959.62 m    | -959.62 m    |
      | Montney | Hori_03 | 21       | Well Head   | 829.56 m    | -426.24 m    | -426.24 m    |
      | Montney | Vert_01 | 1        | Well Head   | 0.00 m      | 0.00 m       | 0.00 m       |
      | Montney | Vert_01 | 2        | State Plane | 659044.57 m | 6177836.62 m | 6177836.62 m |
      | Montney | Vert_01 | 3        | Well Head   | 0.00 m      | 0.00 m       | 0.00 m       |
      | Montney | Vert_01 | 4        | Project     | 1842.15 m   | -1133.05 m   | -1133.05 m   |
