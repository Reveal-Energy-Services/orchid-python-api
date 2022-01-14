#  Copyright 2017-2022 Reveal Energy Services, Inc 
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

Feature: Low-level DOM API (treatment)
  As a data engineer,
  I want to access treatment information for stages conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Perform a pad analysis for a well treatment
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I calculate the total pumped volume, proppant mass, and median treating pressure for each stage
    And I see correct sample values for <well>, <index>, <stage_no>, <volume>, <proppant> and <median>

    Examples: Bakken
      | field  | well    | index | stage_no | volume          | proppant     | median      |
      | Bakken | Demo_1H | 0     | 1        | 3668.3 oil_bbl  | 128421.2 lb  | 6164.04 psi |
      | Bakken | Demo_1H | 49    | 50       | 4793.33 oil_bbl | 137810.07 lb | 6892.08 psi |
      | Bakken | Demo_1H | 27    | 28       | 6271.89 oil_bbl | 187685.84 lb | 8193.22 psi |
      | Bakken | Demo_1H | 22    | 23       | 7818.02 oil_bbl | 241601.3 lb  | 8224.48 psi |
      | Bakken | Demo_2H | 0     | 1        | 3920.99 oil_bbl | 135560.01 lb | 6535.85 psi |
      | Bakken | Demo_2H | 49    | 50       | 5329.46 oil_bbl | 99195.4 lb   | 6496.81 psi |
      | Bakken | Demo_2H | 44    | 45       | 5371.62 oil_bbl | 98148.74 lb  | 6722.27 psi |
      | Bakken | Demo_2H | 12    | 13       | 8415.64 oil_bbl | 171597.71 lb | 8235.68 psi |
      | Bakken | Demo_4H | 0     | 1        | 3870.54 oil_bbl | 139758.48 lb | 6322.39 psi |
      | Bakken | Demo_4H | 34    | 35       | 8294.68 oil_bbl | 132610.71 lb | 6442.86 psi |
      | Bakken | Demo_4H | 18    | 19       | 9380.16 oil_bbl | 246036.99 lb | 7927.32 psi |
      | Bakken | Demo_4H | 13    | 14       | 10775.5 oil_bbl | 303855.12 lb | 7973.23 psi |

    # With my current setup, `behave` will not read text, 'm\u00b3', as the character m with the unicode
    # superscript 3 character. To work around this, I "encode" this value as 'm^3'. The step will then convert
    # the text, 'm^3', to its unicode equivalent before testing.
    Examples: Montney
      | field   | well    | index | stage_no | volume      | proppant     | median    |
      | Montney | Hori_01 | 0     | 1        | 1651 m^3    | 241729.14 kg | 70.01 kPa |
      | Montney | Hori_01 | 14    | 15       | 1102.71 m^3 | 240220.73 kg | 59.4 kPa  |
      | Montney | Hori_01 | 9     | 10       | 1195.43 m^3 | 236053.95 kg | 58.83 kPa |
      | Montney | Hori_01 | 3     | 4        | 1434.46 m^3 | 239965.18 kg | 66.06 kPa |
      | Montney | Hori_02 | 0     | 1        | 904.53 m^3  | 116006.86 kg | 68.42 kPa |
      | Montney | Hori_02 | 28    | 29       | 483.2 m^3   | 121554.84 kg | 64 kPa    |
      | Montney | Hori_02 | 6     | 7        | 666.19 m^3  | 118818.07 kg | 65.6 kPa  |
      | Montney | Hori_02 | 19    | 20       | 612.17 m^3  | 121388.15 kg | 65.5 kPa  |
      | Montney | Hori_03 | 0     | 1        | 867.18 m^3  | 151695.27 kg | 70.1 kPa  |
      | Montney | Hori_03 | 27    | 28       | 626.74 m^3  | 152069.78 kg | 51.8 kPa  |
      | Montney | Hori_03 | 7     | 8        | 708.44 m^3  | 148828.75 kg | 69.1 kPa  |
      | Montney | Hori_03 | 23    | 24       | 553.83 m^3  | 148729.56 kg | 56.4 kPa  |
      | Montney | Vert_01 | 0     | 1        | NaN m^3     | NaN kg       | NaN kPa   |
      | Montney | Vert_01 | 3     | 4        | NaN m^3     | NaN kg       | NaN kPa   |
      | Montney | Vert_01 | 1     | 2        | NaN m^3     | NaN kg       | NaN kPa   |
      | Montney | Vert_01 | 2     | 3        | NaN m^3     | NaN kg       | NaN kPa   |
