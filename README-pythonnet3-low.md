# Python.NET 3 changes to the Orchid Python API

## Introduction 

This project defines the implementation of the Python API for Orchid*.

Specifically, the `orchid` package makes Orchid features available to Python applications and to the
Python REPL.

(* Orchid is a mark of Reveal Energy Services, Inc.)

This document focuses on a single aspect of that project. Changing from `pythonnet-2.5.2`  to
`pythonnet-3.0.0.post1` caused a number of previously passing tests to fail. This document 
describes the changes that we discovered that resulted in these failures in our low-level examples.

## Changes to low-level examples

Unfortunately, our low-level examples seems to result in more errors when we upgrade `pythonnet` from 2.5.2 to 
3.0.0.post1. 

### Load a targeted runtime must occur before calling `import clr`

The package `pythonnet-3.0.0.post1` supports targeting 3 different runtimes:

- .NET Framework 4.7.2 and above
- .NET Core
- Mono

Targeting these different runtimes is good, but it requires loading the correct runtime **before** executing the 
statement, `import clr`. Further, once the system has loaded a runtime, attempting to load the runtime again results
in the `pythonnet` package raising an exception:

"""
Failed to initialize pythonnet: System.InvalidOperationException: This property must be set before runtime is initialized
   at Python.Runtime.Runtime.set_PythonDLL(String value)
   at Python.Runtime.Loader.Initialize(IntPtr data, Int32 size)
   at Python.Runtime.Runtime.set_PythonDLL(String value)
   at Python.Runtime.Loader.Initialize(IntPtr data, Int32 size)Traceback (most recent call last):
  File "auto_pick.py", line 21, in <module>
    import orchid
  File "C:\src\orchid-python-api\orchid\__init__.py", line 21, in <module>
    pythonnet.load('netfx')
  File "C:\Users\larry.jones\AppData\Local\pypoetry\Cache\virtualenvs\orchid-python-api-WYNzmHwi-py3.8\lib\site-packages\pythonnet\__init__.py", line 144, in load
    raise RuntimeError("Failed to initialize Python.Runtime.dll")
RuntimeError: Failed to initialize Python.Runtime.dll
"""

We have written the `orchid` module in execute the statement `pythonnet.load('netfx')` to load the runtime expected
by the Orchid Python API; consequently, the simplest solution to this issue is to arrange your imports to execute
`import orchid`, even if not otherwise needed, **before** executing `import clr`

### Again, fewer implicit conversions of Python types to .NET `Types`

Python (and `pythonnet-2.5.2`) allow a developer to pass an `int` to a function that expects a `System.Boolean`. 

`pythonnet-3.0.0.post1` does not perform the typical conversion expected by a Python developer; specifically, the value 
zero (0) is converted to `False` and any other `int` value is converted to `True`.

Because of this issue the `auto_pick.py` low-level example (and its related `auto_pick...py` scripts) fail with the 
following stack trace:

"""
Python.Runtime.PythonException: 'int' value cannot be converted to System.Boolean

The above exception was the direct cause of the following exception:

System.ArgumentException: 'int' value cannot be converted to System.Boolean in method Double[] Interpolate(Double[], Boolean) ---> Python.Runtime.PythonException: 'int' value cannot be converted to System.Boolean

System.AggregateException: One or more errors occurred. ---> System.ArgumentException: 'int' value cannot be converted to System.Boolean in method Double[] Interpolate(Double[], Boolean) ---> Python.Runtime.PythonException: 'int' value cannot be converted to System.Boolean
   --- End of inner exception stack trace ---
   --- End of inner exception stack trace ---
---> (Inner Exception #0) System.ArgumentException: 'int' value cannot be converted to System.Boolean in method Double[] Interpolate(Double[], Boolean) ---> Python.Runtime.PythonException: 'int' value cannot be converted to System.Boolean
   --- End of inner exception stack trace ---<---

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "auto_pick.py", line 354, in <module>
    main(args)
  File "auto_pick.py", line 294, in main
    auto_pick_observations(native_project, native_monitor)
  File "auto_pick.py", line 259, in auto_pick_observations
    picked_observation = auto_pick_observation_details(unpicked_observation, native_monitor, part)
  File "auto_pick.py", line 217, in auto_pick_observation_details
    control_point_times = calculate_leak_off_control_point_times(leak_off_curve_times['L1'],
  File "auto_pick.py", line 93, in calculate_leak_off_control_point_times
    pressure_values = time_series_interpolant.Interpolate(time_series_interpolation_points, 0)
TypeError: No method matches given arguments for IInterpolant1D.Interpolate: (<class 'System.Double[]'>, <class 'int'>)
"""

To address this issue, a Python developer using `pythonnet-3.0.0.post1` should either supply a literal `False` or 
perform the explicit conversion, `bool(int)`.

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

## Examples

In addition to the previous descriptions, this release includes two additional files in the directory, 
`orchid_python_api\examples\pythonnet_3`. These files contain experiments run to understand the changes between 
`pythonnet-2.5.2` and `pythonnet-3.0.0.post1`:

- pn3_experiments.py
- pn3_experiments.ipynb
  