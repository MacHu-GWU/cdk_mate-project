# -*- coding: utf-8 -*-

"""
Utility functions.
"""

def to_camel(s: str) -> str:
    """
    Converts a string to camelcased. Useful for turning a function name into a class name.

    >>> to_camel('Hello_world')
    'HelloWorld'
    >>> to_camel('hello-World')
    'HelloWorld'
    >>> to_camel('HELLO WORLD')
    'HelloWorld'
    """
    s = "_".join([w.strip() for w in s.split() if w.strip()])
    s = s.replace("-", "_")
    return "".join(w.capitalize() or "_" for w in s.split("_"))
