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


Feature: Treatment curves API
  As a data engineer,
  I want to access treatment curves for stages conveniently from Orchid projects using Python
  In order to leverage my existing knowledge, code and data

  Scenario Outline: Sample the curves of a stage
    Given I have loaded the project for the field, '<field>'
    When I query the stages for each well in the project
    Then I see correct curve samples for <well>, <stage_no>, <curve_type>, <index>, <timestamp>, and <value>

    Examples: Bakken
      | field  | well    | stage_no | curve_type | index | timestamp             | value               |
      | Bakken | Demo_1H | 1        | pressure   | 3960  | 6/6/2018 2:35:00 PM   | -7.42 psi           |
      | Bakken | Demo_1H | 1        | pressure   | 4637  | 6/6/2018 2:46:17 PM   | -3.76 psi           |
      | Bakken | Demo_1H | 1        | pressure   | 6992  | 6/6/2018 3:25:32 PM   | 6848.79 psi         |
      | Bakken | Demo_1H | 1        | pressure   | 4747  | 6/6/2018 2:48:07 PM   | -0.79 psi           |
      | Bakken | Demo_1H | 1        | pressure   | 9557  | 6/6/2018 4:08:17 PM   | 6254.41 psi         |
      | Bakken | Demo_1H | 1        | pressure   | 7680  | 6/6/2018 3:37:00 PM   | 7214.85 psi         |
      | Bakken | Demo_1H | 1        | pressure   | 7836  | 6/6/2018 3:39:36 PM   | 6855.80 psi         |
      | Bakken | Demo_1H | 1        | pressure   | 3979  | 6/6/2018 2:35:19 PM   | -7.50 psi           |
#      | Bakken | Demo_1H | 1        | proppant   | 10607 | 6/6/2018 4:25:47 PM   | 2.15 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 1        | proppant   | 910   | 6/6/2018 1:44:10 PM   | -0.15 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 1        | proppant   | 1745  | 6/6/2018 1:58:05 PM   | 0.51 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 1        | proppant   | 5037  | 6/6/2018 2:52:57 PM   | -0.45 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 1        | proppant   | 22    | 6/6/2018 1:29:22 PM   | -0.26 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 1        | proppant   | 832   | 6/6/2018 1:42:52 PM   | -0.16 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 1        | proppant   | 11375 | 6/6/2018 4:38:35 PM   | -0.07 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 1        | proppant   | 3160  | 6/6/2018 2:21:40 PM   | -0.08 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 1        | slurry     | 8557  | 6/6/2018 3:51:37 PM   | 35.08 bbl/min       |
#      | Bakken | Demo_1H | 1        | slurry     | 5415  | 6/6/2018 2:59:15 PM   | 0.14 bbl/min        |
#      | Bakken | Demo_1H | 1        | slurry     | 8125  | 6/6/2018 3:44:25 PM   | 35.49 bbl/min       |
#      | Bakken | Demo_1H | 1        | slurry     | 156   | 6/6/2018 1:31:36 PM   | 0.00 bbl/min        |
#      | Bakken | Demo_1H | 1        | slurry     | 4115  | 6/6/2018 2:37:35 PM   | 0.14 bbl/min        |
#      | Bakken | Demo_1H | 1        | slurry     | 10808 | 6/6/2018 4:29:08 PM   | 35.16 bbl/min       |
#      | Bakken | Demo_1H | 1        | slurry     | 6091  | 6/6/2018 3:10:31 PM   | 0.23 bbl/min        |
#      | Bakken | Demo_1H | 1        | slurry     | 4386  | 6/6/2018 2:42:06 PM   | 1.04 bbl/min        |
      | Bakken | Demo_1H | 50       | pressure   | 2971  | 6/28/2018 1:29:31 PM  | 6880.38 psi         |
      | Bakken | Demo_1H | 50       | pressure   | 118   | 6/28/2018 12:41:58 PM | 7853.94 psi         |
      | Bakken | Demo_1H | 50       | pressure   | 3929  | 6/28/2018 1:45:29 PM  | 7008.58 psi         |
      | Bakken | Demo_1H | 50       | pressure   | 2817  | 6/28/2018 1:26:57 PM  | 6882.67 psi         |
      | Bakken | Demo_1H | 50       | pressure   | 2497  | 6/28/2018 1:21:37 PM  | 7109.52 psi         |
      | Bakken | Demo_1H | 50       | pressure   | 1897  | 6/28/2018 1:11:37 PM  | 6828.63 psi         |
      | Bakken | Demo_1H | 50       | pressure   | 260   | 6/28/2018 12:44:20 PM | 7954.80 psi         |
      | Bakken | Demo_1H | 50       | pressure   | 1913  | 6/28/2018 1:11:53 PM  | 6828.10 psi         |
#      | Bakken | Demo_1H | 50       | proppant   | 604   | 6/28/2018 12:50:04 PM | 0.79 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | proppant   | 2509  | 6/28/2018 1:21:49 PM  | 0.48 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | proppant   | 3233  | 6/28/2018 1:33:53 PM  | 0.86 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | proppant   | 1133  | 6/28/2018 12:58:53 PM | 0.84 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | proppant   | 2116  | 6/28/2018 1:15:16 PM  | 1.05 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | proppant   | 1835  | 6/28/2018 1:10:35 PM  | 1.06 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | proppant   | 2481  | 6/28/2018 1:21:21 PM  | 0.41 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | proppant   | 2782  | 6/28/2018 1:26:22 PM  | 0.50 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 50       | slurry     | 3067  | 6/28/2018 1:31:07 PM  | 71.73 bbl/min       |
#      | Bakken | Demo_1H | 50       | slurry     | 3872  | 6/28/2018 1:44:32 PM  | 71.73 bbl/min       |
#      | Bakken | Demo_1H | 50       | slurry     | 1877  | 6/28/2018 1:11:17 PM  | 71.86 bbl/min       |
#      | Bakken | Demo_1H | 50       | slurry     | 1167  | 6/28/2018 12:59:27 PM | 71.98 bbl/min       |
#      | Bakken | Demo_1H | 50       | slurry     | 24    | 6/28/2018 12:40:24 PM | 32.65 bbl/min       |
#      | Bakken | Demo_1H | 50       | slurry     | 2941  | 6/28/2018 1:29:01 PM  | 71.76 bbl/min       |
#      | Bakken | Demo_1H | 50       | slurry     | 1328  | 6/28/2018 1:02:08 PM  | 71.85 bbl/min       |
#      | Bakken | Demo_1H | 50       | slurry     | 2169  | 6/28/2018 1:16:09 PM  | 71.77 bbl/min       |
      | Bakken | Demo_1H | 41       | pressure   | 2427  | 6/26/2018 2:22:29 PM  | 7471.63 psi         |
      | Bakken | Demo_1H | 41       | pressure   | 3272  | 6/26/2018 2:36:34 PM  | 7512.44 psi         |
      | Bakken | Demo_1H | 41       | pressure   | 4045  | 6/26/2018 2:49:27 PM  | 7284.56 psi         |
      | Bakken | Demo_1H | 41       | pressure   | 1752  | 6/26/2018 2:11:14 PM  | 7623.87 psi         |
      | Bakken | Demo_1H | 41       | pressure   | 1969  | 6/26/2018 2:14:51 PM  | 7520.98 psi         |
      | Bakken | Demo_1H | 41       | pressure   | 143   | 6/26/2018 1:44:25 PM  | 7007.66 psi         |
      | Bakken | Demo_1H | 41       | pressure   | 4318  | 6/26/2018 2:54:00 PM  | 7141.08 psi         |
      | Bakken | Demo_1H | 41       | pressure   | 1653  | 6/26/2018 2:09:35 PM  | 7672.33 psi         |
#      | Bakken | Demo_1H | 41       | proppant   | 1833  | 6/26/2018 2:12:35 PM  | 1.06lb/gal (U.S.)   |
#      | Bakken | Demo_1H | 41       | proppant   | 2188  | 6/26/2018 2:18:30 PM  | 1.40 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 41       | proppant   | 3406  | 6/26/2018 2:38:48 PM  | 0.55 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 41       | proppant   | 514   | 6/26/2018 1:50:36 PM  | -0.11 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 41       | proppant   | 1498  | 6/26/2018 2:07:00 PM  | 1.15 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 41       | proppant   | 1586  | 6/26/2018 2:08:28 PM  | 1.12 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 41       | proppant   | 4683  | 6/26/2018 3:00:05 PM  | -0.04 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 41       | proppant   | 1427  | 6/26/2018 2:05:49 PM  | 0.97 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 41       | slurry     | 1976  | 6/26/2018 2:14:58 PM  | 71.88 bbl/min       |
#      | Bakken | Demo_1H | 41       | slurry     | 3273  | 6/26/2018 2:36:35 PM  | 71.87 bbl/min       |
#      | Bakken | Demo_1H | 41       | slurry     | 4813  | 6/26/2018 3:02:15 PM  | 0.38 bbl/min        |
#      | Bakken | Demo_1H | 41       | slurry     | 3542  | 6/26/2018 2:41:04 PM  | 71.80 bbl/min       |
#      | Bakken | Demo_1H | 41       | slurry     | 3701  | 6/26/2018 2:43:43 PM  | 71.79 bbl/min       |
#      | Bakken | Demo_1H | 41       | slurry     | 1927  | 6/26/2018 2:14:09 PM  | 71.91 bbl/min       |
#      | Bakken | Demo_1H | 41       | slurry     | 1409  | 6/26/2018 2:05:31 PM  | 71.90 bbl/min       |
#      | Bakken | Demo_1H | 41       | slurry     | 4135  | 6/26/2018 2:50:57 PM  | 71.46 bbl/min       |
      | Bakken | Demo_1H | 20       | pressure   | 2089  | 6/15/2018 10:01:23 PM | 6354.26 psi         |
      | Bakken | Demo_1H | 20       | pressure   | 6055  | 6/15/2018 11:07:29 PM | 8237.45 psi         |
      | Bakken | Demo_1H | 20       | pressure   | 1562  | 6/15/2018 9:52:36 PM  | 3427.11 psi         |
      | Bakken | Demo_1H | 20       | pressure   | 3195  | 6/15/2018 10:19:49 PM | 6034.64 psi         |
      | Bakken | Demo_1H | 20       | pressure   | 3887  | 6/15/2018 10:31:21 PM | 7358.01 psi         |
      | Bakken | Demo_1H | 20       | pressure   | 6797  | 6/15/2018 11:19:51 PM | 8055.14 psi         |
      | Bakken | Demo_1H | 20       | pressure   | 7593  | 6/15/2018 11:33:07 PM | 8123.00 psi         |
      | Bakken | Demo_1H | 20       | pressure   | 6810  | 6/15/2018 11:20:04 PM | 8053.74 psi         |
#      | Bakken | Demo_1H | 20       | proppant   | 7036  | 6/15/2018 11:23:50 PM | 1.06 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 20       | proppant   | 1361  | 6/15/2018 9:49:15 PM  | 0.08 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 20       | proppant   | 7562  | 6/15/2018 11:32:36 PM | 0.20 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 20       | proppant   | 1908  | 6/15/2018 9:58:22 PM  | 0.60 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 20       | proppant   | 7295  | 6/15/2018 11:28:09 PM | 1.46 lb/gal (U.S.)  |
#      | Bakken | Demo_1H | 20       | proppant   | 400   | 6/15/2018 9:33:14 PM  | -0.30 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 20       | proppant   | 2045  | 6/15/2018 10:00:39 PM | -0.02 lb/gal (U.S.) |
#      | Bakken | Demo_1H | 20       | proppant   | 187   | 6/15/2018 9:29:41 PM  | -0.20
#      | Bakken | Demo_1H | 20       | slurry     | 2500  | 6/15/2018 10:08:14 PM | 29.32 bbl/min       |
#      | Bakken | Demo_1H | 20       | slurry     | 4767  | 6/15/2018 10:46:01 PM | 70.08 bbl/min       |
#      | Bakken | Demo_1H | 20       | slurry     | 4340  | 6/15/2018 10:38:54 PM | 68.13 bbl/min       |
#      | Bakken | Demo_1H | 20       | slurry     | 6728  | 6/15/2018 11:18:42 PM | 70.15 bbl/min       |
#      | Bakken | Demo_1H | 20       | slurry     | 4255  | 6/15/2018 10:37:29 PM | 66.65 bbl/min       |
#      | Bakken | Demo_1H | 20       | slurry     | 2384  | 6/15/2018 10:06:18 PM | 29.40 bbl/min       |
#      | Bakken | Demo_1H | 20       | slurry     | 8183  | 6/15/2018 11:42:57 PM | 70.13 bbl/min       |
#      | Bakken | Demo_1H | 20       | slurry     | 5946  | 6/15/2018 11:05:40 PM | 70.05 bbl/min       |
      | Bakken | Demo_2H | 1        | pressure   | 6948  | 6/6/2018 6:54:21 AM   | 3208.19 psi         |
      | Bakken | Demo_2H | 1        | pressure   | 7430  | 6/6/2018 7:02:23 AM   | 6785.23 psi         |
      | Bakken | Demo_2H | 1        | pressure   | 2240  | 6/6/2018 5:35:53 AM   | 0.00 psi            |
      | Bakken | Demo_2H | 1        | pressure   | 4517  | 6/6/2018 6:13:50 AM   | 592.60 psi          |
      | Bakken | Demo_2H | 1        | pressure   | 3724  | 6/6/2018 6:00:37 AM   | 4059.63 psi         |
      | Bakken | Demo_2H | 1        | pressure   | 11631 | 6/6/2018 8:12:24 AM   | 6345.52 psi         |
      | Bakken | Demo_2H | 1        | pressure   | 3358  | 6/6/2018 5:54:31 AM   | 9.23 psi            |
      | Bakken | Demo_2H | 1        | pressure   | 6133  | 6/6/2018 6:40:46 AM   | 7324.85 psi         |
#      | Bakken | Demo_2H | 1        | proppant   | 9032  | 6/6/2018 7:29:05 AM   | -0.04 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 1        | proppant   | 12912 | 6/6/2018 8:33:45 AM   | 2.12 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 1        | proppant   | 1838  | 6/6/2018 5:29:11 AM   | 1.41 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 1        | proppant   | 4199  | 6/6/2018 6:08:32 AM   | 1.41 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 1        | proppant   | 7351  | 6/6/2018 7:01:04 AM   | -0.01 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 1        | proppant   | 12643 | 6/6/2018 8:29:16 AM   | 2.14 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 1        | proppant   | 2828  | 6/6/2018 5:45:41 AM   | 1.36 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 1        | proppant   | 598   | 6/6/2018 5:08:31 AM   | 1.41 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 1        | slurry     | 11349 | 6/6/2018 8:07:42 AM   | 35.69 bbl/min       |
#      | Bakken | Demo_2H | 1        | slurry     | 7792  | 6/6/2018 7:08:25 AM   | 2.78 bbl/min        |
#      | Bakken | Demo_2H | 1        | slurry     | 14101 | 6/6/2018 8:53:34 AM   | 35.56 bbl/min       |
#      | Bakken | Demo_2H | 1        | slurry     | 14561 | 6/6/2018 9:01:14 AM   | 35.45 bbl/min       |
#      | Bakken | Demo_2H | 1        | slurry     | 12676 | 6/6/2018 8:29:49 AM   | 35.45 bbl/min       |
#      | Bakken | Demo_2H | 1        | slurry     | 1402  | 6/6/2018 5:21:55 AM   | 0.01 bbl/min        |
#      | Bakken | Demo_2H | 1        | slurry     | 7197  | 6/6/2018 6:58:30 AM   | 16.64 bbl/min       |
#      | Bakken | Demo_2H | 1        | slurry     | 2535  | 6/6/2018 5:40:48 AM   | 0.0 bbl/min         |
      | Bakken | Demo_2H | 50       | pressure   | 5047  | 6/30/2018 12:54:07 AM | 6498.32 psi         |
      | Bakken | Demo_2H | 50       | pressure   | 6222  | 6/30/2018 1:13:42 AM  | 5440.37 psi         |
      | Bakken | Demo_2H | 50       | pressure   | 2486  | 6/30/2018 12:11:26 AM | 6707.05 psi         |
      | Bakken | Demo_2H | 50       | pressure   | 141   | 6/29/2018 11:32:21 PM | 7655.24 psi         |
      | Bakken | Demo_2H | 50       | pressure   | 5611  | 6/30/2018 1:03:31 AM  | 6322.34 psi         |
      | Bakken | Demo_2H | 50       | pressure   | 1584  | 6/29/2018 11:56:24 PM | 5333.86 psi         |
      | Bakken | Demo_2H | 50       | pressure   | 7102  | 6/30/2018 1:28:22 AM  | 4536.73 psi         |
      | Bakken | Demo_2H | 50       | pressure   | 5507  | 6/30/2018 1:01:47 AM  | 6340.79 psi         |
#      | Bakken | Demo_2H | 50       | proppant   | 5128  | 6/30/2018 12:55:28 AM | 0.73 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 50       | proppant   | 1980  | 6/30/2018 12:03:00 AM | -0.00 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 50       | proppant   | 1538  | 6/29/2018 11:55:38 PM | -0.06 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 50       | proppant   | 292   | 6/29/2018 11:34:52 PM | -0.10 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 50       | proppant   | 2433  | 6/30/2018 12:10:33 AM | 0.44 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 50       | proppant   | 6840  | 6/30/2018 1:24:00 AM  | -0.10 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 50       | proppant   | 1766  | 6/29/2018 11:59:26 PM | -0.05 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 50       | proppant   | 5595  | 6/30/2018 1:03:15 AM  | 0.96 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 50       | slurry     | 1124  | 6/29/2018 11:48:44 PM | 29.78 bbl/min       |
#      | Bakken | Demo_2H | 50       | slurry     | 74    | 6/29/2018 11:31:14 PM | 0.16 bbl/min        |
#      | Bakken | Demo_2H | 50       | slurry     | 6992  | 6/30/2018 1:26:32 AM  | 0.26 bbl/min        |
#      | Bakken | Demo_2H | 50       | slurry     | 5641  | 6/30/2018 1:04:01 AM  | 71.26 bbl/min       |
#      | Bakken | Demo_2H | 50       | slurry     | 672   | 6/29/2018 11:41:12 PM | 4.68 bbl/min        |
#      | Bakken | Demo_2H | 50       | slurry     | 3647  | 6/30/2018 12:30:47 AM | 72.00 bbl/min       |
#      | Bakken | Demo_2H | 50       | slurry     | 1716  | 6/29/2018 11:58:36 PM | 15.51 bbl/min       |
#      | Bakken | Demo_2H | 50       | slurry     | 2415  | 6/30/2018 12:10:15 AM | 72.02 bbl/min       |
      | Bakken | Demo_2H | 21       | pressure   | 7486  | 6/17/2018 3:12:49 PM  | 8003.40 psi         |
      | Bakken | Demo_2H | 21       | pressure   | 7488  | 6/17/2018 3:12:51 PM  | 8008.10 psi         |
      | Bakken | Demo_2H | 21       | pressure   | 3343  | 6/17/2018 2:03:46 PM  | 8199.19 psi         |
      | Bakken | Demo_2H | 21       | pressure   | 4394  | 6/17/2018 2:21:17 PM  | 8180.12 psi         |
      | Bakken | Demo_2H | 21       | pressure   | 6486  | 6/17/2018 2:56:09 PM  | 8157.84 psi         |
      | Bakken | Demo_2H | 21       | pressure   | 804   | 6/17/2018 1:21:27 PM  | 8366.81 psi         |
      | Bakken | Demo_2H | 21       | pressure   | 5497  | 6/17/2018 2:39:40 PM  | 8409.77 psi         |
      | Bakken | Demo_2H | 21       | pressure   | 3410  | 6/17/2018 2:04:53 PM  | 8177.02 psi         |
#      | Bakken | Demo_2H | 21       | proppant   | 2361  | 6/17/2018 1:47:24 PM  | 0.44 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 21       | proppant   | 6234  | 6/17/2018 2:51:57 PM  | 0.32 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 21       | proppant   | 3781  | 6/17/2018 2:11:04 PM  | 0.03 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 21       | proppant   | 2521  | 6/17/2018 1:50:04 PM  | 0.42 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 21       | proppant   | 999   | 6/17/2018 1:24:42 PM  | -0.02 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 21       | proppant   | 3898  | 6/17/2018 2:13:01 PM  | -0.03 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 21       | proppant   | 4382  | 6/17/2018 2:21:05 PM  | 0.63 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 21       | proppant   | 7186  | 6/17/2018 3:07:49 PM  | 1.22 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 21       | slurry     | 6831  | 6/17/2018 3:01:54 PM  | 69.49 bbl/min       |
#      | Bakken | Demo_2H | 21       | slurry     | 1143  | 6/17/2018 1:27:06 PM  | 28.21 bbl/min       |
#      | Bakken | Demo_2H | 21       | slurry     | 736   | 6/17/2018 1:20:19 PM  | 29.98 bbl/min       |
#      | Bakken | Demo_2H | 21       | slurry     | 5273  | 6/17/2018 2:35:56 PM  | 69.44 bbl/min       |
#      | Bakken | Demo_2H | 21       | slurry     | 1464  | 6/17/2018 1:32:27 PM  | 11.26 bbl/min       |
#      | Bakken | Demo_2H | 21       | slurry     | 3910  | 6/17/2018 2:13:13 PM  | 68.26 bbl/min       |
#      | Bakken | Demo_2H | 21       | slurry     | 4461  | 6/17/2018 2:22:24 PM  | 69.42 bbl/min       |
#      | Bakken | Demo_2H | 21       | slurry     | 2705  | 6/17/2018 1:53:08 PM  | 68.23 bbl/min       |
      | Bakken | Demo_2H | 44       | pressure   | 4064  | 6/29/2018 1:10:05 AM  | 6925.45 psi         |
      | Bakken | Demo_2H | 44       | pressure   | 1785  | 6/29/2018 12:32:06 AM | 5741.40 psi         |
      | Bakken | Demo_2H | 44       | pressure   | 4598  | 6/29/2018 1:18:59 AM  | 6787.36 psi         |
      | Bakken | Demo_2H | 44       | pressure   | 2757  | 6/29/2018 12:48:18 AM | 6878.46 psi         |
      | Bakken | Demo_2H | 44       | pressure   | 1637  | 6/29/2018 12:29:38 AM | 5977.23 psi         |
      | Bakken | Demo_2H | 44       | pressure   | 1030  | 6/29/2018 12:19:31 AM | 6601.06 psi         |
      | Bakken | Demo_2H | 44       | pressure   | 876   | 6/29/2018 12:16:57 AM | 6742.40 psi         |
      | Bakken | Demo_2H | 44       | pressure   | 6129  | 6/29/2018 1:44:30 AM  | 5378.83 psi         |
#      | Bakken | Demo_2H | 44       | proppant   | 4726  | 6/29/2018 1:21:07 AM  | 0.31 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 44       | proppant   | 4039  | 6/29/2018 1:09:40 AM  | -0.04 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 44       | proppant   | 6155  | 6/29/2018 1:44:56 AM  | -0.07 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 44       | proppant   | 386   | 6/29/2018 12:08:47 AM | -0.16 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 44       | proppant   | 2034  | 6/29/2018 12:36:15 AM | 0.19 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 44       | proppant   | 5716  | 6/29/2018 1:37:37 AM  | 0.03 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 44       | proppant   | 4265  | 6/29/2018 1:13:26 AM  | 0.23 lb/gal (U.S.)  |
#      | Bakken | Demo_2H | 44       | proppant   | 1162  | 6/29/2018 12:21:43 AM | -0.06 lb/gal (U.S.) |
#      | Bakken | Demo_2H | 44       | slurry     | 3023  | 6/29/2018 12:52:44 AM | 71.66 bbl/min       |
#      | Bakken | Demo_2H | 44       | slurry     | 2102  | 6/29/2018 12:37:23 AM | 71.41 bbl/min       |
#      | Bakken | Demo_2H | 44       | slurry     | 5629  | 6/29/2018 1:36:10 AM  | 71.66 bbl/min       |
#      | Bakken | Demo_2H | 44       | slurry     | 4423  | 6/29/2018 1:16:04 AM  | 71.49 bbl/min       |
#      | Bakken | Demo_2H | 44       | slurry     | 255   | 6/29/2018 12:06:36 AM | 0.24 bbl/min        |
#      | Bakken | Demo_2H | 44       | slurry     | 242   | 6/29/2018 12:06:23 AM | 0.20 bbl/min        |
#      | Bakken | Demo_2H | 44       | slurry     | 1947  | 6/29/2018 12:34:48 AM | 66.37 bbl/min       |
#      | Bakken | Demo_2H | 44       | slurry     | 5358  | 6/29/2018 1:31:39 AM  | 71.64 bbl/min       |
      | Bakken | Demo_4H | 1        | pressure   | 4219  | 6/6/2018 10:50:19 AM  | 6161.22 psi         |
      | Bakken | Demo_4H | 1        | pressure   | 489   | 6/6/2018 9:48:09 AM   | 6997.94 psi         |
      | Bakken | Demo_4H | 1        | pressure   | 5266  | 6/6/2018 11:07:46 AM  | 6410.75 psi         |
      | Bakken | Demo_4H | 1        | pressure   | 743   | 6/6/2018 9:52:23 AM   | 4581.68 psi         |
      | Bakken | Demo_4H | 1        | pressure   | 3961  | 6/6/2018 10:46:01 AM  | 6175.78 psi         |
      | Bakken | Demo_4H | 1        | pressure   | 5317  | 6/6/2018 11:08:37 AM  | 6398.76 psi         |
      | Bakken | Demo_4H | 1        | pressure   | 5490  | 6/6/2018 11:11:30 AM  | 6350.48 psi         |
      | Bakken | Demo_4H | 1        | pressure   | 6704  | 6/6/2018 11:31:44 AM  | 6207.48 psi         |
#      | Bakken | Demo_4H | 1        | proppant   | 5873  | 6/6/2018 11:17:53 AM  | 2.24 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 1        | proppant   | 6490  | 6/6/2018 11:28:10 AM  | 2.29 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 1        | proppant   | 2994  | 6/6/2018 10:29:54 AM  | 0.04 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 1        | proppant   | 2449  | 6/6/2018 10:20:49 AM  | -0.08 lb/gal (U.S.) |
#      | Bakken | Demo_4H | 1        | proppant   | 6059  | 6/6/2018 11:20:59 AM  | 2.22 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 1        | proppant   | 4607  | 6/6/2018 10:56:47 AM  | 1.31 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 1        | proppant   | 3458  | 6/6/2018 10:37:38 AM  | 0.59 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 1        | proppant   | 7425  | 6/6/2018 11:43:45 AM  | -0.04 lb/gal (U.S.) |
#      | Bakken | Demo_4H | 1        | slurry     | 5568  | 6/6/2018 11:12:48 AM  | 35.32 bbl/min       |
#      | Bakken | Demo_4H | 1        | slurry     | 2419  | 6/6/2018 10:20:19 AM  | 23.57 bbl/min       |
#      | Bakken | Demo_4H | 1        | slurry     | 3821  | 6/6/2018 10:43:41 AM  | 35.40 bbl/min       |
#      | Bakken | Demo_4H | 1        | slurry     | 1454  | 6/6/2018 10:04:14 AM  | 24.03 bbl/min       |
#      | Bakken | Demo_4H | 1        | slurry     | 7746  | 6/6/2018 11:49:06 AM  | 35.00 bbl/min       |
#      | Bakken | Demo_4H | 1        | slurry     | 2666  | 6/6/2018 10:24:26 AM  | 31.60 bbl/min       |
#      | Bakken | Demo_4H | 1        | slurry     | 6664  | 6/6/2018 11:31:04 AM  | 34.77 bbl/min       |
#      | Bakken | Demo_4H | 1        | slurry     | 1798  | 6/6/2018 10:09:58 AM  | 24.09 bbl/min       |
      | Bakken | Demo_4H | 35       | pressure   | 2686  | 6/28/2018 7:11:26 PM  | 6417.34 psi         |
      | Bakken | Demo_4H | 35       | pressure   | 5521  | 6/28/2018 7:58:41 PM  | 6456.36 psi         |
      | Bakken | Demo_4H | 35       | pressure   | 6193  | 6/28/2018 8:09:53 PM  | 6288.27 psi         |
      | Bakken | Demo_4H | 35       | pressure   | 4780  | 6/28/2018 7:46:20 PM  | 6467.84 psi         |
      | Bakken | Demo_4H | 35       | pressure   | 7432  | 6/28/2018 8:30:32 PM  | 5022.38 psi         |
      | Bakken | Demo_4H | 35       | pressure   | 7028  | 6/28/2018 8:23:48 PM  | 6388.34 psi         |
      | Bakken | Demo_4H | 35       | pressure   | 4967  | 6/28/2018 7:49:27 PM  | 6641.41 psi         |
      | Bakken | Demo_4H | 35       | pressure   | 7784  | 6/28/2018 8:36:24 PM  | -7.50 psi           |
#      | Bakken | Demo_4H | 35       | proppant   | 5280  | 6/28/2018 7:54:40 PM  | 0.23 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 35       | proppant   | 5404  | 6/28/2018 7:56:44 PM  | 0.25 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 35       | proppant   | 7722  | 6/28/2018 8:35:22 PM  | -0.20 lb/gal (U.S.) |
#      | Bakken | Demo_4H | 35       | proppant   | 2996  | 6/28/2018 7:16:36 PM  | -0.05 lb/gal (U.S.) |
#      | Bakken | Demo_4H | 35       | proppant   | 3586  | 6/28/2018 7:26:26 PM  | 0.43 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 35       | proppant   | 5831  | 6/28/2018 8:03:51 PM  | 0.38 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 35       | proppant   | 1722  | 6/28/2018 6:55:22 PM  | 0.39 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 35       | proppant   | 4705  | 6/28/2018 7:45:05 PM  | -0.02 lb/gal (U.S.) |
#      | Bakken | Demo_4H | 35       | slurry     | 1503  | 6/28/2018 6:51:43 PM  | 71.97 bbl/min       |
#      | Bakken | Demo_4H | 35       | slurry     | 4876  | 6/28/2018 7:47:56 PM  | 71.75 bbl/min       |
#      | Bakken | Demo_4H | 35       | slurry     | 7327  | 6/28/2018 8:28:47 PM  | 71.64 bbl/min       |
#      | Bakken | Demo_4H | 35       | slurry     | 2285  | 6/28/2018 7:04:45 PM  | 71.89 bbl/min       |
#      | Bakken | Demo_4H | 35       | slurry     | 4176  | 6/28/2018 7:36:16 PM  | 71.88 bbl/min       |
#      | Bakken | Demo_4H | 35       | slurry     | 3284  | 6/28/2018 7:21:24 PM  | 71.79 bbl/min       |
#      | Bakken | Demo_4H | 35       | slurry     | 682   | 6/28/2018 6:38:02 PM  | 52.93 bbl/min       |
#      | Bakken | Demo_4H | 35       | slurry     | 1116  | 6/28/2018 6:45:16 PM  | 71.90 bbl/min       |
      | Bakken | Demo_4H | 10       | pressure   | 9322  | 6/14/2018 5:42:45 AM  | 8119.43 psi         |
      | Bakken | Demo_4H | 10       | pressure   | 10516 | 6/14/2018 6:02:39 AM  | 8068.89 psi         |
      | Bakken | Demo_4H | 10       | pressure   | 12234 | 6/14/2018 6:31:17 AM  | 4742.12 psi         |
      | Bakken | Demo_4H | 10       | pressure   | 8051  | 6/14/2018 5:21:34 AM  | 8478.58 psi         |
      | Bakken | Demo_4H | 10       | pressure   | 4464  | 6/14/2018 4:21:47 AM  | 8302.14 psi         |
      | Bakken | Demo_4H | 10       | pressure   | 5918  | 6/14/2018 4:46:01 AM  | 8504.18 psi         |
      | Bakken | Demo_4H | 10       | pressure   | 561   | 6/14/2018 3:16:44 AM  | 9329.33 psi         |
      | Bakken | Demo_4H | 10       | pressure   | 6671  | 6/14/2018 4:58:34 AM  | 8248.34 psi         |
#      | Bakken | Demo_4H | 10       | proppant   | 8503  | 6/14/2018 5:29:06 AM  | 0.45 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 10       | proppant   | 3646  | 6/14/2018 4:08:09 AM  | 0.45 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 10       | proppant   | 11436 | 6/14/2018 6:17:59 AM  | 0.05 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 10       | proppant   | 8685  | 6/14/2018 5:32:08 AM  | 0.49 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 10       | proppant   | 3521  | 6/14/2018 4:06:04 AM  | 0.59 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 10       | proppant   | 5069  | 6/14/2018 4:31:52 AM  | 0.98 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 10       | proppant   | 12148 | 6/14/2018 6:29:51 AM  | -0.11 lb/gal (U.S.) |
#      | Bakken | Demo_4H | 10       | proppant   | 5902  | 6/14/2018 4:45:45 AM  | 0.49 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 10       | slurry     | 8227  | 6/14/2018 5:24:30 AM  | 71.91 bbl/min       |
#      | Bakken | Demo_4H | 10       | slurry     | 5533  | 6/14/2018 4:39:36 AM  | 71.80 bbl/min       |
#      | Bakken | Demo_4H | 10       | slurry     | 46    | 6/14/2018 3:08:09 AM  | 0.00 bbl/min        |
#      | Bakken | Demo_4H | 10       | slurry     | 8626  | 6/14/2018 5:31:09 AM  | 71.88 bbl/min       |
#      | Bakken | Demo_4H | 10       | slurry     | 3191  | 6/14/2018 4:00:34 AM  | 69.93158627 bbl/min |
#      | Bakken | Demo_4H | 10       | slurry     | 11885 | 6/14/2018 6:25:28 AM  | 0.00 bbl/min        |
#      | Bakken | Demo_4H | 10       | slurry     | 5106  | 6/14/2018 4:32:29 AM  | 71.94 bbl/min       |
#      | Bakken | Demo_4H | 10       | slurry     | 5191  | 6/14/2018 4:33:54 AM  | 71.87 bbl/min       |
      | Bakken | Demo_4H | 26       | pressure   | 7740  | 6/25/2018 10:44:15 AM | 6880.42 psi         |
      | Bakken | Demo_4H | 26       | pressure   | 4525  | 6/25/2018 9:50:40 AM  | 7137.98 psi         |
      | Bakken | Demo_4H | 26       | pressure   | 3497  | 6/25/2018 9:33:32 AM  | 7305.99 psi         |
      | Bakken | Demo_4H | 26       | pressure   | 1620  | 6/25/2018 9:02:15 AM  | 5770.82 psi         |
      | Bakken | Demo_4H | 26       | pressure   | 8410  | 6/25/2018 10:55:25 AM | 6635.30 psi         |
      | Bakken | Demo_4H | 26       | pressure   | 39    | 6/25/2018 8:35:54 AM  | 4848.66 psi         |
      | Bakken | Demo_4H | 26       | pressure   | 7250  | 6/25/2018 10:36:05 AM | 6995.44 psi         |
      | Bakken | Demo_4H | 26       | pressure   | 8631  | 6/25/2018 10:59:06 AM | 7184.69 psi         |
#      | Bakken | Demo_4H | 26       | proppant   | 1983  | 6/25/2018 9:08:18 AM  | -0.01 lb/gal (U.S.) |
#      | Bakken | Demo_4H | 26       | proppant   | 4960  | 6/25/2018 9:57:55 AM  | 0.83 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 26       | proppant   | 6044  | 6/25/2018 10:15:59 AM | 1.78 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 26       | proppant   | 3278  | 6/25/2018 9:29:53 AM  | 0.75 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 26       | proppant   | 4418  | 6/25/2018 9:48:53 AM  | 1.20 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 26       | proppant   | 4296  | 6/25/2018 9:46:51 AM  | 1.15 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 26       | proppant   | 3732  | 6/25/2018 9:37:27 AM  | 0.97 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 26       | proppant   | 8876  | 6/25/2018 11:03:11 AM | 0.07 lb/gal (U.S.)  |
#      | Bakken | Demo_4H | 26       | slurry     | 8610  | 6/25/2018 10:58:45 AM | 71.49 bbl/min       |
#      | Bakken | Demo_4H | 26       | slurry     | 7551  | 6/25/2018 10:41:06 AM | 71.91 bbl/min       |
#      | Bakken | Demo_4H | 26       | slurry     | 2603  | 6/25/2018 9:18:38 AM  | 64.80 bbl/min       |
#      | Bakken | Demo_4H | 26       | slurry     | 418   | 6/25/2018 8:42:13 AM  | 0.28 bbl/min        |
#      | Bakken | Demo_4H | 26       | slurry     | 1117  | 6/25/2018 8:53:52 AM  | 25.17 bbl/min       |
#      | Bakken | Demo_4H | 26       | slurry     | 2263  | 6/25/2018 9:12:58 AM  | 66.84 bbl/min       |
#      | Bakken | Demo_4H | 26       | slurry     | 188   | 6/25/2018 8:38:23 AM  | 0.27 bbl/min        |
#      | Bakken | Demo_4H | 26       | slurry     | 2942  | 6/25/2018 9:24:17 AM  | 70.52 bbl/min       |

#    Examples: Montney
#      | field   | well    | stage_no | curve_type | index | timestamp             | value         |
      | Montney | Hori_01 | 1        | pressure   | 3604  | 4/6/2018 6:09:43 PM   | 63.94 kPa     |
      | Montney | Hori_01 | 1        | pressure   | 8423  | 4/6/2018 7:30:08 PM   | 74.15 kPa     |
      | Montney | Hori_01 | 1        | pressure   | 14699 | 4/6/2018 9:14:46 PM   | 27.84 kPa     |
      | Montney | Hori_01 | 1        | pressure   | 122   | 4/6/2018 5:11:40 PM   | 1.03 kPa      |
      | Montney | Hori_01 | 1        | pressure   | 5652  | 4/6/2018 6:43:51 PM   | 69.32 kPa     |
      | Montney | Hori_01 | 1        | pressure   | 5080  | 4/6/2018 6:34:19 PM   | 70.45 kPa     |
      | Montney | Hori_01 | 1        | pressure   | 6035  | 4/6/2018 6:50:15 PM   | 69.29 kPa     |
      | Montney | Hori_01 | 1        | pressure   | 7288  | 4/6/2018 7:11:11 PM   | 70.62 kPa     |
#      | Montney | Hori_01 | 1        | proppant   | 1853  | 4/6/2018 5:40:32 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 1        | proppant   | 12809 | 4/6/2018 8:43:16 PM   | 251.0 kg/m^3  |
#      | Montney | Hori_01 | 1        | proppant   | 7288  | 4/6/2018 7:11:11 PM   | 225.0 kg/m^3  |
#      | Montney | Hori_01 | 1        | proppant   | 7393  | 4/6/2018 7:12:56 PM   | 251.0 kg/m^3  |
#      | Montney | Hori_01 | 1        | proppant   | 696   | 4/6/2018 5:21:15 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 1        | proppant   | 15141 | 4/7/2018 5:00:23 AM   | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 1        | proppant   | 4684  | 4/6/2018 6:27:43 PM   | 24.0 kg/m^3   |
#      | Montney | Hori_01 | 1        | proppant   | 5772  | 4/6/2018 6:45:51 PM   | 125.0 kg/m^3  |
#      | Montney | Hori_01 | 1        | slurry     | 14446 | 4/6/2018 9:10:33 PM   | 0.0 m^3/min   |
#      | Montney | Hori_01 | 1        | slurry     | 8354  | 4/6/2018 7:28:59 PM   | 9.48 m^3/min  |
#      | Montney | Hori_01 | 1        | slurry     | 3519  | 4/6/2018 6:08:18 PM   | 3.11 m^3/min  |
#      | Montney | Hori_01 | 1        | slurry     | 2785  | 4/6/2018 5:56:04 PM   | 0.0 m^3/min   |
#      | Montney | Hori_01 | 1        | slurry     | 2870  | 4/6/2018 5:57:29 PM   | 0.0 m^3/min   |
#      | Montney | Hori_01 | 1        | slurry     | 6732  | 4/6/2018 7:01:53 PM   | 9.52 m^3/min  |
#      | Montney | Hori_01 | 1        | slurry     | 4878  | 4/6/2018 6:30:57 PM   | 9.18 m^3/min  |
#      | Montney | Hori_01 | 1        | slurry     | 11169 | 4/6/2018 8:15:54 PM   | 9.92 m^3/min  |
      | Montney | Hori_01 | 15       | pressure   | 6005  | 4/19/2018 9:55:59 PM  | 73.3 kPa      |
      | Montney | Hori_01 | 15       | pressure   | 4901  | 4/19/2018 9:36:16 PM  | 72.9 kPa      |
      | Montney | Hori_01 | 15       | pressure   | 857   | 4/19/2018 8:24:01 PM  | 35.6 kPa      |
      | Montney | Hori_01 | 15       | pressure   | 775   | 4/19/2018 8:22:34 PM  | 35.6 kPa      |
      | Montney | Hori_01 | 15       | pressure   | 1623  | 4/19/2018 8:37:43 PM  | 52.5 kPa      |
      | Montney | Hori_01 | 15       | pressure   | 2522  | 4/19/2018 8:53:48 PM  | 56.4 kPa      |
      | Montney | Hori_01 | 15       | pressure   | 2756  | 4/19/2018 8:57:59 PM  | 55.8 kPa      |
      | Montney | Hori_01 | 15       | pressure   | 7413  | 4/19/2018 10:21:06 PM | 65.6 kPa      |
#      | Montney | Hori_01 | 15       | proppant   | 1691  | 4/19/2018 8:38:57 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 15       | proppant   | 1756  | 4/19/2018 8:40:07 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 15       | proppant   | 7690  | 4/19/2018 10:26:02 PM | 475.0 kg/m^3  |
#      | Montney | Hori_01 | 15       | proppant   | 7289  | 4/19/2018 10:18:53 PM | 400.0 kg/m^3  |
#      | Montney | Hori_01 | 15       | proppant   | 6305  | 4/19/2018 10:01:19 PM | 225.0 kg/m^3  |
#      | Montney | Hori_01 | 15       | proppant   | 6143  | 4/19/2018 9:58:26 PM  | 200.0 kg/m^3  |
#      | Montney | Hori_01 | 15       | proppant   | 5911  | 4/19/2018 9:54:17 PM  | 150.0 kg/m^3  |
#      | Montney | Hori_01 | 15       | proppant   | 8475  | 4/19/2018 10:40:02 PM | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 15       | slurry     | 1304  | 4/19/2018 8:32:01 PM  | 1.77 m^3/min  |
#      | Montney | Hori_01 | 15       | slurry     | 1186  | 4/19/2018 8:29:55 PM  | 1.77 m^3/min  |
#      | Montney | Hori_01 | 15       | slurry     | 7477  | 4/19/2018 10:22:14 PM | 10.04 m^3/min |
#      | Montney | Hori_01 | 15       | slurry     | 7703  | 4/19/2018 10:26:16 PM | 10.01 m^3/min |
#      | Montney | Hori_01 | 15       | slurry     | 2830  | 4/19/2018 8:59:19 PM  | 10.03 m^3/min |
#      | Montney | Hori_01 | 15       | slurry     | 4001  | 4/19/2018 9:20:11 PM  | 9.81 m^3/min  |
#      | Montney | Hori_01 | 15       | slurry     | 5467  | 4/19/2018 9:46:22 PM  | 8.02 m^3/min  |
#      | Montney | Hori_01 | 15       | slurry     | 1521  | 4/19/2018 8:35:53 PM  | 1.71 m^3/min  |
      | Montney | Hori_01 | 12       | pressure   | 9057  | 4/12/2018 5:05:52 PM  | 28.8 kPa      |
      | Montney | Hori_01 | 12       | pressure   | 3471  | 4/12/2018 3:32:30 PM  | 52.1 kPa      |
      | Montney | Hori_01 | 12       | pressure   | 8464  | 4/12/2018 4:55:57 PM  | 64.8 kPa      |
      | Montney | Hori_01 | 12       | pressure   | 3004  | 4/12/2018 3:24:43 PM  | 51.6 kPa      |
      | Montney | Hori_01 | 12       | pressure   | 8207  | 4/12/2018 4:51:40 PM  | 66.3 kPa      |
      | Montney | Hori_01 | 12       | pressure   | 6015  | 4/12/2018 4:15:01 PM  | 68.7 kPa      |
      | Montney | Hori_01 | 12       | pressure   | 972   | 4/12/2018 2:50:46 PM  | 55.4 kPa      |
      | Montney | Hori_01 | 12       | pressure   | 4564  | 4/12/2018 3:50:46 PM  | 49.9 kPa      |
#      | Montney | Hori_01 | 12       | proppant   | 4194  | 4/12/2018 3:44:35 PM  | 450.0 kg/m^3  |
#      | Montney | Hori_01 | 12       | proppant   | 2001  | 4/12/2018 3:07:57 PM  | 125.0 kg/m^3  |
#      | Montney | Hori_01 | 12       | proppant   | 1587  | 4/12/2018 3:01:02 PM  | 51.0 kg/m^3   |
#      | Montney | Hori_01 | 12       | proppant   | 268   | 4/12/2018 2:39:01 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 12       | proppant   | 963   | 4/12/2018 2:50:37 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 12       | proppant   | 1010  | 4/12/2018 2:51:24 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 12       | proppant   | 8921  | 4/12/2018 5:03:36 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 12       | proppant   | 2587  | 4/12/2018 3:17:46 PM  | 223.0 kg/m^3  |
#      | Montney | Hori_01 | 12       | slurry     | 5949  | 4/12/2018 4:13:55 PM  | 7.6 m^3/min   |
#      | Montney | Hori_01 | 12       | slurry     | 8757  | 4/12/2018 5:00:52 PM  | 9.93 m^3/min  |
#      | Montney | Hori_01 | 12       | slurry     | 5706  | 4/12/2018 4:09:52 PM  | 7.38 m^3/min  |
#      | Montney | Hori_01 | 12       | slurry     | 1674  | 4/12/2018 3:02:29 PM  | 10.05 m^3/min |
#      | Montney | Hori_01 | 12       | slurry     | 2238  | 4/12/2018 3:11:55 PM  | 10.15 m^3/min |
#      | Montney | Hori_01 | 12       | slurry     | 2715  | 4/12/2018 3:19:54 PM  | 10.02 m^3/min |
#      | Montney | Hori_01 | 12       | slurry     | 3548  | 4/12/2018 3:33:48 PM  | 9.99 m^3/min  |
#      | Montney | Hori_01 | 12       | slurry     | 836   | 4/12/2018 2:48:30 PM  | 1.75 m^3/min  |
      | Montney | Hori_01 | 3        | pressure   | 7636  | 4/7/2018 9:44:39 PM   | 67.62 kPa     |
      | Montney | Hori_01 | 3        | pressure   | 4287  | 4/7/2018 8:48:38 PM   | 31.6 kPa      |
      | Montney | Hori_01 | 3        | pressure   | 11646 | 4/7/2018 10:51:42 PM  | 70.3 kPa      |
      | Montney | Hori_01 | 3        | pressure   | 7318  | 4/7/2018 9:39:20 PM   | 66.31 kPa     |
      | Montney | Hori_01 | 3        | pressure   | 9138  | 4/7/2018 10:09:46 PM  | 28.51 kPa     |
      | Montney | Hori_01 | 3        | pressure   | 2991  | 4/7/2018 8:26:58 PM   | 31.27 kPa     |
      | Montney | Hori_01 | 3        | pressure   | 7611  | 4/7/2018 9:44:14 PM   | 67.7 kPa      |
      | Montney | Hori_01 | 3        | pressure   | 13865 | 4/7/2018 11:28:51 PM  | 72.73 kPa     |
#      | Montney | Hori_01 | 3        | proppant   | 7646  | 4/7/2018 9:44:49 PM   | 275.0 kg/m^3  |
#      | Montney | Hori_01 | 3        | proppant   | 10163 | 4/7/2018 10:26:54 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 3        | proppant   | 10130 | 4/7/2018 10:26:21 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 3        | proppant   | 12142 | 4/7/2018 11:00:01 PM  | 125.0 kg/m^3  |
#      | Montney | Hori_01 | 3        | proppant   | 1324  | 4/7/2018 7:59:05 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 3        | proppant   | 4549  | 4/7/2018 8:53:01 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 3        | proppant   | 3990  | 4/7/2018 8:43:40 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_01 | 3        | proppant   | 6490  | 4/7/2018 9:25:29 PM   | 150.0 kg/m^3  |
#      | Montney | Hori_01 | 3        | slurry     | 9078  | 4/7/2018 10:08:46 PM  | 0.0 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 1077  | 4/7/2018 7:54:57 PM   | 0.0 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 3311  | 4/7/2018 8:32:19 PM   | 1.91 m^3/min  |
#      | Montney | Hori_01 | 3        | slurry     | 14901 | 4/7/2018 11:46:11 PM  | 9.84 m^3/min  |
#      | Montney | Hori_01 | 3        | slurry     | 14496 | 4/7/2018 11:39:24 PM  | 10.07 m^3/min |
#      | Montney | Hori_01 | 3        | slurry     | 11382 | 4/7/2018 10:47:18 PM  | 8.67 m^3/min  |
#      | Montney | Hori_01 | 3        | slurry     | 603   | 4/7/2018 7:47:02 PM   | 0.06 m^3/min  |
#      | Montney | Hori_01 | 3        | slurry     | 13670 | 4/7/2018 11:25:35 PM  | 9.8 m^3/min   |
      | Montney | Hori_02 | 1        | pressure   | 3871  | 4/6/2018 11:50:46 AM  | 69.58 kPa     |
      | Montney | Hori_02 | 1        | pressure   | 722   | 4/6/2018 10:58:17 AM  | 67.51 kPa     |
      | Montney | Hori_02 | 1        | pressure   | 4156  | 4/6/2018 11:55:31 AM  | 70.85 kPa     |
      | Montney | Hori_02 | 1        | pressure   | 5995  | 4/6/2018 12:26:10 PM  | 68.8 kPa      |
      | Montney | Hori_02 | 1        | pressure   | 10139 | 4/6/2018 1:35:17 PM   | 1.08 kPa      |
      | Montney | Hori_02 | 1        | pressure   | 9487  | 4/6/2018 1:24:25 PM   | 1.04 kPa      |
      | Montney | Hori_02 | 1        | pressure   | 4319  | 4/6/2018 11:58:14 AM  | 70.48 kPa     |
      | Montney | Hori_02 | 1        | pressure   | 3399  | 4/6/2018 11:42:54 AM  | 70.24 kPa     |
#      | Montney | Hori_02 | 1        | proppant   | 9160  | 4/6/2018 1:18:58 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 1        | proppant   | 9629  | 4/6/2018 1:26:47 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 1        | proppant   | 922   | 4/6/2018 11:01:37 AM  | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 1        | proppant   | 7119  | 4/6/2018 12:44:56 PM  | 224.0 kg/m^3  |
#      | Montney | Hori_02 | 1        | proppant   | 6715  | 4/6/2018 12:38:11 PM  | 200.0 kg/m^3  |
#      | Montney | Hori_02 | 1        | proppant   | 6735  | 4/6/2018 12:38:31 PM  | 200.0 kg/m^3  |
#      | Montney | Hori_02 | 1        | proppant   | 8360  | 4/6/2018 1:05:38 PM   | 299.0 kg/m^3  |
#      | Montney | Hori_02 | 1        | proppant   | 9897  | 4/6/2018 1:31:15 PM   | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 1        | slurry     | 7581  | 4/6/2018 12:52:39 PM  | 8.03 m^3/min  |
#      | Montney | Hori_02 | 1        | slurry     | 365   | 4/6/2018 10:52:20 AM  | 0.0 m^3/min   |
#      | Montney | Hori_02 | 1        | slurry     | 2597  | 4/6/2018 11:29:32 AM  | 3.25 m^3/min  |
#      | Montney | Hori_02 | 1        | slurry     | 8733  | 4/6/2018 1:11:51 PM   | 8.01 m^3/min  |
#      | Montney | Hori_02 | 1        | slurry     | 4942  | 4/6/2018 12:08:37 PM  | 8.27 m^3/min  |
#      | Montney | Hori_02 | 1        | slurry     | 3606  | 4/6/2018 11:46:21 AM  | 7.81 m^3/min  |
#      | Montney | Hori_02 | 1        | slurry     | 2964  | 4/6/2018 11:35:39 AM  | 5.22 m^3/min  |
#      | Montney | Hori_02 | 1        | slurry     | 7744  | 4/6/2018 12:55:22 PM  | 8.03 m^3/min  |
      | Montney | Hori_02 | 29       | pressure   | 3193  | 4/19/2018 11:06:26 AM | 64.1 kPa      |
      | Montney | Hori_02 | 29       | pressure   | 2758  | 4/19/2018 10:59:11 AM | 64.5 kPa      |
      | Montney | Hori_02 | 29       | pressure   | 3535  | 4/19/2018 11:12:08 AM | 64.9 kPa      |
      | Montney | Hori_02 | 29       | pressure   | 2978  | 4/19/2018 11:02:51 AM | 64.0 kPa      |
      | Montney | Hori_02 | 29       | pressure   | 3521  | 4/19/2018 11:11:54 AM | 64.6 kPa      |
      | Montney | Hori_02 | 29       | pressure   | 2523  | 4/19/2018 10:55:16 AM | 64.9 kPa      |
      | Montney | Hori_02 | 29       | pressure   | 747   | 4/19/2018 10:25:36 AM | 46.8 kPa      |
      | Montney | Hori_02 | 29       | pressure   | 416   | 4/19/2018 10:20:05 AM | 51.0 kPa      |
#      | Montney | Hori_02 | 29       | proppant   | 938   | 4/19/2018 10:28:48 AM | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 29       | proppant   | 605   | 4/19/2018 10:23:14 AM | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 29       | proppant   | 588   | 4/19/2018 10:22:57 AM | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 29       | proppant   | 2106  | 4/19/2018 10:48:19 AM | 323.0 kg/m^3  |
#      | Montney | Hori_02 | 29       | proppant   | 2343  | 4/19/2018 10:52:16 AM | 375.0 kg/m^3  |
#      | Montney | Hori_02 | 29       | proppant   | 1114  | 4/19/2018 10:31:44 AM | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 29       | proppant   | 418   | 4/19/2018 10:20:07 AM | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 29       | proppant   | 3415  | 4/19/2018 11:10:08 AM | 475.0 kg/m^3  |
#      | Montney | Hori_02 | 29       | slurry     | 4072  | 4/19/2018 11:21:06 AM | 0.0 m^3/min   |
#      | Montney | Hori_02 | 29       | slurry     | 2239  | 4/19/2018 10:50:32 AM | 10.14 m^3/min |
#      | Montney | Hori_02 | 29       | slurry     | 613   | 4/19/2018 10:23:22 AM | 1.73 m^3/min  |
#      | Montney | Hori_02 | 29       | slurry     | 1333  | 4/19/2018 10:35:25 AM | 10.05 m^3/min |
#      | Montney | Hori_02 | 29       | slurry     | 2182  | 4/19/2018 10:49:35 AM | 10.15 m^3/min |
#      | Montney | Hori_02 | 29       | slurry     | 4039  | 4/19/2018 11:20:33 AM | 0.0 m^3/min   |
#      | Montney | Hori_02 | 29       | slurry     | 294   | 4/19/2018 10:18:03 AM | 1.72 m^3/min  |
#      | Montney | Hori_02 | 29       | slurry     | 1878  | 4/19/2018 10:44:31 AM | 10.12 m^3/min |
      | Montney | Hori_02 | 5        | pressure   | 1715  | 4/12/2018 1:31:31 AM  | 57.6 kPa      |
      | Montney | Hori_02 | 5        | pressure   | 4104  | 4/12/2018 2:11:23 AM  | 72.43 kPa     |
      | Montney | Hori_02 | 5        | pressure   | 4020  | 4/12/2018 2:09:59 AM  | 72.49 kPa     |
      | Montney | Hori_02 | 5        | pressure   | 1294  | 4/12/2018 1:24:29 AM  | 33.65 kPa     |
      | Montney | Hori_02 | 5        | pressure   | 4390  | 4/12/2018 2:16:09 AM  | 72.83 kPa     |
      | Montney | Hori_02 | 5        | pressure   | 6195  | 4/12/2018 2:46:22 AM  | 29.54 kPa     |
      | Montney | Hori_02 | 5        | pressure   | 5544  | 4/12/2018 2:35:25 AM  | 72.61 kPa     |
      | Montney | Hori_02 | 5        | pressure   | 332   | 4/12/2018 1:08:24 AM  | -0.04 kPa     |
#      | Montney | Hori_02 | 5        | proppant   | 4976  | 4/12/2018 2:25:57 AM  | 392.0 kg/m^3  |
#      | Montney | Hori_02 | 5        | proppant   | 1630  | 4/12/2018 1:30:06 AM  | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 5        | proppant   | 2018  | 4/12/2018 1:36:34 AM  | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 5        | proppant   | 4670  | 4/12/2018 2:20:49 AM  | 350.0 kg/m^3  |
#      | Montney | Hori_02 | 5        | proppant   | 4578  | 4/12/2018 2:19:17 AM  | 325.0 kg/m^3  |
#      | Montney | Hori_02 | 5        | proppant   | 5014  | 4/12/2018 2:26:35 AM  | 400.0 kg/m^3  |
#      | Montney | Hori_02 | 5        | proppant   | 5647  | 4/12/2018 2:37:08 AM  | 475.0 kg/m^3  |
#      | Montney | Hori_02 | 5        | proppant   | 764   | 4/12/2018 1:15:37 AM  | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 5        | slurry     | 5217  | 4/12/2018 2:29:58 AM  | 9.57 m^3/min  |
#      | Montney | Hori_02 | 5        | slurry     | 1408  | 4/12/2018 1:26:23 AM  | 2.03 m^3/min  |
#      | Montney | Hori_02 | 5        | slurry     | 4396  | 4/12/2018 2:16:15 AM  | 10.11 m^3/min |
#      | Montney | Hori_02 | 5        | slurry     | 2570  | 4/12/2018 1:45:46 AM  | 10.01 m^3/min |
#      | Montney | Hori_02 | 5        | slurry     | 2904  | 4/12/2018 1:51:21 AM  | 10.03 m^3/min |
#      | Montney | Hori_02 | 5        | slurry     | 4756  | 4/12/2018 2:22:15 AM  | 9.76 m^3/min  |
#      | Montney | Hori_02 | 5        | slurry     | 1060  | 4/12/2018 1:20:33 AM  | 2.01 m^3/min  |
#      | Montney | Hori_02 | 5        | slurry     | 2997  | 4/12/2018 1:52:54 AM  | 10.06 m^3/min |
      | Montney | Hori_02 | 17       | pressure   | 1851  | 4/16/2018 12:47:31 PM | 71.4 kPa      |
      | Montney | Hori_02 | 17       | pressure   | 3658  | 4/16/2018 1:18:37 PM  | 67.1 kPa      |
      | Montney | Hori_02 | 17       | pressure   | 2920  | 4/16/2018 1:05:52 PM  | 64.2 kPa      |
      | Montney | Hori_02 | 17       | pressure   | 4975  | 4/16/2018 1:41:19 PM  | 68.9 kPa      |
      | Montney | Hori_02 | 17       | pressure   | 3846  | 4/16/2018 1:21:53 PM  | 67.3 kPa      |
      | Montney | Hori_02 | 17       | pressure   | 5348  | 4/16/2018 1:47:45 PM  | 33.6 kPa      |
      | Montney | Hori_02 | 17       | pressure   | 5273  | 4/16/2018 1:46:30 PM  | 34.1 kPa      |
      | Montney | Hori_02 | 17       | pressure   | 3302  | 4/16/2018 1:12:32 PM  | 68.0 kPa      |
#      | Montney | Hori_02 | 17       | proppant   | 706   | 4/16/2018 12:27:44 PM | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 17       | proppant   | 4035  | 4/16/2018 1:25:10 PM  | 375.0 kg/m^3  |
#      | Montney | Hori_02 | 17       | proppant   | 1678  | 4/16/2018 12:44:29 PM | 0.0 kg/m^3    |
#      | Montney | Hori_02 | 17       | proppant   | 1751  | 4/16/2018 12:45:42 PM | 34.0 kg/m^3   |
#      | Montney | Hori_02 | 17       | proppant   | 3023  | 4/16/2018 1:07:42 PM  | 195.0 kg/m^3  |
#      | Montney | Hori_02 | 17       | proppant   | 4207  | 4/16/2018 1:28:03 PM  | 400.0 kg/m^3  |
#      | Montney | Hori_02 | 17       | proppant   | 2461  | 4/16/2018 12:57:57 PM | 101.0 kg/m^3  |
#      | Montney | Hori_02 | 17       | proppant   | 3243  | 4/16/2018 1:11:27 PM  | 223.0 kg/m^3  |
#      | Montney | Hori_02 | 17       | slurry     | 2239  | 4/16/2018 12:54:07 PM | 8.34 m^3/min  |
#      | Montney | Hori_02 | 17       | slurry     | 1597  | 4/16/2018 12:43:07 PM | 8.95 m^3/min  |
#      | Montney | Hori_02 | 17       | slurry     | 3366  | 4/16/2018 1:13:37 PM  | 9.27 m^3/min  |
#      | Montney | Hori_02 | 17       | slurry     | 5082  | 4/16/2018 1:43:11 PM  | 9.23 m^3/min  |
#      | Montney | Hori_02 | 17       | slurry     | 3537  | 4/16/2018 1:16:36 PM  | 9.28 m^3/min  |
#      | Montney | Hori_02 | 17       | slurry     | 4474  | 4/16/2018 1:32:41 PM  | 9.03 m^3/min  |
#      | Montney | Hori_02 | 17       | slurry     | 3616  | 4/16/2018 1:17:55 PM  | 9.29 m^3/min  |
#      | Montney | Hori_02 | 17       | slurry     | 2850  | 4/16/2018 1:04:42 PM  | 8.4 m^3/min   |
      | Montney | Hori_03 | 1        | pressure   | 8568  | 4/6/2018 11:54:24 PM  | 72.32 kPa     |
      | Montney | Hori_03 | 1        | pressure   | 316   | 4/6/2018 9:34:30 PM   | 1.19 kPa      |
      | Montney | Hori_03 | 1        | pressure   | 9966  | 4/7/2018 12:17:42 AM  | 71.1 kPa      |
      | Montney | Hori_03 | 1        | pressure   | 6587  | 4/6/2018 11:21:23 PM  | 70.89 kPa     |
      | Montney | Hori_03 | 1        | pressure   | 6588  | 4/6/2018 11:21:24 PM  | 71.09 kPa     |
      | Montney | Hori_03 | 1        | pressure   | 2800  | 4/6/2018 10:18:13 PM  | 24.03 kPa     |
      | Montney | Hori_03 | 1        | pressure   | 3434  | 4/6/2018 10:28:47 PM  | 19.12 kPa     |
      | Montney | Hori_03 | 1        | pressure   | 3178  | 4/6/2018 10:24:31 PM  | 0.41 kPa      |
#      | Montney | Hori_03 | 1        | proppant   | 10178 | 4/7/2018 12:21:14 AM  | 371.0 kg/m^3  |
#      | Montney | Hori_03 | 1        | proppant   | 2323  | 4/6/2018 10:10:16 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 1        | proppant   | 5517  | 4/6/2018 11:03:33 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 1        | proppant   | 5446  | 4/6/2018 11:02:22 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 1        | proppant   | 10102 | 4/7/2018 12:19:58 AM  | 374.0 kg/m^3  |
#      | Montney | Hori_03 | 1        | proppant   | 6461  | 4/6/2018 11:19:17 PM  | 76.0 kg/m^3   |
#      | Montney | Hori_03 | 1        | proppant   | 4341  | 4/6/2018 10:43:56 PM  | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 1        | proppant   | 9577  | 4/7/2018 12:11:13 AM  | 350.0 kg/m^3  |
#      | Montney | Hori_03 | 1        | slurry     | 5413  | 4/6/2018 11:01:49 PM  | 7.51 m^3/min  |
#      | Montney | Hori_03 | 1        | slurry     | 4910  | 4/6/2018 10:53:26 PM  | 4.03 m^3/min  |
#      | Montney | Hori_03 | 1        | slurry     | 1843  | 4/6/2018 10:02:16 PM  | 0.0 m^3/min   |
#      | Montney | Hori_03 | 1        | slurry     | 10236 | 4/7/2018 12:22:12 AM  | 8.78 m^3/min  |
#      | Montney | Hori_03 | 1        | slurry     | 5346  | 4/6/2018 11:00:42 PM  | 6.31 m^3/min  |
#      | Montney | Hori_03 | 1        | slurry     | 788   | 4/6/2018 9:44:41 PM   | 0.0 m^3/min   |
#      | Montney | Hori_03 | 1        | slurry     | 6713  | 4/6/2018 11:23:29 PM  | 9.56 m^3/min  |
#      | Montney | Hori_03 | 1        | slurry     | 3059  | 4/6/2018 10:22:32 PM  | 0.0 m^3/min   |
      | Montney | Hori_03 | 28       | pressure   | 3094  | 4/20/2018 12:26:59 PM | 51.4 kPa      |
      | Montney | Hori_03 | 28       | pressure   | 3848  | 4/20/2018 12:40:28 PM | 50.6 kPa      |
      | Montney | Hori_03 | 28       | pressure   | 3113  | 4/20/2018 12:27:20 PM | 51.4 kPa      |
      | Montney | Hori_03 | 28       | pressure   | 1378  | 4/20/2018 11:56:16 AM | 55.9 kPa      |
      | Montney | Hori_03 | 28       | pressure   | 638   | 4/20/2018 11:43:02 AM | 31.6 kPa      |
      | Montney | Hori_03 | 28       | pressure   | 3530  | 4/20/2018 12:34:47 PM | 50.7 kPa      |
      | Montney | Hori_03 | 28       | pressure   | 3917  | 4/20/2018 12:41:42 PM | 51.1 kPa      |
      | Montney | Hori_03 | 28       | pressure   | 1574  | 4/20/2018 11:59:48 AM | 53.8 kPa      |
#      | Montney | Hori_03 | 28       | proppant   | 3183  | 4/20/2018 12:28:34 PM | 425.0 kg/m^3  |
#      | Montney | Hori_03 | 28       | proppant   | 1753  | 4/20/2018 12:02:58 PM | 200.0 kg/m^3  |
#      | Montney | Hori_03 | 28       | proppant   | 1607  | 4/20/2018 12:00:23 PM | 175.0 kg/m^3  |
#      | Montney | Hori_03 | 28       | proppant   | 506   | 4/20/2018 11:40:39 AM | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 28       | proppant   | 2503  | 4/20/2018 12:16:24 PM | 325.0 kg/m^3  |
#      | Montney | Hori_03 | 28       | proppant   | 2558  | 4/20/2018 12:17:23 PM | 325.0 kg/m^3  |
#      | Montney | Hori_03 | 28       | proppant   | 1302  | 4/20/2018 11:54:55 AM | 74.0 kg/m^3   |
#      | Montney | Hori_03 | 28       | proppant   | 215   | 4/20/2018 11:35:27 AM | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 28       | slurry     | 1791  | 4/20/2018 12:03:39 PM | 10.0 m^3/min  |
#      | Montney | Hori_03 | 28       | slurry     | 3696  | 4/20/2018 12:37:45 PM | 10.04 m^3/min |
#      | Montney | Hori_03 | 28       | slurry     | 1744  | 4/20/2018 12:02:48 PM | 9.99 m^3/min  |
#      | Montney | Hori_03 | 28       | slurry     | 889   | 4/20/2018 11:47:31 AM | 4.58 m^3/min  |
#      | Montney | Hori_03 | 28       | slurry     | 2661  | 4/20/2018 12:19:14 PM | 10.03 m^3/min |
#      | Montney | Hori_03 | 28       | slurry     | 1239  | 4/20/2018 11:53:47 AM | 10.09 m^3/min |
#      | Montney | Hori_03 | 28       | slurry     | 2669  | 4/20/2018 12:19:23 PM | 10.03 m^3/min |
#      | Montney | Hori_03 | 28       | slurry     | 4166  | 4/20/2018 12:46:09 PM | 10.05 m^3/min |
      | Montney | Hori_03 | 8        | pressure   | 198   | 4/13/2018 10:48:21 PM | 22.8 kPa      |
      | Montney | Hori_03 | 8        | pressure   | 135   | 4/13/2018 10:47:18 PM | 31.4 kPa      |
      | Montney | Hori_03 | 8        | pressure   | 3846  | 4/13/2018 11:49:15 PM | 69.3 kPa      |
      | Montney | Hori_03 | 8        | pressure   | 5396  | 4/14/2018 12:15:08 AM | 72.5 kPa      |
      | Montney | Hori_03 | 8        | pressure   | 803   | 4/13/2018 10:58:27 PM | 31.2 kPa      |
      | Montney | Hori_03 | 8        | pressure   | 3475  | 4/13/2018 11:43:03 PM | 69.2 kPa      |
      | Montney | Hori_03 | 8        | pressure   | 1772  | 4/13/2018 11:14:37 PM | 69.5 kPa      |
      | Montney | Hori_03 | 8        | pressure   | 3203  | 4/13/2018 11:38:30 PM | 69.1 kPa      |
#      | Montney | Hori_03 | 8        | proppant   | 1477  | 4/13/2018 11:09:41 PM | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 8        | proppant   | 4726  | 4/14/2018 12:03:58 AM | 425.0 kg/m^3  |
#      | Montney | Hori_03 | 8        | proppant   | 1689  | 4/13/2018 11:13:13 PM | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 8        | proppant   | 1666  | 4/13/2018 11:12:50 PM | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 8        | proppant   | 373   | 4/13/2018 10:51:16 PM | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 8        | proppant   | 4377  | 4/13/2018 11:58:08 PM | 375.0 kg/m^3  |
#      | Montney | Hori_03 | 8        | proppant   | 5026  | 4/14/2018 12:08:58 AM | 475.0 kg/m^3  |
#      | Montney | Hori_03 | 8        | proppant   | 5518  | 4/14/2018 12:17:11 AM | 504.0 kg/m^3  |
#      | Montney | Hori_03 | 8        | slurry     | 5788  | 4/14/2018 12:21:42 AM | 0.0 m^3/min   |
#      | Montney | Hori_03 | 8        | slurry     | 2853  | 4/13/2018 11:32:39 PM | 9.99 m^3/min  |
#      | Montney | Hori_03 | 8        | slurry     | 880   | 4/13/2018 10:59:44 PM | 0.16 m^3/min  |
#      | Montney | Hori_03 | 8        | slurry     | 2083  | 4/13/2018 11:19:48 PM | 9.3 m^3/min   |
#      | Montney | Hori_03 | 8        | slurry     | 1249  | 4/13/2018 11:05:53 PM | 2.09 m^3/min  |
#      | Montney | Hori_03 | 8        | slurry     | 5905  | 4/14/2018 12:23:39 AM | 0.0 m^3/min   |
#      | Montney | Hori_03 | 8        | slurry     | 3590  | 4/13/2018 11:44:58 PM | 10.0 m^3/min  |
#      | Montney | Hori_03 | 8        | slurry     | 5857  | 4/14/2018 12:22:51 AM | 0.0 m^3/min   |
      | Montney | Hori_03 | 23       | pressure   | 69    | 4/18/2018 9:22:00 AM  | 62.4 kPa      |
      | Montney | Hori_03 | 23       | pressure   | 56    | 4/18/2018 9:09:00 AM  | 64.3 kPa      |
      | Montney | Hori_03 | 23       | pressure   | 65    | 4/18/2018 9:18:00 AM  | 60.8 kPa      |
      | Montney | Hori_03 | 23       | pressure   | 40    | 4/18/2018 8:53:00 AM  | 60.3 kPa      |
      | Montney | Hori_03 | 23       | pressure   | 70    | 4/18/2018 9:23:00 AM  | 63.5 kPa      |
      | Montney | Hori_03 | 23       | pressure   | 78    | 4/18/2018 9:31:00 AM  | 63.7 kPa      |
      | Montney | Hori_03 | 23       | pressure   | 42    | 4/18/2018 8:55:00 AM  | 60.0 kPa      |
      | Montney | Hori_03 | 23       | pressure   | 2     | 4/18/2018 8:15:00 AM  | 29.3 kPa      |
#      | Montney | Hori_03 | 23       | proppant   | 17    | 4/18/2018 8:30:00 AM  | 0.0 kg/m^3    |
#      | Montney | Hori_03 | 23       | proppant   | 31    | 4/18/2018 8:44:00 AM  | 129.0 kg/m^3  |
#      | Montney | Hori_03 | 23       | proppant   | 24    | 4/18/2018 8:37:00 AM  | 23.0 kg/m^3   |
#      | Montney | Hori_03 | 23       | proppant   | 77    | 4/18/2018 9:30:00 AM  | 400.0 kg/m^3  |
#      | Montney | Hori_03 | 23       | proppant   | 49    | 4/18/2018 9:02:00 AM  | 448.0 kg/m^3  |
#      | Montney | Hori_03 | 23       | proppant   | 69    | 4/18/2018 9:22:00 AM  | 47.0 kg/m^3   |
#      | Montney | Hori_03 | 23       | proppant   | 67    | 4/18/2018 9:20:00 AM  | 499.0 kg/m^3  |
#      | Montney | Hori_03 | 23       | proppant   | 75    | 4/18/2018 9:28:00 AM  | 320.0 kg/m^3  |
#      | Montney | Hori_03 | 23       | slurry     | 31    | 4/18/2018 8:44:00 AM  | 10.04 m^3/min |
#      | Montney | Hori_03 | 23       | slurry     | 25    | 4/18/2018 8:38:00 AM  | 10.01 m^3/min |
#      | Montney | Hori_03 | 23       | slurry     | 46    | 4/18/2018 8:59:00 AM  | 10.09 m^3/min |
#      | Montney | Hori_03 | 23       | slurry     | 32    | 4/18/2018 8:45:00 AM  | 10.05 m^3/min |
#      | Montney | Hori_03 | 23       | slurry     | 14    | 4/18/2018 8:27:00 AM  | 1.77 m^3/min  |
#      | Montney | Hori_03 | 23       | slurry     | 59    | 4/18/2018 9:12:00 AM  | 10.03 m^3/min |
#      | Montney | Hori_03 | 23       | slurry     | 8     | 4/18/2018 8:21:00 AM  | 1.76 m^3/min  |
#      | Montney | Hori_03 | 23       | slurry     | 64    | 4/18/2018 9:17:00 AM  | 10.09 m^3/min |
