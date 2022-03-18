#  Copyright (c) 2017-2022 Reveal Energy Services, Inc
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

Feature: High-level DOM API (user data / stage QC information)
  As a Python developer
  I want to access Orchid stage QC information conveniently using Python
  In order to leverage my existing knowledge, code and data

  # I chose to duplicate the test information to avoid multiple opening of the project file
  Scenario: Change the stage QC information for specific stages
    Given I have loaded the changeable project for the field, 'bakken'
    When I change the specified stage correction status
      | well    | stage_no | to_correction_status | to_qc_notes                               |
      | Demo_1H | 1        | New                  |                                           |
      | Demo_2H | 50       | Confirmed            | Stage start/stop times confirmed by Ivalu |
      | Demo_2H | 15       | Confirmed            | Stage start/stop times confirmed by Ivalu |
      | Demo_1H | 10       | Unconfirmed          | Bad stage Ramazan                         |
      | Demo_2H | 21       | Confirmed            | Confirmed by Augustina                    |
      | Demo_4H | 3        | Confirmed            | Stage start/stop times confirmed by Jacob |
      | Demo_2H | 12       | Confirmed            | Confirmed start/stop Kerem                |
      | Demo_4H | 31       | Confirmed            | Confirmed Malthe                          |
      | Demo_2H | 20       | Confirmed            | Confirmed start/stop Kerem                |
      | Demo_2H | 38       | Confirmed            | Confirmed start/stop Kerem                |
    Then I see the changed stage correction status
      | well    | stage_no | to_correction_status | to_qc_notes                               |
      | Demo_1H | 1        | New                  |                                           |
      | Demo_2H | 50       | Confirmed            | Stage start/stop times confirmed by Ivalu |
      | Demo_2H | 15       | Confirmed            | Stage start/stop times confirmed by Ivalu |
      | Demo_1H | 10       | Unconfirmed          | Bad stage Ramazan                         |
      | Demo_2H | 21       | Confirmed            | Confirmed by Augustina                    |
      | Demo_4H | 3        | Confirmed            | Stage start/stop times confirmed by Jacob |
      | Demo_2H | 12       | Confirmed            | Confirmed start/stop Kerem                |
      | Demo_4H | 31       | Confirmed            | Confirmed Malthe                          |
      | Demo_2H | 20       | Confirmed            | Confirmed start/stop Kerem                |
      | Demo_2H | 38       | Confirmed            | Confirmed start/stop Kerem                |
