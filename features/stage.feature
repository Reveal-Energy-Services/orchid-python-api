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
      | Bakken | Demo_4H | 35          |

    Examples: Permian
      | field   | well | stage count |
      | Permian | C1   | 25          |
      | Permian | C2   | 29          |
      | Permian | C3   | 31          |

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

  Scenario Outline: Calculate the bottom location for a stage
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see stage bottom location <well>, <stage_no>, <frame>, <x>, <y>, and <depth>

    Examples: Bakken
      | field  | well    | stage_no | frame       | x             | y              | depth       |
      | Bakken | Demo_1H | 1        | Well Head   | -9949.78 ft   | 1328.93 ft     | 10706.84 ft |
      | Bakken | Demo_1H | 50       | Project     | -13436.85 ft  | 36867.08 ft    | 10770.92 ft |
      | Bakken | Demo_1H | 4        | State Plane | 1980000.65 ft | 17498021.83 ft | 10712.56 ft |
      | Bakken | Demo_1H | 38       | State Plane | 1986629.59 ft | 17498034.85 ft | 10754.41 ft |
      | Bakken | Demo_2H | 1        | Project     | -22957.78 ft  | 36103.41 ft    | 10711.86 ft |
      | Bakken | Demo_2H | 50       | Well Head   | -347.42 ft    | 669.77 ft      | 10766.31 ft |
      | Bakken | Demo_2H | 3        | State Plane | 1979856.09 ft | 17497253.64 ft | 10713.03 ft |
      | Bakken | Demo_2H | 40       | Well Head   | -2320.70 ft   | 668.26 ft      | 10756.22 ft |
      | Bakken | Demo_4H | 1        | Project     | -22974.17 ft  | 34634.35 ft    | 10717.00 ft |
      | Bakken | Demo_4H | 35       | Well Head   | -524.98 ft    | -787.59 ft     | 10767.07 ft |
      | Bakken | Demo_4H | 9        | State Plane | 1981243.43 ft | 17495771.46 ft | 10728.06 ft |
      | Bakken | Demo_4H | 32       | Project     | -14425.49 ft  | 34608.42 ft    | 10759.68 ft |

    Examples: Montney
      | field   | well    | stage_no | frame       | x           | y            | depth     |
      | Montney | Hori_01 | 1        | Project     | 1867.08 m   | -1699.25 m   | 985.27 m  |
      | Montney | Hori_01 | 15       | Project     | -342.00 m   | 17.22 m      | 963.85 m  |
      | Montney | Hori_01 | 9        | Well Head   | 1220.21 m   | -1094.97 m   | 976.55 m  |
      | Montney | Hori_01 | 7        | State Plane | 658124.19 m | 6178007.10 m | 980.48 m  |
      | Montney | Hori_02 | 1        | State Plane | 659041.61 m | 6177489.54 m | 1091.18 m |
      | Montney | Hori_02 | 29       | Project     | -265.31 m   | 136.65 m     | 1079.20 m |
      | Montney | Hori_02 | 4        | Well Head   | 2251.94 m   | -1702.43 m   | 1089.77 m |
      | Montney | Hori_02 | 17       | Project     | 647.61 m    | -565.58 m    | 1088.27 m |
      | Montney | Hori_03 | 1        | State Plane | 659064.68 m | 6177658.76 m | 971.11 m  |
      | Montney | Hori_03 | 28       | Project     | -299.37 m   | 300.25 m     | 962.96 m  |
      | Montney | Hori_03 | 6        | Well Head   | 2079.32 m   | -1384.52 m   | 965.57 m  |
      | Montney | Hori_03 | 16       | Project     | 677.20 m    | -392.31 m    | 960.78 m  |
      | Montney | Vert_01 | 1        | Project     | 1842.15 m   | -1133.05 m   | 1074.50 m |
      | Montney | Vert_01 | 2        | Project     | 1842.15 m   | -1133.05 m   | 1024.50 m |
      | Montney | Vert_01 | 3        | State Plane | 659044.57 m | 6177836.62 m | 974.50 m  |
      | Montney | Vert_01 | 4        | Well Head   | 0.00 m      | 0.00 m       | 924.50 m  |

  Scenario Outline: Calculate the cluster counts for a stage
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see stage cluster count <well>, <stage_no>, and <cluster_count>

    Examples: Bakken
      | field  | well    | stage_no | cluster_count |
      | Bakken | Demo_1H | 1        | 2             |
      | Bakken | Demo_1H | 50       | 4             |
      | Bakken | Demo_1H | 4        | 4             |
      | Bakken | Demo_1H | 42       | 4             |
      | Bakken | Demo_2H | 1        | 8             |
      | Bakken | Demo_2H | 50       | 4             |
      | Bakken | Demo_2H | 42       | 4             |
      | Bakken | Demo_2H | 14       | 4             |
      | Bakken | Demo_4H | 1        | 8             |
      | Bakken | Demo_4H | 35       | 6             |
      | Bakken | Demo_4H | 3        | 4             |
      | Bakken | Demo_4H | 22       | 6             |

    Examples: Montney
      | field   | well    | stage_no | cluster_count |
      | Montney | Hori_01 | 1        | 1             |
      | Montney | Hori_01 | 15       | 1             |
      | Montney | Hori_01 | 6        | 1             |
      | Montney | Hori_01 | 14       | 1             |
      | Montney | Hori_02 | 1        | 1             |
      | Montney | Hori_02 | 28       | 1             |
      | Montney | Hori_02 | 14       | 1             |
      | Montney | Hori_02 | 17       | 1             |
      | Montney | Hori_03 | 1        | 1             |
      | Montney | Hori_03 | 28       | 1             |
      | Montney | Hori_03 | 11       | 1             |
      | Montney | Hori_03 | 21       | 1             |
      | Montney | Vert_01 | 1        | 1             |
      | Montney | Vert_01 | 2        | 1             |
      | Montney | Vert_01 | 3        | 1             |
      | Montney | Vert_01 | 4        | 1             |

  Scenario Outline: Calculate the cluster locations for a stage
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see stage cluster location <well>, <stage_no>, <cluster_no>, <frame>, <x>, <y>, and <depth>

    Examples: Bakken
      | field  | well    | stage_no | cluster_no | frame       | x             | y              | depth       |
      | Bakken | Demo_1H | 1        | 2          | Well Head   | -9899.14 ft   | 1327.94 ft     | 10707.58 ft |
      | Bakken | Demo_1H | 50       | 3          | State Plane | 1989082.45 ft | 17498030.50 ft | 10770.00 ft |
      | Bakken | Demo_1H | 30       | 2          | Well Head   | -4318.54 ft   | 1334.93 ft     | 10735.44 ft |
      | Bakken | Demo_1H | 15       | 3          | Project     | -20206.80 ft  | 36852.34 ft    | 10714.62 ft |
      | Bakken | Demo_2H | 1        | 4          | State Plane | 1979495.65 ft | 17497263.97 ft | 10711.95 ft |
      | Bakken | Demo_2H | 50       | 1          | State Plane | 1989056.74 ft | 17497314.42 ft | 10766.31 ft |
      | Bakken | Demo_2H | 21       | 4          | Project     | -18938.26 ft  | 36108.94 ft    | 10731.79 ft |
      | Bakken | Demo_2H | 30       | 3          | Well Head   | -4195.14 ft   | 640.79 ft      | 10742.82 ft |
      | Bakken | Demo_4H | 1        | 1          | State Plane | 1979447.09 ft | 17495795.77 ft | 10717.00 ft |
      | Bakken | Demo_4H | 35       | 3          | Project     | -13479.38 ft  | 34601.46 ft    | 10766.00 ft |
      | Bakken | Demo_4H | 26       | 6          | State Plane | 1986477.61 ft | 17495761.50 ft | 10756.97 ft |
      | Bakken | Demo_4H | 11       | 6          | Well Head   | -7303.75 ft   | -829.42 ft     | 10722.54 ft |

    Examples: Montney
      | field   | well    | stage_no | cluster_no | frame       | x           | y            | depth     |
      | Montney | Hori_01 | 1        | 1          | State Plane | 659000.89 m | 6177324.27 m | 987.62 m  |
      | Montney | Hori_01 | 15       | 1          | Well Head   | 203.66 m    | -305.76 m    | 962.61 m  |
      | Montney | Hori_01 | 10       | 1          | Project     | 377.19 m    | -543.60 m    | 974.40 m  |
      | Montney | Hori_01 | 2        | 1          | State Plane | 658842.83 m | 6177445.09 m | 986.82 m  |
      | Montney | Hori_02 | 1        | 1          | Project     | 1823.90 m   | -1468.04 m   | 1091.17 m |
      | Montney | Hori_02 | 29       | 1          | Well Head   | 320.78 m    | -218.66 m    | 1078.98 m |
      | Montney | Hori_02 | 5        | 1          | State Plane | 658733.50 m | 6177723.22 m | 1088.52 m |
      | Montney | Hori_02 | 17       | 1          | Project     | 619.24 m    | -543.02 m    | 1088.19 m |
      | Montney | Hori_03 | 1        | 1          | State Plane | 659034.62 m | 6177681.60 m | 970.90 m  |
      | Montney | Hori_03 | 28       | 1          | Project     | -335.49 m   | 311.16 m     | 961.96 m  |
      | Montney | Hori_03 | 2        | 1          | Well Head   | 2364.47 m   | -1607.47 m   | 969.93 m  |
      | Montney | Hori_03 | 22       | 1          | Well Head   | 779.40 m    | -389.37 m    | 964.47 m  |
      | Montney | Vert_01 | 1        | 1          | State Plane | 659044.57 m | 6177836.62 m | 1056.75 m |
      | Montney | Vert_01 | 2        | 1          | State Plane | 659044.57 m | 6177836.62 m | 1006.75 m |
      | Montney | Vert_01 | 3        | 1          | Project     | 1842.15 m   | -1133.05 m   | 956.75 m  |
      | Montney | Vert_01 | 4        | 1          | Well Head   | 0.00 m      | 0.00 m       | 906.75 m  |

  Scenario Outline: Calculate the top location for a stage
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see stage top location <well>, <stage_no>, <frame>, <x>, <y>, and <depth>

    Examples: Bakken
      | field  | well    | stage_no | frame       | x             | y              | depth       |
      | Bakken | Demo_1H | 1        | Well Head   | -9899.14 ft   | 1327.94 ft     | 10707.58 ft |
      | Bakken | Demo_1H | 50       | Well Head   | -295.65 ft    | 1320.65 ft     | 10769.85 ft |
      | Bakken | Demo_1H | 4        | State Plane | 1980052.61 ft | 17498020.42 ft | 10714.07 ft |
      | Bakken | Demo_1H | 38       | Project     | -15644.53 ft  | 36875.19 ft    | 10758.84 ft |
      | Bakken | Demo_2H | 1        | Project     | -22882.73 ft  | 36101.34 ft    | 10712.22 ft |
      | Bakken | Demo_2H | 50       | State Plane | 1989203.51 ft | 17497324.76 ft | 10768.23 ft |
      | Bakken | Demo_2H | 38       | Well Head   | -2567.44 ft   | 667.26 ft      | 10754.86 ft |
      | Bakken | Demo_2H | 19       | State Plane | 1983088.30 ft | 17497264.42 ft | 10727.03 ft |
      | Bakken | Demo_4H | 1        | Well Head   | -9863.91 ft   | -759.13 ft     | 10717.53 ft |
      | Bakken | Demo_4H | 35       | Project     | -13344.88 ft  | 34590.82 ft    | 10762.90 ft |
      | Bakken | Demo_4H | 8        | State Plane | 1981194.48 ft | 17495772.14 ft | 10729.40 ft |
      | Bakken | Demo_4H | 33       | State Plane | 1988534.51 ft | 17495772.51 ft | 10766.40 ft |

    Examples: Montney
      | field   | well    | stage_no | frame       | x           | y            | depth     |
      | Montney | Hori_01 | 1        | Well Head   | 2344.53 m   | -1968.70 m   | 988.91 m  |
      | Montney | Hori_01 | 15       | Project     | -478.23 m   | 127.63 m     | 964.28 m  |
      | Montney | Hori_01 | 7        | Project     | 785.50 m    | -853.64 m    | 977.35 m  |
      | Montney | Hori_01 | 10       | State Plane | 657510.84 m | 6178480.55 m | 973.21 m  |
      | Montney | Hori_02 | 1        | Well Head   | 2423.59 m   | -1832.70 m   | 1091.25 m |
      | Montney | Hori_02 | 29       | Project     | -322.66 m   | 180.15 m     | 1078.73 m |
      | Montney | Hori_02 | 10       | State Plane | 658324.33 m | 6178037.58 m | 1088.78 m |
      | Montney | Hori_02 | 26       | Project     | -91.15 m    | 8.58 m       | 1080.80 m |
      | Montney | Hori_03 | 1        | Project     | 1802.08 m   | -1265.32 m   | 970.70 m  |
      | Montney | Hori_03 | 28       | State Plane | 656830.01 m | 6179288.49 m | 961.03 m  |
      | Montney | Hori_03 | 6        | Project     | 1406.83 m   | -959.62 m    | 964.31 m  |
      | Montney | Hori_03 | 21       | Well Head   | 829.56 m    | -426.24 m    | 964.87 m  |
      | Montney | Vert_01 | 1        | Well Head   | 0.00 m      | 0.00 m       | 1039.00 m |
      | Montney | Vert_01 | 2        | State Plane | 659044.57 m | 6177836.62 m | 989.00 m  |
      | Montney | Vert_01 | 3        | Well Head   | 0.00 m      | 0.00 m       | 939.00 m  |
      | Montney | Vert_01 | 4        | Project     | 1842.15 m   | -1133.05 m   | 889.00 m  |

  Scenario Outline: Calculate additional stage treatment data
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I see additional treatment data for samples <well>, <stage_no>, <shmin>, <isip>, <start_time>, <stop_time>, and <pnet>

    Examples: Bakken
      | field  | well    | stage_no  | shmin       | isip        | start_time           | stop_time              | pnet        |
      | Bakken | Demo_1H | 1         | 8137.56 psi | 4748.92 psi | 6/6/2018 8:37:13 AM  | 6/6/2018 11:55:21 AM   | 1310.69 psi |
      | Bakken | Demo_1H | 9         | 8146.73 psi | 5085.00 psi | 6/12/2018 7:40:58 AM | 6/12/2018 10:12:32 AM  | 1642.89 psi |
      | Bakken | Demo_1H | 13        | 8145.78 psi | 5253.69 psi | 6/13/2018 7:24:06 PM | 6/13/2018 9:47:44 PM   | 1811.98 psi |
      | Bakken | Demo_2H | 2         | 8142.03 psi | 4951.80 psi | 6/8/2018 1:41:57 PM  | 6/8/2018 3:54:15 PM    | 1511.68 psi |
      | Bakken | Demo_2H | 21        | 8156.15 psi | 5150.00 psi | 6/17/2018 8:16:00 AM | 6/17/2018 10:22:46 AM  | 1703.91 psi |
      | Bakken | Demo_2H | 30        | 8164.82 psi | 5100.00 psi | 6/22/2018 1:31:17 PM | 6/22/2018 2:58:13 PM   | 1650.25 psi |
      | Bakken | Demo_4H | 4         | 8145.41 psi | 4919.07 psi | 6/7/2018 1:45:10 AM  | 6/7/2018 4:01:14 AM    | 1477.51 psi |
      | Bakken | Demo_4H | 6         | 8146.03 psi | 4883.45 psi | 6/8/2018 5:01:14 AM  | 6/8/2018 8:09:23 AM    | 1441.63 psi |
      | Bakken | Demo_4H | 35        | 8181.86 psi | 5178.00 psi | 6/28/2018 1:30:42 PM | 6/28/2018 3:32:57 PM   | 1721.05 psi |