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

# noinspection PyUnresolvedReferences
import orchid

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell


class NativeWellAdapter:
    """Adapts a native IWell to python."""
    def __init__(self, native_well: IWell):
        """
        Constructs an instance adapting a .NET IWell.
        :param native_well: The .NET well to be adapted.
        """
        self._adaptee = native_well

    def name(self) -> str:
        """
        Returns the name of the adapted IWell
        :return: The name of the adapted .NET well.
        """
        return self._adaptee.Name

    def display_name(self) -> str:
        """
        Returns the display name of the adapted IWell
        :return: The display name of the adapted .NET well.
        """
        return self._adaptee.DisplayName

    def uwi(self) -> str:
        """
        Returns the uwi of the adapted IWell
        :return: The uwi of the adapted .NET well.
        """
        return self._adaptee.Uwi if self._adaptee.Uwi else 'No UWI'
