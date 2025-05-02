# -*- coding: utf-8 -*-

from .iac_define import cdk, Stack1
from ...bsm import bsm

app = cdk.App()

stack1 = Stack1(
    scope=app,
    id="Stack1",
    stack_name="cdk-mate-stack1",
    env=cdk.Environment(
        account=bsm.aws_account_id,
        region=bsm.aws_region,
    ),
)
