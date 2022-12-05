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
Script demonstrating the changes needed after upgrading Python.NET 3.
"""


# Repairs of Python.NET 3 breaking changes to internal tests

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


title('Repairs of Python.NET 3 breaking changes to internal tests')

section('1 Reduce the implicit conversions between Python types and .NET Types')

sub_section("1.1 Equality between Python `int` values and `DateTimeOffset.MaxValue` no longer supported")

paragraph("""Python.NET 2.5.2 allowed a developer to test for equality between Python `int` values and values of type
`DateTimeOffset` by performing an implicit conversion of the `DateTimeOffset` type. This test raises an exception 
in Python.NET 3.""")

pretty_print_with_error(lambda: 108 == DateTimeOffset.MaxValue, TypeError, '`108 == DateTimeOffset.MaxValue`')
pretty_print_with_error(lambda: 108 == TimeSpan.MaxValue, TypeError, '`108 == TimeSpan.MaxValue`')
wait_for_input()

paragraph("We filed an issue with the Python.NET team. They responded with the following:")

quote("""Yes, we tried to limit the "implicit" conversions to a minimum. I don't even know, which 
change in particular is responsible for the behavioural ~change~ fix that you are observing here, but you are only 
able to compare things to a .NET object that are directly convertible to it. If you'd really require this for 
`DateTimeOffset` and TimeSpan`, you could make them convertible via a
[Codec](https://pythonnet.github.io/pythonnet/codecs.html). Otherwise, I'd suggest you just generate the respective
 comparison values using `.FromTicks`.""")

paragraph("Python.NET 3 requires a developer to explicitly use the `DateTimeOffset.Ticks` for in the equality test.")

pretty_print_with_header(108 == DateTimeOffset.MaxValue.Ticks, '108 == DateTimeOffset.MaxValue.Ticks')
pretty_print_with_header(108 == TimeSpan.MaxValue.Ticks, '108 == TimeSpan.MaxValue.Ticks')
pretty_print_with_header(108 == TimeSpan.MinValue.Ticks, '108 == TimeSpan.MinValue.Ticks')
wait_for_input()

sub_section('1.2 Less effort to make Python constructors "just work"')

paragraph("""Python.NET 2.5.2 allowed expressions like `TimeSpan()`. (Note that the .NET `TimeSpan` class **does not**
have a default constructor.) This expression is no longer supported. Instead, one must supply an argument (typically
 zero (0)) to the constructor or to methods like `TimeSpan.FromTicks()`.""")

pretty_print_with_error(lambda: TimeSpan(), TypeError, '`TimeSpan()`')

pretty_print_net_item_with_header(TimeSpan(8801), 'TimeSpan(8801)')
pretty_print_net_item_with_header(TimeSpan(0), 'TimeSpan(0)')
pretty_print_net_item_with_header(TimeSpan.FromTicks(0), 'TimeSpan.FromTicks(0)')

wait_for_input()

section('2 Adding attributes with integer values requires conversion')

paragraph('(This issue occurred in **both** internal testing and low-level script testing and so is duplicated.)')

paragraph("""During integration testing, we discovered an issue setting an attribute with type, `Int32`, using a Python
`int` value of 7. The run-time reported that the types, `Int32` and `PyInt` were incompatible.""")

paragraph("""This scenario requires significant set up.""")

wait_for_input()

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

# Add attribute with value, 17, to stage 7, with Python `int` type.
with (orchid.dot_net_disposable.disposable(stage_7.dom_object.ToMutable())) as mutable_stage:
    # This action will fail because the attribute type is `System.Int32`
    # and `pythonnet-3.0.0.post1` **does not** implicitly equate these two types.
    pretty_print_with_error(lambda: mutable_stage.SetAttribute(attribute_to_add, int), ArgumentException,
                            'mutable_stage.SetAttribute(attribute_to_add, int)')

wait_for_input()

paragraph("""Using Python.NET 3, one must **explicitly** convert the supplied `int` to `Int32`.""")

# Add attribute to stage 7 with a value of 17 **explicitly** converted to an `Int32`
with (orchid.dot_net_disposable.disposable(stage_7.dom_object.ToMutable())) as mutable_stage:
    pretty_print_with_header(mutable_stage.SetAttribute(attribute_to_add, attribute_to_add_type(7)),
                             'mutable_stage.SetAttribute(attribute_to_add, attribute_to_add_type(7)')

paragraph("""Verify the added attribute value.""")

# Verify added attribute value
ignored_object = object()
is_attribute_present, actual_attribute_value = stage_7.dom_object.TryGetAttributeValue(attribute_to_add,
                                                                                       ignored_object)
pretty_print_with_header(is_attribute_present, 'is_attribute_present')
pretty_print_with_header(type(actual_attribute_value) == int, 'type(actual_attribute_value) == int')
pretty_print_with_header(actual_attribute_value == 7, 'actual_attribute_value == 7')

wait_for_input()

section('3 Disabled implicit conversion from C# Enums to Python `int` and back')

sub_section('3.1 Reduced need for and changed behavior of `Overloads` (`__overloads__` in Python.NET 3)')

paragraph("""The .NET `DateTime` class has many overloaded constructors. Because version Python.NET 2.5.2 converted 
members of .NET Enum types into Python `int` values, the method resolution process could not distinguish between the 
`DateTime` constructor taking 7 `System.Int32` arguments (the last specifying milliseconds) and the constructor 
accepting 6 `System.Int32` values and a `DateTimeKind` member. Consequently, a developer of the Orchid Python API had 
to specify an overload in order to invoke the appropriate constructor.""")

wait_for_input()

paragraph("""Under Python 2.5.2, one used the `Overloads` attribute to select a specific overload. Additionally, the
`Overloads` attribute could be queried to return a `list` of available overloads.

Under Python 3, querying the `__overloads__` (preferred but `Overloads` is also available) produces an unexpected 
result.""")

pretty_print_with_header((DateTime.__overloads__, DateTime.Overloads), '`DateTime.__overloads__, DateTime.Overloads`')

paragraph("""Our working hypothesis is that the Python.NET method resolution algorithm could find any overloads for the 
constructor and, therefore, produces this behavior. 

Additionally, we did create a issue with the Python.NET team. In the response to our issue, the Python.NET team 
indicated that `__overloads__` was not an attribute but a [property](https://realpython.com/python-property/).""")

pretty_print_with_header(DateTime.__overloads__, 'DateTime.__overloads__')

wait_for_input()

sub_section('3.2 .NET Enum members are no longer converted to Python `int` values')

paragraph("""Python.NET 2.5.2 implicitly converted .NET `Enum` members to Python `int` values. Python.NET 3 exposes 
the (derived) .NET `Enum` type to Python.""")

pretty_print_with_header(type(DateTimeKind.Utc), 'type(DateTimeKind.Utc)')

pretty_print_with_header(dir(DateTimeKind.Utc), 'dir(DateTimeKind.Utc)')

pretty_print_with_header(DateTimeKind.Utc.GetType(), 'DateTimeKind.Utc.GetType()')

wait_for_input()

pretty_print_with_header(dir(DateTimeKind.Utc.GetType()), 'dir(DateTimeKind.Utc.GetType())', max_lines=10)

pretty_print_with_header(DateTimeKind.Utc.GetType().BaseType, 'DateTimeKind.Utc.GetType().BaseType')

pretty_print_with_header(DateTimeKind.Utc.GetType().BaseType.FullName, 'DateTimeKind.Utc.GetType().BaseType.FullName')

paragraph("""Because Python.NET 3 retains the .NET `Enum` member, Python.NET can then resolve the `DateTime` 
7-argument constructor with the `DateTimeKind` last argument without "help".""")

pretty_print_with_header(DateTime(2021, 12, 1, 12, 15, 37, DateTimeKind.Utc).ToString('o'),
                         'DateTime(2021, 12, 1, 12, 15, 37, DateTimeKind.Utc).ToString("o")')

wait_for_input()

sub_section('3.3 Eliminated need to inherit from Python `enum.IntEnum` for compatibility with .NET Enum types')

paragraph("""Version 2.5.2 of `pythonnet` converted values of type .NET Enum to Python `int` values. Consequently, 
to support easy comparisons between the .NET type, `Orchid.FractureDiagnostics.FormationConnectionType` and the Python
enumeration, `native_stage_adapter.ConnectionType`, we defined `native_stage_adapter.ConnectionType` to inherit from 
`enum.IntEnum`.  This base class is not needed in `pythonnet-3.0.0.post1` because the enumeration member 
`native_stage_adapter.ConnectionType.PLUG_AND_PERF`, defined to have a value of 
`Orchid.FractureDiagnostics.FormationConnectionType` is no longer of type `int` but is actually of type, 
`Orchid.FractureDiagnostics.FormationConnectionType`.""")

pretty_print_with_header(orchid.net_date_time.TimePointTimeZoneKind.UTC == 0,
                         'The expression, `orchid.net_date_time.TimePointTimeZoneKind.UTC == 0`, returned `True` '
                         'under Python.NET 2.5.2. Under Python.NET 3, this expression returns `False`')

pretty_print_with_header(orchid.native_stage_adapter.ConnectionType == 0,
                         'Similarly, the expression, `orchid.net_date_time.TimePointTimeZoneKind.UTC == 0`, '
                         'returned `True` under Python.NET 2.5.2. Under Python.NET 3, this expression returns `False`')


pretty_print_with_header(orchid.native_stage_adapter.FormationConnectionType,
                         'orchid.native_stage_adapter.FormationConnectionType')

pretty_print_with_header(orchid.native_stage_adapter.ConnectionType, 'orchid.native_stage_adapter.ConnectionType')

pretty_print_with_header(orchid.native_stage_adapter.ConnectionType.PLUG_AND_PERF,
                         'orchid.native_stage_adapter.ConnectionType.PLUG_AND_PERF')

pretty_print_with_header(orchid.native_stage_adapter.ConnectionType.OPEN_HOLE,
                         'orchid.native_stage_adapter.ConnectionType.OPEN_HOLE')

pretty_print_net_item_with_header(orchid.native_stage_adapter.ConnectionType.PLUG_AND_PERF.value,
                                  'orchid.native_stage_adapter.ConnectionType.PLUG_AND_PERF.value')

wait_for_input()

section('4 Return values from .NET methods that return an interface are now automatically wrapped in that interface')

print("""Under `pythonnet-2.5.2`, running the following `doctest` passes:

```
>>> start = pendulum.parse('2022-02-23T15:53:23Z')
>>> stop = pendulum.parse('2022-02-24T05:54:11Z')
>>> net_start = ndt.as_net_date_time(start)
>>> net_stop = ndt.as_net_date_time(stop)
>>> factory = create()
>>> date_time_offset_range = factory.CreateDateTimeOffsetRange(net_start, net_stop)
>>> (date_time_offset_range.Start.ToString('o'), date_time_offset_range.Stop.ToString('o'))
('2022-02-23T15:53:23.0000000+00:00', '2022-02-24T05:54:11.0000000+00:00')
```
""")

wait_for_input()

print("""When running the same `doctest` using `pythonnet-3.0.0.post1`, this code
encounters an unhandled exception:

```
Error
**********************************************************************
File "C:\src\orchid-python-api\orchid\net_fracture_diagnostics_factory.py", line ?, in net_fracture_diagnostics_factory.create
Failed example:
(date_time_offset_range.Start.ToString('o'), date_time_offset_range.Stop.ToString('o'))
Exception raised:
Traceback (most recent call last):
File "C:/Users/larry.jones/AppData/Local/JetBrains/Toolbox/apps/PyCharm-P/ch-0/222.4459.20/plugins/python/helpers/pycharm/docrunner.py", line 138, in __run
exec(compile(example.source, filename, "single",
File "<doctest net_fracture_diagnostics_factory.create[6]>", line 1, in <module>
(date_time_offset_range.Start.ToString('o'), date_time_offset_range.Stop.ToString('o'))
TypeError: No method matches given arguments for Object.ToString: (<class 'str'>)
```
""")

wait_for_input()

start = pendulum.parse('2022-02-23T15:53:23Z')
stop = pendulum.parse('2022-02-24T05:54:11Z')
net_start = orchid.net_date_time.as_net_date_time(start)
net_stop = orchid.net_date_time.as_net_date_time(stop)
factory = orchid.net_fracture_diagnostics_factory.create()

paragraph("""Under Python.NET 2.5.2, the type returned by 
`IFractureDiagnosticsFactory.CreateDateTimeOffsetRange(net_start, net_stop)` is the type of the Orchid object, 
`DateTimeOffsetRange`.""")

paragraph("""Under Python.NET 3, the returned type is an **interface**.""")

date_time_offset_range = factory.CreateDateTimeOffsetRange(net_start, net_stop)
pretty_print_with_header(type(date_time_offset_range), 'type(date_time_offset_range)')

paragraph("""The interface does not explicitly `IDateTimeOffsetRange.Start` (and `Stop`) to return a 
`DateTimeOffset`; instead, these methods return interfaces.""")

pretty_print_with_header(date_time_offset_range.Start.GetType().FullName,
                         'date_time_offset_range.Start.GetType().FullName')

pretty_print_with_header(type(date_time_offset_range.Start), 'type(date_time_offset_range.Start)')

net_range_start = date_time_offset_range.Start
# try:
#     net_range_start.ToString('o')
# except TypeError as te:
#     print(f'TypeError: {te}')
# #%%
# net_range_start.ToString()
# #%%
# net_range_start.ToString.__doc__
# #%%
# dir(DateTimeOffset)
# #%%
# net_date_time_offset = DateTimeOffset.UtcNow
# net_date_time_offset
# #%%
# str(net_date_time_offset)
# #%%
# repr(net_date_time_offset)
# #%%
# net_date_time_offset.ToString()
# #%%
# net_date_time_offset.ToString('o')
# #%%
# type(net_date_time_offset)
# #%%
# type(net_range_start)
# #%%
# net_range_start.GetType().FullName
# #%%
# dir(net_range_start.GetType())
# #%%
# [iface.FullName for iface in net_range_start.GetType().GetInterfaces()]
# #%%
# try:
#     error_net_range_start = Convert.ChangeType(date_time_offset_range, DateTimeOffset)
#     type(error_net_range_start)
# except InvalidCastException as ice:
#     print(f'InvalidCastException {ice}')
# #%%
# clr.AddReference('System.Globalization')
# # noinspection PyUnresolvedReferences,PyPackageRequirements
# from System.Globalization import DateTimeFormatInfo
# #%%
# dir(DateTimeFormatInfo)
# #%%
# try:
#     net_range_start.ToString(DateTimeFormatInfo.SortableDateTimePattern)
# except TypeError as nie:
#     print(f'TypeError: {nie}')
# #%%
# try:
#     orchid.net_date_time.as_date_time(net_range_start)
# except NotImplementedError:
#     print(f'NotImplementedError')
# #%%
# try:
#     (DateTimeOffset)(net_range_start)
# except TypeError as te:
#     print(f'TypeError: {te}')
# #%%
# a_date_time_offset = DateTimeOffset.UtcNow
# a_date_time_offset = net_range_start
# a_date_time_offset
# #%%
# dir(net_range_start)
# #%%
# type(date_time_offset_range)
# #%%
# dir(date_time_offset_range)
# #%%
# net_range_start.GetType().GetElementType()
# #%%
# net_range_start.GetType().GetInterface('DateTimeOffset')
# #%%
# try:
#     DateTimeOffset.GetType().IsInstanceOfType(net_range_start)
# except TypeError as te:
#     print(f'TypeError: {te}')
# #%%
# a_date_time_offset.GetType().IsInstanceOfType(net_range_start)
# #%%
# net_range_start.GetType().BaseType.FullName
# #%% md
# I have not been able to determine a mechanism to convert or cast the type of `IDateTimeOffsetRange.Start`
# (and `IDateTimeOffsetRange.Stop`) from `IComparable` "down" to the concrete type. Consequently, I will use the
# work around of simply invoking `Object.ToString()` and comparing.
# #%%
# date_time_offset_range.Start.ToString(), date_time_offset_range.Stop.ToString()
# #%% md
# After implementing the `ToString()` (no arguments) work around, I received a [response](https://github.com/pythonnet/pythonnet/issues/2034#issuecomment-1332728831) to the issue that I [posted](https://github.com/pythonnet/pythonnet/issues/2034):
#
#                                                                                                 > You can access `__implementation__` (codecs applied) or `__raw_implementaion__` (codecs not applied).
#
# This solution is a much better solution than my work around.
# #%%
# net_range_start.__implementation__
# #%%
# net_range_start.__raw_implementation__
#     #%%
# [o.__implementation__.ToString('o') for o in (date_time_offset_range.Start, date_time_offset_range.Stop)]
# #%%

wait_for_input()
