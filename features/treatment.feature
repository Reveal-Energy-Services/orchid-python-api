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

Feature: Low-level stages API (DOM)
  As a data engineer,
  I want to access treatment information for stages conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Perform a pad analysis for a well treatment
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    And I calculate the total fluid volume, proppant, and median treating pressure for each stage
    Then I see 135 stages for the project
    And I see correct sample values for <index>, <well>, <stage>, <md_top>, and <md_bottom>
    And I see correct sample aggregate values for <index>, <volume>, <proppant> and <median>

    Examples: Bakken
      | field  | index | well    | stage | md_top  | md_bottom | volume  | proppant | median  |
      | Bakken | 0     | Demo_1H | 1     | 20883.3 | 20934.0   | 3668.30 | 139702   | 6164.04 |
      | Bakken | 134   | Demo_4H | 35    | 11260.0 | 11485.0   | 8294.68 | 135936   | 6442.86 |
      | Bakken | 78    | Demo_2H | 29    | 15313.9 | 15461.9   | 6164.56 | 222663   | 7631.72 |
      | Bakken | 9     | Demo_1H | 10    | 19127.4 | 19274.6   | 8667.34 | 220929   | 8271.64 |
      | Bakken | 25    | Demo_1H | 26    | 15986.6 | 16133.8   | 6502.47 | 208507   | 7983.54 |
      | Bakken | 56    | Demo_2H | 7     | 19656.7 | 19804.7   | 8407.48 | 205751   | 8240.48 |
      | Bakken | 3     | Demo_1H | 4     | 20358.3 | 20410.3   | 4055.97 | 233982   | 6516.33 |
