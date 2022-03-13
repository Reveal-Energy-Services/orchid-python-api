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

from hamcrest import assert_that, equal_to

from orchid import native_variant_adapter as nva

from tests import stub_net as tsn

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import Int32, Double, String


# Test ideas
# - Create stage correction status variant returns correct value
# - Create stage correction status variant returns correct type
# - Get value of stage correction status variant returns correct value
# - Type of stage correction status variant returns correct value
# TODO Create other variants as needed

class TestCreateNativeVariantAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_create_variant_returns_value_set_at_creation(self):
        for variant_type, variant_value in [
            (nva.PythonVariantTypes.INT32, -79),
            (nva.PythonVariantTypes.DOUBLE, -136.2),
            (nva.PythonVariantTypes.STRING, 'exspatior'),
        ]:
            with self.subTest(f'{variant_type.name} variant returns value {variant_value}'):
                sut = nva.create_variant(variant_value, variant_type)

                assert_that(sut.value, equal_to(variant_value))

    def test_create_variant_returns_type_set_at_creation(self):
        for variant_type, variant_value in [
            (nva.PythonVariantTypes.INT32, -51),
            (nva.PythonVariantTypes.DOUBLE, 12.52),
            (nva.PythonVariantTypes.STRING, 'fingo'),
        ]:
            with self.subTest(f'{variant_type.name} variant has type {variant_type}'):
                sut = nva.create_variant(variant_value, variant_type)

                assert_that(sut.type, equal_to(variant_type))


class TestNativeVariantAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))

    def test_get_value_returns_value_in_net_variant(self):
        for net_variant_type, variant_value in [
            (Int32, 89),
            (Double, -4.345),
            (String, 'vivum'),
        ]:
            with self.subTest(f'.NET {net_variant_type} variant returns value, {variant_value}'):
                stub_net_variant = tsn.VariantDto(variant_value, net_variant_type).create_net_stub()
                sut = nva.NativeVariantAdapter(stub_net_variant)

                assert_that(sut.value, equal_to(variant_value))

    def test_type_returns_variant_type_corresponding_to_net_variant_type(self):
        for net_variant_type, variant_value, variant_type in [
            (Int32, -40, nva.PythonVariantTypes.INT32),
            (Double, 42.53, nva.PythonVariantTypes.DOUBLE),
            (String, 'mespilae', nva.PythonVariantTypes.DOUBLE),
        ]:
            with self.subTest(f'.NET {net_variant_type} variant returns type, {variant_type}'):
                stub_net_variant = tsn.VariantDto(variant_value, variant_type).create_net_stub()
                sut = nva.NativeVariantAdapter(stub_net_variant)

                assert_that(sut.type, equal_to(variant_type))


if __name__ == '__main__':
    unittest.main()
