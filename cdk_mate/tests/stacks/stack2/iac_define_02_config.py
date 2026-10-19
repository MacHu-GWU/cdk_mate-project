# -*- coding: utf-8 -*-

import typing as T

from aws_cdk import aws_ssm as ssm

if T.TYPE_CHECKING:  # pragma: no cover
    from .iac_define import Stack2


class Stack2ConfigMixin:
    def create_config(self: "Stack2"):
        # a standard SSM parameter is free; it records where to send alerts
        self.alert_topic_arn_parameter = ssm.StringParameter(
            self,
            "AlertTopicArnParameter",
            parameter_name=f"/{self.stack_name}/alert-topic-arn",
            string_value=self.alert_topic.topic_arn,
        )
