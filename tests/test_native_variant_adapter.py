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


import unittest

from hamcrest import assert_that, equal_to, close_to

from orchid import native_variant_adapter as nva

from tests import stub_net as tsn

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import Int32, Double, String


# Test ideas
# - Create new variant with int returns int value
# - Create new variant with float returns float value
# - Create new variant with str returns str value
# TODO Create other variants as needed
class TestNativeVariantAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_create_int_variant_returns_int_value(self):
        sut = nva.create_variant(-79, nva.PythonVariantTypes.INT32)

        assert_that(sut.value, equal_to(-79))

    def test_create_int_variant_returns_variant_with_int_type(self):
        sut = nva.create_variant(-51, nva.PythonVariantTypes.INT32)

        assert_that(sut.type, equal_to(nva.PythonVariantTypes.INT32))

    def test_get_value_of_int_variant_returns_int_in_native_variant(self):
        stub_net_variant = tsn.VariantDto(89, Int32).create_net_stub()
        sut = nva.NativeVariantAdapter(stub_net_variant)

        assert_that(sut.value, equal_to(89))

    def test_get_value_of_double_variant_returns_float_in_native_variant(self):
        stub_net_variant = tsn.VariantDto(-4.345, Double).create_net_stub()
        sut = nva.NativeVariantAdapter(stub_net_variant)

        assert_that(sut.value, close_to(-4.345, 0.001))

    def test_get_value_of_str_variant_returns_str_in_native_variant(self):
        stub_net_variant = tsn.VariantDto('vivum', String).create_net_stub()
        sut = nva.NativeVariantAdapter(stub_net_variant)

        assert_that(sut.value, equal_to('vivum'))


if __name__ == '__main__':
    unittest.main()
