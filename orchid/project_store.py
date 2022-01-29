#  Copyright (c) 2017-2022 Reveal Energy Services, Inc 
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

import functools

import deal

from orchid import (
    dot_net,
    dot_net_disposable as dnd,
    script_adapter_context as sac,
    validation,
)

# noinspection PyUnresolvedReferences
from System import InvalidOperationException
# noinspection PyUnresolvedReferences
from System.IO import (FileStream, FileMode, FileAccess, FileShare)
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import (
    PythonTimesSeriesArraysDto,
    ScriptAdapter,
)
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.TimeSeries import IQuantityTimeSeries

# To support doctests only
import json
import zipfile
import orchid  # to support doctests only


class OrchidError(Exception):
    pass


def as_python_time_series_arrays(native_time_series: IQuantityTimeSeries):
    """
    Calculate the Python time series arrays equivalent to the `native_time_series` samples.
    Args:
        native_time_series: The native time series whose samples are sought.

    Returns:
        A `PythonTimeSeriesArraysDto` containing two arrays:
        - Sample magnitudes
        - Unix time stamps in seconds
    """
    with sac.ScriptAdapterContext():
        result = ScriptAdapter.AsPythonTimeSeriesArrays(native_time_series)
    return result


@functools.lru_cache()
def native_treatment_calculations():
    """
    Returns a .NET ITreatmentCalculations instance to be adapted.

    Returns:
            An `ITreatmentCalculations` implementation.
    """
    with sac.ScriptAdapterContext():
        result = ScriptAdapter.CreateTreatmentCalculations()
    return result


class ProjectStore:
    """Provides an .NET IProject to be adapted."""

    @deal.pre(validation.arg_not_none)
    @deal.pre(validation.arg_neither_empty_nor_all_whitespace)
    def __init__(self, project_pathname: str):
        """
        Construct an instance that loads project data from project_pathname

        Args:
            project_pathname: Identifies the data file for the project of interest.
        """
        self._project_pathname = project_pathname
        self._project = None
        self._in_context = False

    def native_project(self):
        """
        Return the native (.NET) Orchid project.

        Returns:
            The loaded `IProject`.
        """
        if not self._project:
            self.load_project()
        return self._project

    def load_project(self):
        """
        Load a project from the path, `self._project_pathname`.

        >>> load_path = orchid.training_data_path().joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')
        >>> loaded_project = orchid.load_project(str(load_path))
        >>> loaded_project.name
        'frankNstein_Bakken_UTM13_FEET'
        """
        with sac.ScriptAdapterContext():
            reader = ScriptAdapter.CreateProjectFileReader(dot_net.app_settings_path())
            # TODO: These arguments are *copied* from `ProjectFileReaderWriterV2`
            stream_reader = FileStream(self._project_pathname, FileMode.Open, FileAccess.Read, FileShare.Read)
            try:
                self._project = reader.Read(stream_reader)
            finally:
                stream_reader.Close()

    def save_project(self, project):
        """
        Save the specified project to `self._project_pathname`.

        >>> load_path = orchid.training_data_path().joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')
        >>> loaded_project = orchid.load_project(str(load_path))
        >>> # TODO: move this code to the property eventually, I think.
        >>> with (dnd.disposable(loaded_project.dom_object.ToMutable())) as mnp:
        ...     mnp.Name = 'nomen mutatum'
        >>> save_path = load_path.with_name(f'{loaded_project.name}{load_path.suffix}')
        >>> orchid.save_project(loaded_project, str(save_path))
        >>> save_path.exists()
        True
        >>> with zipfile.ZipFile(save_path) as archive:
        ...     content = json.loads(archive.read('project.json'))
        ...     content['Object']['Name']
        'nomen mutatum'

        Args:
            project: The project to be saved.
        """
        with sac.ScriptAdapterContext():
            writer = ScriptAdapter.CreateProjectFileWriter()
            use_binary_format = False
            writer.Write(project.dom_object, str(self._project_pathname), use_binary_format)
        self._project = project


if __name__ == '__main__':
    import doctest
    doctest.testmod()
