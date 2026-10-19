# -*- coding: utf-8 -*-

import typing as T

from aws_cdk import aws_sns as sns

if T.TYPE_CHECKING:  # pragma: no cover
    from .iac_define import Stack1


class Stack1AlertsMixin:
    def create_alerts(self: "Stack1"):
        # an SNS topic costs nothing until it delivers messages;
        # Stack2 receives it as an argument, which makes Stack2 depend on Stack1
        self.alert_topic = sns.Topic(
            self,
            "AlertTopic",
            topic_name=f"{self.stack_name}-alerts",
        )
