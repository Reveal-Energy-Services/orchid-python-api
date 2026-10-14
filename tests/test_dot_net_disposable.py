#  Copyright (c) 2017-2026 KAPPA
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

from hamcrest import assert_that, equal_to, same_instance

from orchid import dot_net_disposable as dnd


class StubDisposable:
    def __init__(self):
        self.dispose_count = 0

    def Dispose(self):
        self.dispose_count += 1


class StubContextManagerDisposable(StubDisposable):
    # Python.NET 3.1 and later add `__enter__` / `__exit__` to .NET `IDisposable` instances
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.Dispose()


# Test ideas
class TestDotNetDisposable(unittest.TestCase):
    def test_disposable_yields_and_disposes_object(self):
        stub = StubDisposable()
        with dnd.disposable(stub) as actual:
            assert_that(actual, same_instance(stub))
        assert_that(stub.dispose_count, equal_to(1))

    def test_disposable_yields_and_disposes_object_already_a_context_manager(self):
        stub = StubContextManagerDisposable()
        with dnd.disposable(stub) as actual:
            assert_that(actual, same_instance(stub))
        assert_that(stub.dispose_count, equal_to(1))

    def test_disposable_yields_object_without_dispose(self):
        stub = object()
        with dnd.disposable(stub) as actual:
            assert_that(actual, same_instance(stub))


if __name__ == '__main__':
    unittest.main()
