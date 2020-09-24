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


class SubsurfacePoint(dna.DotNetAdapter):
    """Adapts a .NET ISubsurfacePoint to be more Pythonic."""

    x = dna.dom_property('x', 'The x-coordinate of this point.')
    y = dna.dom_property('y', 'The y-coordinate of this point.')
    depth = dna.dom_property('depth', 'The z-coordinate (depth) of this point.')
    md_kelly_bushing = dna.dom_property('md_kelly_bushing',
                                        'The measured depth of this point relative to the kelly bushing.')
    xy_origin = dna.dom_property('well_reference_frame_xy',
                                 'The reference frame or origin for the x-y coordinates of this point.')
    depth_origin = dna.dom_property('depth_datum',
                                    'The datum or origin for the z-coordinate of this point.')
