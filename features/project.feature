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

Feature: Low-level DOM API (project)
  As a data engineer,
  I want to access Orchid projects conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Get the name of a project
    Given I have loaded a project from the file, '<filename>'
    When I query the project name
    Then I see the text "<project>"
    Examples:
      | filename                                       | project                                 |
      | frankNstein_Bakken_UTM13_FEET.ifrac            | frankNstein_Bakken_UTM13_FEET           |
      | Project_frankNstein_Permian_UTM13_FEET.ifrac   | Project_frankNstein_subset02_UTM13_FEET |
      | Project-frankNstein_Montney_UTM13_METERS.ifrac | Project-frankNstein                     |

  Scenario Outline: Get the well counts from a project
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    Then I see that the project, <project>, has <well count> wells

    Examples: Bakken
      | field   | project                                 | well count |
      | Bakken  | frankNstein_Bakken_UTM13_FEET           | 4          |
      | Permian | Project_frankNstein_subset02_UTM13_FEET | 4          |
      | Montney | Project-frankNstein                     | 4          |

  Scenario Outline: Get the wells from a project
    Given I have loaded the project for the field, '<field>'
    When I query the project wells
    Then I see the well details <well>, <display name>, and <uwi> for <object id>

    Examples: Bakken
      | field  | well    | display name | uwi    | object id                            |
      | Bakken | Demo_1H | Demo_1H      | No UWI | ce9290bd-f9f1-45c2-b8c8-77b672ec0c43 |
      | Bakken | Demo_2H | Demo_2H      | No UWI | 22afba22-6be4-460d-9b83-a43b8b1eec11 |
      | Bakken | Demo_3H | Demo_3H      | No UWI | 5af7a14e-b7c9-4662-ba95-5ce3a0c39f60 |
      | Bakken | Demo_4H | Demo_4H      | No UWI | 9fe727b0-5fd1-4240-b475-51c1363edb0d |

    Examples: Permian
      | field   | well | display name | uwi    | object id                            |
      | Permian | C1   | C1           | No UWI | 5d11747e-b121-4bdb-8ff6-a3131aafa8e1 |
      | Permian | C2   | C2           | No UWI | 8d5ae42a-28aa-4e1f-9947-3b5511ac3143 |
      | Permian | C3   | C3           | No UWI | d44f70be-b77b-4da6-80d1-5edc76d98839 |
      | Permian | P1   | P1           | No UWI | 918a9c53-63a9-405d-bd03-f43422e0a4c4 |

    Examples: Montney
      | field   | well    | display name | uwi    | object id                            |
      | Montney | Hori_01 | Hori_01      | No UWI | c5eeddd4-62a8-4ab6-a630-bccd7ea629af |
      | Montney | Hori_02 | Hori_02      | No UWI | 1b1689dc-d46f-433f-ada8-a6fb58380954 |
      | Montney | Hori_03 | Hori_03      | No UWI | 40bd58a0-28f5-4af1-8f39-f40c3ebcb8c8 |
      | Montney | Vert_01 | Vert_01      | No UWI | 7f38537e-293b-4b88-8b85-099b28e43c6e |

  Scenario: Get the default well colors from a project
    Given I have loaded the project for the field, 'Montney'
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
