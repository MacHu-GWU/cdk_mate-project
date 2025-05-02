# -*- coding: utf-8 -*-

import typing as T

import aws_cdk as cdk
from constructs import Construct


class Stack1(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        stack_name: str,
        env: cdk.Environment,
    ):
        super().__init__(
            scope=scope,
            id=id,
            stack_name=stack_name,
            env=env,
        )
