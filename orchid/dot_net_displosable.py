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
"""Wrapper function to help dealing with IDisposable classes.

This implementation is based on code in the discussion of
[Python.NET issue 79]( https://github.com/pythonnet/pythonnet/issues/79).
"""

from inspect import isclass, isfunction
from contextlib import contextmanager

__all__ = ['disposable']


@contextmanager
def disposable(obj_or_class, *args, **kwargs):
    """Contextmanager wrapper around IDisposables."""
    if isclass(obj_or_class) or isfunction(obj_or_class):
        obj = obj_or_class(*args, **kwargs)
    else:
        obj = obj_or_class

    if hasattr(obj, '__enter__') and hasattr(obj, '__exit__'):
        # Already a contextmanager, skip
        return obj

    if not hasattr(obj, 'Dispose') or not callable(obj.Dispose):
        # Likely not IDisposable, currently isinstance doesn't work for
        # interfaces so we have to check that in this explicit way
        return obj

    try:
        yield obj
    finally:
        obj.Dispose()
