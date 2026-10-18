# -*- coding: utf-8 -*-

"""
AWS CDK CLI Command Wrapper Classes

This module provides a class-based approach to AWS CDK CLI commands (bootstrap, synth,
deploy, destroy, etc.) with comprehensive option handling and flexible execution support.

.. code-block:: python

    # Deploy a stack with options
    Deploy(
        stacks=["MyStack"],
        profile="my_aws_profile",
        require_approval="never"
    ).run()

    # Destroy a stack with confirmation bypass
    Destroy(
        stacks=["MyStack"],
        force=True
    ).run()
"""

from __future__ import annotations

import typing as T
import dataclasses

from func_args.api import OPT
from func_args.api import BaseModel

from .cli_utils import pos_arg
from .cli_utils import value_arg
from .cli_utils import bool_arg
from .cli_utils import kv_arg
from .cli_utils import array_arg
from .cli_utils import count_arg
from .cli_utils import run_cdk_command

if T.TYPE_CHECKING:  # pragma: no cover
    from .cli_utils import T_PATH_ARG
    from boto_session_manager.api import BotoSesManager


@dataclasses.dataclass
class BaseCommand(BaseModel):
    """
    Base class for all CDK CLI commands.

    Implements common functionality for command execution:

    - Parameter validation
    - Argument processing and conversion
    - Command execution with AWS session integration

    All CDK commands inherit global options from this class, such as:

    - AWS profile and credentials management
    - Output formatting
    - Debug and verbose options
    - And many other global AWS CDK CLI options

    The class uses a metadata-driven approach to process different argument types,
    allowing for a clean, declarative command definition.

    Two fields are not CDK options; they control how the command line is built:

    - ``cdk_cmd``: the executable, ``["cdk"]`` by default. Use it to pin a CLI
      version per project, such as ``["npx", "aws-cdk@2.1145.0"]``.
    - ``extra_args``: arguments appended verbatim at the end, for any option
      this library does not define yet, such as ``["--tags", "team=data"]``.
      An option the installed CLI does not know is ignored by the CLI with a
      warning (exit code 0), so check that your CLI version supports it.
    """

    # fmt: off
    cdk_cmd: list[str] = dataclasses.field(default=OPT)
    extra_args: list[str] = dataclasses.field(default=OPT)
    app: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    asset_metadata: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    build: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    ca_bundle_path: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    ci: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    context: dict[str, str] = dataclasses.field(default=OPT, metadata={"t": kv_arg})
    debug: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    ec2creds: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    help: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    ignore_errors: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    json: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    lookups: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    no_color: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    notices: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    output: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    path_metadata: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    plugin: list[str] = dataclasses.field(default=OPT, metadata={"t": array_arg})
    profile: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    proxy: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    region: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    role_arn: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    staging: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    strict: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    trace: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    unstable: list[str] = dataclasses.field(default=OPT, metadata={"t": array_arg})
    verbose: int = dataclasses.field(default=OPT, metadata={"t": count_arg})
    version: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    version_reporting: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:  # pragma: no cover
        """
        Return the CDK subcommand, such as ``["deploy"]``.
        """
        raise NotImplementedError

    def _process(
        self,
        args: list[str],
        field: dataclasses.Field,
    ):
        """
        Process a field based on its metadata type.
        """
        name = field.name
        # a trailing "_" avoids a Python keyword, e.g. ``import_`` -> ``--import``
        if name.endswith("_"):
            name = name[:-1]
        name = name.replace("_", "-")
        field.metadata["t"].process(
            name=name,
            value=getattr(self, field.name),
            args=args,
        )

    def to_args(self) -> list[str]:
        """
        Convert the command object to a list of CLI arguments.
        """
        if self.cdk_cmd is OPT:
            args = ["cdk"]
        else:
            args = list(self.cdk_cmd)
        args.extend(self._subcommand())

        base_fields = dataclasses.fields(BaseCommand)
        base_field_names = {field.name for field in base_fields}

        # command-specific fields first, so positional arguments follow the subcommand
        for field in dataclasses.fields(self.__class__):
            if field.name not in base_field_names:
                self._process(args, field)

        # then the global options; cdk_cmd and extra_args have no "t" (arg type),
        # because they are not CDK options
        for field in base_fields:
            if "t" in field.metadata:
                self._process(args, field)

        if self.extra_args is not OPT:
            args.extend(self.extra_args)

        return args

    def run(
        self,
        bsm: BotoSesManager | None = None,
        dir_cdk: T_PATH_ARG | None = None,
    ):  # pragma: no cover
        """
        Execute the CDK command with the configured parameters.

        :param bsm: Optional Boto Session Manager for AWS credentials and context
        :param dir_cdk: Optional directory path for executing the CDK command

        :return: CompletedProcess instance with command execution results
        :raises subprocess.CalledProcessError: If the command execution fails
        """
        return run_cdk_command(
            args=self.to_args(),
            bsm=bsm,
            dir_cdk=dir_cdk,
        )


@dataclasses.dataclass
class Acknowledge(BaseCommand):
    """
    Acknowledge a notice by issue number and hide it from displaying again.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-ack.html
    """

    # fmt: off
    notice_id: str = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["acknowledge"]


@dataclasses.dataclass
class Bootstrap(BaseCommand):
    """
    Prepare an AWS environment for CDK deployments by deploying the CDK bootstrap stack,
    named ``CDKToolkit``, into the AWS environment.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-bootstrap.html
    """

    # fmt: off
    aws_environment: str = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    bootstrap_bucket_name: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    bootstrap_customer_key: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    bootstrap_kms_key_id: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    cloudformation_execution_policies: list[str] = dataclasses.field(default=OPT, metadata={"t": array_arg})
    custom_permissions_boundary: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    example_permissions_boundary: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    execute: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    force: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    previous_parameters: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    public_access_block_configuration: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    qualifier: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    show_template: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    tags: dict[str, str] = dataclasses.field(default=OPT, metadata={"t": kv_arg})
    template: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    termination_protection: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    toolkit_stack_name: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    trust: list[str] = dataclasses.field(default=OPT, metadata={"t": array_arg})
    trust_for_lookup: list[str] = dataclasses.field(default=OPT, metadata={"t": array_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["bootstrap"]


@dataclasses.dataclass
class Context(BaseCommand):
    """
    Manage cached context values for your AWS CDK application.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-context.html
    """

    # fmt: off
    clear: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    force: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    reset: str = dataclasses.field(default=OPT, metadata={"t": value_arg})

    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["context"]


@dataclasses.dataclass
class Deploy(BaseCommand):
    """
    Deploy AWS CDK stacks to AWS infrastructure with granular control over deployment parameters.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-deploy.html
    """

    # fmt: off
    stacks: list[str] = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    all: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    asset_parallelism: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    asset_prebuild: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    build_exclude: list[str] = dataclasses.field(default=OPT, metadata={"t": array_arg})
    change_set_name: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    concurrency: int = dataclasses.field(default=OPT, metadata={"t": value_arg})
    exclusively: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    force: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    hotswap: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    hotswap_fallback: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    ignore_no_stacks: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    import_existing_resources: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    logs: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    method: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    notification_arns: list[str] = dataclasses.field(default=OPT, metadata={"t": array_arg})
    outputs_file: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    parameters: dict[str, str] = dataclasses.field(default=OPT, metadata={"t": kv_arg})
    previous_parameters: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    progress: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    require_approval: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    rollback: bool | None = dataclasses.field(default=None, metadata={"t": bool_arg})
    toolkit_stack_name: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    watch: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["deploy"]


@dataclasses.dataclass
class Destroy(BaseCommand):
    """
    Safely remove AWS CDK stacks from infrastructure with flexible destruction options.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-deploy.html
    """

    # fmt: off
    stacks: list[str] = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    all: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    exclusively: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    force: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["destroy"]


@dataclasses.dataclass
class Diff(BaseCommand):
    """
    Compare deployed stacks with current state or a specific CloudFormation template.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html
    """

    # fmt: off
    stacks: list[str] = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    change_set: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    context_lines: int = dataclasses.field(default=OPT, metadata={"t": value_arg})
    exclusively: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    fail: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    processed: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    quiet: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    security_only: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    strict: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    template: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["diff"]


@dataclasses.dataclass
class GC(BaseCommand):
    """
    Perform garbage collection on unused assets stored in the resources of your bootstrap stack.

    Note: This command is still in development and requires the ``--unstable=gc``
    option, so pass ``unstable=["gc"]``.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-gc.html
    """

    # fmt: off
    aws_environment: list[str] = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    action: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    bootstrap_stack_name: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    confirm: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    created_buffer_days: int = dataclasses.field(default=OPT, metadata={"t": value_arg})
    rollback_buffer_days: int = dataclasses.field(default=OPT, metadata={"t": value_arg})
    type: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["gc"]


@dataclasses.dataclass
class Import(BaseCommand):
    """
    Import existing AWS resources into a CDK stack.

    This command allows you to take existing resources that were created using
    other methods and start managing them using the AWS CDK.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-import.html
    """

    # fmt: off
    stacks: list[str] = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    change_set_name: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    execute: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    force: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    record_resource_mapping: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    resource_mapping: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    rollback: bool | None = dataclasses.field(default=None, metadata={"t": bool_arg})
    toolkit_stack_name: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["import"]


@dataclasses.dataclass
class Init(BaseCommand):
    """
    Create a new AWS CDK project from a template.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-init.html
    """

    # fmt: off
    template_type: str = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    generate_only: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    language: str = dataclasses.field(default=OPT, metadata={"t": value_arg})
    list_: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})

    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["init"]


@dataclasses.dataclass
class Synth(BaseCommand):
    """
    Synthesize AWS CDK stacks into CloudFormation templates with comprehensive configuration options.

    Ref: https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-synth.html
    """

    # fmt: off
    stacks: list[str] = dataclasses.field(default=OPT, metadata={"t": pos_arg})
    exclusively: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    quiet: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    validation: bool = dataclasses.field(default=OPT, metadata={"t": bool_arg})
    # fmt: on

    def _subcommand(self) -> list[str]:
        return ["synth"]
