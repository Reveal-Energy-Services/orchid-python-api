# Created by larry.jones at 6/10/2020
Feature: Low-level trajectory API (DOM API)
  As a data engineer,
  I want to access trajectory information conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario: Get the easting and northing trajectories in project units
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
