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

import unittest

from hamcrest import assert_that, equal_to
import option


from orchid import (
    native_stage_adapter as nsa,
    searchable_stages as oss,
)

from tests import stub_net as tsn


class TestSearchableStages(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_search_finds_no_matching_display_stage_number_if_no_stages(self):
        stage_dtos = ()
        to_find_stage_display_number = 4
        stub_net_stages = [tsn.create_stub_net_stage(**stage_dto) for stage_dto in stage_dtos]
        sut = oss.SearchableStages(nsa.NativeStageAdapter, stub_net_stages)

        actual = sut.find_by_display_stage_number(to_find_stage_display_number)

        assert_that(actual, equal_to(option.NONE))


if __name__ == '__main__':
    unittest.main()
