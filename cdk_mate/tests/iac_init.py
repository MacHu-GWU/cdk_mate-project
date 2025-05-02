# -*- coding: utf-8 -*-

import aws_cdk as cdk

from .stacks.stack1.iac_define import Stack1
from .stack_ctx_enum import StackCtxEnum


app = cdk.App()

stack1_dev = Stack1(
    scope=app,
    id=StackCtxEnum.stack1_dev.construct_id,
    stack_name=StackCtxEnum.stack1_dev.stack_name,
    env=cdk.Environment(
        account=StackCtxEnum.stack1_dev.aws_account_id,
        region=StackCtxEnum.stack1_dev.aws_region,
    ),
)

stack1_test = Stack1(
    scope=app,
    id=StackCtxEnum.stack1_test.construct_id,
    stack_name=StackCtxEnum.stack1_test.stack_name,
    env=cdk.Environment(
        account=StackCtxEnum.stack1_test.aws_account_id,
        region=StackCtxEnum.stack1_test.aws_region,
    ),
)
