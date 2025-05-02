# -*- coding: utf-8 -*-

from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

stack_ctx_enum.stack2_dev.cdk_deploy(dir_cdk=__file__, prompt=False)
# stack_ctx_enum.stack2_test.cdk_deploy(dir_cdk=__file__, prompt=False)

# stack_ctx_enum.stack2_dev.cdk_destroy(dir_cdk=__file__, prompt=False)
# stack_ctx_enum.stack2_test.cdk_destroy(dir_cdk=__file__, prompt=False)
