#  Copyright (c) 2017-2024 KAPPA
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

Feature: Low-level example scripts
  As a data engineer,
  I want to access Orchid projects using the low-level API exemplified by scripts
  In order to complete my work in a timely manner

  Scenario Outline: Automatically pick observations
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script using project version <ifrac_version>
    Then I see that <observation_count> observations were picked

    Examples:
      | script_file_name             | ifrac_version | observation_count |
      | auto_pick.py                 | v2            | 120               |
      | auto_pick_iterate_example.py | v2            | 120               |
      | auto_pick.py                 | v11           | 120               |
      | auto_pick_iterate_example.py | v11           | 120               |

  Scenario Outline: Automatically pick observations and create stage attributes
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script using project version <ifrac_version>
    Then I see that <observation_count> observations were picked
    And I see that <attribute_count> attributes were created for each stage of each well

    Examples: auto_pick_and_create_stage_attributes
      | script_file_name                        | ifrac_version | observation_count | attribute_count |
      | auto_pick_and_create_stage_attribute.py | v2            | 120               | 2               |
      | auto_pick_and_create_stage_attribute.py | v11           | 120               | 2               |

  Scenario Outline: Add stages
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script using project version <ifrac_version>
    And I see the following added stages
      | stage_name | clusters | global_seq_no | stage_time_range                                |
      | Stage-36   | 0        | 0             | 2018-06-06T05:34:03.684/2018-06-06T07:19:35.560 |
      | Stage-37   | 0        | 0             | 2018-06-15T14:11:40.450/2018-06-15T15:10:11.200 |
      | Stage-38   | 7        | 0             | 2018-06-28T23:35:54.379/2018-06-29T01:18:05.840 |

    Examples: add_stages
      | script_file_name  | ifrac_version |
      | add_stages_low.py | v2            |
      | add_stages_low.py | v11           |

  Scenario Outline: Monitor time series
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script using project version <ifrac_version>
    Then I see all time series in the project
      """
      {UUID('07d3cc41-1040-4125-8e2e-71726a124181'): <orchid.native_time_series_adapter.NativeTimeSeriesAdapter object at 0x000001A74791DF70>,
       UUID('1b544d11-55bb-4058-a527-7368046045ec'): <orchid.native_time_series_adapter.NativeTimeSeriesAdapter object at 0x000001A7479200D0>,
       UUID('d46ce56b-db33-488f-901f-8ec060a4455c'): <orchid.native_time_series_adapter.NativeTimeSeriesAdapter object at 0x000001A747920220>,
       UUID('ed590275-68e9-4001-8934-40386dfd1472'): <orchid.native_time_series_adapter.NativeTimeSeriesAdapter object at 0x000001A74791D700>}
      """
    And I see all monitors in the project
      """
      {UUID('14607f23-95f4-4405-b34b-daa0f924c2be'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747926550>,
       UUID('182fa5d0-5695-40e8-ad59-ed18e796ee9c'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747926160>,
       UUID('4116e3d3-b1ba-4063-b41e-467c5c00eb20'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747920040>,
       UUID('44e7ad1c-f6b9-411c-84c3-fa903b1a516c'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747926940>,
       UUID('5b68d8c4-a578-44e7-bc08-b1d83483c4ec'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747918C70>,
       UUID('5e51285b-6ac9-4a23-a360-f56399e4fe6b'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A7479267F0>,
       UUID('6777b2fe-7575-4fed-a82a-bb0b0085152d'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A7479266A0>,
       UUID('6b024601-ef74-4a82-ae4a-2a91648cae07'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747926CD0>,
       UUID('8660a506-e2a3-4427-8a03-d20e60c214df'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747920EB0>,
       UUID('8fab7763-8cad-42f4-8d44-899f2e8691bc'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747920D90>,
       UUID('9d702765-5696-4b38-a54c-84813898f907'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747920F70>,
       UUID('be89b07b-e37f-4222-9759-acd5682dc7a0'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A747926400>,
       UUID('c1d35d86-a8a1-4e46-a303-f2f1011a399f'): <orchid.native_monitor_adapter.NativeMonitorAdapter object at 0x000001A7479262B0>}
      """
    And I see the monitor of interest
    """
    Monitor of interest:
      - Object ID: 5b68d8c4-a578-44e7-bc08-b1d83483c4ec
      - Display Name: Demo_2H - stage 1
    """
    And I see the object ID of the monitor time series
      """
      Object ID of monitor time series of interest: 07d3cc41-1040-4125-8e2e-71726a124181
      """
    And I see the first few time series samples for the monitor
      | sample_time               | sample_value |
      | 2018-05-27 18:46:21+00:00 | 13.21247     |
      | 2018-05-27 18:47:18+00:00 | 13.25400     |
      | 2018-05-27 18:47:48+00:00 | 13.28520     |
      | 2018-05-27 18:48:18+00:00 | 13.26438     |
      | 2018-05-27 18:48:48+00:00 | 13.24896     |
    And I see the time series name and data type
      """
      Name: MonitorData-Demo_2H, dtype: float64
      """

    Examples: monitor_time_series
      | script_file_name       | ifrac_version |
      | monitor_time_series.py | v2            |
      | monitor_time_series.py | v11           |

  Scenario Outline: Automatically create multi-pick observations
    Given I have copied the low-level script, '<script_file_name>', to the repository root
    When I execute the script using project version <ifrac_version>
    Then I see that the "ParentWellObservations" set has observations
      | leak_off_count | multi_pick_count |
      | 17             | 0                |
    And I see that the "Multi-pick Observation Set" set has observations
      | leak_off_count | multi_pick_count |
      | 0              | 5                |
    And I can successfully load the file after saving

    Examples: auto_pick_and_create_stage_attributes
      | script_file_name        | ifrac_version |
      | multi_picking_events.py | v11           |
