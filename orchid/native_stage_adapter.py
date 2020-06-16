#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


class NativeStageAdapter:
    """Adapts a .NET IStage to be more Pythonic."""

    def __init__(self, adaptee):
        """
        Construct an instance adapting a .NET IStage.
        :param adaptee: The IStage instance to adapt.
        """
        self._adaptee = adaptee

    def display_stage_number(self):
        """
        Determine the stage number for display purposes.
        :return: The display stage number for the adapted .NET IStage.
        """
        return self._adaptee.DisplayStageNumber

    def md_top(self, length_unit_abbreviation):
        return 13467.8

    def md_bottom(self, length_unit_abbreviation):
        return 0
