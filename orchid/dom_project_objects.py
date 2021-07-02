#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

from typing import Callable, Iterator, Optional
import uuid

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IProjectObject

"""
Provides a common interface to collections of `IProjectObject` instances. These collections provide methods to:

- Query for all object IDs identifying instances in this collection
- Query for the name of all instances in this collection
- Query for the display name of all instances in this collection
- Search for a single instance by object ID
- Search for all instances with a specified name
- Search for all instances with a specified display name

Here are the DOM objects that may be collections:
- Data frames
- Monitors
- Stages
- Well trajectory
- Wells

This objects are all derived from `IProjectObject`. The corresponding instances in the Python API all derive from 
`poa.NativeProjectObjectAdapter` (TODO: to be created).
"""


import toolz.curried as toolz


class ProjectObjects:
    def __init__(self, make_adapter: Callable, net_project_objects: Iterator[IProjectObject]):
        """
        Construct a collection of project objects created my `make_adapter` using the arguments, `net_project_objects`.
        Args:
            make_adapter: The callable that constructs adapter instances using `net_project_objects`.
            net_project_objects: The sequence of .NET `IProjectObject` instances adapted by the Python API.
        """
        self._collection = toolz.pipe(
            net_project_objects,
            toolz.map(lambda kwargs: make_adapter(**kwargs)),
            toolz.map(lambda dom_object: (dom_object.object_id, dom_object)),
            dict,
        )

    def __len__(self):
        """
        Return the number of items in this collection.

        Returns:
            The number of items in this collection.
        """
        return len(self._collection)

    def all_display_names(self) -> Iterator[str]:
        """
        Return an iterator over all the display names of project objects in this collection.

        Returns:
            An iterator over all the display names of project objects in this collection.
        """
        return toolz.map(lambda po: po.display_name, self._collection.values())

    def all_names(self) -> Iterator[str]:
        """
        Return an iterator over all the names of project objects in this collection.

        Returns:
            An iterator over all the names of project objects in this collection.
        """
        return toolz.map(lambda po: po.name, self._collection.values())

    def all_object_ids(self) -> Iterator[uuid.UUID]:
        """
        Return an iterator over all the object IDs of project objects in this collection.

        Returns:
            An iterator over all the object IDs of project objects in this collection.
        """
        return self._collection.keys()

    def find_by_display_name(self, display_name_to_find: str) -> Iterator:
        """
        Return an iterator over all project objects whose `display_name` is the `display_name_to_find`.

        Args:
            display_name_to_find: The display name for all project objects of interest.

        Returns:
            An iterator over all project objects with the specified `display_name` property.
        """
        return toolz.filter(lambda po: po.display_name == display_name_to_find, self._collection.values())

    def find_by_name(self, name_to_find: str) -> Iterator:
        """
        Return an iterator over all project objects whose `name` is the `name_to_find`.

        Args:
            name_to_find: The name for all project objects of interest.

        Returns:
            An iterator over all project objects with the specified `name` property.
        """
        return toolz.filter(lambda po: po.name == name_to_find, self._collection.values())

    def find_by_object_id(self, object_id_to_find: uuid.UUID) -> Optional:
        """
        Return the project object whose `object_id` is the `object_id_to_find` if available; otherwise, `None`.

        Args:
            object_id_to_find: The object ID for the project objects of interest.

        Returns:
            The project objects with the specified `name` property. If no such project is found, return `None`.
        """
        return toolz.get(object_id_to_find, self._collection, default=None)
