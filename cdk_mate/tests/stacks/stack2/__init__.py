# -*- coding: utf-8 -*-

"""
Stack2: the publisher stack.

It uses the SNS topic of :mod:`cdk_mate.tests.stacks.stack1`: an IAM role that
may publish to it, and an SSM parameter that records its ARN. The topic arrives
as an explicit argument of
:class:`~cdk_mate.tests.stacks.stack2.iac_define.Stack2`, so CDK turns the
reference into a CloudFormation export of Stack1 and an import in Stack2, and
deploys Stack1 first. Every resource is free: an IAM role and a standard SSM
parameter.
"""
