#  Copyright 2017-2021 Reveal Energy Services, Inc
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
      | field  | well    | stage_no | curve_type | index | timestamp                    | value            |
      | Bakken | Demo_1H | 1        | pressure   | 3960  | 2018-06-06T14:35:00.0000000Z | -9.99 psi        |
#      | Bakken | Demo_1H | 1        | pressure   | 4637  | 2018-06-06T14:46:17.0000000Z | -3.76 psi        |
#      | Bakken | Demo_1H | 1        | pressure   | 6992  | 2018-06-06T15:25:32.0000000Z | 6848.79 psi      |
#      | Bakken | Demo_1H | 1        | pressure   | 4747  | 2018-06-06T14:48:07.0000000Z | -0.79 psi        |
#      | Bakken | Demo_1H | 1        | pressure   | 9557  | 2018-06-06T16:08:17.0000000Z | 6254.41 psi      |
#      | Bakken | Demo_1H | 1        | pressure   | 7680  | 2018-06-06T15:37:00.0000000Z | 7214.85 psi      |
#      | Bakken | Demo_1H | 1        | pressure   | 7836  | 2018-06-06T15:39:36.0000000Z | 6855.80 psi      |
#      | Bakken | Demo_1H | 1        | pressure   | 3979  | 2018-06-06T14:35:19.0000000Z | -7.50 psi        |
#      | Bakken | Demo_1H | 1        | proppant   | 10607 | 2018-06-06T16:25:47.0000000Z | 2.15 lb/gal      |
#      | Bakken | Demo_1H | 1        | proppant   | 910   | 2018-06-06T13:44:10.0000000Z | -0.15 lb/gal     |
#      | Bakken | Demo_1H | 1        | proppant   | 1745  | 2018-06-06T13:58:05.0000000Z | 0.51 lb/gal      |
#      | Bakken | Demo_1H | 1        | proppant   | 5037  | 2018-06-06T14:52:57.0000000Z | -0.45 lb/gal     |
#      | Bakken | Demo_1H | 1        | proppant   | 22    | 2018-06-06T13:29:22.0000000Z | -0.26 lb/gal     |
#      | Bakken | Demo_1H | 1        | proppant   | 832   | 2018-06-06T13:42:52.0000000Z | -0.16 lb/gal     |
#      | Bakken | Demo_1H | 1        | proppant   | 11375 | 2018-06-06T16:38:35.0000000Z | -0.07 lb/gal     |
#      | Bakken | Demo_1H | 1        | proppant   | 3160  | 2018-06-06T14:21:40.0000000Z | -0.08 lb/gal     |
#      | Bakken | Demo_1H | 1        | slurry     | 8557  | 2018-06-06T15:51:37.0000000Z | 35.08 bpm        |
#      | Bakken | Demo_1H | 1        | slurry     | 5415  | 2018-06-06T14:59:15.0000000Z | 0.14 bpm         |
#      | Bakken | Demo_1H | 1        | slurry     | 8125  | 2018-06-06T15:44:25.0000000Z | 35.49 bpm        |
#      | Bakken | Demo_1H | 1        | slurry     | 156   | 2018-06-06T13:31:36.0000000Z | 0.00 bpm         |
#      | Bakken | Demo_1H | 1        | slurry     | 4115  | 2018-06-06T14:37:35.0000000Z | 0.14 bpm         |
#      | Bakken | Demo_1H | 1        | slurry     | 10808 | 2018-06-06T16:29:08.0000000Z | 35.16 bpm        |
#      | Bakken | Demo_1H | 1        | slurry     | 6091  | 2018-06-06T15:10:31.0000000Z | 0.23 bpm         |
#      | Bakken | Demo_1H | 1        | slurry     | 4386  | 2018-06-06T14:42:06.0000000Z | 1.04 bpm         |
#      | Bakken | Demo_1H | 50       | pressure   | 2971  | 2018-06-28T13:29:31.0000000Z | 6880.38 psi      |
#      | Bakken | Demo_1H | 50       | pressure   | 118   | 2018-06-28T12:41:58.0000000Z | 7853.94 psi      |
#      | Bakken | Demo_1H | 50       | pressure   | 3929  | 2018-06-28T13:45:29.0000000Z | 7008.58 psi      |
#      | Bakken | Demo_1H | 50       | pressure   | 2817  | 2018-06-28T13:26:57.0000000Z | 6882.67 psi      |
#      | Bakken | Demo_1H | 50       | pressure   | 2497  | 2018-06-28T13:21:37.0000000Z | 7109.52 psi      |
#      | Bakken | Demo_1H | 50       | pressure   | 1897  | 2018-06-28T13:11:37.0000000Z | 6828.63 psi      |
#      | Bakken | Demo_1H | 50       | pressure   | 260   | 2018-06-28T12:44:20.0000000Z | 7954.80 psi      |
#      | Bakken | Demo_1H | 50       | pressure   | 1913  | 2018-06-28T13:11:53.0000000Z | 6828.10 psi      |
#      | Bakken | Demo_1H | 50       | proppant   | 604   | 2018-06-28T12:50:04.0000000Z | 0.79 lb/gal      |
#      | Bakken | Demo_1H | 50       | proppant   | 2509  | 2018-06-28T13:21:49.0000000Z | 0.48 lb/gal      |
#      | Bakken | Demo_1H | 50       | proppant   | 3233  | 2018-06-28T13:33:53.0000000Z | 0.86 lb/gal      |
#      | Bakken | Demo_1H | 50       | proppant   | 1133  | 2018-06-28T12:58:53.0000000Z | 0.84 lb/gal      |
#      | Bakken | Demo_1H | 50       | proppant   | 2116  | 2018-06-28T13:15:16.0000000Z | 1.05 lb/gal      |
#      | Bakken | Demo_1H | 50       | proppant   | 1835  | 2018-06-28T13:10:35.0000000Z | 1.06 lb/gal      |
#      | Bakken | Demo_1H | 50       | proppant   | 2481  | 2018-06-28T13:21:21.0000000Z | 0.41 lb/gal      |
#      | Bakken | Demo_1H | 50       | proppant   | 2782  | 2018-06-28T13:26:22.0000000Z | 0.50 lb/gal      |
#      | Bakken | Demo_1H | 50       | slurry     | 3067  | 2018-06-28T13:31:07.0000000Z | 71.73 bpm        |
#      | Bakken | Demo_1H | 50       | slurry     | 3872  | 2018-06-28T13:44:32.0000000Z | 71.73 bpm        |
#      | Bakken | Demo_1H | 50       | slurry     | 1877  | 2018-06-28T13:11:17.0000000Z | 71.86 bpm        |
#      | Bakken | Demo_1H | 50       | slurry     | 1167  | 2018-06-28T12:59:27.0000000Z | 71.98 bpm        |
#      | Bakken | Demo_1H | 50       | slurry     | 24    | 2018-06-28T12:40:24.0000000Z | 32.65 bpm        |
#      | Bakken | Demo_1H | 50       | slurry     | 2941  | 2018-06-28T13:29:01.0000000Z | 71.76 bpm        |
#      | Bakken | Demo_1H | 50       | slurry     | 1328  | 2018-06-28T13:02:08.0000000Z | 71.85 bpm        |
#      | Bakken | Demo_1H | 50       | slurry     | 2169  | 2018-06-28T13:16:09.0000000Z | 71.77 bpm        |
#      | Bakken | Demo_1H | 41       | pressure   | 2427  | 2018-06-26T14:22:29.0000000Z | 7471.63 psi      |
#      | Bakken | Demo_1H | 41       | pressure   | 3272  | 2018-06-26T14:36:34.0000000Z | 7512.44 psi      |
#      | Bakken | Demo_1H | 41       | pressure   | 4045  | 2018-06-26T14:49:27.0000000Z | 7284.56 psi      |
#      | Bakken | Demo_1H | 41       | pressure   | 1752  | 2018-06-26T14:11:14.0000000Z | 7623.87 psi      |
#      | Bakken | Demo_1H | 41       | pressure   | 1969  | 2018-06-26T14:14:51.0000000Z | 7520.98 psi      |
#      | Bakken | Demo_1H | 41       | pressure   | 143   | 2018-06-26T13:44:25.0000000Z | 7007.66 psi      |
#      | Bakken | Demo_1H | 41       | pressure   | 4318  | 2018-06-26T14:54:00.0000000Z | 7141.08 psi      |
#      | Bakken | Demo_1H | 41       | pressure   | 1653  | 2018-06-26T14:09:35.0000000Z | 7672.33 psi      |
#      | Bakken | Demo_1H | 41       | proppant   | 1833  | 2018-06-26T14:12:35.0000000Z | 1.06 lb/gal      |
#      | Bakken | Demo_1H | 41       | proppant   | 2188  | 2018-06-26T14:18:30.0000000Z | 1.40 lb/gal      |
#      | Bakken | Demo_1H | 41       | proppant   | 3406  | 2018-06-26T14:38:48.0000000Z | 0.55 lb/gal      |
#      | Bakken | Demo_1H | 41       | proppant   | 514   | 2018-06-26T13:50:36.0000000Z | -0.11 lb/gal     |
#      | Bakken | Demo_1H | 41       | proppant   | 1498  | 2018-06-26T14:07:00.0000000Z | 1.15 lb/gal      |
#      | Bakken | Demo_1H | 41       | proppant   | 1586  | 2018-06-26T14:08:28.0000000Z | 1.12 lb/gal      |
#      | Bakken | Demo_1H | 41       | proppant   | 4683  | 2018-06-26T15:00:05.0000000Z | -0.04 lb/gal     |
#      | Bakken | Demo_1H | 41       | proppant   | 1427  | 2018-06-26T14:05:49.0000000Z | 0.97 lb/gal      |
#      | Bakken | Demo_1H | 41       | slurry     | 1976  | 2018-06-26T14:14:58.0000000Z | 71.88 bpm        |
#      | Bakken | Demo_1H | 41       | slurry     | 3273  | 2018-06-26T14:36:35.0000000Z | 71.87 bpm        |
#      | Bakken | Demo_1H | 41       | slurry     | 4813  | 2018-06-26T15:02:15.0000000Z | 0.38 bpm         |
#      | Bakken | Demo_1H | 41       | slurry     | 3542  | 2018-06-26T14:41:04.0000000Z | 71.80 bpm        |
#      | Bakken | Demo_1H | 41       | slurry     | 3701  | 2018-06-26T14:43:43.0000000Z | 71.79 bpm        |
#      | Bakken | Demo_1H | 41       | slurry     | 1927  | 2018-06-26T14:14:09.0000000Z | 71.91 bpm        |
#      | Bakken | Demo_1H | 41       | slurry     | 1409  | 2018-06-26T14:05:31.0000000Z | 71.90 bpm        |
#      | Bakken | Demo_1H | 41       | slurry     | 4135  | 2018-06-26T14:50:57.0000000Z | 71.46 bpm        |
#      | Bakken | Demo_1H | 20       | pressure   | 2089  | 2018-06-15T22:01:23.0000000Z | 6354.26 psi      |
#      | Bakken | Demo_1H | 20       | pressure   | 6055  | 2018-06-15T23:07:29.0000000Z | 8237.45 psi      |
#      | Bakken | Demo_1H | 20       | pressure   | 1562  | 2018-06-15T21:52:36.0000000Z | 3427.11 psi      |
#      | Bakken | Demo_1H | 20       | pressure   | 3195  | 2018-06-15T22:19:49.0000000Z | 6034.64 psi      |
#      | Bakken | Demo_1H | 20       | pressure   | 3887  | 2018-06-15T22:31:21.0000000Z | 7358.01 psi      |
#      | Bakken | Demo_1H | 20       | pressure   | 6797  | 2018-06-15T23:19:51.0000000Z | 8055.14 psi      |
#      | Bakken | Demo_1H | 20       | pressure   | 7593  | 2018-06-15T23:33:07.0000000Z | 8123.00 psi      |
#      | Bakken | Demo_1H | 20       | pressure   | 6810  | 2018-06-15T23:20:04.0000000Z | 8053.74 psi      |
#      | Bakken | Demo_1H | 20       | proppant   | 7036  | 2018-06-15T23:23:50.0000000Z | 1.06 lb/gal      |
#      | Bakken | Demo_1H | 20       | proppant   | 1361  | 2018-06-15T21:49:15.0000000Z | 0.08 lb/gal      |
#      | Bakken | Demo_1H | 20       | proppant   | 7562  | 2018-06-15T23:32:36.0000000Z | 0.20 lb/gal      |
#      | Bakken | Demo_1H | 20       | proppant   | 1908  | 2018-06-15T21:58:22.0000000Z | 0.60 lb/gal      |
#      | Bakken | Demo_1H | 20       | proppant   | 7295  | 2018-06-15T23:28:09.0000000Z | 1.46 lb/gal      |
#      | Bakken | Demo_1H | 20       | proppant   | 400   | 2018-06-15T21:33:14.0000000Z | -0.30 lb/gal     |
#      | Bakken | Demo_1H | 20       | proppant   | 2045  | 2018-06-15T22:00:39.0000000Z | -0.02 lb/gal     |
#      | Bakken | Demo_1H | 20       | proppant   | 187   | 2018-06-15T21:29:41.0000000Z | -0.20 lb/gal     |
#      | Bakken | Demo_1H | 20       | slurry     | 2500  | 2018-06-15T22:08:14.0000000Z | 29.32 bpm        |
#      | Bakken | Demo_1H | 20       | slurry     | 4767  | 2018-06-15T22:46:01.0000000Z | 70.08 bpm        |
#      | Bakken | Demo_1H | 20       | slurry     | 4340  | 2018-06-15T22:38:54.0000000Z | 68.13 bpm        |
#      | Bakken | Demo_1H | 20       | slurry     | 6728  | 2018-06-15T23:18:42.0000000Z | 70.15 bpm        |
#      | Bakken | Demo_1H | 20       | slurry     | 4255  | 2018-06-15T22:37:29.0000000Z | 66.65 bpm        |
#      | Bakken | Demo_1H | 20       | slurry     | 2384  | 2018-06-15T22:06:18.0000000Z | 29.40 bpm        |
#      | Bakken | Demo_1H | 20       | slurry     | 8183  | 2018-06-15T23:42:57.0000000Z | 70.13 bpm        |
#      | Bakken | Demo_1H | 20       | slurry     | 5946  | 2018-06-15T23:05:40.0000000Z | 70.05 bpm        |
#      | Bakken | Demo_2H | 1        | pressure   | 6948  | 2018-06-06T06:54:21.0000000Z | 3208.19 psi      |
#      | Bakken | Demo_2H | 1        | pressure   | 7430  | 2018-06-06T07:02:23.0000000Z | 6785.23 psi      |
#      | Bakken | Demo_2H | 1        | pressure   | 2240  | 2018-06-06T05:35:53.0000000Z | 0.00 psi         |
#      | Bakken | Demo_2H | 1        | pressure   | 4517  | 2018-06-06T06:13:50.0000000Z | 592.60 psi       |
#      | Bakken | Demo_2H | 1        | pressure   | 3724  | 2018-06-06T06:00:37.0000000Z | 4059.63 psi      |
#      | Bakken | Demo_2H | 1        | pressure   | 11631 | 2018-06-06T08:12:24.0000000Z | 6345.52 psi      |
#      | Bakken | Demo_2H | 1        | pressure   | 3358  | 2018-06-06T05:54:31.0000000Z | 9.23 psi         |
#      | Bakken | Demo_2H | 1        | pressure   | 6133  | 2018-06-06T06:40:46.0000000Z | 7324.85 psi      |
#      | Bakken | Demo_2H | 1        | proppant   | 9032  | 2018-06-06T07:29:05.0000000Z | -0.04 lb/gal     |
#      | Bakken | Demo_2H | 1        | proppant   | 12912 | 2018-06-06T08:33:45.0000000Z | 2.12 lb/gal      |
#      | Bakken | Demo_2H | 1        | proppant   | 1838  | 2018-06-06T05:29:11.0000000Z | 1.41 lb/gal      |
#      | Bakken | Demo_2H | 1        | proppant   | 4199  | 2018-06-06T06:08:32.0000000Z | 1.41 lb/gal      |
#      | Bakken | Demo_2H | 1        | proppant   | 7351  | 2018-06-06T07:01:04.0000000Z | -0.01 lb/gal     |
#      | Bakken | Demo_2H | 1        | proppant   | 12643 | 2018-06-06T08:29:16.0000000Z | 2.14 lb/gal      |
#      | Bakken | Demo_2H | 1        | proppant   | 2828  | 2018-06-06T05:45:41.0000000Z | 1.36 lb/gal      |
#      | Bakken | Demo_2H | 1        | proppant   | 598   | 2018-06-06T05:08:31.0000000Z | 1.41 lb/gal      |
#      | Bakken | Demo_2H | 1        | slurry     | 11349 | 2018-06-06T08:07:42.0000000Z | 35.69 bpm        |
#      | Bakken | Demo_2H | 1        | slurry     | 7792  | 2018-06-06T07:08:25.0000000Z | 2.78 bpm         |
#      | Bakken | Demo_2H | 1        | slurry     | 14101 | 2018-06-06T08:53:34.0000000Z | 35.56 bpm        |
#      | Bakken | Demo_2H | 1        | slurry     | 14561 | 2018-06-06T09:01:14.0000000Z | 35.45 bpm        |
#      | Bakken | Demo_2H | 1        | slurry     | 12676 | 2018-06-06T08:29:49.0000000Z | 35.45 bpm        |
#      | Bakken | Demo_2H | 1        | slurry     | 1402  | 2018-06-06T05:21:55.0000000Z | 0.01 bpm         |
#      | Bakken | Demo_2H | 1        | slurry     | 7197  | 2018-06-06T06:58:30.0000000Z | 16.64 bpm        |
#      | Bakken | Demo_2H | 1        | slurry     | 2535  | 2018-06-06T05:40:48.0000000Z | 0.0 bpm          |
#      | Bakken | Demo_2H | 50       | pressure   | 5047  | 2018-06-30T00:54:07.0000000Z | 6498 psi         |
#      | Bakken | Demo_2H | 50       | pressure   | 6222  | 2018-06-30T01:13:42.0000000Z | 5440 psi         |
#      | Bakken | Demo_2H | 50       | pressure   | 2486  | 2018-06-30T00:11:26.0000000Z | 6707 psi         |
#      | Bakken | Demo_2H | 50       | pressure   | 141   | 2018-06-29T23:32:21.0000000Z | 7655 psi         |
#      | Bakken | Demo_2H | 50       | pressure   | 5611  | 2018-06-30T01:03:31.0000000Z | 6322 psi         |
#      | Bakken | Demo_2H | 50       | pressure   | 1584  | 2018-06-29T23:56:24.0000000Z | 5334 psi         |
#      | Bakken | Demo_2H | 50       | pressure   | 7102  | 2018-06-30T01:28:22.0000000Z | 4537 psi         |
#      | Bakken | Demo_2H | 50       | pressure   | 5507  | 2018-06-30T01:01:47.0000000Z | 6341 psi         |
#      | Bakken | Demo_2H | 50       | proppant   | 5128  | 2018-06-30T00:55:28.0000000Z | 0.7288 lb/gal    |
#      | Bakken | Demo_2H | 50       | proppant   | 1980  | 2018-06-30T00:03:00.0000000Z | -3.059e-3 lb/gal |
#      | Bakken | Demo_2H | 50       | proppant   | 1538  | 2018-06-29T23:55:38.0000000Z | -6.446e-2 lb/gal |
#      | Bakken | Demo_2H | 50       | proppant   | 292   | 2018-06-29T23:34:52.0000000Z | -9.890e-2 lb/gal |
#      | Bakken | Demo_2H | 50       | proppant   | 2433  | 2018-06-30T00:10:33.0000000Z | 0.4354 lb/gal    |
#      | Bakken | Demo_2H | 50       | proppant   | 6840  | 2018-06-30T01:24:00.0000000Z | -0.1004 lb/gal   |
#      | Bakken | Demo_2H | 50       | proppant   | 1766  | 2018-06-29T23:59:26.0000000Z | -4.708e-2 lb/gal |
#      | Bakken | Demo_2H | 50       | proppant   | 5595  | 2018-06-30T01:03:15.0000000Z | 0.9640 lb/gal    |
#      | Bakken | Demo_2H | 50       | slurry     | 1124  | 2018-06-29T23:48:44.0000000Z | 29.78 bpm        |
#      | Bakken | Demo_2H | 50       | slurry     | 74    | 2018-06-29T23:31:14.0000000Z | 0.1565 bpm       |
#      | Bakken | Demo_2H | 50       | slurry     | 6992  | 2018-06-30T01:26:32.0000000Z | 0.2609 bpm       |
#      | Bakken | Demo_2H | 50       | slurry     | 5641  | 2018-06-30T01:04:01.0000000Z | 71.26 bpm        |
#      | Bakken | Demo_2H | 50       | slurry     | 672   | 2018-06-29T23:41:12.0000000Z | 4.675 bpm        |
#      | Bakken | Demo_2H | 50       | slurry     | 3647  | 2018-06-30T00:30:47.0000000Z | 72.00 bpm        |
#      | Bakken | Demo_2H | 50       | slurry     | 1716  | 2018-06-29T23:58:36.0000000Z | 15.51 bpm        |
#      | Bakken | Demo_2H | 50       | slurry     | 2415  | 2018-06-30T00:10:15.0000000Z | 72.02 bpm        |
#      | Bakken | Demo_2H | 21       | pressure   | 7486  | 2018-06-17T15:12:49.0000000Z | 8003 psi         |
#      | Bakken | Demo_2H | 21       | pressure   | 7488  | 2018-06-17T15:12:51.0000000Z | 8008 psi         |
#      | Bakken | Demo_2H | 21       | pressure   | 3343  | 2018-06-17T14:03:46.0000000Z | 8199 psi         |
#      | Bakken | Demo_2H | 21       | pressure   | 4394  | 2018-06-17T14:21:17.0000000Z | 8180 psi         |
#      | Bakken | Demo_2H | 21       | pressure   | 6486  | 2018-06-17T14:56:09.0000000Z | 8157 psi         |
#      | Bakken | Demo_2H | 21       | pressure   | 804   | 2018-06-17T13:21:27.0000000Z | 8367 psi         |
#      | Bakken | Demo_2H | 21       | pressure   | 5497  | 2018-06-17T14:39:40.0000000Z | 8410 psi         |
#      | Bakken | Demo_2H | 21       | pressure   | 3410  | 2018-06-17T14:04:53.0000000Z | 8177 psi         |
#      | Bakken | Demo_2H | 21       | proppant   | 2361  | 2018-06-17T13:47:24.0000000Z | 0.4382 lb/gal    |
#      | Bakken | Demo_2H | 21       | proppant   | 6234  | 2018-06-17T14:51:57.0000000Z | 0.3165 lb/gal    |
#      | Bakken | Demo_2H | 21       | proppant   | 3781  | 2018-06-17T14:11:04.0000000Z | 3.467e-2 lb/gal  |
#      | Bakken | Demo_2H | 21       | proppant   | 2521  | 2018-06-17T13:50:04.0000000Z | 0.4257 lb/gal    |
#      | Bakken | Demo_2H | 21       | proppant   | 999   | 2018-06-17T13:24:42.0000000Z | -2.390e-2 lb/gal |
#      | Bakken | Demo_2H | 21       | proppant   | 3898  | 2018-06-17T14:13:01.0000000Z | -3.143e-2 lb/gal |
#      | Bakken | Demo_2H | 21       | proppant   | 4382  | 2018-06-17T14:21:05.0000000Z | 0.6323 lb/gal    |
#      | Bakken | Demo_2H | 21       | proppant   | 7186  | 2018-06-17T15:07:49.0000000Z | 1.222 lb/gal     |
#      | Bakken | Demo_2H | 21       | slurry     | 6831  | 2018-06-17T15:01:54.0000000Z | 69.49 bpm        |
#      | Bakken | Demo_2H | 21       | slurry     | 1143  | 2018-06-17T13:27:06.0000000Z | 28.21 bpm        |
#      | Bakken | Demo_2H | 21       | slurry     | 736   | 2018-06-17T13:20:19.0000000Z | 29.98 bpm        |
#      | Bakken | Demo_2H | 21       | slurry     | 5273  | 2018-06-17T14:35:56.0000000Z | 69.44 bpm        |
#      | Bakken | Demo_2H | 21       | slurry     | 1464  | 2018-06-17T13:32:27.0000000Z | 11.26 bpm        |
#      | Bakken | Demo_2H | 21       | slurry     | 3910  | 2018-06-17T14:13:13.0000000Z | 68.26 bpm        |
#      | Bakken | Demo_2H | 44       | pressure   | 1785  | 2018-06-29T00:32:06.0000000Z | 5741 psi         |
#      | Bakken | Demo_2H | 44       | pressure   | 4598  | 2018-06-29T01:18:59.0000000Z | 6787 psi         |
#      | Bakken | Demo_2H | 44       | pressure   | 2757  | 2018-06-29T00:48:18.0000000Z | 6878 psi         |
#      | Bakken | Demo_2H | 44       | pressure   | 1637  | 2018-06-29T00:29:38.0000000Z | 5977 psi         |
#      | Bakken | Demo_2H | 44       | pressure   | 1030  | 2018-06-29T00:19:31.0000000Z | 6601 psi         |
#      | Bakken | Demo_2H | 44       | pressure   | 876   | 2018-06-29T00:16:57.0000000Z | 6742 psi         |
#      | Bakken | Demo_2H | 44       | pressure   | 6129  | 2018-06-29T01:44:30.0000000Z | 5379 psi         |
#      | Bakken | Demo_2H | 44       | proppant   | 4726  | 2018-06-29T01:21:07.0000000Z | 0.3101 lb/gal    |
#      | Bakken | Demo_2H | 44       | proppant   | 4039  | 2018-06-29T01:09:40.0000000Z | -3.825e-2 lb/gal |
#      | Bakken | Demo_2H | 44       | proppant   | 6155  | 2018-06-29T01:44:56.0000000Z | -6.655e-2 lb/gal |
#      | Bakken | Demo_2H | 44       | proppant   | 386   | 2018-06-29T00:08:47.0000000Z | -0.1605 lb/gal   |
#      | Bakken | Demo_2H | 44       | proppant   | 2034  | 2018-06-29T00:36:15.0000000Z | 0.1910 lb/gal    |
#      | Bakken | Demo_2H | 44       | proppant   | 5716  | 2018-06-29T01:37:37.0000000Z | 0.0284 lb/gal    |
#      | Bakken | Demo_2H | 44       | proppant   | 4265  | 2018-06-29T01:13:26.0000000Z | 0.2296lb/gal     |
#      | Bakken | Demo_2H | 44       | proppant   | 1162  | 2018-06-29T00:21:43.0000000Z | -5.815e-2 lb/gal |
#      | Bakken | Demo_2H | 44       | slurry     | 3023  | 2018-06-29T00:52:44.0000000Z | 71.66 bpm        |
#      | Bakken | Demo_2H | 44       | slurry     | 2102  | 2018-06-29T00:37:23.0000000Z | 71.41 bpm        |
#      | Bakken | Demo_2H | 44       | slurry     | 5629  | 2018-06-29T01:36:10.0000000Z | 71.66 bpm        |
#      | Bakken | Demo_2H | 44       | slurry     | 4423  | 2018-06-29T01:16:04.0000000Z | 71.49 bpm        |
#      | Bakken | Demo_2H | 44       | slurry     | 255   | 2018-06-29T00:06:36.0000000Z | 0.2400 bpm       |
#      | Bakken | Demo_2H | 44       | slurry     | 242   | 2018-06-29T00:06:23.0000000Z | 0.1983 bpm       |
#      | Bakken | Demo_2H | 44       | slurry     | 1947  | 2018-06-29T00:34:48.0000000Z | 66.37 bpm        |
#      | Bakken | Demo_2H | 44       | slurry     | 5358  | 2018-06-29T01:31:39.0000000Z | 71.64 bpm        |
#      | Bakken | Demo_4H | 1        | pressure   | 4219  | 2018-06-06T10:50:19.0000000Z | 6161 psi         |
#      | Bakken | Demo_4H | 1        | pressure   | 489   | 2018-06-06T09:48:09.0000000Z | 6998 psi         |
#      | Bakken | Demo_4H | 1        | pressure   | 5266  | 2018-06-06T11:07:46.0000000Z | 6411 psi         |
#      | Bakken | Demo_4H | 1        | pressure   | 743   | 2018-06-06T09:52:23.0000000Z | 4582 psi         |
#      | Bakken | Demo_4H | 1        | pressure   | 3961  | 2018-06-06T10:46:01.0000000Z | 6176 psi         |
#      | Bakken | Demo_4H | 1        | pressure   | 5317  | 2018-06-06T11:08:37.0000000Z | 6399 psi         |
#      | Bakken | Demo_4H | 1        | pressure   | 5490  | 2018-06-06T11:11:30.0000000Z | 6350 psi         |
#      | Bakken | Demo_4H | 1        | pressure   | 6704  | 2018-06-06T11:31:44.0000000Z | 6207 psi         |
#      | Bakken | Demo_4H | 1        | proppant   | 5873  | 2018-06-06T11:17:53.0000000Z | 2.245 lb/gal     |
#      | Bakken | Demo_4H | 1        | proppant   | 6490  | 2018-06-06T11:28:10.0000000Z | 2.289 lb/gal     |
#      | Bakken | Demo_4H | 1        | proppant   | 2994  | 2018-06-06T10:29:54.0000000Z | 4.342e-2 lb/gal  |
#      | Bakken | Demo_4H | 1        | proppant   | 2449  | 2018-06-06T10:20:49.0000000Z | -8.491e-2 lb/gal |
#      | Bakken | Demo_4H | 1        | proppant   | 6059  | 2018-06-06T11:20:59.0000000Z | 2.220 lb/gal     |
#      | Bakken | Demo_4H | 1        | proppant   | 4607  | 2018-06-06T10:56:47.0000000Z | 1.311 lb/gal     |
#      | Bakken | Demo_4H | 1        | proppant   | 3458  | 2018-06-06T10:37:38.0000000Z | 0.595 lb/gal     |
#      | Bakken | Demo_4H | 1        | proppant   | 7425  | 2018-06-06T11:43:45.0000000Z | -3.851e-2 lb/gal |
#      | Bakken | Demo_4H | 1        | slurry     | 5568  | 2018-06-06T11:12:48.0000000Z | 35.32 bpm        |
#      | Bakken | Demo_4H | 1        | slurry     | 2419  | 2018-06-06T10:20:19.0000000Z | 23.57 bpm        |
#      | Bakken | Demo_4H | 1        | slurry     | 3821  | 2018-06-06T10:43:41.0000000Z | 35.40 bpm        |
#      | Bakken | Demo_4H | 1        | slurry     | 1454  | 2018-06-06T10:04:14.0000000Z | 24.03 bpm        |
#      | Bakken | Demo_4H | 1        | slurry     | 7746  | 2018-06-06T11:49:06.0000000Z | 35.00 bpm        |
#      | Bakken | Demo_4H | 1        | slurry     | 2666  | 2018-06-06T10:24:26.0000000Z | 31.60 bpm        |
#      | Bakken | Demo_4H | 1        | slurry     | 6664  | 2018-06-06T11:31:04.0000000Z | 34.77 bpm        |
#      | Bakken | Demo_4H | 1        | slurry     | 1798  | 2018-06-06T10:09:58.0000000Z | 24.09 bpm        |
#      | Bakken | Demo_4H | 35       | pressure   | 2686  | 2018-06-28T19:11:26.0000000Z | 6417 psi         |
#      | Bakken | Demo_4H | 35       | pressure   | 5521  | 2018-06-28T19:58:41.0000000Z | 6456 psi         |
#      | Bakken | Demo_4H | 35       | pressure   | 6193  | 2018-06-28T20:09:53.0000000Z | 6288 psi         |
#      | Bakken | Demo_4H | 35       | pressure   | 4780  | 2018-06-28T19:46:20.0000000Z | 6468 psi         |
#      | Bakken | Demo_4H | 35       | pressure   | 7432  | 2018-06-28T20:30:32.0000000Z | 5022 psi         |
#      | Bakken | Demo_4H | 35       | pressure   | 7028  | 2018-06-28T20:23:48.0000000Z | 6388 psi         |
#      | Bakken | Demo_4H | 35       | pressure   | 4967  | 2018-06-28T19:49:27.0000000Z | 6641 psi         |
#      | Bakken | Demo_4H | 35       | pressure   | 7784  | 2018-06-28T20:36:24.0000000Z | -7.500 psi       |
#      | Bakken | Demo_4H | 35       | proppant   | 5280  | 2018-06-28T19:54:40.0000000Z | 0.2331 lb/gal    |
#      | Bakken | Demo_4H | 35       | proppant   | 5404  | 2018-06-28T19:56:44.0000000Z | 0.2512 lb/gal    |
#      | Bakken | Demo_4H | 35       | proppant   | 7722  | 2018-06-28T20:35:22.0000000Z | -0.2054 lb/gal   |
#      | Bakken | Demo_4H | 35       | proppant   | 2996  | 2018-06-28T19:16:36.0000000Z | -5.288e-2 lb/gal |
#      | Bakken | Demo_4H | 35       | proppant   | 3586  | 2018-06-28T19:26:26.0000000Z | 0.4304 lb/gal    |
#      | Bakken | Demo_4H | 35       | proppant   | 5831  | 2018-06-28T20:03:51.0000000Z | 0.3854 lb/gal    |
#      | Bakken | Demo_4H | 35       | proppant   | 1722  | 2018-06-28T18:55:22.0000000Z | 0.3903 lb/gal    |
#      | Bakken | Demo_4H | 35       | proppant   | 4705  | 2018-06-28T19:45:05.0000000Z | -2.078e-2 lb/gal |
#      | Bakken | Demo_4H | 35       | slurry     | 1503  | 2018-06-28T18:51:43.0000000Z | 71.97 bpm        |
#      | Bakken | Demo_4H | 35       | slurry     | 4876  | 2018-06-28T19:47:56.0000000Z | 71.75 bpm        |
#      | Bakken | Demo_4H | 35       | slurry     | 7327  | 2018-06-28T20:28:47.0000000Z | 71.64 bpm        |
#      | Bakken | Demo_4H | 35       | slurry     | 2285  | 2018-06-28T19:04:45.0000000Z | 71.89 bpm        |
#      | Bakken | Demo_4H | 35       | slurry     | 4176  | 2018-06-28T19:36:16.0000000Z | 71.88 bpm        |
#      | Bakken | Demo_4H | 35       | slurry     | 3284  | 2018-06-28T19:21:24.0000000Z | 71.79 bpm        |
#      | Bakken | Demo_4H | 35       | slurry     | 682   | 2018-06-28T18:38:02.0000000Z | 52.93 bpm        |
#      | Bakken | Demo_4H | 35       | slurry     | 1116  | 2018-06-28T18:45:16.0000000Z | 71.90 bpm        |
#      | Bakken | Demo_4H | 10       | pressure   | 9322  | 2018-06-14T05:42:45.0000000Z | 8119 psi         |
#      | Bakken | Demo_4H | 10       | pressure   | 10516 | 2018-06-14T06:02:39.0000000Z | 8069 psi         |
#      | Bakken | Demo_4H | 10       | pressure   | 12234 | 2018-06-14T06:31:17.0000000Z | 4742 psi         |
#      | Bakken | Demo_4H | 10       | pressure   | 8051  | 2018-06-14T05:21:34.0000000Z | 8479 psi         |
#      | Bakken | Demo_4H | 10       | pressure   | 4464  | 2018-06-14T04:21:47.0000000Z | 8302 psi         |
#      | Bakken | Demo_4H | 10       | pressure   | 5918  | 2018-06-14T04:46:01.0000000Z | 8504 psi         |
#      | Bakken | Demo_4H | 10       | pressure   | 561   | 2018-06-14T03:16:44.0000000Z | 9329 psi         |
#      | Bakken | Demo_4H | 10       | pressure   | 6671  | 2018-06-14T04:58:34.0000000Z | 8248 psi         |
#      | Bakken | Demo_4H | 10       | proppant   | 8503  | 2018-06-14T05:29:06.0000000Z | 0.4468 lb/gal    |
#      | Bakken | Demo_4H | 10       | proppant   | 3646  | 2018-06-14T04:08:09.0000000Z | 0.4516 lb/gal    |
#      | Bakken | Demo_4H | 10       | proppant   | 11436 | 2018-06-14T06:17:59.0000000Z | 5.351e-2 lb/gal  |
#      | Bakken | Demo_4H | 10       | proppant   | 8685  | 2018-06-14T05:32:08.0000000Z | 0.4909 lb/gal    |
#      | Bakken | Demo_4H | 10       | proppant   | 3521  | 2018-06-14T04:06:04.0000000Z | 0.5903 lb/gal    |
#      | Bakken | Demo_4H | 10       | proppant   | 5069  | 2018-06-14T04:31:52.0000000Z | 0.9827 lb/gal    |
#      | Bakken | Demo_4H | 10       | proppant   | 12148 | 2018-06-14T06:29:51.0000000Z | -0.1134 lb/gal   |
#      | Bakken | Demo_4H | 10       | proppant   | 5902  | 2018-06-14T04:45:45.0000000Z | 0.4883 lb/gal    |
#      | Bakken | Demo_4H | 10       | slurry     | 8227  | 2018-06-14T05:24:30.0000000Z | 71.91 bpm        |
#      | Bakken | Demo_4H | 10       | slurry     | 5533  | 2018-06-14T04:39:36.0000000Z | 71.80 bpm        |
#      | Bakken | Demo_4H | 10       | slurry     | 46    | 2018-06-14T03:08:09.0000000Z | 0.0 bpm          |
#      | Bakken | Demo_4H | 10       | slurry     | 8626  | 2018-06-14T05:31:09.0000000Z | 71.88 bpm        |
#      | Bakken | Demo_4H | 10       | slurry     | 3191  | 2018-06-14T04:00:34.0000000Z | 69.93 bpm        |
#      | Bakken | Demo_4H | 10       | slurry     | 11885 | 2018-06-14T06:25:28.0000000Z | 0.000 bpm        |
#      | Bakken | Demo_4H | 10       | slurry     | 5106  | 2018-06-14T04:32:29.0000000Z | 71.94 bpm        |
#      | Bakken | Demo_4H | 10       | slurry     | 5191  | 2018-06-14T04:33:54.0000000Z | 71.87 bpm        |
#      | Bakken | Demo_4H | 26       | pressure   | 7740  | 2018-06-25T10:44:15.0000000Z | 6880 psi         |
#      | Bakken | Demo_4H | 26       | pressure   | 4525  | 2018-06-25T09:50:40.0000000Z | 7138 psi         |
#      | Bakken | Demo_4H | 26       | pressure   | 3497  | 2018-06-25T09:33:32.0000000Z | 7306 psi         |
#      | Bakken | Demo_4H | 26       | pressure   | 1620  | 2018-06-25T09:02:15.0000000Z | 5771 psi         |
#      | Bakken | Demo_4H | 26       | pressure   | 8410  | 2018-06-25T10:55:25.0000000Z | 6635 psi         |
#      | Bakken | Demo_4H | 26       | pressure   | 39    | 2018-06-25T08:35:54.0000000Z | 4849 psi         |
#      | Bakken | Demo_4H | 26       | pressure   | 7250  | 2018-06-25T10:36:05.0000000Z | 6995 psi         |
#      | Bakken | Demo_4H | 26       | pressure   | 8631  | 2018-06-25T10:59:06.0000000Z | 7185 psi         |
#      | Bakken | Demo_4H | 26       | proppant   | 1983  | 2018-06-25T09:08:18.0000000Z | -8.272e-3 lb/gal |
#      | Bakken | Demo_4H | 26       | proppant   | 4960  | 2018-06-25T09:57:55.0000000Z | 0.8330 lb/gal    |
#      | Bakken | Demo_4H | 26       | proppant   | 6044  | 2018-06-25T10:15:59.0000000Z | 1.783 lb/gal     |
#      | Bakken | Demo_4H | 26       | proppant   | 3278  | 2018-06-25T09:29:53.0000000Z | 0.7526 lb/gal    |
#      | Bakken | Demo_4H | 26       | proppant   | 4418  | 2018-06-25T09:48:53.0000000Z | 1.1966 lb/gal    |
#      | Bakken | Demo_4H | 26       | proppant   | 4296  | 2018-06-25T09:46:51.0000000Z | 1.1468 lb/gal    |
#      | Bakken | Demo_4H | 26       | proppant   | 3723  | 2018-06-25T09:37:18.0000000Z | 0.9455 lb/gal    |
#      | Bakken | Demo_4H | 26       | proppant   | 8876  | 2018-06-25T11:03:11.0000000Z | 6.637e-2 lb/gal  |
#      | Bakken | Demo_4H | 26       | slurry     | 8610  | 2018-06-25T10:58:45.0000000Z | 71.48 bpm        |
#      | Bakken | Demo_4H | 26       | slurry     | 7551  | 2018-06-25T10:41:06.0000000Z | 71.91 bpm        |
#      | Bakken | Demo_4H | 26       | slurry     | 2603  | 2018-06-25T09:18:38.0000000Z | 64.80 bpm        |
#      | Bakken | Demo_4H | 26       | slurry     | 418   | 2018-06-25T08:42:13.0000000Z | 0.28 bpm         |
#      | Bakken | Demo_4H | 26       | slurry     | 1117  | 2018-06-25T08:53:52.0000000Z | 25.17 bpm        |
#      | Bakken | Demo_4H | 26       | slurry     | 2263  | 2018-06-25T09:12:58.0000000Z | 66.84 bpm        |
#      | Bakken | Demo_4H | 26       | slurry     | 188   | 2018-06-25T08:38:23.0000000Z | 0.27 bpm         |
#      | Bakken | Demo_4H | 26       | slurry     | 2942  | 2018-06-25T09:24:17.0000000Z | 70.52 bpm        |

    # With my current setup, `behave` will not read text, 'm\u00b3', as the character m with the unicode
    # superscript 3 character. to work around this, i "encode" this value as 'm^3'. the step will then convert
    # the text, 'm^3', to its unicode equivalent before testing.
    Examples: Montney
      | field   | well    | stage_no | curve_type | index | timestamp                    | value          |
#      | Montney | Hori_01 | 1        | pressure   | 3604  | 2018-04-06T18:09:43.0000000Z | 63.94 kPa      |
#      | Montney | Hori_01 | 1        | pressure   | 8423  | 2018-04-06T19:30:08.0000000Z | 74.15 kPa      |
#      | Montney | Hori_01 | 1        | pressure   | 14699 | 2018-04-06T21:14:46.0000000Z | 27.84 kPa      |
#      | Montney | Hori_01 | 1        | pressure   | 122   | 2018-04-06T17:11:40.0000000Z | 1.03 kPa       |
#      | Montney | Hori_01 | 1        | pressure   | 5652  | 2018-04-06T18:43:51.0000000Z | 69.32 kPa      |
#      | Montney | Hori_01 | 1        | pressure   | 5080  | 2018-04-06T18:34:19.0000000Z | 70.45 kPa      |
#      | Montney | Hori_01 | 1        | pressure   | 6035  | 2018-04-06T18:50:15.0000000Z | 69.29 kPa      |
#      | Montney | Hori_01 | 1        | pressure   | 7288  | 2018-04-06T19:11:11.0000000Z | 70.62 kPa      |
#      | Montney | Hori_01 | 1        | proppant   | 1853  | 2018-04-06T17:40:32.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 1        | proppant   | 12809 | 2018-04-06T20:43:16.0000000Z | 251.0 kg/m^3   |
#      | Montney | Hori_01 | 1        | proppant   | 7288  | 2018-04-06T19:11:11.0000000Z | 225.0 kg/m^3   |
#      | Montney | Hori_01 | 1        | proppant   | 7393  | 2018-04-06T19:12:56.0000000Z | 251.0 kg/m^3   |
#      | Montney | Hori_01 | 1        | proppant   | 696   | 2018-04-06T17:21:15.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 1        | proppant   | 15141 | 2018-04-07T05:00:23.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 1        | proppant   | 4684  | 2018-04-06T18:27:43.0000000Z | 24.0 kg/m^3    |
#      | Montney | Hori_01 | 1        | proppant   | 5772  | 2018-04-06T18:45:51.0000000Z | 125.0 kg/m^3   |
#      | Montney | Hori_01 | 1        | slurry     | 14446 | 2018-04-06T21:10:33.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_01 | 1        | slurry     | 8354  | 2018-04-06T19:28:59.0000000Z | 9.48 m^3/min   |
#      | Montney | Hori_01 | 1        | slurry     | 3519  | 2018-04-06T18:08:18.0000000Z | 3.11 m^3/min   |
#      | Montney | Hori_01 | 1        | slurry     | 2785  | 2018-04-06T17:56:04.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_01 | 1        | slurry     | 2870  | 2018-04-06T17:57:29.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_01 | 1        | slurry     | 6732  | 2018-04-06T19:01:53.0000000Z | 9.52 m^3/min   |
#      | Montney | Hori_01 | 1        | slurry     | 4878  | 2018-04-06T18:30:57.0000000Z | 9.18 m^3/min   |
#      | Montney | Hori_01 | 1        | slurry     | 11169 | 2018-04-06T20:15:54.0000000Z | 9.92 m^3/min   |
#      | Montney | Hori_01 | 15       | pressure   | 6005  | 2018-04-19T21:55:59.0000000Z | 73.3 kPa       |
#      | Montney | Hori_01 | 15       | pressure   | 4901  | 2018-04-19T21:36:16.0000000Z | 72.9 kPa       |
#      | Montney | Hori_01 | 15       | pressure   | 857   | 2018-04-19T20:24:01.0000000Z | 35.6 kPa       |
#      | Montney | Hori_01 | 15       | pressure   | 775   | 2018-04-19T20:22:34.0000000Z | 35.6 kPa       |
#      | Montney | Hori_01 | 15       | pressure   | 1623  | 2018-04-19T20:37:43.0000000Z | 52.5 kPa       |
#      | Montney | Hori_01 | 15       | pressure   | 2522  | 2018-04-19T20:53:48.0000000Z | 56.4 kPa       |
#      | Montney | Hori_01 | 15       | pressure   | 2756  | 2018-04-19T20:57:59.0000000Z | 55.8 kPa       |
#      | Montney | Hori_01 | 15       | pressure   | 7413  | 2018-04-19T22:21:06.0000000Z | 65.6 kPa       |
#      | Montney | Hori_01 | 15       | proppant   | 1691  | 2018-04-19T20:38:57.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 15       | proppant   | 1756  | 2018-04-19T20:40:07.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 15       | proppant   | 7690  | 2018-04-19T22:26:02.0000000Z | 475.0 kg/m^3   |
#      | Montney | Hori_01 | 15       | proppant   | 7289  | 2018-04-19T22:18:53.0000000Z | 400.0 kg/m^3   |
#      | Montney | Hori_01 | 15       | proppant   | 6305  | 2018-04-19T22:01:19.0000000Z | 225.0 kg/m^3   |
#      | Montney | Hori_01 | 15       | proppant   | 6143  | 2018-04-19T21:58:26.0000000Z | 200.0 kg/m^3   |
#      | Montney | Hori_01 | 15       | proppant   | 5911  | 2018-04-19T21:54:17.0000000Z | 150.0 kg/m^3   |
#      | Montney | Hori_01 | 15       | proppant   | 8475  | 2018-04-19T22:40:02.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 15       | slurry     | 1304  | 2018-04-19T20:32:01.0000000Z | 1.77 m^3/min
#      | Montney | Hori_01 | 15       | slurry     | 1186  | 2018-04-19T20:29:55.0000000Z | 1.77 m^3/min   |
#      | Montney | Hori_01 | 15       | slurry     | 7477  | 2018-04-19T22:22:14.0000000Z | 10.04 m^3/min  |
#      | Montney | Hori_01 | 15       | slurry     | 7703  | 2018-04-19T22:26:16.0000000Z | 10.01 m^3/min  |
#      | Montney | Hori_01 | 15       | slurry     | 2830  | 2018-04-19T20:59:19.0000000Z | 10.03 m^3/min  |
#      | Montney | Hori_01 | 15       | slurry     | 4001  | 2018-04-19T21:20:11.0000000Z | 9.81 m^3/min   |
#      | Montney | Hori_01 | 15       | slurry     | 5467  | 2018-04-19T21:46:22.0000000Z | 8.02 m^3/min   |
#      | Montney | Hori_01 | 15       | slurry     | 1521  | 2018-04-19T20:35:53.0000000Z | 1.71 m^3/min   |
#      | Montney | Hori_01 | 12       | pressure   | 9057  | 2018-04-12T17:05:52.0000000Z | 28.8 kPa       |
#      | Montney | Hori_01 | 12       | pressure   | 3471  | 2018-04-12T15:32:30.0000000Z | 52.1 kPa       |
#      | Montney | Hori_01 | 12       | pressure   | 8464  | 2018-04-12T16:55:57.0000000Z | 64.8 kPa       |
#      | Montney | Hori_01 | 12       | pressure   | 3004  | 2018-04-12T15:24:43.0000000Z | 51.6 kPa       |
#      | Montney | Hori_01 | 12       | pressure   | 8207  | 2018-04-12T16:51:40.0000000Z | 66.3 kPa       |
#      | Montney | Hori_01 | 12       | pressure   | 6015  | 2018-04-12T16:15:01.0000000Z | 68.7 kPa       |
#      | Montney | Hori_01 | 12       | pressure   | 972   | 2018-04-12T14:50:46.0000000Z | 55.4 kPa       |
#      | Montney | Hori_01 | 12       | pressure   | 4564  | 2018-04-12T15:50:46.0000000Z | 49.9 kPa       |
#      | Montney | Hori_01 | 12       | proppant   | 4194  | 2018-04-12T15:44:35.0000000Z | 450.0 kg/m^3   |
#      | Montney | Hori_01 | 12       | proppant   | 2001  | 2018-04-12T15:07:57.0000000Z | 125.0 kg/m^3   |
#      | Montney | Hori_01 | 12       | proppant   | 1587  | 2018-04-12T15:01:02.0000000Z | 51.0 kg/m^3    |
#      | Montney | Hori_01 | 12       | proppant   | 268   | 2018-04-12T14:39:01.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 12       | proppant   | 963   | 2018-04-12T14:50:37.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 12       | proppant   | 1010  | 2018-04-12T14:51:24.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 12       | proppant   | 8921  | 2018-04-12T17:03:36.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 12       | proppant   | 2587  | 2018-04-12T15:17:46.0000000Z | 223.0 kg/m^3   |
#      | Montney | Hori_01 | 12       | slurry     | 5949  | 2018-04-12T16:13:55.0000000Z | 7.6 m^3/min    |
#      | Montney | Hori_01 | 12       | slurry     | 8757  | 2018-04-12T17:00:52.0000000Z | 9.93 m^3/min   |
#      | Montney | Hori_01 | 12       | slurry     | 5706  | 2018-04-12T16:09:52.0000000Z | 7.38 m^3/min   |
#      | Montney | Hori_01 | 12       | slurry     | 1674  | 2018-04-12T15:02:29.0000000Z | 10.05 m^3/min  |
#      | Montney | Hori_01 | 12       | slurry     | 2238  | 2018-04-12T15:11:55.0000000Z | 10.15 m^3/min  |
#      | Montney | Hori_01 | 12       | slurry     | 2715  | 2018-04-12T15:19:54.0000000Z | 10.02 m^3/min  |
#      | Montney | Hori_01 | 12       | slurry     | 3548  | 2018-04-12T15:33:48.0000000Z | 9.99 m^3/min   |
#      | Montney | Hori_01 | 12       | slurry     | 836   | 2018-04-12T14:48:30.0000000Z | 1.75 m^3/min   |
#      | Montney | Hori_01 | 3        | pressure   | 7636  | 2018-04-07T21:44:39.0000000Z | 67.62 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 4287  | 2018-04-07T20:48:38.0000000Z | 31.6 kPa       |
#      | Montney | Hori_01 | 3        | pressure   | 11646 | 2018-04-07T22:51:42.0000000Z | 70.3 kPa       |
#      | Montney | Hori_01 | 3        | pressure   | 7318  | 2018-04-07T21:39:20.0000000Z | 66.31 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 9138  | 2018-04-07T22:09:46.0000000Z | 28.51 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 2991  | 2018-04-07T20:26:58.0000000Z | 31.27 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 7611  | 2018-04-07T21:44:14.0000000Z | 67.7 kPa       |
#      | Montney | Hori_01 | 3        | pressure   | 13865 | 2018-04-07T23:28:51.0000000Z | 72.73 kPa      |
#      | Montney | Hori_01 | 3        | proppant   | 7646  | 2018-04-07T21:44:49.0000000Z | 275.0 kg/m^3   |
#      | Montney | Hori_01 | 3        | proppant   | 10163 | 2018-04-07T22:26:54.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 10130 | 2018-04-07T22:26:21.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 12142 | 2018-04-07T23:00:01.0000000Z | 125.0 kg/m^3   |
#      | Montney | Hori_01 | 3        | proppant   | 1324  | 2018-04-07T19:59:05.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 4549  | 2018-04-07T20:53:01.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 3990  | 2018-04-07T20:43:40.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 6490  | 2018-04-07T21:25:29.0000000Z | 150.0 kg/m^3   |
#      | Montney | Hori_01 | 3        | slurry     | 9078  | 2018-04-07T22:08:46.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_01 | 3        | slurry     | 1077  | 2018-04-07T19:54:57.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_01 | 3        | slurry     | 3311  | 2018-04-07T20:32:19.0000000Z | 1.91 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 14901 | 2018-04-07T23:46:11.0000000Z | 9.84 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 14496 | 2018-04-07T23:39:24.0000000Z | 10.07 m^3/min  |
#      | Montney | Hori_01 | 3        | slurry     | 11382 | 2018-04-07T22:47:18.0000000Z | 8.67 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 603   | 2018-04-07T19:47:02.0000000Z | 0.06 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 13670 | 2018-04-07T23:25:35.0000000Z | 9.8 m^3/min    |
#      | Montney | Hori_01 | 3        | pressure   | 7636  | 4/7/2018 9:44:39 PM          | 67.62 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 4287  | 4/7/2018 8:48:38 PM          | 31.6 kPa       |
#      | Montney | Hori_01 | 3        | pressure   | 11646 | 4/7/2018 10:51:42 PM         | 70.3 kPa       |
#      | Montney | Hori_01 | 3        | pressure   | 7318  | 4/7/2018 9:39:20 PM          | 66.31 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 9138  | 4/7/2018 10:09:46 PM         | 28.51 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 2991  | 4/7/2018 8:26:58 PM          | 31.27 kPa      |
#      | Montney | Hori_01 | 3        | pressure   | 7611  | 4/7/2018 9:44:14 PM          | 67.7 kPa       |
#      | Montney | Hori_01 | 3        | pressure   | 13865 | 4/7/2018 11:28:51 PM         | 72.73 kPa      |
#      | Montney | Hori_01 | 3        | proppant   | 7646  | 4/7/2018 9:44:49 PM          | 275.0 kg/m^3   |
#      | Montney | Hori_01 | 3        | proppant   | 10163 | 4/7/2018 10:26:54 PM         | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 10130 | 4/7/2018 10:26:21 PM         | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 12142 | 4/7/2018 11:00:01 PM         | 125.0 kg/m^3   |
#      | Montney | Hori_01 | 3        | proppant   | 1324  | 4/7/2018 7:59:05 PM          | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 4549  | 4/7/2018 8:53:01 PM          | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 3990  | 4/7/2018 8:43:40 PM          | 0.0 kg/m^3     |
#      | Montney | Hori_01 | 3        | proppant   | 6490  | 4/7/2018 9:25:29 PM          | 150.0 kg/m^3   |
#      | Montney | Hori_01 | 3        | slurry     | 9078  | 4/7/2018 10:08:46 PM         | 0.0 m^3/min    |
#      | Montney | Hori_01 | 3        | slurry     | 1077  | 4/7/2018 7:54:57 PM          | 0.0 m^3/min    |
#      | Montney | Hori_01 | 3        | slurry     | 3311  | 4/7/2018 8:32:19 PM          | 1.91 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 14901 | 4/7/2018 11:46:11 PM         | 9.84 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 14496 | 4/7/2018 11:39:24 PM         | 10.07 m^3/min  |
#      | Montney | Hori_01 | 3        | slurry     | 11382 | 4/7/2018 10:47:18 PM         | 8.67 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 603   | 4/7/2018 7:47:02 PM          | 0.06 m^3/min   |
#      | Montney | Hori_01 | 3        | slurry     | 13670 | 4/7/2018 11:25:35 PM         | 9.8 m^3/min    |
#      | Montney | Hori_02 | 1        | pressure   | 3871  | 2018-04-06T11:50:46.0000000Z | 69.58 kPa      |
#      | Montney | Hori_02 | 1        | pressure   | 722   | 2018-04-06T10:58:17.0000000Z | 67.51 kPa      |
#      | Montney | Hori_02 | 1        | pressure   | 4156  | 2018-04-06T11:55:31.0000000Z | 70.85 kPa      |
#      | Montney | Hori_02 | 1        | pressure   | 5995  | 2018-04-06T12:26:10.0000000Z | 68.8 kPa       |
#      | Montney | Hori_02 | 1        | pressure   | 10139 | 2018-04-06T13:35:17.0000000Z | 1.08 kPa       |
#      | Montney | Hori_02 | 1        | pressure   | 9487  | 2018-04-06T13:24:25.0000000Z | 1.04 kPa       |
#      | Montney | Hori_02 | 1        | pressure   | 4319  | 2018-04-06T11:58:14.0000000Z | 70.48 kPa      |
#      | Montney | Hori_02 | 1        | pressure   | 3399  | 2018-04-06T11:42:54.0000000Z | 70.24 kPa      |
#      | Montney | Hori_02 | 1        | proppant   | 9160  | 2018-04-06T13:18:58.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 1        | proppant   | 9629  | 2018-04-06T13:26:47.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 1        | proppant   | 922   | 2018-04-06T11:01:37.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 1        | proppant   | 7119  | 2018-04-06T12:44:56.0000000Z | 224.0 kg/m^3   |
#      | Montney | Hori_02 | 1        | proppant   | 6715  | 2018-04-06T12:38:11.0000000Z | 200.0 kg/m^3   |
#      | Montney | Hori_02 | 1        | proppant   | 6735  | 2018-04-06T12:38:31.0000000Z | 200.0 kg/m^3   |
#      | Montney | Hori_02 | 1        | proppant   | 8360  | 2018-04-06T13:05:38.0000000Z | 299.0 kg/m^3   |
#      | Montney | Hori_02 | 1        | proppant   | 9897  | 2018-04-06T13:31:15.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 1        | slurry     | 7581  | 2018-04-06T12:52:39.0000000Z | 8.03 m^3/min   |
#      | Montney | Hori_02 | 1        | slurry     | 365   | 2018-04-06T10:52:20.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_02 | 1        | slurry     | 2597  | 2018-04-06T11:29:32.0000000Z | 3.25 m^3/min   |
#      | Montney | Hori_02 | 1        | slurry     | 8733  | 2018-04-06T13:11:51.0000000Z | 8.01 m^3/min   |
#      | Montney | Hori_02 | 1        | slurry     | 4942  | 2018-04-06T12:08:37.0000000Z | 8.27 m^3/min   |
#      | Montney | Hori_02 | 1        | slurry     | 3606  | 2018-04-06T11:46:21.0000000Z | 7.81 m^3/min   |
#      | Montney | Hori_02 | 1        | slurry     | 2964  | 2018-04-06T11:35:39.0000000Z | 5.22 m^3/min   |
#      | Montney | Hori_02 | 1        | slurry     | 7744  | 2018-04-06T12:55:22.0000000Z | 8.03 m^3/min   |
#      | Montney | Hori_02 | 29       | pressure   | 3193  | 2018-04-19T11:06:26.0000000Z | 64.1 kPa       |
#      | Montney | Hori_02 | 29       | pressure   | 2758  | 2018-04-19T10:59:11.0000000Z | 64.5 kPa       |
#      | Montney | Hori_02 | 29       | pressure   | 3535  | 2018-04-19T11:12:08.0000000Z | 64.9 kPa       |
#      | Montney | Hori_02 | 29       | pressure   | 2978  | 2018-04-19T11:02:51.0000000Z | 64.0 kPa       |
#      | Montney | Hori_02 | 29       | pressure   | 3521  | 2018-04-19T11:11:54.0000000Z | 64.6 kPa       |
#      | Montney | Hori_02 | 29       | pressure   | 2523  | 2018-04-19T10:55:16.0000000Z | 64.9 kPa       |
#      | Montney | Hori_02 | 29       | pressure   | 747   | 2018-04-19T10:25:36.0000000Z | 46.8 kPa       |
#      | Montney | Hori_02 | 29       | pressure   | 416   | 2018-04-19T10:20:05.0000000Z | 51.0 kPa       |
#      | Montney | Hori_02 | 29       | proppant   | 938   | 2018-04-19T10:28:48.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 29       | proppant   | 605   | 2018-04-19T10:23:14.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 29       | proppant   | 588   | 2018-04-19T10:22:57.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 29       | proppant   | 2106  | 2018-04-19T10:48:19.0000000Z | 323.0 kg/m^3   |
#      | Montney | Hori_02 | 29       | proppant   | 2343  | 2018-04-19T10:52:16.0000000Z | 375.0 kg/m^3   |
#      | Montney | Hori_02 | 29       | proppant   | 1114  | 2018-04-19T10:31:44.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 29       | proppant   | 418   | 2018-04-19T10:20:07.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 29       | slurry     | 4072  | 2018-04-19T11:21:06.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_02 | 29       | slurry     | 2239  | 2018-04-19T10:50:32.0000000Z | 10.14 m^3/min  |
#      | Montney | Hori_02 | 29       | slurry     | 613   | 2018-04-19T10:23:22.0000000Z | 1.73 m^3/min   |
#      | Montney | Hori_02 | 29       | slurry     | 1333  | 2018-04-19T10:35:25.0000000Z | 10.05 m^3/min
#      | Montney | Hori_02 | 29       | slurry     | 4039  | 2018-04-19T11:20:33.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_02 | 29       | slurry     | 294   | 2018-04-19T10:18:03.0000000Z | 1.72 m^3/min   |
#      | Montney | Hori_02 | 29       | slurry     | 1878  | 2018-04-19T10:44:31.0000000Z | 10.12 m^3/min  |
#      | Montney | Hori_02 | 5        | pressure   | 1715  | 2018-04-12T01:31:31.0000000Z | 57.6 kPa       |
#      | Montney | Hori_02 | 5        | pressure   | 4104  | 2018-04-12T02:11:23.0000000Z | 72.43 kPa      |
#      | Montney | Hori_02 | 5        | pressure   | 4020  | 2018-04-12T02:09:59.0000000Z | 72.49 kPa      |
#      | Montney | Hori_02 | 5        | pressure   | 1294  | 2018-04-12T01:24:29.0000000Z | 33.65 kPa      |
#      | Montney | Hori_02 | 5        | pressure   | 4390  | 2018-04-12T02:16:09.0000000Z | 72.83 kPa      |
#      | Montney | Hori_02 | 5        | pressure   | 6195  | 2018-04-12T02:46:22.0000000Z | 29.54 kPa      |
#      | Montney | Hori_02 | 5        | pressure   | 5544  | 2018-04-12T02:35:25.0000000Z | 72.61 kPa      |
#      | Montney | Hori_02 | 5        | pressure   | 332   | 2018-04-12T01:08:24.0000000Z | -0.04 kPa      |
#      | Montney | Hori_02 | 5        | proppant   | 4976  | 2018-04-12T02:25:57.0000000Z | 392.0 kg/m^3   |
#      | Montney | Hori_02 | 5        | proppant   | 1630  | 2018-04-12T01:30:06.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 5        | proppant   | 2018  | 2018-04-12T01:36:34.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 5        | proppant   | 4670  | 2018-04-12T02:20:49.0000000Z | 350.0 kg/m^3   |
#      | Montney | Hori_02 | 5        | proppant   | 4578  | 2018-04-12T02:19:17.0000000Z | 325.0 kg/m^3   |
#      | Montney | Hori_02 | 5        | proppant   | 5014  | 2018-04-12T02:26:35.0000000Z | 400.0 kg/m^3   |
#      | Montney | Hori_02 | 5        | proppant   | 5647  | 2018-04-12T02:37:08.0000000Z | 475.0 kg/m^3   |
#      | Montney | Hori_02 | 5        | proppant   | 764   | 2018-04-12T01:15:37.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 5        | slurry     | 5217  | 2018-04-12T02:29:58.0000000Z | 9.57 m^3/min   |
#      | Montney | Hori_02 | 5        | slurry     | 1408  | 2018-04-12T01:26:23.0000000Z | 2.03 m^3/min   |
#      | Montney | Hori_02 | 5        | slurry     | 4396  | 2018-04-12T02:16:15.0000000Z | 10.11 m^3/min  |
#      | Montney | Hori_02 | 5        | slurry     | 2570  | 2018-04-12T01:45:46.0000000Z | 10.01 m^3/min  |
#      | Montney | Hori_02 | 5        | slurry     | 2904  | 2018-04-12T01:51:21.0000000Z | 10.03 m^3/min  |
#      | Montney | Hori_02 | 5        | slurry     | 4756  | 2018-04-12T02:22:15.0000000Z | 9.76 m^3/min   |
#      | Montney | Hori_02 | 5        | slurry     | 1060  | 2018-04-12T01:20:33.0000000Z | 2.01 m^3/min   |
#      | Montney | Hori_02 | 5        | slurry     | 2997  | 2018-04-12T01:52:54.0000000Z | 10.06 m^3/min  |
#      | Montney | Hori_02 | 17       | pressure   | 1851  | 2018-04-16T12:47:31.0000000Z | 71.4 kPa       |
#      | Montney | Hori_02 | 17       | pressure   | 3658  | 2018-04-16T13:18:37.0000000Z | 67.1 kPa       |
#      | Montney | Hori_02 | 17       | pressure   | 2920  | 2018-04-16T13:05:52.0000000Z | 64.2 kPa       |
#      | Montney | Hori_02 | 17       | pressure   | 4975  | 2018-04-16T13:41:19.0000000Z | 68.9 kPa       |
#      | Montney | Hori_02 | 17       | pressure   | 3846  | 2018-04-16T13:21:53.0000000Z | 67.3 kPa       |
#      | Montney | Hori_02 | 17       | pressure   | 5348  | 2018-04-16T13:47:45.0000000Z | 33.6 kPa       |
#      | Montney | Hori_02 | 17       | pressure   | 5273  | 2018-04-16T13:46:30.0000000Z | 34.1 kPa       |
#      | Montney | Hori_02 | 17       | pressure   | 3302  | 2018-04-16T13:12:32.0000000Z | 68.0 kPa       |
#      | Montney | Hori_02 | 17       | proppant   | 706   | 2018-04-16T12:27:44.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 17       | proppant   | 4035  | 2018-04-16T13:25:10.0000000Z | 375.0 kg/m^3   |
#      | Montney | Hori_02 | 17       | proppant   | 1678  | 2018-04-16T12:44:29.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_02 | 17       | proppant   | 1751  | 2018-04-16T12:45:42.0000000Z | 34.0 kg/m^3    |
#      | Montney | Hori_02 | 17       | proppant   | 3023  | 2018-04-16T13:07:42.0000000Z | 195.0 kg/m^3   |
#      | Montney | Hori_02 | 17       | proppant   | 4207  | 2018-04-16T13:28:03.0000000Z | 400.0 kg/m^3   |
#      | Montney | Hori_02 | 17       | proppant   | 2461  | 2018-04-16T12:57:57.0000000Z | 101.0 kg/m^3   |
#      | Montney | Hori_02 | 17       | proppant   | 3243  | 2018-04-16T13:11:27.0000000Z | 223.0 kg/m^3   |
#      | Montney | Hori_02 | 17       | slurry     | 2239  | 2018-04-16T12:54:07.0000000Z | 8.34 m^3/min   |
#      | Montney | Hori_02 | 17       | slurry     | 1597  | 2018-04-16T12:43:07.0000000Z | 8.95 m^3/min   |
#      | Montney | Hori_02 | 17       | slurry     | 3366  | 2018-04-16T13:13:37.0000000Z | 9.27 m^3/min   |
#      | Montney | Hori_02 | 17       | slurry     | 5082  | 2018-04-16T13:43:11.0000000Z | 9.23 m^3/min   |
#      | Montney | Hori_02 | 17       | slurry     | 3537  | 2018-04-16T13:16:36.0000000Z | 9.28 m^3/min   |
#      | Montney | Hori_02 | 17       | slurry     | 4474  | 2018-04-16T13:32:41.0000000Z | 9.03 m^3/min   |
#      | Montney | Hori_02 | 17       | slurry     | 3616  | 2018-04-16T13:17:55.0000000Z | 9.29 m^3/min   |
#      | Montney | Hori_02 | 17       | slurry     | 2850  | 2018-04-16T13:04:42.0000000Z | 8.4 m^3/min    |
#      | Montney | Hori_03 | 1        | pressure   | 8568  | 2018-04-06T23:54:24.0000000Z | 72.32 kPa      |
#      | Montney | Hori_03 | 1        | pressure   | 316   | 2018-04-06T21:34:30.0000000Z | 1.19 kPa       |
#      | Montney | Hori_03 | 1        | pressure   | 9966  | 2018-04-07T00:17:42.0000000Z | 71.1 kPa       |
#      | Montney | Hori_03 | 1        | pressure   | 6587  | 2018-04-06T23:21:23.0000000Z | 70.89 kPa      |
#      | Montney | Hori_03 | 1        | pressure   | 6588  | 2018-04-06T23:21:24.0000000Z | 71.09 kPa      |
#      | Montney | Hori_03 | 1        | pressure   | 2800  | 2018-04-06T22:18:13.0000000Z | 24.03 kPa      |
#      | Montney | Hori_03 | 1        | pressure   | 3434  | 2018-04-06T22:28:47.0000000Z | 19.12 kPa      |
#      | Montney | Hori_03 | 1        | pressure   | 3178  | 2018-04-06T22:24:31.0000000Z | 0.41 kPa       |
#      | Montney | Hori_03 | 1        | proppant   | 10178 | 2018-04-07T00:21:14.0000000Z | 371.0 kg/m^3   |
#      | Montney | Hori_03 | 1        | proppant   | 2323  | 2018-04-06T22:10:16.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 1        | proppant   | 5517  | 2018-04-06T23:03:33.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 1        | proppant   | 5446  | 2018-04-06T23:02:22.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 1        | proppant   | 10102 | 2018-04-07T00:19:58.0000000Z | 374.0 kg/m^3   |
#      | Montney | Hori_03 | 1        | proppant   | 6461  | 2018-04-06T23:19:17.0000000Z | 76.0 kg/m^3    |
#      | Montney | Hori_03 | 1        | proppant   | 4341  | 2018-04-06T22:43:56.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 1        | proppant   | 9577  | 2018-04-07T00:11:13.0000000Z | 350.0 kg/m^3   |
#      | Montney | Hori_03 | 1        | slurry     | 5413  | 2018-04-06T23:01:49.0000000Z | 7.51 m^3/min   |
#      | Montney | Hori_03 | 1        | slurry     | 4910  | 2018-04-06T22:53:26.0000000Z | 4.03 m^3/min   |
#      | Montney | Hori_03 | 1        | slurry     | 1843  | 2018-04-06T22:02:16.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_03 | 1        | slurry     | 10236 | 2018-04-07T00:22:12.0000000Z | 8.78 m^3/min   |
#      | Montney | Hori_03 | 1        | slurry     | 5346  | 2018-04-06T23:00:42.0000000Z | 6.31 m^3/min   |
#      | Montney | Hori_03 | 1        | slurry     | 788   | 2018-04-06T21:44:41.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_03 | 1        | slurry     | 6713  | 2018-04-06T23:23:29.0000000Z | 9.56 m^3/min   |
#      | Montney | Hori_03 | 1        | slurry     | 3059  | 2018-04-06T22:22:32.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_03 | 28       | pressure   | 3094  | 2018-04-20T12:26:59.0000000Z | 51.4 kPa       |
#      | Montney | Hori_03 | 28       | pressure   | 3848  | 2018-04-20T12:40:28.0000000Z | 50.6 kPa       |
#      | Montney | Hori_03 | 28       | pressure   | 3113  | 2018-04-20T12:27:20.0000000Z | 51.4 kPa       |
#      | Montney | Hori_03 | 28       | pressure   | 1378  | 2018-04-20T11:56:16.0000000Z | 55.9 kPa       |
#      | Montney | Hori_03 | 28       | pressure   | 638   | 2018-04-20T11:43:02.0000000Z | 31.6 kPa       |
#      | Montney | Hori_03 | 28       | pressure   | 3530  | 2018-04-20T12:34:47.0000000Z | 50.7 kPa       |
#      | Montney | Hori_03 | 28       | pressure   | 3917  | 2018-04-20T12:41:42.0000000Z | 51.1 kPa       |
#      | Montney | Hori_03 | 28       | pressure   | 1574  | 2018-04-20T11:59:48.0000000Z | 53.8 kPa       |
#      | Montney | Hori_03 | 28       | proppant   | 3183  | 2018-04-20T12:28:34.0000000Z | 425.0 kg/m^3   |
#      | Montney | Hori_03 | 28       | proppant   | 1753  | 2018-04-20T12:02:58.0000000Z | 200.0 kg/m^3   |
#      | Montney | Hori_03 | 28       | proppant   | 1607  | 2018-04-20T12:00:23.0000000Z | 175.0 kg/m^3   |
#      | Montney | Hori_03 | 28       | proppant   | 506   | 2018-04-20T11:40:39.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 28       | proppant   | 2503  | 2018-04-20T12:16:24.0000000Z | 325.0 kg/m^3   |
#      | Montney | Hori_03 | 28       | proppant   | 2558  | 2018-04-20T12:17:23.0000000Z | 325.0 kg/m^3   |
#      | Montney | Hori_03 | 28       | proppant   | 1302  | 2018-04-20T11:54:55.0000000Z | 74.0 kg/m^3    |
#      | Montney | Hori_03 | 28       | proppant   | 215   | 2018-04-20T11:35:27.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 28       | slurry     | 1791  | 2018-04-20T12:03:39.0000000Z | 10.0 m^3/min   |
#      | Montney | Hori_03 | 28       | slurry     | 3696  | 2018-04-20T12:37:45.0000000Z | 10.04 m^3/min  |
#      | Montney | Hori_03 | 28       | slurry     | 1744  | 2018-04-20T12:02:48.0000000Z | 9.99 m^3/min   |
#      | Montney | Hori_03 | 28       | slurry     | 889   | 2018-04-20T11:47:31.0000000Z | 4.58 m^3/min   |
#      | Montney | Hori_03 | 28       | slurry     | 2661  | 2018-04-20T12:19:14.0000000Z | 10.03 m^3/min  |
#      | Montney | Hori_03 | 28       | slurry     | 1239  | 2018-04-20T11:53:47.0000000Z | 10.09 m^3/min  |
#      | Montney | Hori_03 | 28       | slurry     | 2699  | 2018-04-20T12:19:56.0000000Z | 10.03 m^3/min  |
#      | Montney | Hori_03 | 28       | slurry     | 4166  | 2018-04-20T12:46:09.0000000Z | 10.05 m^3/min  |
#      | Montney | Hori_03 | 8        | pressure   | 198   | 2018-04-13T22:48:21.0000000Z | 22.8 kPa       |
#      | Montney | Hori_03 | 8        | pressure   | 135   | 2018-04-13T22:47:18.0000000Z | 31.4 kPa       |
#      | Montney | Hori_03 | 8        | pressure   | 3846  | 2018-04-13T23:49:15.0000000Z | 69.3 kPa       |
#      | Montney | Hori_03 | 8        | pressure   | 5396  | 2018-04-14T00:15:08.0000000Z | 72.5 kPa       |
#      | Montney | Hori_03 | 8        | pressure   | 803   | 2018-04-13T22:58:27.0000000Z | 31.2 kPa       |
#      | Montney | Hori_03 | 8        | pressure   | 3475  | 2018-04-13T23:43:03.0000000Z | 69.2 kPa       |
#      | Montney | Hori_03 | 8        | pressure   | 1772  | 2018-04-13T23:14:37.0000000Z | 69.5 kPa       |
#      | Montney | Hori_03 | 8        | pressure   | 3203  | 2018-04-13T23:38:30.0000000Z | 69.1 kPa       |
#      | Montney | Hori_03 | 8        | proppant   | 1477  | 2018-04-13T23:09:41.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 8        | proppant   | 4726  | 2018-04-14T00:03:58.0000000Z | 425.0 kg/m^3   |
#      | Montney | Hori_03 | 8        | proppant   | 1689  | 2018-04-13T23:13:13.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 8        | proppant   | 1666  | 2018-04-13T23:12:50.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 8        | proppant   | 373   | 2018-04-13T22:51:16.0000000Z | 0.0 kg/m^3     |
#      | Montney | Hori_03 | 8        | proppant   | 4377  | 2018-04-13T23:58:08.0000000Z | 375.0 kg/m^3   |
#      | Montney | Hori_03 | 8        | proppant   | 5026  | 2018-04-14T00:08:58.0000000Z | 475.0 kg/m^3   |
#      | Montney | Hori_03 | 8        | proppant   | 5518  | 2018-04-14T00:17:11.0000000Z | 504.0 kg/m^3   |
#      | Montney | Hori_03 | 8        | slurry     | 5788  | 2018-04-14T00:21:42.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_03 | 8        | slurry     | 2853  | 2018-04-13T23:32:39.0000000Z | 9.99 m^3/min   |
#      | Montney | Hori_03 | 8        | slurry     | 880   | 2018-04-13T22:59:44.0000000Z | 0.16 m^3/min   |
#      | Montney | Hori_03 | 8        | slurry     | 2083  | 2018-04-13T23:19:48.0000000Z | 9.3 m^3/min    |
#      | Montney | Hori_03 | 8        | slurry     | 1249  | 2018-04-13T23:05:53.0000000Z | 2.09 m^3/min   |
#      | Montney | Hori_03 | 8        | slurry     | 5905  | 2018-04-14T00:23:39.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_03 | 8        | slurry     | 3590  | 2018-04-13T23:44:58.0000000Z | 10.0 m^3/min   |
#      | Montney | Hori_03 | 8        | slurry     | 5857  | 2018-04-14T00:22:51.0000000Z | 0.0 m^3/min    |
#      | Montney | Hori_03 | 23       | pressure   | 69    | 2018-04-18T09:22:00.0000000Z | 62.4 kPa       |
#      | Montney | Hori_03 | 23       | pressure   | 56    | 2018-04-18T09:09:00.0000000Z | 64.3 kPa       |
#      | Montney | Hori_03 | 23       | pressure   | 65    | 2018-04-18T09:18:00.0000000Z | 60.8 kPa       |
#      | Montney | Hori_03 | 23       | pressure   | 40    | 2018-04-18T08:53:00.0000000Z | 60.3 kPa       |
#      | Montney | Hori_03 | 23       | pressure   | 70    | 2018-04-18T09:23:00.0000000Z | 63.5 kPa       |
#      | Montney | Hori_03 | 23       | pressure   | 78    | 2018-04-18T09:31:00.0000000Z | 63.7 kPa       |
#      | Montney | Hori_03 | 23       | pressure   | 42    | 2018-04-18T08:55:00.0000000Z | 60.0 kPa       |
#      | Montney | Hori_03 | 23       | pressure   | 2     | 2018-04-18T08:15:00.0000000Z | 29.3 kPa       |
#      | Montney | Hori_03 | 23       | proppant   | 17    | 2018-04-18T08:30:00.0000000Z | 0.0 kg/m^33    |
#      | Montney | Hori_03 | 23       | proppant   | 31    | 2018-04-18T08:44:00.0000000Z | 129.0 kg/m^33  |
#      | Montney | Hori_03 | 23       | proppant   | 24    | 2018-04-18T08:37:00.0000000Z | 23.0 kg/m^33   |
#      | Montney | Hori_03 | 23       | proppant   | 77    | 2018-04-18T09:30:00.0000000Z | 400.0 kg/m^33  |
#      | Montney | Hori_03 | 23       | proppant   | 49    | 2018-04-18T09:02:00.0000000Z | 448.0 kg/m^33  |
#      | Montney | Hori_03 | 23       | proppant   | 69    | 2018-04-18T09:22:00.0000000Z | 47.0 kg/m^33   |
#      | Montney | Hori_03 | 23       | proppant   | 67    | 2018-04-18T09:20:00.0000000Z | 499.0 kg/m^33  |
#      | Montney | Hori_03 | 23       | proppant   | 75    | 2018-04-18T09:28:00.0000000Z | 320.0 kg/m^33  |
#      | Montney | Hori_03 | 23       | slurry     | 31    | 2018-04-18T08:44:00.0000000Z | 10.04 m^33/min |
#      | Montney | Hori_03 | 23       | slurry     | 25    | 2018-04-18T08:38:00.0000000Z | 10.01 m^33/min |
#      | Montney | Hori_03 | 23       | slurry     | 46    | 2018-04-18T08:59:00.0000000Z | 10.09 m^33/min |
#      | Montney | Hori_03 | 23       | slurry     | 32    | 2018-04-18T08:45:00.0000000Z | 10.05 m^33/min |
#      | Montney | Hori_03 | 23       | slurry     | 14    | 2018-04-18T08:27:00.0000000Z | 1.77 m^33/min  |
#      | Montney | Hori_03 | 23       | slurry     | 59    | 2018-04-18T09:12:00.0000000Z | 10.03 m^33/min |
#      | Montney | Hori_03 | 23       | slurry     | 8     | 2018-04-18T08:21:00.0000000Z | 1.76 m^33/min  |
#      | Montney | Hori_03 | 23       | slurry     | 64    | 2018-04-18T09:17:00.0000000Z | 10.09 m^33/min |

