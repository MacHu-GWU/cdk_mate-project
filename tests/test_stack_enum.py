# -*- coding: utf-8 -*-

import os
import pytest

from cdk_mate.tests.mock_aws import BaseMockAwsTest


class TestStackEnum(BaseMockAwsTest):
    def test_synth(self):
        from cdk_mate.tests.stack_enum import stack_enum

        _ = stack_enum.stack1_dev
        _ = stack_enum.stack1_test
        _ = stack_enum.stack2_dev
        _ = stack_enum.stack2_test

        stack_enum.app.synth()


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate",
        preview=False,
    )
