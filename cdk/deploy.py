# -*- coding: utf-8 -*-

import cdk_mate.api as cdk_mate
from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

# --- Synth all
cdk_mate.cli.Synth().run(dir_cdk=__file__)

# fmt: off
# --- Work on Dev environment
dev_stack_ctx_list = [
    stack_ctx_enum.stack1_dev,
    stack_ctx_enum.stack2_dev,
]
# cdk_mate.cdk_diff_many(stack_ctx_list=dev_stack_ctx_list, dir_cdk=__file__)
# cdk_mate.cdk_deploy_many(stack_ctx_list=dev_stack_ctx_list, dir_cdk=__file__, prompt=False)
# cdk_mate.cdk_destroy_many(stack_ctx_list=dev_stack_ctx_list, dir_cdk=__file__, prompt=False)

# --- Work on Test environment
test_stack_ctx_list = [
    stack_ctx_enum.stack1_test,
    stack_ctx_enum.stack2_test,
]
# cdk_mate.cdk_diff_many(stack_ctx_list=test_stack_ctx_list, dir_cdk=__file__)
# cdk_mate.cdk_deploy_many(stack_ctx_list=test_stack_ctx_list, dir_cdk=__file__, prompt=False)
# cdk_mate.cdk_destroy_many(stack_ctx_list=test_stack_ctx_list, dir_cdk=__file__, prompt=False)
# fmt: on
