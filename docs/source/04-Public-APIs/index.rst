Public APIs
==============================================================================
Everything public is in ``cdk_mate.api``; the CDK CLI commands are in its ``cli`` namespace.

.. code-block:: python

    import cdk_mate.api as cdk_mate

    cdk_mate.StackCtx
    cdk_mate.cli.Deploy

Stack context:

- :class:`cdk_mate.api.StackCtx <cdk_mate.stack_ctx.StackCtx>`
- :meth:`cdk_mate.api.StackCtx.make_stack_ctx_kwargs <cdk_mate.stack_ctx.StackCtx.make_stack_ctx_kwargs>`
- :meth:`cdk_mate.api.StackCtx.new <cdk_mate.stack_ctx.StackCtx.new>`
- :meth:`cdk_mate.api.StackCtx.to_stack_kwargs <cdk_mate.stack_ctx.StackCtx.to_stack_kwargs>`
- :meth:`cdk_mate.api.StackCtx.cdk_synth <cdk_mate.stack_ctx.StackCtx.cdk_synth>`
- :meth:`cdk_mate.api.StackCtx.cdk_diff <cdk_mate.stack_ctx.StackCtx.cdk_diff>`
- :meth:`cdk_mate.api.StackCtx.cdk_deploy <cdk_mate.stack_ctx.StackCtx.cdk_deploy>`
- :meth:`cdk_mate.api.StackCtx.cdk_destroy <cdk_mate.stack_ctx.StackCtx.cdk_destroy>`
- :attr:`cdk_mate.api.StackCtx.stack_console_url <cdk_mate.stack_ctx.StackCtx.stack_console_url>`
- :func:`cdk_mate.api.build_cmd <cdk_mate.stack_ctx.build_cmd>`
- :func:`cdk_mate.api.cdk_synth_many <cdk_mate.stack_ctx.cdk_synth_many>`
- :func:`cdk_mate.api.cdk_diff_many <cdk_mate.stack_ctx.cdk_diff_many>`
- :func:`cdk_mate.api.cdk_deploy_many <cdk_mate.stack_ctx.cdk_deploy_many>`
- :func:`cdk_mate.api.cdk_destroy_many <cdk_mate.stack_ctx.cdk_destroy_many>`

Utilities:

- :func:`cdk_mate.api.to_camel <cdk_mate.utils.to_camel>`
- :func:`cdk_mate.api.to_slug <cdk_mate.utils.to_slug>`

CDK CLI commands, one class per command (see :mod:`cdk_mate.cli.cli_cmd`):

- :class:`cdk_mate.api.cli.BaseCommand <cdk_mate.cli.cli_cmd.BaseCommand>`
- :class:`cdk_mate.api.cli.Acknowledge <cdk_mate.cli.cli_cmd.Acknowledge>`
- :class:`cdk_mate.api.cli.Bootstrap <cdk_mate.cli.cli_cmd.Bootstrap>`
- :class:`cdk_mate.api.cli.CliTelemetry <cdk_mate.cli.cli_cmd.CliTelemetry>`
- :class:`cdk_mate.api.cli.Context <cdk_mate.cli.cli_cmd.Context>`
- :class:`cdk_mate.api.cli.Deploy <cdk_mate.cli.cli_cmd.Deploy>`
- :class:`cdk_mate.api.cli.Destroy <cdk_mate.cli.cli_cmd.Destroy>`
- :class:`cdk_mate.api.cli.Diagnose <cdk_mate.cli.cli_cmd.Diagnose>`
- :class:`cdk_mate.api.cli.Diff <cdk_mate.cli.cli_cmd.Diff>`
- :class:`cdk_mate.api.cli.Doctor <cdk_mate.cli.cli_cmd.Doctor>`
- :class:`cdk_mate.api.cli.Drift <cdk_mate.cli.cli_cmd.Drift>`
- :class:`cdk_mate.api.cli.Flags <cdk_mate.cli.cli_cmd.Flags>`
- :class:`cdk_mate.api.cli.GC <cdk_mate.cli.cli_cmd.GC>`
- :class:`cdk_mate.api.cli.Import <cdk_mate.cli.cli_cmd.Import>`
- :class:`cdk_mate.api.cli.Init <cdk_mate.cli.cli_cmd.Init>`
- :class:`cdk_mate.api.cli.List <cdk_mate.cli.cli_cmd.List>`
- :class:`cdk_mate.api.cli.Metadata <cdk_mate.cli.cli_cmd.Metadata>`
- :class:`cdk_mate.api.cli.Migrate <cdk_mate.cli.cli_cmd.Migrate>`
- :class:`cdk_mate.api.cli.Notices <cdk_mate.cli.cli_cmd.Notices>`
- :class:`cdk_mate.api.cli.Orphan <cdk_mate.cli.cli_cmd.Orphan>`
- :class:`cdk_mate.api.cli.PublishAssets <cdk_mate.cli.cli_cmd.PublishAssets>`
- :class:`cdk_mate.api.cli.Refactor <cdk_mate.cli.cli_cmd.Refactor>`
- :class:`cdk_mate.api.cli.Rollback <cdk_mate.cli.cli_cmd.Rollback>`
- :class:`cdk_mate.api.cli.Synth <cdk_mate.cli.cli_cmd.Synth>`
- :class:`cdk_mate.api.cli.Validate <cdk_mate.cli.cli_cmd.Validate>`
- :class:`cdk_mate.api.cli.Watch <cdk_mate.cli.cli_cmd.Watch>`
