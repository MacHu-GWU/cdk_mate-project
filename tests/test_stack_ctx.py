# -*- coding: utf-8 -*-

from cdk_mate.stack_ctx import StackCtx

import pytest
from func_args.api import ParamError

from cdk_mate.tests.mock_aws import BaseMockAwsTest


class TestStackCtx:
    def test_stack_ctx(self):
        stack_ctx = StackCtx(
            construct_id="MyStack",
            stack_name="my-stack",
            aws_account_id="123456789012",
            aws_region="us-east-1",
        )
        kwargs = stack_ctx.to_stack_kwargs()
        assert kwargs["id"] == "MyStack"
        assert kwargs["stack_name"] == "my-stack"
        assert kwargs["env"].account == "123456789012"
        assert kwargs["env"].region == "us-east-1"
        assert "filteringText=my-stack" in stack_ctx.stack_console_url

        with pytest.raises(ParamError):
            StackCtx()


class TestStackCtxSynth(BaseMockAwsTest):
    """
    End-to-end: build StackCtx from (mocked) boto sessions, create the example
    stacks in ``cdk_mate/tests/stacks``, and synthesize them with aws-cdk-lib.
    Needs node on PATH (aws-cdk-lib's jsii runtime), but no AWS account.
    """

    def test_new(self):
        from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

        stack_ctx = stack_ctx_enum.stack1_dev
        assert stack_ctx.construct_id == "CdkMateStack1Dev"
        assert stack_ctx.stack_name == "cdk-mate-stack1-dev"
        assert stack_ctx.aws_account_id == "123456789012"  # moto's fake account
        assert stack_ctx.aws_region == "us-east-1"

    def test_synth(self):
        from cdk_mate.tests.stack_enum import stack_enum

        _ = stack_enum.stack1_dev
        _ = stack_enum.stack1_test
        _ = stack_enum.stack2_dev
        _ = stack_enum.stack2_test

        cloud_assembly = stack_enum.app.synth()
        stack_names = {stack.stack_name for stack in cloud_assembly.stacks}
        assert stack_names == {
            "cdk-mate-stack1-dev",
            "cdk-mate-stack1-test",
            "cdk-mate-stack2-dev",
            "cdk-mate-stack2-test",
        }


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.stack_ctx",
        preview=False,
    )
