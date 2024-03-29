# Python.NET 3 changes to the Orchid Python API

## Introduction 

This project defines the implementation of the Python API for Orchid*.

Specifically, the `orchid` package makes Orchid features available to Python applications and to the
Python REPL.

(* Orchid is a mark of KAPPA)

This document focuses on a single aspect of that project. Changing from `pythonnet-2.5.2`  to
`pythonnet-3.0.0.post1` caused a number of previously passing tests to fail. This document 
describes the changes that we discovered that resulted in these failures in our internal tests.

## Changes needed to pass all developer tests

The Orchid Python API initially depended on 
version 2.5.2 of the Python.NET package. When we updated the package dependencies to use 
`pythonnet-3.0.0.post1`, we had to make a number of changes to repair issues uncovered by our tests.
This document describes the changes we made to repair these issue.

### Fewer .NET methods need a developer to select a specific method overload

In `pythonnet-2.5.2`, a developer specified the overload by selecting it from the array returned by the `Overloads`
property of the class. In `pythonnet-3.0.0.post1`, the preferred way to access overloads is via the `__overloads__` 
property although the `Overloads` property is still available. In addition, the `__overloads__` / `Overloads` property 
cryptically reports, "<unbound method `__init__`>" of type `CLR.MethodBinding`.
  
### No automatic conversion between .NET `Enum` and Python `int` types 
  
For example, the `System.DateTimeKind` is exposed to Python as type, `System.DateTimeKind`. This change, 
in particular, helped reduce the need for developers to specify a .NET method overload.

### Equality with .NET objects (and _implicit_ conversions)

Using `pythonnet-2.5.2`, expressions like:

- `108 == DateTime.MaxValue`
- `108 == TimeSpan.MaxValue`
- `108 == TimeSpan.MinValue`

all returned `False`. In `pythonnet-3.0.0.post1`, these expressions now raise an exception, 
"TypeError: No method matches given arguments for TimeSpan.op_Equality: (<class 'int'>)". This author filed a "bug"
with the Python.NET team; however, the team eventually state:

"""
Yes, we tried to limit the "implicit" conversions to a minimum. I don't even know, which change in particular is
responsible for the behavioural change fix that you are observing here, but you are only able to compare things to a
.NET object that are directly convertible to it. If you'd really require this for `DateTimeOffset` and `TimeSpan`,
you could make them convertible via a Codec. Otherwise, I'd suggest you just generate the respective comparison
values using `.FromTicks`.
"""

### Default constructors for TimeSpan

The package, `pythonnet-2.5.2` allowed expressions like `TimeSpan()` even though no default constructor is documented
for the .NET `TimeSpan` class. In `pythonnet-3.0.0.post`, this expression raises an exception, 
`TypeError: No method matches given arguments for TimeSpan..ctor: ()`

The fix is to explicitly supply zero (0 - an `int` argument). An alternative is to invoke an explicit method like 
`TimeSpan.FromTicks`.

### Fewer implicit conversions from `int` to `System.Int32`

When adding attribute values to a stage, `pythonnet-2.5.2` supported an implicit conversion between a Python `int` and  
a `System.Int32`. The updated package, `pythonnet-3.0.0.post1`, raises a .NET `ArgumentException` indicating that the 
attribute expected a value of type, `System.Int32`, but it received a value of `PyInt`.

To repair this error, I needed to **explicitly** convert the Python `int` value to `System.Int32` before invoking the 
`IMutableStage.SetAttribute()` method.

### .NET Enum members no longer converted to Python `int`

Version 2.5.2 of `pythonnet` return values of `int` type when exposing .NET `Enum` members to Python. For example, in 
2.5.2, `System.DateTimeKind.Utc` was zero (0). Similarly, `Orchid.FractureDiagnostics.FormationConnectionType.OpenHole`
was 3. 

However, version 3.0.0.post1 of `pythonnet` returns the .NET Enum member itself. So, both `System.DateTimeKind.Utc` and
`Orchid.FractureDiagnostics.FormationConnectionType` return themselves. 

In most situations, this change does not cause any behavior change in the Orchid Python API implementation. However,
the **Python** enumeration, three Python enumerations defined its members as the **integral** value of the 
corresponding .NET Enum type.

- `native_stage_adapter.ConnectionType`
- `reference_origins.WellReferenceFrameXy`
- `reference_origins.DepthDatum`

In addition, other parts of the Orchid Python API implementation tested for equality of the converted `int` value of
the .NET Enum to the Python enumeration members whose value was also of type `int`. In `pythonnet-3.0.0.post1`, this
comparison returned `False`. 

To correct these issue, we changed the base class of the three Python enumerations from `enum.IntEnum` to `enum.Enum`. 
In addition, we needed to change any comparisons involving the types to use the Python enumeration member `value`.

In addition, if you are unfamiliar with the Python `enum` module (the author was), read about it in 
[the standard library](https://docs.python.org/3.8/library/enum.html).

### `DateTimeOffset` returned by `IDateTimeOffsetRange.Start` does not support `ToString(string)`

The following doctest in `net_fracture_diagnostics_factory` passes in `pythonnet-2.5.2`:

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

However, when run using `pythonnet-3.0.0.post1`, this same doctest fails with the exception

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

Investigating this issue, I discovered that `IFractureDiagnosticsFactory.CreateDateTimeOffsetRange()` returns an
instance of `IDateTimeOffsetRange`; however, both `IDateTimeOffsetRange.Start` and `IDateTimeOffsetRange.Stop` return
values of instance `IComparable`. (Because, I think, of the base interface, `IRange`. Even though the derived generic
interface, `IRange<T>`, is instantiated concretely as `IRange<DateTimeOffset>`, because `IRange<T>.Start` is a property
that returns an argument of type, `T`, it only appears as a single property at runtime.)

I have created [bug #2034](https://github.com/pythonnet/pythonnet/issues/2034). 
[This response](https://github.com/pythonnet/pythonnet/issues/2034#issuecomment-1332728831) indicates that the behavior
is as designed. The document `CHANGELOG.md`, searching for "BREAKING" changes, confirms that using either 
`__implementation__` or `__raw_implementation__` is the solution.

## Examples

In addition to the previous descriptions, this release includes two additional files in the directory, 
`orchid_python_api\examples\pythonnet3`. These files contain experiments run to understand the changes between 
`pythonnet-2.5.2` and `pythonnet-3.0.0.post1` related to internal tests:

- internal_tests.py
- internal_tests.ipynb
  