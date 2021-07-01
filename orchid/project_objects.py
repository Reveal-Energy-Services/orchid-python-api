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
    def __init__(self, create_callable, net_project_objects):
        self._collection = toolz.map(lambda kwargs: create_callable(**kwargs), net_project_objects)

    def __len__(self):
        return toolz.count(self._collection)
