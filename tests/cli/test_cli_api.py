# -*- coding: utf-8 -*-

from cdk_mate.cli import api


def test():
    _ = api
    _ = api.BaseCommand
    _ = api.Acknowledge
    _ = api.Bootstrap
    _ = api.Context
    _ = api.Deploy
    _ = api.Destroy
    _ = api.Diff
    _ = api.GC
    _ = api.Import
    _ = api.Init
    _ = api.Synth


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.api",
        preview=False,
    )
