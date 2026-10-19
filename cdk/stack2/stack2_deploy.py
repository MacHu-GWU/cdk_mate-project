# -*- coding: utf-8 -*-

from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

# --- 📦 cdk synth
# stack_ctx_enum.stack2_dev.cdk_synth(dir_cdk=__file__)
# stack_ctx_enum.stack2_test.cdk_synth(dir_cdk=__file__)

# --- 🔍 cdk diff
# stack_ctx_enum.stack2_dev.cdk_diff(dir_cdk=__file__)
# stack_ctx_enum.stack2_test.cdk_diff(dir_cdk=__file__)

# --- 🚀 cdk deploy
# Stack2 depends on Stack1, so the CDK CLI deploys Stack1 first if it changed
# (pass exclusively=True to deploy Stack2 only).
# stack_ctx_enum.stack2_dev.cdk_deploy(dir_cdk=__file__, prompt=False)
# stack_ctx_enum.stack2_test.cdk_deploy(dir_cdk=__file__, prompt=False)

# --- 💥 cdk destroy
# stack_ctx_enum.stack2_dev.cdk_destroy(dir_cdk=__file__, prompt=False)
# stack_ctx_enum.stack2_test.cdk_destroy(dir_cdk=__file__, prompt=False)
