# -*- coding: utf-8 -*-

import typing as T

from aws_cdk import aws_ssm as ssm

if T.TYPE_CHECKING:  # pragma: no cover
    from .iac_define import Stack1


class Stack1ConfigMixin:
    def create_config(self: "Stack1"):
        # a standard SSM parameter is free; its value differs per environment
        self.log_level_parameter = ssm.StringParameter(
            self,
            "LogLevelParameter",
            parameter_name=f"/{self.stack_name}/log-level",
            string_value=self.log_level,
        )
