#!/usr/bin/env python3

from cdk_mate.tests.stack_enum import stack_enum

_ = stack_enum.stack1_dev
_ = stack_enum.stack1_test
_ = stack_enum.stack2_dev
_ = stack_enum.stack2_test

stack_enum.app.synth()
