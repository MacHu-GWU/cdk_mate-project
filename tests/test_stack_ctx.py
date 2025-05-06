# -*- coding: utf-8 -*-

import pytest
from func_args.api import ParamError
from cdk_mate.stack_ctx import StackCtx


class TestStackCtx:
    def test_stack_ctx(self):
        stack_ctx = StackCtx(
            construct_id="MyStack",
            stack_name="my-stack",
            aws_account_id="123456789012",
            aws_region="us-east-1",
        )
        _ = stack_ctx.to_stack_kwargs()
        _ = stack_ctx.stack_console_url

        with pytest.raises(ParamError):
            stack_ctx = StackCtx()


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.stack_ctx",
        preview=False,
    )
