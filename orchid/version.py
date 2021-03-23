#  Copyright 2017-2021 Reveal Energy Services, Inc 
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

from collections import namedtuple
import pathlib
from typing import Tuple

import packaging.version as pv


VersionId = namedtuple('VersionId', ['major', 'minor', 'patch'])


class Version:
    def __init__(self, version=()):
        """
        Constructs an instance.

        If no version is supplied, this method will try to read the file, 'VERSION', in the same directory
        as this module.

        Args:
            version (Tuple[int, int, int]): The 3-part (major, minor, patch) version identifier.
        """
        if version:
            self.major, self.minor, self.patch = version
        else:
            with pathlib.Path(__file__).parent.joinpath('VERSION').open() as version_file:
                text_version = version_file.read()
                version = pv.parse(text_version)
                self.major = version.major
                self.minor = version.minor
                self.patch = version.micro
                if version.is_prerelease:
                    self.pre = version.pre

    @property
    def is_prerelease(self):
        return self._is_prerelease()

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False

        return self.id() == other.id()

    def __repr__(self):
        return f'Version(major={self.major}, minor={self.minor}, patch={self.patch})'

    def _is_prerelease(self) -> bool:
        """
        Is this version a pre-release version?

        Returns:
            True if this version is a pre-release; otherwise, false.
        """
        return hasattr(self, 'pre')

    def id(self) -> VersionId:
        """
        Calculates the version identifier.

        Returns:
            The identifier for this instance.
        """
        return VersionId(self.major, self.minor, self.patch)


def api_version():
    """
    Calculate the Python API version.

    Returns:
        The Python API version read from the `VERSION` file.
    """
    return Version()
