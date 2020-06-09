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
        | number | name |
        | 1 | Crane_7B |
        | 2 | Crane_9B |
        | 3 | Crane_41_26H |
        | 3 | Crane_12B |
