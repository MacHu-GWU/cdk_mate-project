# -*- coding: utf-8 -*-

from cdk_mate.cli.cli_cmd_base import BaseCommandMixin

import sys
import dataclasses

from func_args.api import OPT

from cdk_mate.cli.cli_utils import bool_arg
from cdk_mate.cli.cli_cmd import BaseCommand
from cdk_mate.cli.cli_cmd import Deploy
from cdk_mate.cli.cli_cmd import Destroy
from cdk_mate.cli.cli_cmd import GC
from cdk_mate.cli.cli_cmd import Synth


def test_base_command_class():
    assert Deploy._base_command_class() is BaseCommand
    assert BaseCommand._base_command_class() is BaseCommand
    assert issubclass(BaseCommand, BaseCommandMixin)


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
    assert Synth(stacks=["StackA"], quiet=True, no_color=True).to_args() == [
        "cdk",
        "synth",
        "StackA",
        "--quiet",
        "--no-color",
    ]
    # False turns off an option that is on by default
    assert Deploy(rollback=False, staging=False).to_args() == [
        "cdk",
        "deploy",
        "--no-rollback",
        "--no-staging",
    ]
    assert GC(confirm=False).to_args() == ["cdk", "gc", "--no-confirm"]


def test_global_options():
    args = GC(
        unstable=["gc"],
        region="us-east-2",
        build="make",
    ).to_args()
    assert args == [
        "cdk",
        "gc",
        "--build",
        "make",
        "--region",
        "us-east-2",
        "--unstable",
        "gc",
    ]


def test_zero_and_empty_string():
    # 0 overrides a CLI default (gc's --created-buffer-days defaults to 1); "" passes nothing
    assert GC(created_buffer_days=0, bootstrap_stack_name="").to_args() == [
        "cdk",
        "gc",
        "--created-buffer-days",
        "0",
    ]
    assert Deploy(concurrency=0).to_args() == ["cdk", "deploy", "--concurrency", "0"]


def test_cdk_cmd():
    args = Synth(cdk_cmd=["npx", "aws-cdk@2.1145.0"], quiet=True).to_args()
    assert args == ["npx", "aws-cdk@2.1145.0", "synth", "--quiet"]


def test_extra_args():
    args = Deploy(
        stacks=["StackA"],
        profile="my_profile",
        extra_args=["--tags", "team=data"],
    ).to_args()
    assert args == [
        "cdk",
        "deploy",
        "StackA",
        "--profile",
        "my_profile",
        "--tags",
        "team=data",
    ]


def test_trailing_underscore_field():
    @dataclasses.dataclass
    class MySynth(Synth):
        # fmt: off
        global_: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
        # fmt: on

    assert MySynth(global_=True).to_args() == ["cdk", "synth", "--global"]


def test_run():
    # cdk_cmd makes run() testable without the cdk CLI:
    # "python -c 'import sys; ...' synth" exits 0 when argv[1] is "synth"
    cmd = Synth(
        cdk_cmd=[
            sys.executable,
            "-c",
            "import sys; sys.exit(sys.argv[1:] != ['synth'])",
        ],
    )
    result = cmd.run()
    assert result.returncode == 0


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_cmd_base",
        preview=False,
    )
