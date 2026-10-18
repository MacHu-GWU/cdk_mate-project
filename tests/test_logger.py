# -*- coding: utf-8 -*-

from cdk_mate.logger import logger

import io
import logging
import contextlib

import pytest


def test_plain_message_on_stdout(capsys: pytest.CaptureFixture):
    logger.info("hello")
    assert capsys.readouterr().out == "hello\n"


def test_follows_redirected_stdout():
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        logger.info("redirected")
    assert buffer.getvalue() == "redirected\n"


def test_silence(capsys: pytest.CaptureFixture):
    logger.setLevel(logging.WARNING)
    try:
        logger.info("hidden")
        logger.warning("shown")
    finally:
        logger.setLevel(logging.INFO)
    assert capsys.readouterr().out == "shown\n"


def test_setup():
    assert logger.name == "cdk_mate"
    assert logger.propagate is False
    handler = logger.handlers[0]
    handler.stream = (
        io.StringIO()
    )  # ignored: it always writes to the current sys.stdout
    assert handler.stream is not None


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.logger",
        preview=False,
    )
