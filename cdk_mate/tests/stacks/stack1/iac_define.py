# -*- coding: utf-8 -*-

import aws_cdk as cdk
from constructs import Construct

from .iac_define_01_alerts import Stack1AlertsMixin
from .iac_define_02_config import Stack1ConfigMixin


class Stack1(
    cdk.Stack,
    Stack1AlertsMixin,
    Stack1ConfigMixin,
):
    """
    The alerts stack.

    :param log_level: The log level of this environment, such as ``"DEBUG"``
        in dev and ``"INFO"`` in test. It is an explicit argument, so each
        environment sets it in :mod:`cdk_mate.tests.stack_enum`.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        stack_name: str,
        env: cdk.Environment,
        log_level: str,
    ):
        super().__init__(
            scope=scope,
            id=id,
            stack_name=stack_name,
            env=env,
        )
        self.log_level = log_level
        self.create_alerts()
        self.create_config()
