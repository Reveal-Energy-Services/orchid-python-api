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

"""
Provides a common interface to collections of `IProjectObject` instances. These collections provide methods to:

- Query for all object IDs identifying instances in this collection
- Query for the name of all instances in this collection
- Query for the display name of all instances in this collection
- Search for a single instance by object ID
- Search for all instances with a specified name
- Search for all instances with a specified display name
"""


import toolz.curried as toolz


class ProjectObjects:
    def __init__(self, make_adapter, net_project_objects):
        self._collection = toolz.pipe(
            net_project_objects,
            toolz.map(lambda kwargs: make_adapter(**kwargs)),
            toolz.map(lambda dom_object: (dom_object.object_id, dom_object)),
            dict,
        )

    def __len__(self):
        return len(self._collection)

    def all_display_names(self):
        return toolz.map(lambda po: po.display_name, self._collection.values())

    def all_names(self):
        return toolz.map(lambda po: po.name, self._collection.values())

    def find_by_object_id(self, id_sought):
        return toolz.get(id_sought, self._collection, default=None)

    def object_ids(self):
        return self._collection.keys()
