Public APIs
==============================================================================
The main public API is available through the cdk_mate.api module which provides access to all core functionality.

.. code-block:: python

    import cdk_mate.api as cdk_mate

Public API List:

- :class:`cdk_mate.api.Acknowledge <cdk_mate.cli.cli_cmd.Acknowledge>`
- :class:`cdk_mate.api.Bootstrap <cdk_mate.cli.cli_cmd.Bootstrap>`
- :class:`cdk_mate.api.Context <cdk_mate.cli.cli_cmd.Context>`
- :class:`cdk_mate.api.Deploy <cdk_mate.cli.cli_cmd.Deploy>`
- :class:`cdk_mate.api.Destroy <cdk_mate.cli.cli_cmd.Destroy>`
- :class:`cdk_mate.api.Diff <cdk_mate.cli.cli_cmd.Diff>`
- :class:`cdk_mate.api.GC <cdk_mate.cli.cli_cmd.GC>`
- :class:`cdk_mate.api.Import <cdk_mate.cli.cli_cmd.Import>`
- :class:`cdk_mate.api.Init <cdk_mate.cli.cli_cmd.Init>`
- :class:`cdk_mate.api.Synth <cdk_mate.cli.cli_cmd.Synth>`
- :class:`cdk_mate.api.to_camel <cdk_mate.utils.to_camel>`
- :class:`cdk_mate.api.to_slug <cdk_mate.utils.to_slug>`
- :class:`cdk_mate.api.StackCtx <cdk_mate.stack_ctx.StackCtx>`
- :meth:`cdk_mate.api.StackCtx.new <cdk_mate.stack_ctx.StackCtx.new>`
- :meth:`cdk_mate.api.StackCtx.to_stack_kwargs <cdk_mate.stack_ctx.StackCtx.to_stack_kwargs>`
- :meth:`cdk_mate.api.StackCtx.stack_console_url <cdk_mate.stack_ctx.StackCtx.stack_console_url>`
- :meth:`cdk_mate.api.StackCtx.cdk_synth <cdk_mate.stack_ctx.StackCtx.cdk_synth>`
- :meth:`cdk_mate.api.StackCtx.cdk_diff <cdk_mate.stack_ctx.StackCtx.cdk_diff>`
- :meth:`cdk_mate.api.StackCtx.cdk_deploy <cdk_mate.stack_ctx.StackCtx.cdk_deploy>`
- :meth:`cdk_mate.api.StackCtx.cdk_destroy <cdk_mate.stack_ctx.StackCtx.cdk_destroy>`
- :meth:`cdk_mate.api.cdk_diff_many <cdk_mate.stack_ctx.cdk_diff_many>`
- :meth:`cdk_mate.api.cdk_deploy_many <cdk_mate.stack_ctx.cdk_deploy_many>`
- :meth:`cdk_mate.api.cdk_destroy_many <cdk_mate.stack_ctx.cdk_destroy_many>`
