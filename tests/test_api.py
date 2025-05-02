# -*- coding: utf-8 -*-

from cdk_mate import api


def test():
    _ = api
    _ = api.cli.synth
    _ = api.cli.deploy
    _ = api.cli.destroy
    _ = api.StackCtx
    _ = api.to_camel
    _ = api.to_slug


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.api",
        preview=False,
    )
