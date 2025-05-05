# -*- coding: utf-8 -*-

import aws_cdk as cdk

from cdk_mate.stack_params import ConstructParams, StackParams


class TestConstructParams:
    def test(self):
        construct_params = ConstructParams(
            scope=cdk.App(),
            id="MyConstruct",
        )
        construct_params.to_construct_kwargs()

class TestStackParams:
    def test(self):
        stack_params = StackParams(
            scope=cdk.App(),
            id="MyStack",
            stack_name="MyStackName",
            env=cdk.Environment(
                account="123456789012",
                region="us-east-1",
            ),
        )
        kwargs = stack_params.to_stack_kwargs()

        req_kwargs, opt_kwargs = StackParams._split_req_opt(kwargs)
        assert set(req_kwargs) == {"scope", "id"}
        assert set(opt_kwargs) == {"stack_name", "env"}


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.stack_params",
        preview=False,
    )
