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

import pandas as pd
from toolz.curried import map, partial, thread_last

from orchid.net_quantity import as_datetime
import orchid.project_units as opu


def _dom_property(attribute_name, docstring):
    """
    Return the property of the DOM corresponding to `attribute_name` with doc string, `docstring`.
    :param attribute_name: The name of the original attribute.
    :param docstring: The doc string to be attached to the resultant property.
    :return: The property correctly accessing the DOM.
    """

    # This implementation is based on the StackOverflow post:
    # https://stackoverflow.com/questions/36580931/python-property-factory-or-descriptor-class-for-wrapping-an-external-library
    #
    # More importantly, it resolves an issue I was experiencing with PyCharm: when I used `property` directly
    # in the class definition, PyCharm reported "Property 'xyz' could not be read. I think it might have been
    # than I needed to apply `curry` to the "getter method" I also defined in the class in order to pass he
    # attribute name at definition time (because `self` was only available at run-time).
    def getter(self):
        result = thread_last(attribute_name.split('_'),  # split the attribute name into words
                             map(str.capitalize),  # capitalize each word
                             lambda capitalized_pieces: ''.join(capitalized_pieces),  # concatenate words
                             lambda capitalized: 'get_' + capitalized,  # convert to .NET get method for property
                             partial(getattr, self._adaptee))  # look up this new attribute in the adaptee
        return result

    # Ensure no setter for the DOM properties
    return property(fget=getter, doc=docstring, fset=None)


class NativeTreatmentCurveFacade:
    def __init__(self, net_treatment_curve):
        self._adaptee = net_treatment_curve
        self._quantity_name_physical_quantity_map = {'Pressure': 'pressure',
                                                     'Slurry Rate': 'slurry rate',
                                                     'Proppant Concentration': 'proppant concentration'}
        # noinspection PyArgumentList
        self._sample_unit_func = partial(opu.unit, net_treatment_curve.Stage.Well.Project)

    display_name = _dom_property('display_name', 'Return the display name for this treatment curve.')
    name = _dom_property('name', 'Return the name for this treatment curve.')
    sampled_quantity_name = _dom_property('sampled_quantity_name',
                                          'Return the sampled quantity name for this treatment curve.')
    suffix = _dom_property('suffix', 'Return the suffix for this treatment curve.')

    def sampled_quantity_unit(self) -> str:
        """
        Return the measurement unit of the samples in this treatment curve.
        :return: A string containing an abbreviation for the unit  of each sample in this treatment curve.
        """
        result = self._sample_unit_func(self._quantity_name_physical_quantity_map[self.sampled_quantity_name()])
        return result

    def time_series(self) -> pd.Series:
        """
        Return the suffix for this treatment curve.
        :return: The suffix of this treatment curve.
        """
        # Because I use `samples` twice in the subsequent expression, I must *actualize* the map by invoking `list`.
        samples = list(map(lambda s: (s.Timestamp, s.Value), self._adaptee.GetOrderedTimeSeriesHistory()))
        result = pd.Series(data=map(lambda s: s[1], samples), index=map(as_datetime, map(lambda s: s[0], samples)),
                           name=self.name())
        return result
