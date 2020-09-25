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


import orchid.dot_net_dom_access as dna
import orchid.net_quantity as onq

import toolz.curried as toolz


class SubsurfacePoint(dna.DotNetAdapter):
    """Adapts a .NET ISubsurfacePoint to be more Pythonic."""

    x = dna.transformed_dom_property('x', 'The x-coordinate of this point.', onq.as_measurement)
    y = dna.transformed_dom_property('y', 'The y-coordinate of this point.', onq.as_measurement)
    depth = dna.transformed_dom_property('depth', 'The z-coordinate (depth) of this point.', onq.as_measurement)
    md_kelly_bushing = dna.transformed_dom_property('md_kelly_bushing',
                                                    'The measured depth of this point relative to the kelly bushing.',
                                                    onq.as_measurement)
    xy_origin = dna.dom_property('well_reference_frame_xy',
                                 'The reference frame or origin for the x-y coordinates of this point.')
    depth_origin = dna.dom_property('depth_datum',
                                    'The datum or origin for the z-coordinate of this point.')

    def as_length_unit(self, as_length_unit):
        return SubsurfacePointUsingLengthUnit(self._adaptee, as_length_unit)


class SubsurfacePointUsingLengthUnit(dna.DotNetAdapter):
    """Adapts a .NET ISubsurfacePoint to be more Pythonic. Always returns lengths in the specified units."""

    def __init__(self, adaptee, in_length_unit):
        super().__init__(adaptee)
        self._length_converter_func = toolz.flip(onq.convert_net_quantity_to_different_unit,
                                                 in_length_unit.abbreviation)

    xy_origin = dna.dom_property('well_reference_frame_xy',
                                 'The reference frame or origin for the x-y coordinates of this point.')
    depth_origin = dna.dom_property('depth_datum',
                                    'The datum or origin for the z-coordinate of this point.')

    @property
    def x(self):
        """The x-coordinate of this point."""
        return onq.as_measurement(self._length_converter_func(self._adaptee.X))

    @property
    def y(self):
        """The y-coordinate of this point."""
        return onq.as_measurement(self._length_converter_func(self._adaptee.Y))

    @property
    def depth(self):
        """The depth of this point."""
        return onq.as_measurement(self._length_converter_func(self._adaptee.Depth))

    @property
    def md_kelly_bushing(self):
        """The md_kelly_bushing of this point."""
        return onq.as_measurement(self._length_converter_func(self._adaptee.MdKellyBushing))
