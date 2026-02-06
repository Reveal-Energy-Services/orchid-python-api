#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2025 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest
import uuid

from hamcrest import assert_that, equal_to, calling, raises

from orchid import dom_project_object as dpo

from tests import stub_net as tsn


class TestProjectObject(unittest.TestCase):

    def test_constructed_instance_has_display_name_supplied_to_constructor(self):
        display_name = 'pellueram'
        stub_net_project_object = tsn.create_stub_net_project_object(display_name=display_name)
        sut = dpo.DomProjectObject(stub_net_project_object)

        assert_that(sut.display_name, equal_to(display_name))

    def test_constructed_instance_has_no_display_name_supplied_to_constructor(self):
        display_name = None
        stub_net_project_object = tsn.create_stub_net_project_object(display_name=display_name)
        sut = dpo.DomProjectObject(stub_net_project_object)

        # Because `display_name` is a `property` and not simply an attribute, one cannot simply pass
        # `sut.display_name` to `calling`. (This simple action results in sending the **result** of
        # invoking the `__get__` method of `sut.display_name` (a property is a descriptor). Consequently, I create a
        # function of no arguments that simply calls `sut.display_name` to run the test.
        assert_that(calling(lambda: sut.display_name).with_args(),
                    raises(ValueError, pattern='Unexpected value, `None`, for `display_name`.'))

    def test_constructed_instance_has_name_supplied_to_constructor(self):
        name = 'ducueram'
        stub_net_project_object = tsn.create_stub_net_project_object(name=name)
        sut = dpo.DomProjectObject(stub_net_project_object)

        assert_that(sut.name, equal_to(name))

    def test_constructed_instance_has_object_id_supplied_to_constructor(self):
        object_id = 'bb56fd83-7280-498b-88f9-d03ec2b344fc'
        stub_net_project_object = tsn.create_stub_net_project_object(object_id=object_id)
        sut = dpo.DomProjectObject(stub_net_project_object)

        assert_that(sut.object_id, equal_to(uuid.UUID(object_id)))


if __name__ == '__main__':
    unittest.main()
