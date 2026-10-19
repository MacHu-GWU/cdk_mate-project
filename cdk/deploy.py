# -*- coding: utf-8 -*-

import cdk_mate.api as cdk_mate
from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

# --- 🗂️ group stacks by aws account / environment
# --- 🟢 creation order: Stack1 first, since Stack2 uses its alert topic
# (the CDK CLI orders them by their dependencies anyway; the list order documents it)
create_dev_stack_ctx_list = [
    stack_ctx_enum.stack1_dev,
    stack_ctx_enum.stack2_dev,
]

create_test_stack_ctx_list = [
    stack_ctx_enum.stack1_test,
    stack_ctx_enum.stack2_test,
]

# --- 🔴 deletion order: Stack2 imports the alert topic of Stack1, so it goes first
# (the CDK CLI orders them by their dependencies anyway; the list order documents it)
delete_dev_stack_ctx_list = [
    stack_ctx_enum.stack2_dev,
    stack_ctx_enum.stack1_dev,
]

delete_test_stack_ctx_list = [
    stack_ctx_enum.stack2_test,
    stack_ctx_enum.stack1_test,
]

# --- 📦 cdk synth
cdk_mate.cli.Synth().run(dir_cdk=__file__)
# cdk_mate.cdk_synth_many(create_dev_stack_ctx_list, dir_cdk=__file__)
# cdk_mate.cdk_synth_many(create_test_stack_ctx_list, dir_cdk=__file__)

# --- 🔍 cdk diff
# cdk_mate.cdk_diff_many(create_dev_stack_ctx_list, dir_cdk=__file__)
# cdk_mate.cdk_diff_many(create_test_stack_ctx_list, dir_cdk=__file__)

# --- 🚀 cdk deploy
cdk_mate.cdk_deploy_many(create_dev_stack_ctx_list, dir_cdk=__file__, prompt=False)
cdk_mate.cdk_deploy_many(create_test_stack_ctx_list, dir_cdk=__file__, prompt=False)

# --- 💥 cdk destroy
cdk_mate.cdk_destroy_many(delete_dev_stack_ctx_list, dir_cdk=__file__, prompt=False)
cdk_mate.cdk_destroy_many(delete_test_stack_ctx_list, dir_cdk=__file__, prompt=False)
