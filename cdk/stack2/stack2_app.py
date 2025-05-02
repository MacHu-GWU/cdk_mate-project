#!/usr/bin/env python3

from cdk_mate.tests.iac_init import stack_enum

_ = stack_enum.stack2_dev
_ = stack_enum.stack2_test

stack_enum.app.synth()
