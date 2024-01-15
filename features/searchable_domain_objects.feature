#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2024 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#


Feature: Search for domain objects within a project
  As a data engineer,
  I want to find domain objects using different information
  In order to reduce manually written search code

  Scenario Outline: Search for data frame by name
    Given I have loaded the project for the field, '05Permian'
    When I query the loaded project for the data frame named '<name>' with <surrounding> whitespace
    Then I see a single data frame named '<name>' with no surrounding whitespace

    # TODO: Uncomment the commented out example when Geraldine deletes and recreates the project and its data frames.
    Examples:
      | name                                                     | surrounding          |
      | Microseismic Stage Specific Data Frame (Well: C3)        | trailing             |
#      | Well Log Set Stage Data Frame                            | no                   |
      | FR_allwells_LeakOffAnalysis - QCed(LeakOff Observations) | leading and trailing |
      | Fiber Observation Set Data Frame                         | leading              |

  Scenario Outline: Search for data frame by display name
    Given I have loaded the project for the field, '05Permian'
    When I query the loaded project for the data frame with display name '<display_name>' and <surrounding> whitespace
    Then I see a single data frame with display name '<display_name>' and no surrounding whitespace

    # TODO: Uncomment the commented out example when Geraldine deletes and recreates the project and its data frames.
    Examples:
      | display_name                                      | surrounding          |
      | Stage Data Frame                                  | no                   |
      | Microseismic Stage Specific Data Frame (Well: C3) | leading              |
#      | FusedDataFrame_FR-FDI_diff_dP_dT                  | trailing             |
      | Well Log Set Data Frame                           | leading and trailing |

  # TODO: Add tests to search for other domain objects using different criteria
  # - Data Frames
  # - Monitors
  # - Stages
  # - Stage parts
  # - Time Series
  # - Wells
