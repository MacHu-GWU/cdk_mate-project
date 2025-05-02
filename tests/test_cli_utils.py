# -*- coding: utf-8 -*-

import pytest
from cdk_mate.arg import NA
from cdk_mate.cli.cli_utils import (
    pos_arg,
    value_arg,
    bool_arg,
    kv_arg,
    array_arg,
    count_arg,
)


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

        # Test with NA value (should be ignored)
        args = []
        pos_arg.process("id", NA, args)
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

        # Test with NA value (should be ignored)
        args = []
        value_arg.process("stack", NA, args)
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

        # Test with NA value (should be ignored)
        args = []
        bool_arg.process("help", NA, args)
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

        # Test with NA value (should be ignored)
        args = []
        kv_arg.process("parameter", NA, args)
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

        # Test with NA value (should be ignored)
        args = []
        array_arg.process("plugin", NA, args)
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

        # Test with NA value (should be ignored)
        args = []
        count_arg.process("verbose", NA, args)
        assert args == []


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_utils",
        preview=False,
    )
