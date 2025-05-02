# -*- coding: utf-8 -*-

from cdk_mate.tests.stack_ctx_enum import StackCtxEnum

StackCtxEnum.stack1_dev.cdk_deploy(dir_cdk=__file__, prompt=False)
# StackCtxEnum.stack1_test.cdk_deploy(dir_cdk=__file__, prompt=False)

# StackCtxEnum.stack1_dev.cdk_destroy(dir_cdk=__file__, prompt=False)
# StackCtxEnum.stack1_test.cdk_destroy(dir_cdk=__file__, prompt=False)
