# Created by larry.jones at 6/8/2020
Feature: Low-level DOM API (project)
  As a data engineer,
  I want to access Orchid projects conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario: Get the name of a project
    Given I have loaded the "Oasis_Crane_II" project
    When I query the project name
    Then I see the text "Oasis_Crane_II"
