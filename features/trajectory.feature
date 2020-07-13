# Created by larry.jones at 6/10/2020
Feature: Low-level trajectory API (DOM API)
  As a data engineer,
  I want to access trajectory information conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  @wip
  Scenario Outline: Get the easting and northing trajectories in project units
    Given I have loaded the project for the field, '<field name>'
    When I query the project wells
    When I query the trajectory for well "<well name>"
    And I query the easting and northing arrays in the project reference frame in project units
    Then I see correct <easting> and <northing> values at <index>

    Examples: Bakken
      | field name | well name | index | easting | northing |
      | Bakken     | Demo_1H   | 0     | -12994  | 35549    |
      | Bakken     | Demo_1H   | 252   | -23010  | 36879    |
      | Bakken     | Demo_1H   | 146   | -13280  | 36870    |
      | Bakken     | Demo_1H   | 174   | -15903  | 36872    |
      | Bakken     | Demo_1H   | 99    | -12732  | 36547    |
      | Bakken     | Demo_1H   | 185   | -16947  | 36880    |
      | Bakken     | Demo_2H   | 0     | -13017  | 35483    |
      | Bakken     | Demo_2H   | 245   | -23024  | 36105    |
      | Bakken     | Demo_2H   | 203   | -19077  | 36105    |
      | Bakken     | Demo_2H   | 154   | -14420  | 36141    |
      | Bakken     | Demo_2H   | 155   | -14512  | 36142    |
      | Bakken     | Demo_2H   | 241   | -22683  | 36095    |
      | Bakken     | Demo_3H   | 0     | -12039  | 34745    |
      | Bakken     | Demo_3H   | 233   | -22849  | 35477    |
      | Bakken     | Demo_3H   | 121   | -12638  | 35145    |
      | Bakken     | Demo_3H   | 19    | -12037  | 34727    |
      | Bakken     | Demo_3H   | 213   | -21008  | 35450    |
      | Bakken     | Demo_3H   | 53    | -12021  | 34724    |
      | Bakken     | Demo_4H   | 0     | -13044  | 35392    |
      | Bakken     | Demo_4H   | 256   | -23040  | 34637    |
      | Bakken     | Demo_4H   | 53    | -13037  | 35364    |
      | Bakken     | Demo_4H   | 14    | -13042  | 35390    |
      | Bakken     | Demo_4H   | 144   | -13383  | 34595    |
      | Bakken     | Demo_4H   | 140   | -13224  | 34576    |


  Scenario: Get the easting and northing trajectories in project units (old)
    Given I have loaded the "Oasis_Crane_II" project
    When I query the trajectory for well "Crane_9B"
    And I query the easting and northing arrays in the project reference frame in project units
    Then I see 246 values in each array
    Then I see correct <easting> and <northing> values for specific points
      | index | easting  | northing |
      | 0     | -22.9020 | -65.0600 |
      | 245   | -10029.5 | 556.742  |
      | 156   | -1614.23 | 595.169  |
      | 121   | 271.234  | 582.288  |
      | 8     | -25.4570 | -62.1584 |
      | 76    | 159.898  | 282.814  |
