#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import ArgumentError, c_char_p
from functools import wraps


def c_char_p_wrapper(string):
    """Wrapper for ``ctypes.c_char_p`` where ``str``'s are automatically encoded to a utf-8 bytestring."""
    if isinstance(string, str):
        string = string.encode("utf-8")
    if isinstance(string, (str, bytes)):
        return c_char_p(string)
    raise ArgumentError("argument '%s': exceptions.TypeError: wrong type [%s]" % (string, type(string)))


def memoized_property(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter any more.
    source: https://pypi.python.org/pypi/memoized-property/1.0.1
    """
    attr_name = "_" + fget.__name__
    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)
    return property(fget_memoized)

def memoize(f):
    """Memoization decorator
    source: http://code.activestate.com/recipes/577219-minimalistic-memoization/"""
    # see also issue # 22
    cache = {}
    MAXCACHE = 10 ** 7
    @wraps(f)
    def memf(*datetime):
        if datetime in cache:
            return cache[datetime]
        elif len(cache) < MAXCACHE:
            result = f(*datetime)
            cache[datetime] = result
            return result
        return f(*datetime)
    return memf
