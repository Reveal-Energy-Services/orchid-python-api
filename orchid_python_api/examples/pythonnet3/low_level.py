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

"""
Script demonstrating the changes to repair low-level examples after upgrading Python.NET 3.
"""


# Repairs of Python.NET 3 breaking changes to low-level examples

# 0 Load a runtime before calling `import clr`

# In order to access .NET assemblies (`.dll` files), one must load an available runtime before executing the
# `import clr` statement. (If one calls `import clr` before specifying a runtime, Python.NET will load a default
# runtime which may **not** be compatible with the installed Orchid assemblies.
#
# To make this easier, when we `import` the `orchid` package, the Orchid Python API will load the runtime
# corresponding to the configured Orchid installation.

# noinspection PyUnresolvedReferences
import orchid

# noinspection PyUnresolvedReferences,PyPackageRequirements
import clr

import pprint  # Used to "pretty-print" complex data, for example, lists
import textwrap  # Help to format pretty printed text

import pendulum

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Factories.Implementations import Attribute

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import (
    ArgumentException,
    Convert,
    DateTime,
    DateTimeKind,
    DateTimeOffset,
    Int32,
    InvalidCastException,
    TimeSpan,
)


DEFAULT_TEXTWRAP_WIDTH = 70


def print_underline(text, ch):
    print(textwrap.fill(text))
    print(min(len(text), DEFAULT_TEXTWRAP_WIDTH) * ch)
    print()


def title(text):
    print(min(len(text), DEFAULT_TEXTWRAP_WIDTH) * '#')
    print_underline(text, '#')


def section(text):
    print_underline(text, '=')


def sub_section(text):
    print_underline(text, '-')


def sub_sub_section(text):
    print_underline(text, '^')


def paragraph(text):
    print(textwrap.fill(text, replace_whitespace=True))
    print()


def quote(text):
    print(textwrap.fill(text, replace_whitespace=True, initial_indent='> ', subsequent_indent='> '))
    print()


# noinspection DuplicatedCode
def banner(banner_text):
    print(len(banner_text) * '=')
    print(banner_text)
    print(len(banner_text) * '=')
    print()


def empty_line():
    print()


def pretty_print_with_header(item, header, max_lines=None):
    header_text = f'`{header}` returns:'
    pretty_printed_text = (textwrap
                           .TextWrapper(initial_indent=2 * ' ', subsequent_indent=(2 + 1) * ' ', max_lines=max_lines)
                           .fill(f'{pprint.pformat(item)}'))
    text_to_print = f'{header_text}\n{pretty_printed_text}'
    print(text_to_print)
    print()


def pretty_print_net_item_with_header(net_item, header, max_lines=None):
    header_text = f'`{header}.ToString()` returns:'
    pretty_printed_text = (textwrap
                           .TextWrapper(initial_indent=2 * ' ', subsequent_indent=(2 + 1) * ' ', max_lines=max_lines)
                           .fill(f'{pprint.pformat(net_item.ToString())}'))
    text_to_print = f'{header_text}\n{pretty_printed_text}'
    print(text_to_print)
    print()


def pretty_print_with_error(error_callable, error_type, header, max_lines=None):
    header_text = f'Trying {header} raises:'
    try:
        error_callable()
    except error_type as et:
        pretty_printed_text = (textwrap
                               .TextWrapper(initial_indent=2 * ' ', subsequent_indent=(2 + 1) * ' ',
                                            max_lines=max_lines)
                               .fill(f'{pprint.pformat(et)}'))
        text_to_print = f'{header_text}\n{pretty_printed_text}'
        print(text_to_print)
    print()


def wait_for_input():
    input('Press enter to continue...')
    print()

section('1 Fewer implicit conversions between Python values and .NET values')

sub_section('1.1 Adding attributes with integer values requires conversion')

# (This issue occurred in **both** internal testing and low-level script testing and so is duplicated.)

paragraph("""Under Python.NET 2.5.2, one could supply a Python `int` value to the `SetAttribute` call for an 
`IAttribute` with a `System.Int32` value.""")

paragraph('(This scenario requires significant set up. Please wait patiently...)')

# Find the well named 'Demo_1H'
bakken = orchid.load_project('c:/src/Orchid.IntegrationTestData/frankNstein_Bakken_UTM13_FEET.ifrac')
candidate_wells = list(bakken.wells().find_by_name('Demo_1H'))
assert len(candidate_wells) == 1
demo_1h = candidate_wells[0]

# Create an attribute with name, 'My New Attribute', and type, `System.Int32`
attribute_to_add_type = Int32
attribute_to_add = Attribute[attribute_to_add_type].Create('My New Attribute')

# Add newly created attribute to well, 'Demo_1H'
with orchid.dot_net_disposable.disposable(demo_1h.dom_object.ToMutable()) as mutable_well:
    mutable_well.AddStageAttribute(attribute_to_add)

# Find stage number 7 in well, 'Demo_1H'
maybe_stage = demo_1h.stages().find_by_display_stage_number(7)
assert maybe_stage is not None
stage_7 = maybe_stage

paragraph("""Executing this same code, under Python.NET 3, raises an `ArgumentException`.""")

# Add attribute with value, 17, to stage 7, with Python `int` type.
with (orchid.dot_net_disposable.disposable(stage_7.dom_object.ToMutable())) as mutable_stage:
    # This action will fail because the attribute type is `System.Int32`
    # and `pythonnet-3.0.0.post1` **does not** implicitly equate these two types.
    try:
        mutable_stage.SetAttribute(attribute_to_add, int)
    except ArgumentException as ae:
        print(f'ArgumentException: {ae}')
empty_line()

paragraph("""Using Python.NET 3, one must **explicitly** convert the supplied `int` to `Int32`.""")

# Add attribute to stage 7 with a value of 17 **explicitly** converted to an `Int32`
with (orchid.dot_net_disposable.disposable(stage_7.dom_object.ToMutable())) as mutable_stage:
    mutable_stage.SetAttribute(attribute_to_add, attribute_to_add_type(7))

# Verify added attribute value
ignored_object = object()
is_attribute_present, actual_attribute_value = stage_7.dom_object.TryGetAttributeValue(attribute_to_add,
                                                                                       ignored_object)
assert is_attribute_present
assert type(actual_attribute_value) == int
assert actual_attribute_value == 7

wait_for_input()

sub_section('1.2 `Leakoff.ControlPoints` and no ValueType() ctor error')

paragraph("""This issue seems similar to the internal test issue in which the .NET `TimeSpan` class did not have a 
default constructor, but Python.NET 2.5.2 accepted the expression, `TimeSpan()`, and appeared to 'do the right 
thing.'""")

paragraph("""In this situation, our low-level example code contained the expression:""")

paragraph("""
```Leakoff.ControlPoint(DateTime=some_time, Pressure=some_pressure)```
""")

paragraph("""Although Python.NET 2.5.2 seemed to "do the right thing" with this expression, executing this expression 
using Python.NET 3 raises an exception with a somewhat obscure (in retrospect) error message.
""")

wait_for_input()
