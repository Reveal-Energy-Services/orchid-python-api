#
# This file is part of IMAGEFrac (R) and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# IMAGEFrac contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities
# except under appropriate precautions to maintain the confidentiality hereof,
# and may not be used in any way not expressly authorized by the Company.
#

"""A module for creating 'stub" .NET classes for use in testing.

Note that these stubs are "duck typing" stubs for .NET classes; that is, they have the same methods and
properties required during testing but do not actually implement the .NET class interfaces.
"""

import datetime
import unittest.mock
from typing import Sequence

# TODO: Remove the clr dependency and spec's using .NET types if tests too slow
# To mitigate risks of tests continuing to pass if the .NET types change, I have chosen to add arguments like
# `spec=IProject` to a number of `MagicMock` calls. As explained in the documentation, these specs cause the
# mocks to fail if a mocked method *does not* adhere to the interface exposed by the type used for the spec
# (in this case, `IProject`).
#
# A consequence of this choice is a noticeable slowing of the tests (hypothesized to result from loading the
# .NET assemblies and reflecting on the .NET types to determine correct names). Before this change, this
# author noticed that tests were almost instantaneous (11 tests). Afterwards, a slight, but noticeable pause
# occurs before the tests complete.
#
# If these slowdowns become "too expensive," our future selves will need to remove dependencies on the clr
# and the .NET types used for specs.


# TODO: Replace some of this code with configuration and/or a method to use `clr.AddReference`
import sys
import clr
IMAGE_FRAC_ASSEMBLIES_DIR = r'c:/src/OrchidApp/ImageFrac/ImageFrac.Application/bin/Debug'
if IMAGE_FRAC_ASSEMBLIES_DIR not in sys.path:
    sys.path.append(IMAGE_FRAC_ASSEMBLIES_DIR)

# noinspection PyUnresolvedReferences
from System import DateTime

clr.AddReference('ImageFrac.FractureDiagnostics')
# noinspection PyUnresolvedReferences
from ImageFrac.FractureDiagnostics import IProject, IWell, IStage

clr.AddReference('UnitsNet')
# noinspection PyUnresolvedReferences
import UnitsNet


class StubNetSample:
    def __init__(self, time_point: datetime.datetime, value: float):
        # I chose to use capitalized names for compatability with .NET
        self.Timestamp = DateTime(time_point.year, time_point.month, time_point.day, time_point.hour,
                                  time_point.minute, time_point.second)
        self.Value = value


def create_30_second_time_points(start_time_point: datetime.datetime, count: int):
    """
    Create a sequence of `count` time points, 30-seconds apart.
    :param start_time_point: The starting time point of the sequence.
    :param count: The number of time points in the sequence.
    :return: The sequence of time points.
    """
    return [start_time_point + i * datetime.timedelta(seconds=30) for i in range(count)]


def create_stub_net_time_series(start_time_point: datetime, sample_values) -> Sequence[StubNetSample]:
    """
    Create a stub .NET time series.

    The "stub .NET" nature is satisfied by returning a sequence in which each item is an instance of `StubNetSample`.

    :param start_time_point: The time point at which the time series starts.
    :param sample_values: The values in the stub samples.
    :return: A sequence a samples implementing the `ITick<double>` interface using "duck typing."
    """
    sample_time_points = create_30_second_time_points(start_time_point, len(sample_values))
    samples = [StubNetSample(st, sv) for (st, sv) in zip(sample_time_points, sample_values)]
    return samples


class StubNetTreatmentCurve:
    def __init__(self, curve_name, curve_quantity, time_series):
        self._time_series = time_series
        self.SampledQuantityName = curve_name
        if curve_quantity == 'pressure':
            self.SampledQuantityType = UnitsNet.QuantityType.Pressure
        elif curve_quantity == 'ratio':
            self.SampledQuantityType = UnitsNet.QuantityType.Ratio

    # noinspection PyPep8Naming
    def GetOrderedTimeSeriesHistory(self):
        return self._time_series


def create_net_treatment(start_time_point, treating_pressure_values, rate_values, concentration_values):
    treating_pressure_time_series = create_stub_net_time_series(start_time_point, treating_pressure_values)
    treating_pressure_curve = StubNetTreatmentCurve('Pressure', 'pressure', treating_pressure_time_series)
    rate_time_series = create_stub_net_time_series(start_time_point, rate_values)
    rate_curve = StubNetTreatmentCurve('Slurry Rate', 'ratio', rate_time_series)
    concentration_time_series = create_stub_net_time_series(start_time_point, concentration_values)
    concentration_curve = StubNetTreatmentCurve('Proppant Concentration', 'ratio', concentration_time_series)

    return [treating_pressure_curve, rate_curve, concentration_curve]


def create_stub_stage(stage_no, treatment_curves):
    result = unittest.mock.MagicMock(name=stage_no, spec=IStage)
    result.DisplayStageNumber = stage_no
    result.TreatmentCurves.Items = treatment_curves

    return result


def quantity_coordinate(raw_coordinates, i, stub_net_project):
    result = [UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(c), stub_net_project.ProjectUnits.LengthUnit)
              for c in raw_coordinates[i]] if raw_coordinates else []
    return result


def create_stub_net_project(project_length_unit_abbreviation='', well_names=None, well_display_names=None, uwis=None,
                            eastings=None, northings=None, tvds=None, about_stages=None):
    well_names = well_names if well_names else []
    well_display_names = well_display_names if well_display_names else []
    uwis = uwis if uwis else []
    eastings = eastings if eastings else []
    northings = northings if northings else []
    tvds = tvds if tvds else []
    about_stages = about_stages if about_stages else []

    stub_net_project = unittest.mock.MagicMock(name='stub_net_project', spec=IProject)
    if project_length_unit_abbreviation == 'ft':
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Foot
    elif project_length_unit_abbreviation == 'm':
        stub_net_project.ProjectUnits.LengthUnit = UnitsNet.Units.LengthUnit.Meter

    stub_net_project.Wells.Items = [unittest.mock.MagicMock(name=well_name, spec=IWell) for well_name in well_names]

    for i in range(len(well_names)):
        stub_well = stub_net_project.Wells.Items[i]
        stub_well.Uwi = uwis[i] if uwis else None
        stub_well.DisplayName = well_display_names[i] if well_display_names else None
        stub_well.Name = well_names[i]

        # The Pythonnet package has an open issue that the "Implicit Operator does not work from python"
        # (https://github.com/pythonnet/pythonnet/issues/253).
        #
        # One of the comments identifies a work-around from StackOverflow
        # (https://stackoverflow.com/questions/11544056/how-to-cast-implicitly-on-a-reflected-method-call/11563904).
        # This post states that "the trick is to realize that the compiler creates a special static method
        # called `op_Implicit` for your implicit conversion operator."
        stub_well.Trajectory.GetEastingArray.return_value = quantity_coordinate(eastings, i, stub_net_project)
        stub_well.Trajectory.GetNorthingArray.return_value = quantity_coordinate(northings, i, stub_net_project)
        stub_well.Trajectory.GetTvdArray.return_value = quantity_coordinate(tvds, i, stub_net_project)

        stub_well.Stages.Items = [create_stub_stage(stage_no, treatment_curves)
                                  for (stage_no, treatment_curves) in about_stages]

    return stub_net_project
