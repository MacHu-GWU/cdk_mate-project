# -*- coding: utf-8 -*-

import typing as T

from aws_cdk import aws_ssm as ssm

if T.TYPE_CHECKING:  # pragma: no cover
    from .iac_define import Stack2


class Stack2Mixin:
    def create_everything(self: "Stack2"):
        # a standard SSM parameter is free, so the real deployments in cdk/ cost nothing;
        # the stack name keeps it unique across stacks and environments
        self.parameter = ssm.StringParameter(
            self,
            "Parameter",
            parameter_name=f"/{self.stack_name}/example",
            string_value="stack2",
        )
