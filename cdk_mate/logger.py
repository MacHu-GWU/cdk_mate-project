# -*- coding: utf-8 -*-

"""
The ``cdk_mate`` logger.

cdk_mate reports what it is about to do (console URLs, the AWS identity, the
command line) through the standard :mod:`logging` module, under the logger
name ``cdk_mate``. By default it writes plain messages to stdout, so the output
looks like plain ``print``.

Silence it, or keep only the warnings::

    import logging

    logging.getLogger("cdk_mate").setLevel(logging.WARNING)

Send it to your own handlers instead::

    cdk_mate_logger = logging.getLogger("cdk_mate")
    cdk_mate_logger.handlers.clear()
    cdk_mate_logger.propagate = True
"""

import sys
import logging


class _StdoutHandler(logging.StreamHandler):
    """
    A handler that writes to whatever ``sys.stdout`` is when a record is
    emitted, so redirected stdout (``contextlib.redirect_stdout``, pytest's
    ``capsys``) is honored, like ``print``.
    """

    def __init__(self):
        super().__init__(stream=sys.stdout)

    @property
    def stream(self):
        return sys.stdout

    @stream.setter
    def stream(self, value):
        pass


#: The logger of cdk_mate; its name is ``"cdk_mate"``.
logger = logging.getLogger("cdk_mate")

if not logger.handlers:
    _handler = _StdoutHandler()
    _handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    # the handler above already prints; propagating would print twice
    # for an application that configured the root logger
    logger.propagate = False
