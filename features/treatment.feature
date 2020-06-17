# Created by larry.jones at 6/14/2020
Feature: Low-level stages API (DOM)
  As a data engineer,
  I want to access treatment information for stages conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario: Perform a pad analysis for a well treatment
    Given I have loaded the "Demo_Project" project
    When I query the stages for each well in the project
    And I calculate the total fluid volume, proppant, and median treating pressure for each stage
    Then I see 136 stages
    And I see correct sample values for <Project>, <WellName>, <Stage>, <MdTop>, and <MdBottom>
      | index | Project      | WellName | Stage | MdTop   | MdBottom |
      | 0     | Demo_Project | Demo_1H  | 1     | 20883.3 | 20934.0  |
      | 135   | Demo_Project | Demo_4H  | 35    | 11260.0 | 11485.0  |
      | 78    | Demo_Project | Demo_2H  | 29    | 15313.9 | 15461.9  |
      | 9     | Demo_Project | Demo_1H  | 10    | 19127.4 | 19274.6  |
      | 25    | Demo_Project | Demo_1H  | 26    | 15986.6 | 16133.8  |
      | 56    | Demo_Project | Demo_2H  | 7     | 19656.7 | 19804.7  |
      | 3     | Demo_Project | Demo_1H  | 4     | 20358.3 | 20410.3  |
    And I see correct sample aggregate values for <Volume>, <Proppant> and <Median>
      | index | Volume  | Proppant | Median  |
      | 0     | 3668.36 | 139702   | 6164.03 |
      | 135   | 8294.88 | 135941   | 6442.86 |
      | 78    | 6165.12 | 222663   | 7631.71 |
      | 9     | 8667.40 | 220929   | 8271.60 |
      | 25    | 6502.98 | 208507   | 7938.53 |
      | 56    | 8407.92 | 205751   | 8240.44 |
      | 3     | 4056.39 | 233985   | 6516.34 |
