# -*- coding: utf-8 -*-

import os
import pytest
from cdk_mate.tests.stack_enum import stack_enum


@pytest.mark.skipif("CI" in os.environ, reason="Skip test in CI")
def test_iac_init():
    _ = stack_enum.stack1_dev
    _ = stack_enum.stack1_test
    _ = stack_enum.stack2_dev
    _ = stack_enum.stak2_test

    stack_enum.app.synth()


if __name__ == "__main__":
    from cdk_mate.tests import run_unit_test

    run_unit_test(__file__)
