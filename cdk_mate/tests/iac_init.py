# -*- coding: utf-8 -*-

import aws_cdk as cdk

from .stacks.stack1.iac_define import Stack1
from .stacks.stack2.iac_define import Stack2

from .stack_ctx_enum import stack_ctx_enum


app = cdk.App()


stack1_dev = Stack1(
    scope=app,
    **stack_ctx_enum.stack1_dev.to_stack_kwargs(),
)

stack1_test = Stack1(
    scope=app,
    **stack_ctx_enum.stack1_test.to_stack_kwargs(),
)

stack2_dev = Stack2(
    scope=app,
    **stack_ctx_enum.stack2_dev.to_stack_kwargs(),
)

stack2_test = Stack2(
    scope=app,
    **stack_ctx_enum.stack2_test.to_stack_kwargs(),
)
