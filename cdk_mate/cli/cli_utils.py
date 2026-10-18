# -*- coding: utf-8 -*-

"""
Utility Functions for AWS CDK CLI Command Processing

This module provides a set of utility classes and functions for handling AWS CDK CLI
command arguments, execution contexts, and environment management.
"""

from __future__ import annotations

import typing as T
import os
import subprocess
from pathlib import Path

from func_args.api import OPT

if T.TYPE_CHECKING:  # pragma: no cover
    from boto_session_manager.api import BotoSesManager

#: A file system path: a ``str`` or any ``os.PathLike``, such as ``pathlib.Path``.
T_PATH_ARG = str | os.PathLike[str]


class BaseArgType:
    """
    Base class for CLI argument type processors.

    Defines the interface for processing different types of CLI arguments
    when building command lines for AWS CDK operations.
    """

    def process(
        self,
        name: str,
        value: T.Any,
        args: list[str],
    ):  # pragma: no cover
        """
        Process an argument for CLI commands.

        :param name: The name of the argument (without '--' prefix)
        :param value: The value of the argument, or ``OPT`` (not set), which
            passes nothing; func_args has no public type for ``OPT``, hence ``T.Any``
        :param args: The list of arguments to append the processed argument to

        :return: None, modifies the args list in-place
        """
        raise NotImplementedError


class PositionalArg(BaseArgType):
    """
    Process a positional argument for CLI commands.

    Example::

        name = "id"
        value = "my-stack"
        # will be encoded as
        "my-stack"
    """

    def process(
        self,
        name: str,
        value: T.Any,
        args: list[str],
    ):
        if value is OPT:
            return
        if value:
            if isinstance(value, list):
                for item in value:
                    args.append(str(item))
            else:
                args.append(str(value))


class ValueArg(BaseArgType):
    """
    Process a standard value argument for CLI commands.

    Example::

        name = "stack"
        value = "my-stack"
        # will be encoded as
        "--stack my-stack"
    """

    def process(
        self,
        name: str,
        value: T.Any,
        args: list[str],
    ):
        if value is OPT:
            return
        if value:
            args.append(f"--{name}")
            args.append(str(value))


class BoolArg(BaseArgType):
    """
    Process a boolean argument for CLI commands.

    ``True`` becomes ``--name`` and ``False`` becomes ``--no-name``, so an
    option that is on by default in the CDK CLI (``--rollback``, ``--staging``,
    ``--confirm``, ...) can be turned off. ``OPT`` and ``None`` pass nothing,
    leaving the CLI default. An option that is already negative, such as
    ``--no-color``, passes nothing for ``False``.

    Example::

        name = "rollback"
        value = True   # will be encoded as "--rollback"
        value = False  # will be encoded as "--no-rollback"
    """

    def process(
        self,
        name: str,
        value: T.Any,
        args: list[str],
    ):
        if value is OPT or value is None:
            return
        if value:
            args.append(f"--{name}")
        elif not name.startswith("no-"):
            args.append(f"--no-{name}")


class KeyValueArg(BaseArgType):
    """
    Process a key-value pair argument for CLI commands.

    Example::

        name = "parameter"
        value = {"key1": "value1", "key2": "value2"}
        # will be encoded as
        "--parameter key1=value1 --parameter key2=value2"
    """

    def process(
        self,
        name: str,
        value: T.Any,
        args: list[str],
    ):
        if value is OPT:
            return
        if value:
            for k, v in value.items():
                args.append(f"--{name}")
                args.append(f"{k}={v}")


class ArrayArg(BaseArgType):
    """
    Process array-type arguments for CLI commands.

    Example::

        name = "plugin"
        value = ["plugin1", "plugin2"]
        # will be encoded as
        "--plugin plugin1 --plugin plugin2"
    """

    def process(
        self,
        name: str,
        value: T.Any,
        args: list[str],
    ):
        if value is OPT:
            return
        if value:
            for item in value:
                args.append(f"--{name}")
                args.append(str(item))


class CountArg(BaseArgType):
    """
    Process count-based arguments for CLI commands.

    Example::

        name = "verbose"
        value = 2
        # will be encoded as
        "--verbose --verbose"
    """

    def process(
        self,
        name: str,
        value: T.Any,
        args: list[str],
    ):
        if value is OPT:
            return
        if value:
            for _ in range(value):
                args.append(f"--{name}")


pos_arg = PositionalArg()
value_arg = ValueArg()
bool_arg = BoolArg()
kv_arg = KeyValueArg()
array_arg = ArrayArg()
count_arg = CountArg()


def run_cmd_v1(
    args: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """
    Run a terminal command using subprocess with standard output.

    :param args: The command and its arguments
    :param cwd: Run the command in this directory; ``None`` means the current one
    :param env: The full environment of the command; ``None`` means inherit ours
    """
    cmd = " ".join(args)
    print("--- Run command ---")
    print(cmd)
    return subprocess.run(args, check=True, cwd=cwd, env=env)


def run_cmd_v2(
    args: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    show_output: bool = True,
) -> subprocess.CompletedProcess:  # pragma: no cover
    """
    Run a terminal command with advanced output handling.

    :param args: The command and its arguments
    :param cwd: Run the command in this directory; ``None`` means the current one
    :param env: The full environment of the command; ``None`` means inherit ours
    :param show_output: Print the captured stdout and stderr
    """
    try:
        result = subprocess.run(
            args,
            check=True,
            cwd=cwd,
            env=env,
            capture_output=True,
            encoding="utf-8",
        )
        if show_output:
            print(result.stdout)
            print(result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error code: {e.returncode}")
        print(f"Error message:\n{e.stderr}")
        raise


run_cmd = run_cmd_v1
# run_cmd = run_cmd_v2


#: Environment variables the AWS CLI and the CDK CLI read credentials from.
#: :func:`get_aws_cli_env` removes all of them first, so a value left in the
#: parent process can never mix with the boto session's credentials.
AWS_CRED_ENV_VARS = (
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "AWS_PROFILE",
)


def get_aws_cli_env(
    bsm: BotoSesManager,
    base_env: dict[str, str] | None = None,
) -> dict[str, str]:
    """
    Build the environment of a subprocess that should act as ``bsm``.

    A session created from a named profile passes ``AWS_PROFILE``, so the CLI
    resolves (and refreshes) the credentials itself. Any other session passes
    a frozen snapshot of its access key, secret key, and session token.
    ``AWS_REGION`` is always set. The current process is not changed.

    :param bsm: The boto session the subprocess should use
    :param base_env: The environment to start from; ``None`` means ``os.environ``

    :returns: A new dict, ready for the ``env`` argument of ``subprocess.run``
    """
    if base_env is None:
        env = dict(os.environ)
    else:
        env = dict(base_env)
    for key in AWS_CRED_ENV_VARS:
        env.pop(key, None)

    env["AWS_REGION"] = bsm.aws_region
    # boto_session_manager's "not set" sentinel is falsy, like None
    if bsm.profile_name:
        env["AWS_PROFILE"] = bsm.profile_name
    else:
        cred = bsm.boto_ses.get_credentials().get_frozen_credentials()
        env["AWS_ACCESS_KEY_ID"] = cred.access_key
        env["AWS_SECRET_ACCESS_KEY"] = cred.secret_key
        if cred.token is not None:
            env["AWS_SESSION_TOKEN"] = cred.token
    return env


def resolve_dir_cdk(dir_cdk: T_PATH_ARG) -> Path:
    """
    Resolve the directory a CDK command runs in.

    :param dir_cdk: A directory, or a file inside it, such as ``__file__`` of
        the deploy script next to ``cdk.json``

    :raises NotADirectoryError: If the path is neither a file nor a directory

    :returns: The absolute directory path
    """
    path = Path(dir_cdk).absolute()
    if path.is_file():
        path = path.parent
    if not path.is_dir():
        raise NotADirectoryError(f"{path} is not a directory!")
    return path


def print_aws_identity(bsm: BotoSesManager) -> None:
    """
    Print the AWS account and principal that ``bsm`` acts as, masked.

    This is informational only, so a failure (for example a role without
    ``iam:ListAccountAliases``, or expired credentials) prints a warning
    instead of raising. A real credential problem still surfaces when the
    CDK command runs.
    """
    try:
        bsm.print_who_am_i(masked=True)
    except Exception as e:
        print(f"Warning: cannot show the AWS identity ({type(e).__name__}: {e})")


def run_cdk_command(
    args: list[str],
    bsm: BotoSesManager | None = None,
    dir_cdk: T_PATH_ARG | None = None,
) -> subprocess.CompletedProcess:
    """
    Execute an AWS CDK command with optional AWS session and directory context.

    The directory and the credentials are handed to the subprocess only (its
    ``cwd`` and ``env``); the working directory and ``os.environ`` of the
    calling process never change, so this is safe to call from threads.

    :param args: List of CDK command arguments to execute
    :param bsm: Optional Boto Session Manager whose credentials the command uses
    :param dir_cdk: Optional directory (or a file in it) to run the command in

    :raises subprocess.CalledProcessError: If the command execution fails
    :raises NotADirectoryError: If ``dir_cdk`` does not exist

    :return: Completed process result from subprocess
    """
    cwd = None
    if dir_cdk is not None:
        cwd = resolve_dir_cdk(dir_cdk)
        print("--- Using CDK directory ---")
        print(cwd)
    env = None
    if bsm is not None:
        print("--- Using boto session ---")
        print_aws_identity(bsm)
        env = get_aws_cli_env(bsm)
    return run_cmd(args, cwd=cwd, env=env)
