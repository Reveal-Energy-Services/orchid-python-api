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
        self._native_project = None
        self._in_context = False

    def native_project(self):
        """
        Return the native (.NET) Orchid project.

        Returns:
            The loaded `IProject`.
        """
        if self._native_project is None:
            self.load_project()
        return self._native_project

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
            try:
                self._native_project = reader.Read(self._project_pathname)
            except:
                raise

    def save_project(self, project):
        """
        Save the specified project to `self._project_pathname`.

        >>> # Test saving changed project
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
        >>> # Test side_effect of `save_project`: `native_project` returns project that was saved
        >>> # I do not expect end users to utilize this side-effect.
        >>> # TODO: Because this code tests a side-effect, an actual unit test might be better.
        >>> load_path = orchid.training_data_path().joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')
        >>> to_save_project = orchid.load_project(str(load_path))
        >>> # TODO: move this code to the property eventually, I think.
        >>> with (dnd.disposable(to_save_project.dom_object.ToMutable())) as mnp:
        ...     mnp.Name = 'mutatio project'
        >>> save_path = load_path.with_name(f'{to_save_project.name}{load_path.suffix}')
        >>> save_store = ProjectStore(str(save_path))
        >>> save_store.save_project(to_save_project)
        >>> to_save_project.dom_object == save_store.native_project()
        True

        Args:
            project: The project to be saved.
        """
        with sac.ScriptAdapterContext():
            writer = ScriptAdapter.CreateProjectFileWriter()
            use_binary_format = False
            writer.Write(project.dom_object, str(self._project_pathname), use_binary_format)
        self._native_project = project.dom_object

    def optimized_but_possibly_unsafe_save(self, project, to_pathname):
        """
        Saves `project` `to_pathname` is an optimized, but possibly "unsafe" manner.

        This method is unsafe because it only writes some data from `project`; the remainder of the data is simply
        (bulk) copied from the `project_pathname` supplied to the constructor.

        This method assumes that `project` was originally loaded from `project_pathname` and was then changed in
        such a way that the "bulk" data **was not** changed. If this assumption is not true, the project saved in
        `to_pathname` will **not** contain all the changes to `project`.

        Specifically, this method **does not** save changes to data like:

        - Trajectories
        - Treatment curves
        - Monitor curves

        We believe that this method will generally finish more quickly than `save_project`; however, we cannot
        guarantee this behavior. We encourage the developer calling this method to perform her own performance tests
        and to understand if his use case meets the assumptions made by this method.

        >>> # Test saving changed project
        >>> load_path = orchid.training_data_path().joinpath('Project_frankNstein_Permian_UTM13_FEET.ifrac')
        >>> loaded_project = orchid.load_project(str(load_path))
        >>> # TODO: move this code to the property eventually, I think.
        >>> with (dnd.disposable(loaded_project.dom_object.ToMutable())) as mnp:
        ...     mnp.Name = 'nomen mutatum'
        >>> save_path = load_path.with_name(f'{loaded_project.name}{load_path.suffix}')
        >>> store = ProjectStore(str(load_path))
        >>> store.optimized_but_possibly_unsafe_save(loaded_project, str(save_path))
        >>> save_path.exists()
        True
        >>> with zipfile.ZipFile(save_path) as archive:
        ...     content = json.loads(archive.read('project.json'))
        ...     content['Object']['Name']
        'nomen mutatum'
        >>> # Test side_effect of `save_project`: `native_project` returns project that was saved
        >>> # I do not expect end users to utilize this side-effect.
        >>> # TODO: Because this code tests a side-effect, an actual unit test might be better.
        >>> load_path = orchid.training_data_path().joinpath('Project_frankNstein_Permian_UTM13_FEET.ifrac')
        >>> source_project = orchid.load_project(str(load_path))
        >>> # TODO: move this code to the property eventually, I think.
        >>> with (dnd.disposable(source_project.dom_object.ToMutable())) as mnp:
        ...     mnp.Name = 'mutatio project'
        >>> save_path = load_path.with_name(f'{source_project.name}{load_path.suffix}')
        >>> save_store = ProjectStore(str(save_path))
        >>> save_store.optimized_but_possibly_unsafe_save(source_project, str(save_path))
        >>> source_project.dom_object == save_store.native_project()
        True

        Args:
            project: The project to be saved.
            to_pathname: The "target" pathname for the newly saved data.

            Note that this pathname **cannot** refer to the same pathname as the "source pathname" supplied to the
            class constructor.
        """
        with sac.ScriptAdapterContext():
            writer = ScriptAdapter.CreateProjectFileWriter()
            use_binary_format = False
            writer.Write(project.dom_object, str(self._project_pathname), to_pathname, use_binary_format)
        self._native_project = project.dom_object


if __name__ == '__main__':
    import doctest
    doctest.testmod()
