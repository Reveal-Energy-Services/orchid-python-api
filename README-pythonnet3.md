# Python.NET 3 changes to the Orchid Python API

## Introduction 

This project defines the implementation of the Python API for Orchid*.

Specifically, the `orchid` package makes Orchid features available to Python applications and to the
Python REPL.

(* Orchid is a mark of Reveal Energy Services, Inc.)

This document focuses on a single aspect of that project. Changing from `pythonnet-2.5.2`  to
`pythonnet-3.0.0.post1` caused a number of previously passing tests to fail. This document 
describes the changes that we discovered that resulted in these failures.

## Changes needed to pass all developer tests

The Orchid Python API initially depended on 
version 2.5.2 of the Python.NET package. When we updated the package dependencies to use 
`pythonnet-3.0.0.post1`, we had to make a number of changes to repair issues uncovered by our tests.
This document describes the changes we made to repair these issue.

- Fewer .NET methods needed developer intervention to select a specific method overload.

  In `pythonnet-2.5.2`, a developer specified the overload by selecting it from the array returned by the `Overloads`
  property of the class. In `pythonnet-3.0.0.post1`, the preferred way to access overloads is via the `__overloads__` 
  property although the `Overloads` property is still available. In addition, the `__overloads__` / `Overloads` property 
  cryptically reports, "<unbound method `__init__`>" of type `CLR.MethodBinding`.
  
- No automatic conversion between .NET `Enum` and Python `int` types. 
  
  For example, the `System.DateTimeKind` is exposed to Python as type, `System.DateTimeKind`. This change, 
  in particular, helped reduce the need for developers to specify a .NET method overload.

## Examples

In addition to the previous descriptions, this release includes two additional files in the directory, 
`orchid_python_api\examples\pythonnet_3`. These files contain experiments run to understand the changes between 
`pythonnet-2.5.2` and `pythonnet-3.0.0.post1`:

- pn3_experiments.py
- pn3_experiments.ipynb
  