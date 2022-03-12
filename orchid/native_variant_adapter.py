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

from orchid import dot_net_dom_access as dna

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Settings import Variant
# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import Int32, Type


def make_variant(o):
    pass


class NativeVariantAdapter(dna.DotNetAdapter):
    """Adapts a .NET Variant to python"""

    # Although the .NET `Variant` provides a number of ways to convert the value of the `Variant` to other .NET types,
    # I do not believe this interface is the most Pythonic interface. Instead, I have chosen simply to implement the
    # `value` property and let callers convert the value using typing Python code; for example, by calling `int`,
    # `float`, or `str`.

    def __init__(self, adaptee: Variant):
        """
        Construct an instance adapting `adaptee`.

        Args:
            adaptee: The .NET `Variant` to be adapted.
        """
        super().__init__(adaptee)

    @property
    def value(self):
        return self.dom_object.GetValue[self.dom_object.Type()]()
