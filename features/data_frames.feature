#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


Feature: Adapted IDataFrame DOM API
  As a data engineer,
  I want to access Orchid data frames conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Retrieved data frames dave the correct identifying information
    Given I have loaded the project for the field, '<field>'
    When I query the project data frames identified by '<object_id>'
    Then I see a single data frame identified by <object_id>, <name> and <display_name>

    Examples:
      | field     | object_id                            | name                          | display_name |
      | Permian-a | 0d2ec4b2-5766-461a-b57d-cc711576f46f | Project Data Frame 01         | Not set      |
      | Permian-a | 0339e49a-a534-4d6f-b218-9862eeb73019 | FDI Observations              | Not set      |
      | Permian-a | a48e71d9-50ce-49c4-bde2-c1915cb87bd4 | C3-Microseismic Data Frame 01 | Not set      |

    Examples: GnG
      | field | object_id                            | name                            | display_name |
      | GnG   | 9acfc88f-44f3-4f23-ac78-6ca94bae2d84 | Project Data Frame 01           | Not set      |
      | GnG   | db5dc0c7-9132-4270-9bff-2bbf32ed93e3 | Fault Trace Set Data Frame 01   | Not set      |
      | GnG   | e16f00ad-4c42-4726-8996-22a4632beaa9 | Stage Data Frame 01             | Not set      |
      | GnG   | a287e63d-fd15-48e8-b5fc-99eb57244f18 | Well Log Set Data Frame 01      | Not set      |
      | GnG   | 1cef6417-acb4-478c-b270-ca7022fc6003 | Horizon Marker Set Data Frame01 | Not set      |

#  Scenario: Sampled Permian project data frame have the correct cells
#    Given I have loaded the project for the field, 'Permian-a'
#    When I query the loaded project for the data frame named 'Project Data Frame 01'
#    Then I see the sampled cells
#      | sample | bh_easting   | md_bottom | part_end_time          | stage_part_pumped_vol | pnet        | pump_time |
#      | 0      | 2.141259e+06 | 16773.0   | 11/13/2018 10:37:40 PM | 8423.638083           | 7522.805942 | 135       |
#      | 31     | 2.141585e+06 | 15865.0   | 11/18/2018 7:17:34 AM  | 10292.204517          | 8128.011899 | 199       |
#      | 39     | 2.141585e+06 | 14671.0   | 11/20/2018 10:10:27 PM | 10835.269733          | 7546.839462 | 209       |
#      | 51     | 2.141585e+06 | 13016.0   | 11/26/2018 9:39:09 PM  | 5337.422217           | 8881.240715 | 117       |
#      | 52     | 2.141585e+06 | 12862.0   | 11/27/2018 4:39:44 AM  | 11738.620958          | 8935.191079 | 216       |
#      | 58     | 2.142179e+06 | 16676.0   | 11/14/2018 6:06:20 AM  | 10096.559025          | 6573.648542 | 151       |
#      | 62     | 2.142179e+06 | 16080.0   | 11/15/2018 7:43:47 PM  | 10059.747108          | 7555.899247 | 147       |
#      | 87     | 2.141879e+06 |           |                        |                       |             |           |
#
#  Scenario: Sampled Permian FDI data frame have the correct cells
#    Given I have loaded the project for the field, 'Permian-a'
#    When I query the loaded project for the data frame named 'FDI Observations'
#    Then I see the sampled cells
#      | sample | obs_set_name     | monitor_well | treatment_well | stage_part_no | delta_p    | vol_to_pick  |
#      | 0      | FDI Observations | P1           | C1             | Stage-01      | 0.362115   | 4299.649417  |
#      | 1      | FDI Observations | P1           | C1             | Stage-02      | 0.595053   | 5009.373675  |
#      | 20     | FDI Observations | P1           | C1             | Stage-19      | 39.059964  | 8056.843667  |
#      | 28     | FDI Observations | P1           | C2             | Stage-02      | 6.170513   | 9859.784375  |
#      | 45     | FDI Observations | P1           | C2             | Stage-20      | 98.717645  | 10014.638758 |
#      | 52     | FDI Observations | P1           | C2             | Stage-29      | 94.454784  | 5920.732675  |
#      | 53     | FDI Observations | P1           | C3             | Stage-01      | 214.641797 | 11681.990733 |
#      | 83     | FDI Observations | P1           | C3             | Stage-31      | 31.818509  | 6803.360483  |
#
#  Scenario: Sampled Permian microseismic data frame have the correct cells
#    Given I have loaded the project for the field, 'Permian-a'
#    When I query the loaded project for the data frame named 'C3-Microseismic Data Frame 01'
#    Then I see the sampled cells
#      | sample | northing    | depth_tvd_ss | stage_no   | dist_3d    | planar_dist_azimuth | vert_dist |
#      | 0      | 11663896.37 | 11468.62     | 1          | 499.111743 |                     |           |
#      | 12     | 11664068.45 | 11457.64     | 1          | 237.902313 |                     |           |
#      | 79     | 11664385.37 | 11492.23     | 1          | 106.474419 | 28.857372           | 45.813477 |
#      | 96     | 11664433.12 | 11451.57     | 365.32802  | 5.15332    |                     |           |
#      | 99     | 11664441.39 | 11309.02     | 297.033256 | 137.397461 |                     |           |
#      | 330    | 11665140.80 | 11486.48     | 6          | 372.566085 | 360.100056          | 40.708984 |
#      | 366    | 11665255.69 | 11465.79     | 7          | 243.671    | 234.874205          | 20.594727 |
#      | 479    | 11666700.54 | 11395.45     | 16         | 237.502735 | 180.208587          | 47.088867 |

  Scenario: Sampled GnG project data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Project Data Frame 01'
    Then I see the sampled cells
      | sample | sh_easting | bh_northing  | bh_tdv      | stage_no | stage_length | p_net |
      | 0      | 6043583.9  | 6.040989e+06 | 3340.507353 | 1        | 57.0         |       |
      | 23     | 6043583.9  | 6.040989e+06 | 3340.507353 | 24       | 57.0         |       |
      | 37     | 6043593.0  | 6.040993e+06 | 3294.425439 | 5        | 28.0         |       |
      | 58     | 6043593.0  | 6.040993e+06 | 3294.425439 | 26       | 28.0         |       |
      | 65     | 6043593.0  | 6.040993e+06 | 3294.425439 | 33       | 29.0         |       |
      | 89     | 6043602.2  | 6.040994e+06 | 3335.243499 | 1        | 21.0         |       |
      | 170    | 6043611.3  | 6.041006e+06 | 3396.249537 | 39       | 29.0         |       |
      | 210    | 6041330.2  | 6.042960e+06 | 3311.431913 |          |              |       |

  Scenario: Sampled GnG fault trace set data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Fault Trace Set Data Frame 01'
    Then I see the sampled cells
      | sample | length     | mean_azimuth |
      | 0      | 291.065844 | 35.607995    |
      | 6      | 221.386108 | 28.704976    |
      | 10     | 588.771423 | 42.394236    |
      | 18     | 310.084679 | 16.612221    |
      | 19     | 410.819195 | 46.381994    |
      | 20     | 133.201626 | 25.686016    |
      | 25     | 75.438820  | 14.980341    |
      | 29     | 188.149197 | 243.339280   |

  Scenario: Sampled GnG stage data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Stage Data Frame 01'
    Then I see the sampled cells
      | sample | dept_max | rla4_max | tend_max  | pefz_mean | lcal_mean | dpo_ls_min |
      | 0      |          |          |           |           |           |            |
      | 2      |          |          |           |           |           |            |
      | 9      | 16620.5  |          | 4830.145  |           | 8.486763  | -0.0132    |
      | 19     | 14140.0  |          | 5855.6372 |           | 8.827104  | 0.0184     |
      | 20     | 13904.0  |          | 6054.6211 |           | 8.817269  | 0.0406     |
      | 25     | 12729.5  |          | 4131.1743 |           | 8.602036  | -0.0315    |
      | 29     | 11830.5  | 738.3865 | 4695.3057 | 3.800887  |           |            |
      | 32     | 11128.5  | 238.891  | 4563.0464 | 3.73148   |           |            |

  Scenario: Sampled GnG well log set data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Well Log Set Data Frame 01'
    Then I see the sampled cells
      | sample | tvd_ss      | rla3    | dtco    | hdra    | rhoz   | lcal   |
      | 0      | 62.494284   |         |         |         |        |        |
      | 628    | 158.207645  |         |         |         |        |        |
      | 3748   | 633.599359  |         |         |         |        |        |
      | 12682  | 1987.537640 | 2.7129  | 70.8107 | -0.0032 | 2.4729 |        |
      | 23352  | 3319.966951 | 38.5122 | 73.5543 | -0.0009 | 2.5748 |        |
      | 30556  | 3325.316915 |         |         |         |        | 8.9676 |
      | 30813  | 3326.166599 |         |         |         |        | 8.5149 |
      | 35490  | 3335.688645 |         |         |         |        |        |

#  Scenario: Sampled GnG horizon marker set data frame have the correct cells
#    Given I have loaded the project for the field, 'GnG'
#    When I query the loaded project for the data frame named 'Horizon Marker Set Data Frame01'
#    Then I see the sampled cells
#      | sample | marker_description | horizon_marker_set | boundary_type | well | md     | tvd         |
#      | 0      |                    | Bakken             | Top           | #1   | 3300.0 | 3276.823560 |
#      | 1      |                    | Bakken             | Top           | #4   | 3320.0 | 3296.963144 |
#      | 2      |                    | Lodgepole          | Top           | #1   | 3250.0 | 3239.071727 |
#      | 3      |                    | Lodgepole          | Top           | #4   | 3270.0 | 3253.421091 |
#      | 4      |                    | Three Forks        | Top           | #4   | 3360.0 | 3323.416432 |
