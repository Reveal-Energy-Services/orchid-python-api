#  Copyright (c) 2017-2022 Reveal Energy Services, Inc
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

Feature: Low-level example scripts
  As a data engineer,
  I want to access Orchid projects using the low-level API exemplified by scripts
  In order to complete my work in a timely manner

  Scenario: Automatically pick observations
    Given I have copied the low-level script, '<auto_pick.py>', to the repository root
    When I execute the script
    Then I see that <120> observations were picked

#  Scenario: Automatically pick observations and create stage attributes
#    Given I have copied the low-level script, '<auto_pick_and_create_stage_attribute.py>', to the repository root
#    When I execute the script
#    Then I see that <120> observations were picked
#    And I see that <2> attributes were created for each stage of each well
