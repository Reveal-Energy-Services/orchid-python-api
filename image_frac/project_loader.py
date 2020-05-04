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


class ProjectLoader:
    """Provides an .NET IProject to be adapted."""

    def __init__(self, project_pathname: str):
        """
        Construct an instance that loads project data from project_pathname

        :param project_pathname: Identifies the data file for the project of interest.
        """
        self._project_pathname = project_pathname
