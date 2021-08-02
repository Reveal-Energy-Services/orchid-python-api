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

  Scenario Outline: Retrieved data frames have the correct identifying information
    Given I have loaded the project for the field, '<field>'
    When I query the project data frames identified by '<object_id>'
    Then I see a single data frame identified by <object_id>

    Examples: Permian Uncorrupted
      | field     | object_id                            |
      | Permian-u | c08e6988-d8f5-4d7b-bccd-de968a5b398b |
      | Permian-u | 08bea47e-5160-4f32-b8c4-3b3efa3d512b |
      | Permian-u | bbcdf86e-7cfe-437e-bc38-18d3389ada74 |
      | Permian-u | ce279d16-355c-4868-bbe7-21a8cb69cbc0 |
      | Permian-u | f1d406e6-c264-4d10-9fd5-b47a7be04aa9 |
      | Permian-u | 5304d2ac-dbf8-44db-8dd8-c2203714c456 |
      | Permian-u | 2b482b37-964e-4a54-89d3-8a28c24fe0c0 |
      | Permian-u | 34ec8d14-96b2-4156-abfd-18fe58e978e2 |

    Examples: Permian Corrupted
      | field     | object_id                            |
      | Permian-c | 0d2ec4b2-5766-461a-b57d-cc711576f46f |
      | Permian-c | 0339e49a-a534-4d6f-b218-9862eeb73019 |
      | Permian-c | a48e71d9-50ce-49c4-bde2-c1915cb87bd4 |

    Examples: GnG
      | field     | object_id                            |
      | GnG       | 9acfc88f-44f3-4f23-ac78-6ca94bae2d84 |
      | GnG       | db5dc0c7-9132-4270-9bff-2bbf32ed93e3 |
      | GnG       | e16f00ad-4c42-4726-8996-22a4632beaa9 |
      | GnG       | a287e63d-fd15-48e8-b5fc-99eb57244f18 |
      | GnG       | 1cef6417-acb4-478c-b270-ca7022fc6003 |

  Scenario Outline: Retrieved data frames have the correct alternate identifying information
    Given I have loaded the project for the field, '<field>'
    When I query all the project data frames by <name> and by <display_name>
    Then I see a single data frame alternatively identified by <name> and <display_name>

    Examples: Permian 06-16
      | field     | name                                                  | display_name                                          |
      | Permian-u | Project Data Frame 01                                 | Project Data Frame 01                                 |
      | Permian-u | FDI Observations                                      | FDI Observations                                      |
      | Permian-u | Microseismic Data Frame 01 (Potentially Corrupted)    | Microseismic Data Frame 01 (Potentially Corrupted)    |
      | Permian-u | Stage Data Frame 01                                   | Stage Data Frame 01                                   |
      | Permian-u | Well Log Set Data Frame 01                            | Well Log Set Data Frame 01                            |
      | Permian-u | C2-stg12_Xft_Permian_Edited_19-Nov-2018               | C2-stg12_Xft_Permian_Edited_19-Nov-2018               |
      | Permian-u | Fault Trace Set Data Frame 01                         | Fault Trace Set Data Frame 01                         |
      | Permian-u | Fault Set Data Frame 01                               | Fault Set Data Frame 01                               |

    Examples: Permian 04-12
      | field     | name                                                  | display_name                                          |
      | Permian-c | Project Data Frame 01 (Potentially Corrupted)         | Project Data Frame 01 (Potentially Corrupted)         |
      | Permian-c | FDI Observations (Potentially Corrupted)              | FDI Observations (Potentially Corrupted)              |
      | Permian-c | C3-Microseismic Data Frame 01 (Potentially Corrupted) | C3-Microseismic Data Frame 01 (Potentially Corrupted) |

    Examples: GnG
      | field     | name                                                  | display_name                                          |
      | GnG       | Project Data Frame 01                                 | Project Data Frame 01                                 |
      | GnG       | Fault Trace Set Data Frame 01                         | Fault Trace Set Data Frame 01                         |
      | GnG       | Stage Data Frame 01                                   | Stage Data Frame 01                                   |
      | GnG       | Well Log Set Data Frame 01                            | Well Log Set Data Frame 01                            |
      | GnG       | Horizon Marker Set Data Frame01                       | Horizon Marker Set Data Frame01                       |


  Scenario Outline: Identify potentially corrupted data frames
    Given I have loaded the project for the field, '<field>'
    When I query the project data frames identified by '<object_id>'
    Then I see the specified data frame <is_potentially_corrupt>

    Examples: Permian 06-16
      | field     | object_id                            | is_potentially_corrupt |
      | Permian-u | c08e6988-d8f5-4d7b-bccd-de968a5b398b | False                  |
      | Permian-u | 08bea47e-5160-4f32-b8c4-3b3efa3d512b | False                  |
      | Permian-u | bbcdf86e-7cfe-437e-bc38-18d3389ada74 | True                   |
      | Permian-u | ce279d16-355c-4868-bbe7-21a8cb69cbc0 | False                  |
      | Permian-u | f1d406e6-c264-4d10-9fd5-b47a7be04aa9 | False                  |
      | Permian-u | 5304d2ac-dbf8-44db-8dd8-c2203714c456 | False                  |
      | Permian-u | 2b482b37-964e-4a54-89d3-8a28c24fe0c0 | False                  |
      | Permian-u | 34ec8d14-96b2-4156-abfd-18fe58e978e2 | False                  |

    Examples: Permian 04-12
      | field     | object_id                            | is_potentially_corrupt |
      | Permian-c | 0d2ec4b2-5766-461a-b57d-cc711576f46f | True                   |
      | Permian-c | 0339e49a-a534-4d6f-b218-9862eeb73019 | True                   |
      | Permian-c | a48e71d9-50ce-49c4-bde2-c1915cb87bd4 | True                   |

    Examples: GnG
      | field     | object_id                            | is_potentially_corrupt |
      | GnG       | 9acfc88f-44f3-4f23-ac78-6ca94bae2d84 | False                  |
      | GnG       | db5dc0c7-9132-4270-9bff-2bbf32ed93e3 | False                  |
      | GnG       | e16f00ad-4c42-4726-8996-22a4632beaa9 | False                  |
      | GnG       | a287e63d-fd15-48e8-b5fc-99eb57244f18 | False                  |
      | GnG       | 1cef6417-acb4-478c-b270-ca7022fc6003 | False                  |

  Scenario: Sampled Permian 06-16 project data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'Project Data Frame 01'
    Then I see the sampled cells
      | sample | well_name | sh_easting  | sh_elev_msl | part_num | stage_pumped_vol | part_pump_time |
      | 0      | C1        | 11669250.21 | -2872.0     | 1.0      | 8423.638083      | 135.0          |
      | 1      | C1        | 11669250.21 | -2872.0     | 1.0      | 7643.193050      | 154.0          |
      | 2      | C1        | 11669250.21 | -2872.0     | 1.0      | 7981.894542      | 151.0          |
      | 6      | C1        | 11669250.21 | -2872.0     | 1.0      | 8658.708958      | 163.0          |
      | 44     | C2        | 11669250.83 | -2872.0     | 1.0      | 10014.638758     | 175.0          |
      | 64     | C3        | 11669252.01 | -2872.0     | 1.0      | 10722.694383     | 158.0          |
      | 70     | C3        | 11669252.01 | -2872.0     | 1.0      | 10209.304483     | 138.0          |
      | 87     | P1        | 11669251.42 | -2872.0     | NaN      | NaN              | NaN            |

  Scenario: Sampled Permian 06-16 FDI data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'FDI Observations'
    Then I see the sampled cells
      | sample | obs_set_name     | monitor_name             | signal_quality              | delta_t_263 | vol_to_pick  | dist_along_azm |
      | 0      | FDI Observations | P1 - 12555 - MonitorWell | Undrained Rock Deformation  | 82.316455   | 4299.649417  | 627.625427     |
      | 4      | FDI Observations | P1 - 12555 - MonitorWell | Fluid Migration Interaction | 165.366667  | 8083.696100  | 629.201111     |
      | 24     | FDI Observations | P1 - 12555 - MonitorWell | Fluid Migration Interaction | 161.539663  | 7812.571525  | 651.677185     |
      | 37     | FDI Observations | P1 - 12555 - MonitorWell | Fluid Migration Interaction | 185.866667  | 9852.505017  | 383.421539     |
      | 45     | FDI Observations | P1 - 12555 - MonitorWell | Undrained Rock Deformation  | 175.433333  | 10014.638758 | 374.613373     |
      | 60     | FDI Observations | P1 - 12555 - MonitorWell | Direct Fluid Interaction    | 75.147263   | 4356.223542  | 339.606445     |
      | 82     | FDI Observations | P1 - 12555 - MonitorWell | Undrained Rock Deformation  | 129.501522  | 7283.534992  | 358.738800     |
      | 83     | FDI Observations | P1 - 12555 - MonitorWell | Undrained Rock Deformation  | 115.197748  | 6803.360483  | 321.932404     |

  Scenario: Sampled Permian 06-16 microseismic data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'Microseismic Data Frame 01 (Potentially Corrupted)'
    Then I see the sampled cells
      | sample | northing    | p_amplitude | dist_3d    | hor_dist   | dist_azm   | dist_90    |
      | 0      | 11663896.37 | 0.003326    | 499.111743 | 498.619689 | NaN        | NaN        |
      | 125    | 11664521.24 | 0.009633    | NaN        | NaN        | 212.847744 | 212.813919 |
      | 218    | 11668658.41 | 0.003350    | 160.460792 | 159.241187 | 24.074542  | 24.000208  |
      | 221    | 11668660.34 | 0.006479    | 676.201188 | 671.302824 | 678.503481 | 678.413086 |
      | 269    | 11667224.22 | 0.006231    | 449.637745 | 449.446398 | 440.568094 | 440.689972 |
      | 284    | 11665719.88 | 0.000785    | 489.848493 | 470.937401 | 486.483152 | 486.400513 |
      | 405    | 11667844.41 | 0.009308    | 254.010571 | 253.549584 | 235.283835 | 235.172806 |
      | 479    | 11666700.54 | 0.003202    | 237.502735 | 233.605190 | 186.259267 | 186.299286 |

  Scenario: Sampled Permian 06-16 stage data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'Stage Data Frame 01'
    Then I see the sampled cells
      | sample | dept_min | rla5_max | hcal_mean | dtco_min | hdra_min | rhom_max |
      | 0      | 16573.0  | None     | None      | None     | None     | 2.7224   |
      | 3      | 15913.0  | None     | None      | None     | None     | 2.6397   |
      | 11     | 14353.0  | None     | None      | None     | None     | 2.7100   |
      | 12     | 14233.0  | None     | None      | None     | None     | 2.7688   |
      | 13     | 14113.0  | None     | None      | None     | None     | 2.7330   |
      | 20     | 13273.0  | None     | None      | None     | None     | 2.6642   |
      | 22     | 13033.0  | None     | None      | None     | None     | 2.6150   |
      | 24     | 12793.0  | None     | None      | None     | None     | 2.6258   |

  Scenario: Sampled Permian 06-16 well log set data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'Well Log Set Data Frame 01'
    Then I see the sampled cells
      | sample | dtco    | tnph_ls | rhoz   | hsgrd   | aplc_ls | rhom   |
      | 0      | NaN     | 0.5430  | NaN    | NaN     | NaN     | NaN    |
      | 5505   | 79.3469 | 0.2002  | 2.3959 | NaN     | NaN     | NaN    |
      | 5570   | 75.2105 | 0.2342  | 2.4360 | NaN     | NaN     | NaN    |
      | 7211   | 70.3145 | 0.1728  | 2.5795 | NaN     | NaN     | NaN    |
      | 7435   | 63.1550 | 0.0895  | 2.5584 | NaN     | NaN     | NaN    |
      | 8164   | 65.9307 | 0.1062  | 2.5278 | NaN     | NaN     | NaN    |
      | 15242  | NaN     | NaN     | NaN    | 84.7616 | 0.0613  | 2.6723 |
      | 17745  | NaN     | NaN     | NaN    | NaN     | NaN     | NaN    |

  Scenario: Sampled Permian 06-16 C2 Stage 12 Xft data frame
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'C2-stg12_Xft_Permian_Edited_19-Nov-2018'
    Then I see the sampled cells
      | sample | tr_pressure | slurry_rate | proppant_conc | cum_slurry  | xf         |
      | 0      | 7.50        | 0.00        | 0.00          | 0.000000    | NaN        |
      | 616    | 8523.66     | 30.63       | 0.00          | 221.605167  | NaN        |
      | 708    | 8872.18     | 28.71       | 0.00          | 311.449500  | NaN        |
      | 1166   | 8302.97     | 53.32       | 0.00          | 752.475667  | 267.281922 |
      | 2146   | 8179.10     | 72.04       | 0.56          | 2977.429333 | 619.506580 |
      | 3104   | 7.08        | 0.00        | 0.00          | 4756.123000 | NaN        |
      | 3574   | 0.00        | 0.00        | 0.00          | 4756.123000 | NaN        |
      | 3600   | 0.00        | 0.00        | 0.00          | 4756.123000 | NaN        |

  Scenario: Sampled Permian 06-16 fault trace set data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'Fault Trace Set Data Frame 01'
    Then I see the sampled cells
      | sample | fault_no | length       | mean_azm   |
      | 0      | 1        | 21981.651123 | 117.139913 |
      | 1      | 2        | 26871.854248 | 106.933235 |

  Scenario: Sampled Permian 06-16 fault set data frame is empty
    Given I have loaded the project for the field, 'Permian-u'
    When I query the loaded project for the data frame named 'Fault Set Data Frame 01'
    Then I see an empty data frame

  Scenario: Sampled Permian 04-12 project data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-c'
    When I query the loaded project for the data frame named 'Project Data Frame 01 (Potentially Corrupted)'
    Then I see the sampled cells
      | sample | bh_easting   | md_bottom | part_end_time                 | part_pumped_vol | p_net       | pump_time |
      | 0      | 2.141259e+06 | 16773.0   | 2018-11-13T22:37:40.000+00:00 | 8423.638083     | 7522.805942 | 135       |
      | 31     | 2.141585e+06 | 15865.0   | 2018-11-18T07:17:34.942+00:00 | 10292.204517    | 8128.011899 | 199       |
      | 39     | 2.141585e+06 | 14671.0   | 2018-11-20T22:10:27.000+00:00 | 10835.269733    | 7546.839462 | 209       |
      | 51     | 2.141585e+06 | 13016.0   | 2018-11-26T21:39:09.000+00:00 | 5337.422217     | 8881.240715 | 117       |
      | 52     | 2.141585e+06 | 12862.0   | 2018-11-27T04:39:44.000+00:00 | 11738.620958    | 8935.191079 | 216       |
      | 58     | 2.142179e+06 | 16676.0   | 2018-11-14T06:06:20.000+00:00 | 10096.559025    | 6573.648542 | 151       |
      | 62     | 2.142179e+06 | 16080.0   | 2018-11-15T19:43:47.000+00:00 | 10059.747108    | 7555.899247 | 147       |
      | 87     | 2.141879e+06 | NaN       | NaT                           | NaN             | NaN         | NaN       |

  Scenario: Sampled Permian 04-12 FDI data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-c'
    When I query the loaded project for the data frame named 'FDI Observations (Potentially Corrupted)'
    Then I see the sampled cells
      | sample | obs_set_name     | tr_stg_part_no | timestamp                     | delta_t          | delta_p    | vol_to_pick  |
      | 0      | FDI Observations | Stage-01       | 2018-11-13T21:45:11.987+00:00 | 01:22:18.9873152 | 0.362115   | 4299.649417  |
      | 1      | FDI Observations | Stage-02       | 2018-11-14T23:46:24.428+00:00 | 01:49:01.4282880 | 0.595053   | 5009.373675  |
      | 20     | FDI Observations | Stage-19       | 2018-11-27T16:14:52.341+00:00 | 02:42:24.3412096 | 39.059964  | 8056.843667  |
      | 26     | FDI Observations | Stage-25       | NaT                           | NaT              | NaN        | 8532.661850  |
      | 28     | FDI Observations | Stage-02       | 2018-11-13T04:20:10.000+00:00 | 02:20:11         | 6.170513   | 9859.784375  |
      | 45     | FDI Observations | Stage-20       | 2018-11-24T16:39:09.000+00:00 | 02:55:26         | 98.717645  | 10014.638758 |
      | 52     | FDI Observations | Stage-29       | 2018-11-27T19:13:34.110+00:00 | 02:01:22.1109888 | 94.454784  | 5920.732675  |
      | 53     | FDI Observations | Stage-01       | 2018-11-12T17:07:02.302+00:00 | 02:52:32.3021312 | 214.641797 | 11681.990733 |
      | 83     | FDI Observations | Stage-31       | 2018-11-29T04:02:02.864+00:00 | 01:55:11.8648576 | 31.818509  | 6803.360483  |

  Scenario: Sampled Permian 04-12 microseismic data frame have the correct cells
    Given I have loaded the project for the field, 'Permian-c'
    When I query the loaded project for the data frame named 'C3-Microseismic Data Frame 01 (Potentially Corrupted)'
    Then I see the sampled cells
      | sample | timestamp                     | northing    | depth_tvd_ss | dist_3d    | planar_dist_azm | vert_dist  |
      | 0      | 2018-11-12T14:14:30.000+00:00 | 11663896.37 | 11468.62     | 499.111743 | NaN             | NaN        |
      | 12     | 2018-11-12T14:41:56.500+00:00 | 11664068.45 | 11457.64     | 237.902313 | NaN             | NaN        |
      | 79     | 2018-11-12T16:53:39.700+00:00 | 11664385.37 | 11492.23     | 106.474419 | 28.857372       | 45.813477  |
      | 96     | 2018-11-13T02:32:16.600+00:00 | 11664433.12 | 11451.57     | NaN        | 365.32802       | 5.15332    |
      | 99     | 2018-11-13T02:38:59.650+00:00 | 11664441.39 | 11309.02     | NaN        | 297.033256      | 137.397461 |
      | 330    | 2018-11-15T03:15:00.000+00:00 | 11665140.80 | 11486.48     | 372.566085 | 360.100056      | 40.708984  |
      | 366    | 2018-11-15T10:31:00.000+00:00 | 11665255.69 | 11465.79     | 243.671    | 234.874205      | 20.594727  |
      | 479    | 2018-11-19T21:25:23.077+00:00 | 11666700.54 | 11395.45     | 237.502735 | 180.208587      | 47.088867  |

  Scenario: Sampled local Permian microseismic data frame have the correct UTC and local timestamp cells
    Given I have loaded the project for the field, 'Permian-n'
    When I query the loaded project for the data frame named 'Microseismic Data Frame 01'
    Then I see the sampled cells
      | sample | timestamp_utc                     | timestamp_local                   |
      | 0      | 2018-11-24T12:30:45.0000000+00:00 | 2018-11-24T06:30:45.0000000-06:00 |
      | 54     | 2018-11-12T15:47:48.1000000+00:00 | 2018-11-12T09:47:48.1000000-06:00 |
      | 169    | 2018-11-20T15:36:30.0000000+00:00 | 2018-11-20T09:36:30.0000000-06:00 |
      | 176    | 2018-11-16T08:55:57.0000000+00:00 | 2018-11-16T02:55:57.0000000-06:00 |
      | 197    | 2018-11-13T16:25:24.3333330+00:00 | 2018-11-13T10:25:24.3333330-06:00 |
      | 451    | 2018-11-19T02:45:52.5000000+00:00 | 2018-11-18T20:45:52.5000000-06:00 |
      | 468    | 2018-11-19T12:44:15.0000000+00:00 | 2018-11-19T06:44:15.0000000-06:00 |
      | 479    | 2018-11-19T21:25:23.0770000+00:00 | 2018-11-19T15:25:23.0770000-06:00 |

  Scenario: Sampled GnG project data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Project Data Frame 01'
    Then I see the sampled cells
      | sample | sh_easting | bh_northing  | bh_tdv      | stage_no | stage_length | p_net |
      | 0      | 6043583.9  | 6.040989e+06 | 3340.507353 | 1        | 57.0         | NaN   |
      | 23     | 6043583.9  | 6.040989e+06 | 3340.507353 | 24       | 57.0         | NaN   |
      | 37     | 6043593.0  | 6.040993e+06 | 3294.425439 | 5        | 28.0         | NaN   |
      | 58     | 6043593.0  | 6.040993e+06 | 3294.425439 | 26       | 28.0         | NaN   |
      | 65     | 6043593.0  | 6.040993e+06 | 3294.425439 | 33       | 29.0         | NaN   |
      | 89     | 6043602.2  | 6.040994e+06 | 3335.243499 | 1        | 21.0         | NaN   |
      | 170    | 6043611.3  | 6.041006e+06 | 3396.249537 | 39       | 29.0         | NaN   |
      | 210    | 6041330.2  | 6.042960e+06 | 3311.431913 | NaN      | NaN          | NaN   |

  Scenario: Sampled GnG fault trace set data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Fault Trace Set Data Frame 01'
    Then I see the sampled cells
      | sample | length     | mean_azm   |
      | 0      | 291.065844 | 35.607995  |
      | 6      | 221.386108 | 28.704976  |
      | 10     | 588.771423 | 42.394236  |
      | 18     | 310.084679 | 16.612221  |
      | 19     | 410.819195 | 46.381994  |
      | 20     | 133.201626 | 25.686016  |
      | 25     | 75.438820  | 14.980341  |
      | 29     | 188.149197 | 243.339280 |

  Scenario: Sampled GnG stage data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Stage Data Frame 01'
    Then I see the sampled cells
      | sample | dept_max | rla4_max | tend_max  | pefz_mean | lcal_mean | dpo_ls_min |
      | 0      | NaN      | NaN      | NaN       | NaN       | NaN       | NaN        |
      | 2      | NaN      | NaN      | NaN       | NaN       | NaN       | NaN        |
      | 9      | 16620.5  | NaN      | 4830.145  | NaN       | 8.486763  | -0.0132    |
      | 19     | 14140.0  | NaN      | 5855.6372 | NaN       | 8.827104  | 0.0184     |
      | 20     | 13904.0  | NaN      | 6054.6211 | NaN       | 8.817269  | 0.0406     |
      | 25     | 12729.5  | NaN      | 4131.1743 | NaN       | 8.602036  | -0.0315    |
      | 29     | 11830.5  | 738.3865 | 4695.3057 | 3.800887  | NaN       | NaN        |
      | 32     | 11128.5  | 238.891  | 4563.0464 | 3.73148   | NaN       | NaN        |

  Scenario: Sampled GnG well log set data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Well Log Set Data Frame 01'
    Then I see the sampled cells
      | sample | tvd_ss      | rla3    | dtco    | hdra    | rhoz   | lcal   |
      | 0      | 62.494284   | NaN     | NaN     | NaN     | NaN    | NaN    |
      | 628    | 158.207645  | NaN     | NaN     | NaN     | NaN    | NaN    |
      | 3748   | 633.599359  | NaN     | NaN     | NaN     | NaN    | NaN    |
      | 12682  | 1987.537640 | 2.7129  | 70.8107 | -0.0032 | 2.4729 | NaN    |
      | 23352  | 3319.966951 | 38.5122 | 73.5543 | -0.0009 | 2.5748 | NaN    |
      | 30556  | 3325.316915 | NaN     | NaN     | NaN     | NaN    | 8.9676 |
      | 30813  | 3326.166599 | NaN     | NaN     | NaN     | NaN    | 8.5149 |
      | 35490  | 3335.688645 | NaN     | NaN     | NaN     | NaN    | NaN    |

  Scenario: Sampled GnG horizon marker set data frame have the correct cells
    Given I have loaded the project for the field, 'GnG'
    When I query the loaded project for the data frame named 'Horizon Marker Set Data Frame01'
    Then I see the sampled cells
      | sample | marker_description | horizon_marker_set | boundary_type | well | md     | tvd         |
      | 0      | None               | Bakken             | Top           | #1   | 3300.0 | 3276.823560 |
      | 1      | None               | Bakken             | Top           | #4   | 3320.0 | 3296.963144 |
      | 2      | None               | Lodgepole          | Top           | #1   | 3250.0 | 3239.071727 |
      | 3      | None               | Lodgepole          | Top           | #4   | 3270.0 | 3253.421091 |
      | 4      | None               | Three Forks        | Top           | #4   | 3360.0 | 3323.416432 |
