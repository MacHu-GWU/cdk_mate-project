# -*- coding: utf-8 -*-

"""
Stack1: the alerts stack.

It owns an SNS topic that other stacks publish alerts to, and a log level that
differs per environment. Every resource is free: an SNS topic with no traffic
and a standard SSM parameter.

The stack definition follows the mixin pattern:

- ``iac_define.py``: the :class:`~cdk_mate.tests.stacks.stack1.iac_define.Stack1`
  class. Its ``__init__`` takes the standard arguments from
  :meth:`cdk_mate.stack_ctx.StackCtx.to_stack_kwargs` plus its own, explicit
  arguments, then calls one ``create_*`` method per mixin.
- ``iac_define_01_alerts.py``, ``iac_define_02_config.py``: one mixin per group
  of resources, so a large stack stays split into small files.
"""
