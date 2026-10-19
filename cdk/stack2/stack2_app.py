#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_mate.tests.stack_enum import StackEnum

stack_enum = StackEnum(app=cdk.App())

# Stack2 takes the alert topic of Stack1, so these also create stack1_dev and stack1_test
_ = stack_enum.stack2_dev
_ = stack_enum.stack2_test

stack_enum.app.synth()
