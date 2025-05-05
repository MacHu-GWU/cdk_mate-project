Public APIs
==============================================================================
The main public API is available through the cdk_mate.api module which provides access to all core functionality.

.. code-block:: python

    import cdk_mate.api as cdk_mate

Public API List:

- :class:`cdk_mate.Bootstrap <cdk_mate.cli.cli_cmd.Bootstrap>`
- :class:`cdk_mate.Synth <cdk_mate.cli.cli_cmd.Synth>`
- :class:`cdk_mate.Diff <cdk_mate.cli.cli_cmd.Diff>`
- :class:`cdk_mate.Deploy <cdk_mate.cli.cli_cmd.Deploy>`
- :class:`cdk_mate.Destroy <cdk_mate.cli.cli_cmd.Destroy>`
- :class:`cdk_mate.to_camel <cdk_mate.utils.to_camel>`
- :class:`cdk_mate.to_slug <cdk_mate.utils.to_slug>`
- :class:`cdk_mate.StackCtx <cdk_mate.stack_ctx.StackCtx>`
- :class:`cdk_mate.cdk_diff_many <cdk_mate.stack_ctx.cdk_diff_many>`
- :class:`cdk_mate.cdk_deploy_many <cdk_mate.stack_ctx.cdk_deploy_many>`
- :class:`cdk_mate.cdk_destroy_many <cdk_mate.stack_ctx.cdk_destroy_many>`
