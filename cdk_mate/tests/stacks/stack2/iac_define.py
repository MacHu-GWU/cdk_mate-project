# -*- coding: utf-8 -*-

import aws_cdk as cdk
from aws_cdk import aws_sns as sns
from constructs import Construct

from .iac_define_01_publisher import Stack2PublisherMixin
from .iac_define_02_config import Stack2ConfigMixin


class Stack2(
    cdk.Stack,
    Stack2PublisherMixin,
    Stack2ConfigMixin,
):
    """
    The publisher stack.

    :param alert_topic: The alert topic of a
        :class:`~cdk_mate.tests.stacks.stack1.iac_define.Stack1` in the same
        environment. It is an explicit argument, so the dependency on Stack1
        is visible in the signature and wired in :mod:`cdk_mate.tests.stack_enum`.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        stack_name: str,
        env: cdk.Environment,
        alert_topic: sns.ITopic,
    ):
        super().__init__(
            scope=scope,
            id=id,
            stack_name=stack_name,
            env=env,
        )
        self.alert_topic = alert_topic
        self.create_publisher()
        self.create_config()
