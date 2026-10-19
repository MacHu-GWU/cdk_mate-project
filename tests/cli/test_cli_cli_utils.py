# -*- coding: utf-8 -*-

from cdk_mate.cli.cli_utils import pos_arg
from cdk_mate.cli.cli_utils import value_arg
from cdk_mate.cli.cli_utils import bool_arg
from cdk_mate.cli.cli_utils import kv_arg
from cdk_mate.cli.cli_utils import array_arg
from cdk_mate.cli.cli_utils import count_arg
from cdk_mate.cli.cli_utils import run_cmd
from cdk_mate.cli.cli_utils import get_aws_cli_env
from cdk_mate.cli.cli_utils import resolve_dir_cdk
from cdk_mate.cli.cli_utils import log_aws_identity
from cdk_mate.cli.cli_utils import run_cdk_command

import os
import sys
import json
import logging
import subprocess
from pathlib import Path

import pytest
from func_args.api import OPT
from boto_session_manager.api import BotoSesManager

from cdk_mate.logger import logger
from cdk_mate.tests.mock_aws import BaseMockAwsTest

#: A child Python process that dumps its working directory and AWS env vars
#: to the JSON file given as its first argument.
DUMP_SCRIPT = """
import os, sys, json
keys = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "AWS_PROFILE", "AWS_REGION"]
data = {"cwd": os.getcwd(), "env": {k: os.environ.get(k) for k in keys}}
with open(sys.argv[1], "w") as f:
    json.dump(data, f)
"""


class TestArgumentTypes:
    def test_positional_arg(self):
        """Test PositionalArg processes arguments correctly"""
        args = []

        # Test with single value
        pos_arg.process("id", "my-stack", args)
        assert args == ["my-stack"]

        # Test with list of values
        args = []
        pos_arg.process("ids", ["stack1", "stack2"], args)
        assert args == ["stack1", "stack2"]

        # Test with OPT value (should be ignored)
        args = []
        pos_arg.process("id", OPT, args)
        assert args == []

        # Test with falsy value (should be ignored)
        args = []
        pos_arg.process("id", "", args)
        assert args == []

        # Test with None value (should be ignored)
        args = []
        pos_arg.process("id", None, args)
        assert args == []

        # Test with 0 (a real value, passed)
        args = []
        pos_arg.process("id", 0, args)
        assert args == ["0"]

        # Test with empty and None items in a list (skipped), 0 kept
        args = []
        pos_arg.process("ids", ["stack1", "", None, OPT, 0], args)
        assert args == ["stack1", "0"]

        # Test with an empty list (nothing)
        args = []
        pos_arg.process("ids", [], args)
        assert args == []

    def test_value_arg(self):
        """Test ValueArg processes arguments correctly"""
        args = []

        # Test with value
        value_arg.process("stack", "my-stack", args)
        assert args == ["--stack", "my-stack"]

        # Test with OPT value (should be ignored)
        args = []
        value_arg.process("stack", OPT, args)
        assert args == []

        # Test with empty string (should be ignored)
        args = []
        value_arg.process("stack", "", args)
        assert args == []

        # Test with None value (should be ignored)
        args = []
        value_arg.process("stack", None, args)
        assert args == []

        # Test with 0 (a real value, passed): it can override a CLI default
        args = []
        value_arg.process("created-buffer-days", 0, args)
        assert args == ["--created-buffer-days", "0"]

    def test_bool_arg(self):
        """Test BoolArg processes arguments correctly"""
        args = []

        # Test with True value
        bool_arg.process("rollback", True, args)
        assert args == ["--rollback"]

        # Test with False value (turns off an option that is on by default)
        args = []
        bool_arg.process("rollback", False, args)
        assert args == ["--no-rollback"]

        # Test with an already negative option: False is its default
        args = []
        bool_arg.process("no-color", True, args)
        assert args == ["--no-color"]
        args = []
        bool_arg.process("no-color", False, args)
        assert args == []

        # Test with OPT and None value (should be ignored)
        args = []
        bool_arg.process("rollback", OPT, args)
        bool_arg.process("rollback", None, args)
        assert args == []

    def test_key_value_arg(self):
        """Test KeyValueArg processes arguments correctly"""
        args = []

        # Test with dictionary
        kv_arg.process("parameter", {"key1": "value1", "key2": "value2"}, args)
        # Check either order since dictionaries are unordered
        assert "--parameter" in args
        assert "key1=value1" in args
        assert "key2=value2" in args
        assert len(args) == 4

        # Test with OPT value (should be ignored)
        args = []
        kv_arg.process("parameter", OPT, args)
        assert args == []

        # Test with empty dictionary (should be ignored)
        args = []
        kv_arg.process("parameter", {}, args)
        assert args == []

    def test_array_arg(self):
        """Test ArrayArg processes arguments correctly"""
        args = []

        # Test with list
        array_arg.process("plugin", ["plugin1", "plugin2"], args)
        assert args == ["--plugin", "plugin1", "--plugin", "plugin2"]

        # Test with OPT value (should be ignored)
        args = []
        array_arg.process("plugin", OPT, args)
        assert args == []

        # Test with empty list (should be ignored)
        args = []
        array_arg.process("plugin", [], args)
        assert args == []

    def test_count_arg(self):
        """Test CountArg processes arguments correctly"""
        args = []

        # Test with positive count
        count_arg.process("verbose", 2, args)
        assert args == ["--verbose", "--verbose"]

        # Test with zero count (should be ignored)
        args = []
        count_arg.process("verbose", 0, args)
        assert args == []

        # Test with OPT value (should be ignored)
        args = []
        count_arg.process("verbose", OPT, args)
        assert args == []


def test_run_cmd():
    # sys.executable, not "pip": a uv-managed .venv has no pip
    run_cmd([sys.executable, "--version"])

    with pytest.raises(subprocess.CalledProcessError):
        run_cmd([sys.executable, "-c", "raise SystemExit(1)"])

    with pytest.raises(FileNotFoundError):
        run_cmd(["invalid-command"])


def test_run_cmd_logs_a_runnable_line(capsys: pytest.CaptureFixture):
    # an argument with a space is quoted, so the logged line can be copied and run
    run_cmd([sys.executable, "-c", "print('a b')"])
    out = capsys.readouterr().out
    assert "-c 'print('\"'\"'a b'\"'\"')'" in out


def test_run_cmd_cwd_and_env(tmp_path: Path):
    path_out = tmp_path / "out.json"
    env = {**os.environ, "AWS_REGION": "eu-west-1"}
    run_cmd([sys.executable, "-c", DUMP_SCRIPT, str(path_out)], cwd=tmp_path, env=env)
    data = json.loads(path_out.read_text())
    assert Path(data["cwd"]).resolve() == tmp_path.resolve()
    assert data["env"]["AWS_REGION"] == "eu-west-1"


class TestGetAwsCliEnv:
    def test_access_key(self):
        bsm = BotoSesManager(
            aws_access_key_id="AKID",
            aws_secret_access_key="SECRET",
            aws_session_token="TOKEN",
            region_name="us-east-2",
        )
        base_env = {
            "AWS_PROFILE": "stale_profile",  # must not leak into the subprocess
            "AWS_SESSION_TOKEN": "stale_token",
            "OTHER": "kept",
        }
        env = get_aws_cli_env(bsm, base_env=base_env)
        assert env == {
            "OTHER": "kept",
            "AWS_REGION": "us-east-2",
            "AWS_ACCESS_KEY_ID": "AKID",
            "AWS_SECRET_ACCESS_KEY": "SECRET",
            "AWS_SESSION_TOKEN": "TOKEN",
        }
        # the caller's dict is left alone
        assert base_env["AWS_PROFILE"] == "stale_profile"

    def test_access_key_without_token(self):
        bsm = BotoSesManager(
            aws_access_key_id="AKID",
            aws_secret_access_key="SECRET",
            region_name="us-east-2",
        )
        env = get_aws_cli_env(bsm, base_env={"AWS_SESSION_TOKEN": "stale_token"})
        assert "AWS_SESSION_TOKEN" not in env
        assert env["AWS_ACCESS_KEY_ID"] == "AKID"

    def test_profile(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        path_config = tmp_path / "config"
        path_config.write_text("[profile cdk_mate_test]\nregion = ap-northeast-1\n")
        monkeypatch.setenv("AWS_CONFIG_FILE", str(path_config))
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "stale_key")
        bsm = BotoSesManager(profile_name="cdk_mate_test")
        env = get_aws_cli_env(bsm)
        assert env["AWS_PROFILE"] == "cdk_mate_test"
        assert env["AWS_REGION"] == "ap-northeast-1"
        assert "AWS_ACCESS_KEY_ID" not in env
        # the current process is not changed
        assert os.environ["AWS_ACCESS_KEY_ID"] == "stale_key"


def test_resolve_dir_cdk(tmp_path: Path):
    path_file = tmp_path / "deploy.py"
    path_file.write_text("")
    assert resolve_dir_cdk(tmp_path) == tmp_path.absolute()
    assert resolve_dir_cdk(str(path_file)) == tmp_path.absolute()
    with pytest.raises(NotADirectoryError):
        resolve_dir_cdk(tmp_path / "not-exists")


class TestLogAwsIdentity(BaseMockAwsTest):
    def test_ok(self, capsys: pytest.CaptureFixture):
        bsm = BotoSesManager(region_name="us-east-1")
        log_aws_identity(bsm)
        out = capsys.readouterr().out
        assert "AWS Account Id = 12" in out
        assert "Principal Arn = " in out
        assert "AWS Region = us-east-1" in out

    def test_failure_is_a_warning(self, capsys: pytest.CaptureFixture):
        class ExpiredBsm:
            @property
            def masked_aws_account_id(self):
                raise PermissionError("ExpiredToken")

        log_aws_identity(ExpiredBsm())
        out = capsys.readouterr().out
        assert "Warning: cannot show the AWS identity" in out
        assert "PermissionError" in out

    def test_no_aws_call_when_silenced(self, capsys: pytest.CaptureFixture):
        class ForbiddenBsm:
            def __getattr__(self, name):
                raise AssertionError(f"unexpected AWS call: {name}")

        logger.setLevel(logging.WARNING)
        try:
            log_aws_identity(ForbiddenBsm())
        finally:
            logger.setLevel(logging.INFO)
        assert capsys.readouterr().out == ""


class TestRunCdkCommand(BaseMockAwsTest):
    def test_without_bsm(self, tmp_path: Path):
        cwd_before = os.getcwd()
        path_out = tmp_path / "out.json"
        run_cdk_command(
            [sys.executable, "-c", DUMP_SCRIPT, str(path_out)],
            dir_cdk=tmp_path,
        )
        data = json.loads(path_out.read_text())
        assert Path(data["cwd"]).resolve() == tmp_path.resolve()
        assert os.getcwd() == cwd_before

    def test_with_bsm(self, tmp_path: Path):
        env_before = dict(os.environ)
        bsm = BotoSesManager(
            aws_access_key_id="AKID",
            aws_secret_access_key="SECRET",
            region_name="us-west-2",
        )
        path_out = tmp_path / "out.json"
        run_cdk_command(
            [sys.executable, "-c", DUMP_SCRIPT, str(path_out)],
            bsm=bsm,
        )
        data = json.loads(path_out.read_text())
        assert data["env"]["AWS_ACCESS_KEY_ID"] == "AKID"
        assert data["env"]["AWS_SECRET_ACCESS_KEY"] == "SECRET"
        assert data["env"]["AWS_REGION"] == "us-west-2"
        assert data["env"]["AWS_PROFILE"] is None
        assert dict(os.environ) == env_before


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_utils",
        preview=False,
    )
