#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

import unittest.mock
import uuid

import deal
from hamcrest import assert_that, equal_to, contains_exactly, calling, raises
import numpy as np
import vectormath as vmath

import image_frac


class TrajectoryCoordinatorShould(unittest.TestCase):
    """Defines the unit tests for the TrajectoryCoordinator class."""

    @staticmethod
    def test_canary_test():
        assert_that(2 + 2, equal_to(4))

    @staticmethod
    def test_ctor_null_pathname_raises_exception():
        assert_that(calling(image_frac.TrajectoryCoordinator).with_args(None),
                    raises(deal.PreContractError))

    @staticmethod
    def test_ctor_empty_pathname_raises_exception():
        assert_that(calling(image_frac.TrajectoryCoordinator).with_args(''),
                    raises(deal.PreContractError))

    @staticmethod
    def test_ctor_whitespace_pathname_raises_exception():
        assert_that(calling(image_frac.TrajectoryCoordinator).with_args('\n'),
                    raises(deal.PreContractError))

    @staticmethod
    def test_no_wells_produces_no_trajectories():
        sut = image_frac.TrajectoryCoordinator('dont_care')

        assert_that(sut.trajectories_for_all_wells(), equal_to({}))

    @staticmethod
    @unittest.mock.patch('image_frac.trajectory_coordinator.ProjectAdapter', name='mock_project_adapter', autospec=True)
    def test_one_well_produces_one_trajectory(mock_project_adapter):
        project = mock_project_adapter.return_value
        one_well_id = uuid.UUID('8a0ea32ed8d244b0a07b120b911a2b4f')
        project.well_ids.return_value = [one_well_id]
        expected_trajectory_points = vmath.Vector3Array([[720486, 6825178, -6315],
                                                         [720578, 6285197, -6312], [720669, 6825221,  -6312]])

        def trajectory_points_returns(well_id):
            # Passing a function to `side_effect` invokes the function with the **actual** arguments passed to
            # call. I look up these actual arguments in a dictionary of expected results. If the actual
            # arguments are **not** present in the results, I return the `DEFAULT` value (a newly created Mock).
            results = {one_well_id: expected_trajectory_points}
            return results.get(well_id, unittest.mock.DEFAULT)
        project.trajectory_points.side_effect = trajectory_points_returns

        sut = image_frac.TrajectoryCoordinator('dont_care')

        actual_trajectories = sut.trajectories_for_all_wells()
        assert_that(len(actual_trajectories), equal_to(1))
        # noinspection PyTypeChecker
        assert_that(actual_trajectories.keys(), contains_exactly(one_well_id))
        for (actual, expected) in zip(actual_trajectories.values(), [expected_trajectory_points]):
            np.testing.assert_array_equal(actual, expected)

    @staticmethod
    @unittest.mock.patch('image_frac.trajectory_coordinator.ProjectAdapter', name='mock_project_adapter', autospec=True)
    def test_many_wells_produces_many_trajectories(mock_project_adapter):
        project = mock_project_adapter.return_value
        many_well_ids = [uuid.UUID(i) for i in ['2f3b8e73a7724bbf960f4ed40eabc2c5',
                                                '176d7ff23287400c89ebf8f2cf90d337', '698cf8e5440d43e4966e35e49d82d359']]
        project.well_ids.return_value = many_well_ids
        expected_trajectory_points = [vmath.Vector3Array([[61058, 1449386, -3098],
                                                         [61124, 1449452, -3100], [61196, 1449513, -3100]]),
                                      vmath.Vector3Array([[199043, 1232404, -2826],
                                                          [199136, 1232395, -2834], [199230, 1232390, -2826]]),
                                      vmath.Vector3Array([[149580, 1469502, -2482],
                                                          [149656, 1469447, -2486], [149727, 1469385, -2483]])]

        def trajectory_points_returns(well_id):
            # Passing a function to `side_effect` invokes the function with the **actual** arguments passed to
            # call. I look up these actual arguments in a dictionary of expected results. If the actual
            # arguments are **not** present in the results, I return the `DEFAULT` value (a newly created Mock).
            results = {well_id: trajectory
                       for (well_id, trajectory) in zip(many_well_ids, expected_trajectory_points)}
            return results.get(well_id, unittest.mock.DEFAULT)
        project.trajectory_points.side_effect = trajectory_points_returns

        sut = image_frac.TrajectoryCoordinator('dont_care')

        actual_trajectories = sut.trajectories_for_all_wells()
        assert_that(len(actual_trajectories), equal_to(3))
        # noinspection PyTypeChecker
        assert_that(actual_trajectories.keys(), contains_exactly(*many_well_ids))
        for (actual, expected) in zip(actual_trajectories.values(), expected_trajectory_points):
            np.testing.assert_array_equal(actual, expected)


if __name__ == '__main__':
    unittest.main()
