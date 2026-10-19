# -*- coding: utf-8 -*-

"""
The stack contexts of the example project: layer 1 of the two-layer pattern.

A multi-stack, multi-environment CDK project keeps two enums with one entry per
(stack, environment) pair:

1. **This module, the stack context enum.** Each entry is a
   :class:`~cdk_mate.stack_ctx.StackCtx`: plain data that names one stack in
   one environment (construct id, stack name, AWS account, region) plus the
   boto session that deploys it. Building one creates no CDK construct.
2. :mod:`cdk_mate.tests.stack_enum`, **the stack enum.** Each entry creates
   the CDK stack itself, in a given ``cdk.App``, from the matching entry here.

Why two layers, although four stacks then take eight entries:

- **The deploy scripts need only this layer.** ``cdk diff``, ``cdk deploy``
  and ``cdk destroy`` need the stack names and the credentials, not the stack
  objects. ``cdk/deploy.py`` imports this module and never loads a stack
  definition, so it stays fast however large the stacks grow.
- **The stack layer stays explicit.** Each stack is created by its own method,
  which passes that stack's own arguments by name and wires the stacks it
  depends on (see :mod:`cdk_mate.tests.stack_enum`). A generic "create the
  stack of this context" helper would have to forward them through
  ``**kwargs``, which hides the signature from the reader and the IDE.

Every entry is a ``cached_property``: nothing is built, and no AWS call is made
(:meth:`~cdk_mate.stack_ctx.StackCtx.new` reads the account id of the boto
session), until an entry is first used, and then it is built once.

To add a stack or an environment, add one entry here and one in
:mod:`cdk_mate.tests.stack_enum`, with the same attribute name.
"""

from functools import cached_property

from ..stack_ctx import StackCtx
from .bsm_enum import bsm_enum


class StackCtxEnum:
    """
    One :class:`~cdk_mate.stack_ctx.StackCtx` per (stack, environment) pair,
    named ``<stack>_<environment>``, created on first use.
    """

    @cached_property
    def stack1_dev(self) -> StackCtx:
        return StackCtx.new(
            stack_name="cdk-mate-stack1-dev",
            bsm=bsm_enum.dev,
        )

    @cached_property
    def stack1_test(self) -> StackCtx:
        return StackCtx.new(
            stack_name="cdk-mate-stack1-test",
            bsm=bsm_enum.test,
        )

    @cached_property
    def stack2_dev(self) -> StackCtx:
        return StackCtx.new(
            stack_name="cdk-mate-stack2-dev",
            bsm=bsm_enum.dev,
        )

    @cached_property
    def stack2_test(self) -> StackCtx:
        return StackCtx.new(
            stack_name="cdk-mate-stack2-test",
            bsm=bsm_enum.test,
        )


stack_ctx_enum = StackCtxEnum()
