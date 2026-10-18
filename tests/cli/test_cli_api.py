# -*- coding: utf-8 -*-

from cdk_mate.cli import api


def test():
    _ = api
    _ = api.BaseCommand
    _ = api.Acknowledge
    _ = api.Bootstrap
    _ = api.CliTelemetry
    _ = api.Context
    _ = api.Deploy
    _ = api.Destroy
    _ = api.Diagnose
    _ = api.Diff
    _ = api.Doctor
    _ = api.Drift
    _ = api.Flags
    _ = api.GC
    _ = api.Import
    _ = api.Init
    _ = api.List
    _ = api.Metadata
    _ = api.Migrate
    _ = api.Notices
    _ = api.Orphan
    _ = api.PublishAssets
    _ = api.Refactor
    _ = api.Rollback
    _ = api.Synth
    _ = api.Validate
    _ = api.Watch


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.api",
        preview=False,
    )
