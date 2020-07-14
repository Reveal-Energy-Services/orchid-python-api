# Created by larry.jones at 7/14/2020
Feature: Low-level DOM API (stage)
  As a data engineer,
  I want to access Orchid projects conveniently using Python
  In order to leverage my existing knowledge, code and data

  @wip
  Scenario Outline: Get the stage counts for each well in a project
    Given I have loaded the project for the field, '<field name>'
    When I query the project wells
    Then I see <stage count> stages for well <well name>

    Examples: Bakken
      | field name | well name | stage count |
      | Bakken     | Demo_1H   | 50          |
      | Bakken     | Demo_2H   | 50          |
      | Bakken     | Demo_3H   | 1           |
      | Bakken     | Demo_4H   | 35          |

    Examples: Permian
      | field name | well name | stage count |
      | Permian    | C1        | 25          |
      | Permian    | C2        | 29          |
      | Permian    | C3        | 31          |
      | Permian    | P1        | 1           |

    Examples: Montney
      | field name | well name | stage count |
      | Montney    | Hori_01   | 15          |
      | Montney    | Hori_02   | 29          |
      | Montney    | Hori_03   | 28          |
      | Montney    | Vert_01   | 4           |
