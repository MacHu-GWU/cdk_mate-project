# -*- coding: utf-8 -*-

from cdk_mate.cli.cli_cmd import Acknowledge
from cdk_mate.cli.cli_cmd import Bootstrap
from cdk_mate.cli.cli_cmd import Context
from cdk_mate.cli.cli_cmd import Deploy
from cdk_mate.cli.cli_cmd import Destroy
from cdk_mate.cli.cli_cmd import Diff
from cdk_mate.cli.cli_cmd import GC
from cdk_mate.cli.cli_cmd import Import
from cdk_mate.cli.cli_cmd import Init
from cdk_mate.cli.cli_cmd import Synth

import dataclasses

from func_args.api import OPT

from cdk_mate.cli.cli_utils import bool_arg


def test_subcommand():
    # fmt: off
    cases = [
        (Acknowledge, ["cdk", "acknowledge"]),
        (Bootstrap, ["cdk", "bootstrap"]),
        (Context, ["cdk", "context"]),
        (Deploy, ["cdk", "deploy"]),
        (Destroy, ["cdk", "destroy"]),
        (Diff, ["cdk", "diff"]),
        (GC, ["cdk", "gc"]),
        (Import, ["cdk", "import"]),
        (Init, ["cdk", "init"]),
        (Synth, ["cdk", "synth"]),
    ]
    # fmt: on
    for klass, expected in cases:
        assert klass().to_args() == expected


def test_command_options_before_global_options():
    args = Deploy(
        stacks=["StackA", "StackB"],
        require_approval="never",
        parameters={"Env": "dev"},
        profile="my_profile",
        verbose=2,
    ).to_args()
    assert args == [
        "cdk",
        "deploy",
        "StackA",
        "StackB",
        "--parameters",
        "Env=dev",
        "--require-approval",
        "never",
        "--profile",
        "my_profile",
        "--verbose",
        "--verbose",
    ]


def test_bool_option():
    assert Destroy(stacks=["StackA"], force=True).to_args() == [
        "cdk",
        "destroy",
        "StackA",
        "--force",
    ]
    assert Synth(quiet=True, no_color=True).to_args() == [
        "cdk",
        "synth",
        "--quiet",
        "--no-color",
    ]


def test_trailing_underscore_field():
    @dataclasses.dataclass
    class MySynth(Synth):
        # fmt: off
        global_: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
        # fmt: on

    assert MySynth(global_=True).to_args() == ["cdk", "synth", "--global"]


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_cmd",
        preview=False,
    )
