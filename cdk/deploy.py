# -*- coding: utf-8 -*-

from cdk_mate.stack_ctx import cdk_deploy_many, cdk_destroy_many
from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

stack_ctx_list = [
    stack_ctx_enum.stack1_dev,
    stack_ctx_enum.stack2_dev,
]
cdk_deploy_many(stack_ctx_list=stack_ctx_list, dir_cdk=__file__, prompt=False)
# cdk_destroy_many(stack_ctx_list=stack_ctx_list, dir_cdk=__file__, prompt=False)

stack_ctx_list = [
    stack_ctx_enum.stack1_test,
    stack_ctx_enum.stack2_test,
]
# cdk_deploy_many(stack_ctx_list=stack_ctx_list, dir_cdk=__file__, prompt=False)
# cdk_destroy_many(stack_ctx_list=stack_ctx_list, dir_cdk=__file__, prompt=False)
