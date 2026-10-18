# -*- coding: utf-8 -*-

"""
The behavior shared by every command class in :mod:`cdk_mate.cli.cli_cmd`.

``cli_cmd.py`` is generated from the option registry of the CDK CLI and holds
only field definitions. Everything that turns those fields into a command line
and runs it lives here, in hand-written code.
"""

from __future__ import annotations

import typing as T
import dataclasses

from func_args.api import OPT

from .cli_utils import run_cdk_command

if T.TYPE_CHECKING:  # pragma: no cover
    from boto_session_manager.api import BotoSesManager

    from .cli_utils import T_PATH_ARG


class BaseCommandMixin:
    """
    Turn a command dataclass into a CDK command line, and run it.

    A command class is a dataclass whose fields are CLI options. Each option
    field carries its argument type in ``metadata["t"]`` (see
    :mod:`cdk_mate.cli.cli_utils`). The fields of ``BaseCommand``, the first
    dataclass that mixes this class in, are the global options; the fields a
    subclass adds are that command's own options and positional arguments.

    ``BaseCommand`` also defines two fields that are not CDK options:
    ``cdk_cmd``, the executable, and ``extra_args``, arguments appended verbatim.
    """

    def _subcommand(self) -> list[str]:  # pragma: no cover
        """
        Return the CDK subcommand, such as ``["deploy"]``.
        """
        raise NotImplementedError

    @classmethod
    def _base_command_class(cls) -> type:
        """
        Return ``BaseCommand``: the dataclass closest to the root of the MRO
        that mixes this class in. Its fields are the global options.
        """
        for klass in reversed(cls.__mro__):
            if dataclasses.is_dataclass(klass) and issubclass(klass, BaseCommandMixin):
                return klass
        raise TypeError(f"{cls} is not a command dataclass")  # pragma: no cover

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

        base_fields = dataclasses.fields(self._base_command_class())
        base_field_names = {field.name for field in base_fields}

        # command-specific fields first, so positional arguments follow the subcommand
        for field in dataclasses.fields(self):
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
    ):
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
