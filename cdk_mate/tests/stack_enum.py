# -*- coding: utf-8 -*-

"""
The CDK stacks of the example project: layer 2 of the two-layer pattern.

Layer 1, :mod:`cdk_mate.tests.stack_ctx_enum`, says *which* stacks exist and
where they go. This module says *how* each one is created: one method per
(stack, environment) pair, with the same name as its stack context.

Each method is a few lines, and they look alike, but this is where the stacks
differ, so each one is written out instead of generated:

- **Per-environment arguments, by name.** ``Stack1`` takes a ``log_level``:
  ``stack1_dev`` passes ``"DEBUG"`` and ``stack1_test`` passes ``"INFO"``. A new
  argument shows up in the stack's signature, and every method that must pass
  it fails until it does.
- **Dependencies between stacks.** ``Stack2`` takes the alert topic of
  ``Stack1``: ``stack2_dev`` passes ``self.stack1_dev.alert_topic``. Using
  ``stack2_dev`` therefore creates ``stack1_dev`` first, and CDK turns the
  reference into an export of Stack1 and an import in Stack2.
- **One instance per stack.** Each method is a ``cached_property``, so
  ``stack1_dev`` is created once however many stacks depend on it. Creating
  the same construct id twice in one ``cdk.App`` is an error.
- **Only what you ask for.** A stack is created on first use, so an app
  script creates just the stacks it names, plus their dependencies.

The ``cdk.App`` is passed in, not created at import time, so every app script
and every test gets a fresh app::

    import aws_cdk as cdk

    from cdk_mate.tests.stack_enum import StackEnum

    stack_enum = StackEnum(app=cdk.App())
    _ = stack_enum.stack2_dev  # also creates stack1_dev
    stack_enum.app.synth()
"""

import dataclasses
from functools import cached_property

import aws_cdk as cdk

from .stacks.stack1.iac_define import Stack1
from .stacks.stack2.iac_define import Stack2
from .stack_ctx_enum import stack_ctx_enum


@dataclasses.dataclass
class StackEnum:
    """
    One CDK stack per (stack, environment) pair, created in ``app`` on first
    use, named like its entry in
    :class:`~cdk_mate.tests.stack_ctx_enum.StackCtxEnum`.
    """

    # fmt: off
    app: cdk.App = dataclasses.field()
    # fmt: on

    @cached_property
    def stack1_dev(self) -> Stack1:
        return Stack1(
            scope=self.app,
            **stack_ctx_enum.stack1_dev.to_stack_kwargs(),
            log_level="DEBUG",
        )

    @cached_property
    def stack1_test(self) -> Stack1:
        return Stack1(
            scope=self.app,
            **stack_ctx_enum.stack1_test.to_stack_kwargs(),
            log_level="INFO",
        )

    @cached_property
    def stack2_dev(self) -> Stack2:
        return Stack2(
            scope=self.app,
            **stack_ctx_enum.stack2_dev.to_stack_kwargs(),
            alert_topic=self.stack1_dev.alert_topic,
        )

    @cached_property
    def stack2_test(self) -> Stack2:
        return Stack2(
            scope=self.app,
            **stack_ctx_enum.stack2_test.to_stack_kwargs(),
            alert_topic=self.stack1_test.alert_topic,
        )
