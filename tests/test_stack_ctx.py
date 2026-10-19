# -*- coding: utf-8 -*-

from cdk_mate.stack_ctx import StackCtx
from cdk_mate.stack_ctx import build_cmd
from cdk_mate.stack_ctx import _get_bsm_for_many
from cdk_mate.stack_ctx import cdk_synth_many
from cdk_mate.stack_ctx import cdk_diff_many
from cdk_mate.stack_ctx import cdk_deploy_many
from cdk_mate.stack_ctx import cdk_destroy_many

import pytest
from func_args.api import ParamError

from cdk_mate.cli.cli_cmd import Synth
from cdk_mate.cli.cli_cmd import Diff
from cdk_mate.cli.cli_cmd import Deploy
from cdk_mate.cli.cli_cmd import Destroy

from cdk_mate.tests.mock_aws import BaseMockAwsTest


class TestStackCtx:
    def test_stack_ctx(self):
        stack_ctx = StackCtx(
            construct_id="MyStack",
            stack_name="my-stack",
            aws_account_id="123456789012",
            aws_region="us-east-1",
        )
        kwargs = stack_ctx.to_stack_kwargs()
        assert kwargs["id"] == "MyStack"
        assert kwargs["stack_name"] == "my-stack"
        assert kwargs["env"].account == "123456789012"
        assert kwargs["env"].region == "us-east-1"
        assert "filteringText=my-stack" in stack_ctx.stack_console_url

        with pytest.raises(ParamError):
            StackCtx()


def _make_ctx(name: str, account: str, bsm=None) -> StackCtx:
    return StackCtx(
        construct_id=name,
        stack_name=name,
        aws_account_id=account,
        aws_region="us-east-1",
        bsm=bsm,
    )


class TestBuildCmd:
    def test_synth(self):
        cmd = build_cmd(Synth, [_make_ctx("a", "111111111111")])
        assert isinstance(cmd, Synth)
        # only this stack, like diff / deploy / destroy
        assert cmd.to_args() == ["cdk", "synth", "a"]

    def test_synth_many(self):
        ctx_list = [
            _make_ctx("a", "111111111111"),
            _make_ctx("b", "111111111111"),
        ]
        assert build_cmd(Synth, ctx_list, quiet=True).to_args() == [
            "cdk",
            "synth",
            "a",
            "b",
            "--quiet",
        ]

    def test_diff_many(self):
        ctx_list = [
            _make_ctx("a", "111111111111"),
            _make_ctx("b", "111111111111"),
        ]
        assert build_cmd(Diff, ctx_list, fail=True).to_args() == [
            "cdk",
            "diff",
            "a",
            "b",
            "--fail",
        ]

    def test_deploy(self):
        ctx_list = [_make_ctx("a", "111111111111")]
        assert build_cmd(Deploy, ctx_list).to_args() == [
            "cdk",
            "deploy",
            "a",
            "--require-approval",
            "never",
        ]
        assert build_cmd(Deploy, ctx_list, prompt=True).to_args() == [
            "cdk",
            "deploy",
            "a",
        ]
        # an explicit field wins over the prompt default
        args = build_cmd(
            Deploy,
            ctx_list,
            require_approval="broadening",
            profile="my_profile",
        ).to_args()
        assert args == [
            "cdk",
            "deploy",
            "a",
            "--require-approval",
            "broadening",
            "--profile",
            "my_profile",
        ]

    def test_destroy(self):
        ctx_list = [_make_ctx("a", "111111111111")]
        assert build_cmd(Destroy, ctx_list).to_args() == [
            "cdk",
            "destroy",
            "a",
            "--force",
        ]
        assert build_cmd(Destroy, ctx_list, prompt=True).to_args() == [
            "cdk",
            "destroy",
            "a",
        ]
        assert build_cmd(Destroy, ctx_list, force=False).to_args() == [
            "cdk",
            "destroy",
            "a",
            "--no-force",
        ]

    def test_empty(self):
        with pytest.raises(ValueError):
            build_cmd(Deploy, [])


class TestGetBsmForMany:
    def test_empty(self):
        with pytest.raises(ValueError):
            _get_bsm_for_many([])
        # the *_many functions fail before running anything
        for func in [cdk_synth_many, cdk_diff_many, cdk_deploy_many, cdk_destroy_many]:
            with pytest.raises(ValueError):
                func([])

    def test_same_account(self, capsys: pytest.CaptureFixture):
        bsm = object()
        ctx_list = [
            _make_ctx("a", "111111111111", bsm=bsm),
            _make_ctx("b", "111111111111"),
        ]
        assert _get_bsm_for_many(ctx_list) is bsm
        assert "Warning" not in capsys.readouterr().out

    def test_mixed_accounts(self, capsys: pytest.CaptureFixture):
        bsm = object()
        ctx_list = [
            _make_ctx("a", "111111111111", bsm=bsm),
            _make_ctx("b", "222222222222"),
        ]
        assert _get_bsm_for_many(ctx_list) is bsm
        out = capsys.readouterr().out
        assert "Warning: these stacks target more than one AWS account" in out
        assert "'a'" in out


class TestStackCtxSynth(BaseMockAwsTest):
    """
    End-to-end: build StackCtx from (mocked) boto sessions, create the example
    stacks in ``cdk_mate/tests/stacks``, and synthesize them with aws-cdk-lib.
    Needs node on PATH (aws-cdk-lib's jsii runtime), but no AWS account.
    """

    def test_new(self):
        from cdk_mate.tests.stack_ctx_enum import stack_ctx_enum

        stack_ctx = stack_ctx_enum.stack1_dev
        assert stack_ctx.construct_id == "CdkMateStack1Dev"
        assert stack_ctx.stack_name == "cdk-mate-stack1-dev"
        assert stack_ctx.aws_account_id == "123456789012"  # moto's fake account
        assert stack_ctx.aws_region == "us-east-1"

    def test_synth(self):
        import aws_cdk as cdk
        from cdk_mate.tests.stack_enum import StackEnum

        stack_enum = StackEnum(app=cdk.App())
        _ = stack_enum.stack1_dev
        _ = stack_enum.stack1_test
        _ = stack_enum.stack2_dev
        _ = stack_enum.stack2_test

        cloud_assembly = stack_enum.app.synth()
        stack_names = {stack.stack_name for stack in cloud_assembly.stacks}
        assert stack_names == {
            "cdk-mate-stack1-dev",
            "cdk-mate-stack1-test",
            "cdk-mate-stack2-dev",
            "cdk-mate-stack2-test",
        }

        # per-environment argument: the log level of stack1 differs by environment
        for stack_name, log_level in [
            ("cdk-mate-stack1-dev", "DEBUG"),
            ("cdk-mate-stack1-test", "INFO"),
        ]:
            template = cloud_assembly.get_stack_by_name(stack_name).template
            types = [r["Type"] for r in template["Resources"].values()]
            assert sorted(types) == ["AWS::SNS::Topic", "AWS::SSM::Parameter"]
            parameter = _find_resource(template, "AWS::SSM::Parameter")
            assert parameter["Properties"]["Name"] == f"/{stack_name}/log-level"
            assert parameter["Properties"]["Value"] == log_level

        # dependency: stack2 imports the alert topic of stack1 in its own environment
        for env_name in ["dev", "test"]:
            stack1 = cloud_assembly.get_stack_by_name(f"cdk-mate-stack1-{env_name}")
            stack2 = cloud_assembly.get_stack_by_name(f"cdk-mate-stack2-{env_name}")
            # stack2 also depends on its own asset manifest, so check membership
            assert stack1.id in [dep.id for dep in stack2.dependencies]
            parameter = _find_resource(stack2.template, "AWS::SSM::Parameter")
            assert "Fn::ImportValue" in parameter["Properties"]["Value"]
            policy = _find_resource(stack2.template, "AWS::IAM::Policy")
            statement = policy["Properties"]["PolicyDocument"]["Statement"][0]
            assert statement["Action"] == "sns:Publish"
            assert "Fn::ImportValue" in statement["Resource"]

    def test_dependency_is_created_on_demand(self):
        import aws_cdk as cdk
        from cdk_mate.tests.stack_enum import StackEnum

        stack_enum = StackEnum(app=cdk.App())
        _ = stack_enum.stack2_dev  # creates stack1_dev, which it depends on
        _ = stack_enum.stack2_dev  # cached: no second instance

        cloud_assembly = stack_enum.app.synth()
        stack_names = {stack.stack_name for stack in cloud_assembly.stacks}
        assert stack_names == {
            "cdk-mate-stack1-dev",
            "cdk-mate-stack2-dev",
        }


def _find_resource(template: dict, resource_type: str) -> dict:
    resources = [
        r for r in template["Resources"].values() if r["Type"] == resource_type
    ]
    assert len(resources) == 1, resource_type
    return resources[0]


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.stack_ctx",
        preview=False,
    )
