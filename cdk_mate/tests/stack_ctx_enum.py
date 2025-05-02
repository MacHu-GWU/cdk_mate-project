# -*- coding: utf-8 -*-

from ..stack_ctx import StackCtx
from .bsm_enum import BsmEnum


class StackCtxEnum:
    stack1_dev = StackCtx(
        construct_id="Stack1Dev",
        stack_name="cdk-mate-stack1-dev",
        aws_account_id=BsmEnum.dev.aws_account_id,
        aws_region=BsmEnum.dev.aws_region,
        bsm=BsmEnum.dev,
    )
    stack1_test = StackCtx(
        construct_id="Stack1Test",
        stack_name="cdk-mate-stack1-test",
        aws_account_id=BsmEnum.test.aws_account_id,
        aws_region=BsmEnum.test.aws_region,
        bsm=BsmEnum.test,
    )
