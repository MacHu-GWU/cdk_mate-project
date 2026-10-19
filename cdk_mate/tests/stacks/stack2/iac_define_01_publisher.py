# -*- coding: utf-8 -*-

import typing as T

from aws_cdk import aws_iam as iam

if T.TYPE_CHECKING:  # pragma: no cover
    from .iac_define import Stack2


class Stack2PublisherMixin:
    def create_publisher(self: "Stack2"):
        # an IAM role is free; granting it sns:Publish on a topic of Stack1
        # puts the topic ARN, exported by Stack1, into this stack's policy
        self.publisher_role = iam.Role(
            self,
            "PublisherRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        self.alert_topic.grant_publish(self.publisher_role)
