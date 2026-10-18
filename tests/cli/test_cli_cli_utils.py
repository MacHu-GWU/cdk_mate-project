# -*- coding: utf-8 -*-

from cdk_mate.cli.cli_utils import pos_arg
from cdk_mate.cli.cli_utils import value_arg
from cdk_mate.cli.cli_utils import bool_arg
from cdk_mate.cli.cli_utils import kv_arg
from cdk_mate.cli.cli_utils import array_arg
from cdk_mate.cli.cli_utils import count_arg
from cdk_mate.cli.cli_utils import run_cmd

import sys
import subprocess

import pytest
from func_args.api import OPT


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

        # Test with falsy value (should be ignored)
        args = []
        value_arg.process("stack", "", args)
        assert args == []

    def test_bool_arg(self):
        """Test BoolArg processes arguments correctly"""
        args = []

        # Test with True value
        bool_arg.process("help", True, args)
        assert args == ["--help"]

        # Test with False value (should be ignored)
        args = []
        bool_arg.process("help", False, args)
        assert args == []

        # Test with OPT value (should be ignored)
        args = []
        bool_arg.process("help", OPT, args)
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


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_utils",
        preview=False,
    )
