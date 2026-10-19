#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_mate.tests.stack_enum import StackEnum

stack_enum = StackEnum(app=cdk.App())

_ = stack_enum.stack1_dev
_ = stack_enum.stack1_test

stack_enum.app.synth()
