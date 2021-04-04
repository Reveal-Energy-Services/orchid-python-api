# Orchid Python API Release Notes

## Release notes for 2021.1.399

This release is the second production release of the Orchid Python API. This release changes the 
implementation of measurements to use the [pint](https://pint.readthedocs.io/en/stable/) package and adds
access to additional Orchid features.

### Resolved issues

- [GitHub issue 6](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/6)
- [GitHub issue 10](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/10)
- [GitHub issue 13](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/13)
- [GitHub issue 14](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/14)
- [GitHub issue 15](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/15)

### Features

- Project
  - Azimuth
  - Fluid density
  - Project bounds
  - Project center (and center location)
  - Monitors
- Well
  - Formation
  - Wellhead location
- Monitor
  - Name
  - Display name
  - Start time
  - Stop time
  - Time range (contains start and stop time)
- Examples
  - Volume to first response
  
Replace custom `Measurement` class with the features available in `pint`.

### Known issues

- [GitHub issue 16](https://github.com/Reveal-Energy-Services/orchid-python-api/issues)
  
  All monitor curves can be access indirectly via the `Project.monitor_curves()` method. The work-around for
  this issue is then to search for curves by with a matching name.
  
- [GitHub issue 17](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/17)

  The work-around is to search the iterable returned by Project.monitor_curves for a curve with the name of
  the monitor of interest. Because of issue #16, beware that this work around may not return all monitors
  with the name of interest.

## Release notes for 2020.4.690

This release is the first production release of the Orchid Python API. This release offers access to the
following Orchid features.

### Features

- General
  - Loading Orchid `.ifrac` files
- Project
  - Name
  - Project units
  - Wells
  - Default well colors
  - Monitor curves
  - Searching for wells by name
- Well
  - Name
  - Display name
  - Stages
  - Trajectory
  - UWI
- Stage
  - Cluster count
  - Display name with well
  - Display name without well
  - Display stage number
  - Global stage sequence number
  - Order of completion on well
  - Stage (formation connection) type
  - Start time
  - Stop time
  - Bottom location
  - Center location
    - In addition, to the subsurface point
      - Easting
      - Northing
      - Measured depth (MD)
      - Total vertical depth (TVD) relative to
        - Ground level
        - Seal level
      - XY (both easting and northing)
  - Cluster location
  - Instantaneous shut in pressure (ISIP)
  - Measured depth of stage top
  - Measured depth of stage bottom
  - Net pressure (PNet)
  - Minimum shear (ShMin)
  - Stage length
  - Top location
  - Treatment curves
- TimeSeries (monitor and treatment curves)
  - Name
  - Display name
  - Sampled quantity name
  - Sampled quantity unit
  - Time series
- Calculations
  - For treatment
    - Median treating pressure
    - Pumped fluid volume
    - Total proppant mass

### Known issues

- [GitHub issue 18](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/18)
  
  This issue is a deprecation warning from `matplotlib`. It began occurring after updating the package
  dependencies. We do not believe this error will affect customer code.
  
- [GitHub issue 14](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/14)

  The work-around for this issue is to configure the locations of both Orchid training data and the Orchid
  binaries.

- [GitHub issue 13](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/13)

  We believe that this warning is caused by the `pandas` package interacting with `numpy`, and plan to
  investigate this issue.

- [GitHub issue 12](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/12)
  
  Some versions of `numpy` encounter an issue with the `fmod` function on Windows. The current work-around
  fixes the version of `numpy` at 1.19.3.
  
- [GitHub issue 10](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/10)

  Although we have increased the scope of our internal testing to cover many more units of measure, we plan to
  implement the convenience function suggested by the author.
  
- [GitHub issue 6](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/6)

  This issue is an internal issues and currently has no effect on installation or usage of the API.

- [GitHub issue 3](https://github.com/Reveal-Energy-Services/orchid-python-api/issues/3)

  This issue may relate to `numpy` 1.19.1 (the version mentioned in the issue). We plan to retest against 
  `numpy` 1.19.3. We have had no other reports of this issue.
