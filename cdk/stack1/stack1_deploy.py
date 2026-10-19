# -*- coding: utf-8 -*-

from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

# --- 📦 cdk synth
# stack_ctx_enum.stack1_dev.cdk_synth(dir_cdk=__file__)
# stack_ctx_enum.stack1_test.cdk_synth(dir_cdk=__file__)

# --- 🔍 cdk diff
# stack_ctx_enum.stack1_dev.cdk_diff(dir_cdk=__file__)
# stack_ctx_enum.stack1_test.cdk_diff(dir_cdk=__file__)

# --- 🚀 cdk deploy
# stack_ctx_enum.stack1_dev.cdk_deploy(dir_cdk=__file__, prompt=False)
# stack_ctx_enum.stack1_test.cdk_deploy(dir_cdk=__file__, prompt=False)

# --- 💥 cdk destroy
# Stack2 imports the alert topic of Stack1, so the CDK CLI destroys Stack2 of the same
# environment as well, before Stack1 (exclusively=True would fail while Stack2 still exists).
# stack_ctx_enum.stack1_dev.cdk_destroy(dir_cdk=__file__, prompt=False)
# stack_ctx_enum.stack1_test.cdk_destroy(dir_cdk=__file__, prompt=False)
