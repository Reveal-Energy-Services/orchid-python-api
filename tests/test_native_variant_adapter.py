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


# Test ideas
# - Create int variant
# - Create double variant
# - Create str variant
# - Get value of int variant
# - Get value of double variant
# - Get value of str variant
# - Convert int variant to double
# - Convert int variant to str
# - Convert double variant to int
# - Convert double variant to str
# - Convert str variant to int
# - Convert str variant to double
# - Convert double variant to int fails
# - Convert str variant to int fails
# - Convert str variant to double fails
# TODO Create other variants as needed
class TestNativeVariantAdapter(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, equal_to(4))


if __name__ == '__main__':
    unittest.main()
