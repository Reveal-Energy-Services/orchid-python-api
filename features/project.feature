# Created by larry.jones at 6/8/2020
Feature: Low-level DOM API (project)
  As a data engineer,
  I want to access Orchid projects conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario: Get the name of a project
    Given I have loaded the "Oasis_Crane_II" project
    When I query the project name
    Then I see the text "Oasis_Crane_II"

  Scenario: Get the wells from a project
    Given I have loaded the "Oasis_Crane_II" project
    When I query the project wells
    Then I see the well information
      | name         | display_name | uwi    |
      | Crane_7B     | Crane_7B     | No UWI |
      | Crane_9B     | Crane_9B     | No UWI |
      | Crane_41_26H | Crane_41_26H | No UWI |
      | Crane_12B    | Crane_12B    | No UWI |

  Scenario: Get the default well colors from a project
    Given I have loaded the "Oasis_Crane_II" project
    When I query the project default well colors
    Then I see the colors
      | red   | green | blue  |
      | 0.0   | 0.447 | 0.741 |
      | 0.85  | 0.325 | 0.098 |
      | 0.929 | 0.694 | 0.125 |
      | 0.494 | 0.184 | 0.556 |
      | 0.466 | 0.674 | 0.188 |
      | 0.301 | 0.745 | 0.933 |
      | 0.635 | 0.078 | 0.184 |
      | 0.0   | 0.447 | 0.741 |
      | 0.85  | 0.325 | 0.098 |
      | 0.929 | 0.694 | 0.125 |
      | 0.494 | 0.184 | 0.556 |
      | 0.466 | 0.674 | 0.188 |
      | 0.301 | 0.745 | 0.933 |
      | 0.635 | 0.078 | 0.184 |
