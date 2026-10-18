# -*- coding: utf-8 -*-

"""
Stack Context Management for AWS CDK Deployments

This module provides utilities for managing stack contexts across multiple
environments, enabling flexible and consistent infrastructure deployment.
"""

from __future__ import annotations

import typing as T
import dataclasses

import aws_cdk as cdk

from func_args.api import T_KWARGS
from func_args.api import REQ
from func_args.api import OPT
from func_args.api import BaseModel

from .cli.cli_cmd import Synth
from .cli.cli_cmd import Diff
from .cli.cli_cmd import Deploy
from .cli.cli_cmd import Destroy
from .utils import to_camel
from .utils import to_slug


if T.TYPE_CHECKING:  # pragma: no cover
    from boto_session_manager.api import BotoSesManager
    from .cli.cli_utils import T_PATH_ARG


@dataclasses.dataclass
class StackCtx(BaseModel):
    """
    Represents the configuration and deployment context for an AWS CDK stack.

    This dataclass encapsulates all necessary information for deploying
    a stack across different environments, providing a flexible and
    reusable approach to infrastructure management.

    - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk_mate/tests/stack_ctx_enum.py>`__

    :param construct_id: Unique identifier for the CDK construct
    :param stack_name: Descriptive name of the stack (used in AWS CloudFormation)
    :param aws_account_id: AWS Account ID where the stack will be deployed
    :param aws_region: AWS Region where the stack will be deployed
    :param bsm: Optional Boto Session Manager for AWS credentials
    """

    # fmt: off
    construct_id: str = dataclasses.field(default=REQ)
    stack_name: str = dataclasses.field(default=REQ)
    aws_account_id: str = dataclasses.field(default=REQ)
    aws_region: str = dataclasses.field(default=REQ)
    bsm: BotoSesManager | None = dataclasses.field(default=None)
    # fmt: on

    @classmethod
    def make_stack_ctx_kwargs(
        cls,
        stack_name: str,
        bsm: BotoSesManager,
    ) -> T_KWARGS:
        """
        Create a new StackCtx instance.
        """
        return {
            "construct_id": to_camel(stack_name),
            "stack_name": to_slug(stack_name),
            "aws_account_id": bsm.aws_account_id,
            "aws_region": bsm.aws_region,
            "bsm": bsm,
        }

    @classmethod
    def new(
        cls,
        stack_name: str,
        bsm: BotoSesManager,
    ):
        """
        Create a new StackCtx instance.
        """
        return cls(
            **cls.make_stack_ctx_kwargs(
                stack_name=stack_name,
                bsm=bsm,
            )
        )

    def to_stack_kwargs(self) -> dict[str, T.Any]:
        """
        Generate keyword arguments for CDK stack initialization. Your stack
        definition should look like this:

        .. code-block:: python

            import aws_cdk as cdk
            from constructs import Construct

            class MyStack(
                cdk.Stack,
            ):
                def __init__(
                    self,
                    scope: Construct,
                    id: str,
                    stack_name: str,
                    env: cdk.Environment,
                    ...
                ):
                    super().__init__(
                        scope=scope,
                        id=id,
                        stack_name=stack_name,
                        env=env,
                        ...
                    )
                    ...
        """
        return dict(
            id=self.construct_id,
            stack_name=self.stack_name,
            env=cdk.Environment(
                account=self.aws_account_id,
                region=self.aws_region,
            ),
        )

    @property
    def stack_console_url(self) -> str:
        """
        Generate the AWS CloudFormation console URL for this stack.
        """
        return (
            f"https://{self.aws_region}.console.aws.amazon.com/cloudformation"
            f"/home?region={self.aws_region}#/stacks?"
            f"filteringStatus=active&filteringText={self.stack_name}&viewNested=true"
        )

    def cdk_synth(
        self,
        dir_cdk: T_PATH_ARG | None = None,
        **kwargs: T_KWARGS,
    ):  # pragma: no cover
        """
        Synthesize the stack using AWS CDK CLI.

        - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/stack1/stack1_deploy.py>`__

        :param dir_cdk: Optional directory path for CDK synthesis context
        """
        print("--- Preview in AWS Console ---")
        print(f"{self.stack_name}: {self.stack_console_url}")
        cmd = Synth(
            **kwargs,
        )
        return cmd.run(bsm=self.bsm, dir_cdk=dir_cdk)

    def cdk_diff(
        self,
        dir_cdk: T_PATH_ARG | None = None,
        **kwargs: T_KWARGS,
    ):  # pragma: no cover
        """
        Show the differences between the current stack and the deployed stack.

        - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/stack1/stack1_deploy.py>`__

        :param dir_cdk: Optional directory path for CDK diff context
        """
        print("--- Preview in AWS Console ---")
        print(f"{self.stack_name}: {self.stack_console_url}")
        cmd = Diff(
            stacks=[self.construct_id],
            **kwargs,
        )
        return cmd.run(bsm=self.bsm, dir_cdk=dir_cdk)

    def cdk_deploy(
        self,
        dir_cdk: T_PATH_ARG | None = None,
        prompt: bool = False,
        **kwargs: T_KWARGS,
    ):  # pragma: no cover
        """
        Deploy the stack using AWS CDK CLI.

        - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/stack1/stack1_deploy.py>`__

        :param dir_cdk: Optional directory path for CDK deployment context
        :param prompt: Whether to prompt for approval before deployment
        """
        print("--- Preview in AWS Console ---")
        print(f"{self.stack_name}: {self.stack_console_url}")
        cmd = Deploy(
            stacks=[self.construct_id],
            require_approval=OPT if prompt else "never",
            **kwargs,
        )
        return cmd.run(bsm=self.bsm, dir_cdk=dir_cdk)

    def cdk_destroy(
        self,
        dir_cdk: T_PATH_ARG | None = None,
        prompt: bool = False,
        **kwargs: T_KWARGS,
    ):  # pragma: no cover
        """
        Destroy the stack using AWS CDK CLI.

        - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/stack1/stack1_deploy.py>`__

        :param dir_cdk: Optional directory path for CDK deployment context
        :param prompt: Whether to prompt for approval before destruction
        """
        print("--- Preview in AWS Console ---")
        print(f"{self.stack_name}: {self.stack_console_url}")
        cmd = Destroy(
            stacks=[self.construct_id],
            force=OPT if prompt else True,
            **kwargs,
        )
        return cmd.run(bsm=self.bsm, dir_cdk=dir_cdk)


def cdk_diff_many(
    stack_ctx_list: list[StackCtx],
    dir_cdk: T_PATH_ARG | None = None,
    **kwargs: T_KWARGS,
):  # pragma: no cover
    """
    Show the differences between multiple stacks and their deployed versions.

    - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/deploy.py>`__

    :param stack_ctx_list: List of stack contexts to compare
    :param dir_cdk: Optional directory path for CDK context
    """
    print("--- Preview in AWS Console ---")
    for stack_ctx in stack_ctx_list:
        print(f"{stack_ctx.stack_name}: {stack_ctx.stack_console_url}")
    cmd = Diff(
        stacks=[stack_ctx.construct_id for stack_ctx in stack_ctx_list],
        **kwargs,
    )
    return cmd.run(bsm=stack_ctx_list[0].bsm, dir_cdk=dir_cdk)


def cdk_deploy_many(
    stack_ctx_list: list[StackCtx],
    dir_cdk: T_PATH_ARG | None = None,
    prompt: bool = False,
    **kwargs: T_KWARGS,
):  # pragma: no cover
    """
    Deploy multiple stacks in a single operation.

    - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/deploy.py>`__

    :param stack_ctx_list: List of stack contexts to deploy
    :param dir_cdk: Optional directory path for CDK deployment context
    :param prompt: Whether to prompt for approval before deployment
    """
    print("--- Preview in AWS Console ---")
    for stack_ctx in stack_ctx_list:
        print(f"{stack_ctx.stack_name}: {stack_ctx.stack_console_url}")
    cmd = Deploy(
        stacks=[stack_ctx.construct_id for stack_ctx in stack_ctx_list],
        require_approval=OPT if prompt else "never",
        **kwargs,
    )
    return cmd.run(bsm=stack_ctx_list[0].bsm, dir_cdk=dir_cdk)


def cdk_destroy_many(
    stack_ctx_list: list[StackCtx],
    dir_cdk: T_PATH_ARG | None = None,
    prompt: bool = False,
    **kwargs: T_KWARGS,
):  # pragma: no cover
    """
    Destroy multiple stacks in a single operation.

    - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/deploy.py>`__

    :param stack_ctx_list: List of stack contexts to destroy
    :param dir_cdk: Optional directory path for CDK deployment context
    :param prompt: Whether to prompt for approval before destruction
    """
    print("--- Preview in AWS Console ---")
    for stack_ctx in stack_ctx_list:
        print(f"{stack_ctx.stack_name}: {stack_ctx.stack_console_url}")
    cmd = Destroy(
        stacks=[stack_ctx.construct_id for stack_ctx in stack_ctx_list],
        force=OPT if prompt else True,
        **kwargs,
    )
    return cmd.run(bsm=stack_ctx_list[0].bsm, dir_cdk=dir_cdk)
