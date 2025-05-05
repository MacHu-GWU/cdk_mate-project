# -*- coding: utf-8 -*-

import aws_cdk as cdk

from .stack_params import StackParams


class BaseStack(cdk.Stack):
    def __init__(
        self,
        params: StackParams,
    ):
        super().__init__(**params.to_stack_kwargs())
        self.params = params
