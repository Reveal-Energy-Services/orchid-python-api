#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


Feature: Adapted IDataFrame DOM API
  As a data engineer,
  I want to access Orchid data frames conveniently using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Retrieved data frames has the correct identifying information
    Given I have loaded the project for the field, '<field>'
    When I query the data frames for the project for '<field>'
    Then I see a single data frame identified by <object_id>, <name> and <display_name>

#    Examples:
#      | field     | object_id                            | name                          | display_name |
#      | Permian-a | 0d2ec4b2-5766-461a-b57d-cc711576f46f | Project Data Frame 01         | None         |
#      | Permian-a | 0339e49a-a534-4d6f-b218-9862eeb73019 | FDI Observations              | None         |
#      | Permian-a | a48e71d9-50ce-49c4-bde2-c1915cb87bd4 | C3-Microseismic Data Frame 01 | None         |

    Examples: GnG
      | field | object_id                            | name                            | display_name |
      | GnG   | 9acfc88f-44f3-4f23-ac78-6ca94bae2d84 | Project Data Frame 01           | None         |
#      | GnG   | db5dc0c7-9132-4270-9bff-2bbf32ed93e3 | Fault Trace Set Data Frame 01   | None         |
#      | GnG   | e16f00ad-4c42-4726-8996-22a4632beaa9 | Stage Data Frame 01             | None         |
#      | GnG   | a287e63d-fd15-48e8-b5fc-99eb57244f18 | Well Log Set Data Frame 01      | None         |
#      | GnG   | 1cef6417-acb4-478c-b270-ca7022fc6003 | Horizon Marker Set Data Frame01 | None         |
