#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2022 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest
import uuid

import toolz.curried as toolz
from hamcrest import assert_that, equal_to, calling, raises

from orchid import (
    searchable_data_frames as sdf,
)
from tests import stub_net as tsn

# noinspection PyUnresolvedReferences
from System import Guid


class TestSearchableDataFrames(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_find_by_object_id_raises_warning_if_guid_column(self):
        table_data_dto = tsn.TableDataDto([uuid.UUID],
                                          [{'pertinacis': 'af777540-05b2-49aa-9965-5ce20cb93ccd'}],
                                          toolz.identity)
        project = tsn.create_stub_net_project(data_frame_dtos=[{'table_data_dto': table_data_dto}])
        assert_that(calling(project.data_frames), raises(sdf.SearchableDataFramesSystemGuidWarning))


if __name__ == '__main__':
    unittest.main()
