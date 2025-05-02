# -*- coding: utf-8 -*-

from cdk_mate import api


def test():
    _ = api
    _ = api.cli.Bootstrap
    _ = api.cli.Synth
    _ = api.cli.Diff
    _ = api.cli.Deploy
    _ = api.cli.Destroy
    _ = api.StackCtx
    _ = api.cdk_diff_many
    _ = api.cdk_deploy_many
    _ = api.cdk_destroy_many
    _ = api.to_camel
    _ = api.to_slug


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.api",
        preview=False,
    )
