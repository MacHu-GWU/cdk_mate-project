# -*- coding: utf-8 -*-

from cdk_mate import api


def test():
    _ = api
    _ = api.cli.BaseCommand
    _ = api.cli.Acknowledge
    _ = api.cli.Bootstrap
    _ = api.cli.Context
    _ = api.cli.Deploy
    _ = api.cli.Destroy
    _ = api.cli.Diff
    _ = api.cli.GC
    _ = api.cli.Import
    _ = api.cli.Init
    _ = api.cli.Synth
    _ = api.to_camel
    _ = api.to_slug
    _ = api.StackCtx
    _ = api.StackCtx.make_stack_ctx_kwargs
    _ = api.StackCtx.new
    _ = api.StackCtx.to_stack_kwargs
    _ = api.StackCtx.stack_console_url
    _ = api.StackCtx.cdk_synth
    _ = api.StackCtx.cdk_diff
    _ = api.StackCtx.cdk_deploy
    _ = api.StackCtx.cdk_destroy
    _ = api.cdk_diff_many
    _ = api.cdk_deploy_many
    _ = api.cdk_destroy_many


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.api",
        preview=False,
    )
