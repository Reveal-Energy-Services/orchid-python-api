# -*- coding: utf-8 -*-

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


import deal

from orchid.project import Project
from orchid.project_store import ProjectStore

# To support doctests only
import orchid


# TODO: change `ifrac_pathname` to be `str` or `pathlib.Path`
@deal.pre(lambda ifrac_pathname: len(ifrac_pathname.strip()) != 0)
@deal.pre(lambda ifrac_pathname: ifrac_pathname is not None)
def load_project(ifrac_pathname: str) -> Project:
    """
    Return the project for the specified `.ifrac` file.

    Args:
        ifrac_pathname: The path identifying the data file of the project of interest.

    Returns:
        The project of interest.

    Examples:
        >>> load_path = orchid.training_data_path().joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')
        >>> loaded_project = orchid.load_project(str(load_path))
        >>> loaded_project.name
        'frankNstein_Bakken_UTM13_FEET'
    """
    loader = ProjectStore(ifrac_pathname.strip())
    result = Project(loader)
    return result


# TODO: change `ifrac_pathname` to be `str` or `pathlib.Path`
@deal.pre(lambda project, _: project is not None)
@deal.pre(lambda _, ifrac_pathname: ifrac_pathname is not None)
@deal.pre(lambda _, ifrac_pathname: len(ifrac_pathname) != 0)
@deal.pre(lambda _, ifrac_pathname: len(ifrac_pathname.strip()) != 0)
def save_project(project: Project, ifrac_pathname: str) -> None:
    """
    Return the project for the specified `.ifrac` file.

    Args:
        ifrac_pathname: The path identifying the data file of the project of interest.
        project: The project of interest.

    Examples:
        >>> # Test saving changed project
        >>> load_path = orchid.training_data_path().joinpath('frankNstein_Bakken_UTM13_FEET.ifrac')
        >>> loaded_project = orchid.load_project(str(load_path))
        >>> save_path = load_path.with_name(f'salvus{load_path.suffix}')
        >>> orchid.save_project(loaded_project, str(save_path))
        >>> save_path.exists()
        True
    """

    store = ProjectStore(ifrac_pathname.strip())
    store.save_project(project)
