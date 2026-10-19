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

from .cli.cli_cmd import BaseCommand
from .cli.cli_cmd import Synth
from .cli.cli_cmd import Diff
from .cli.cli_cmd import Deploy
from .cli.cli_cmd import Destroy
from .utils import to_camel
from .utils import to_slug
from .logger import logger


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
        Build the keyword arguments of a :class:`StackCtx` from one name and a
        boto session, without creating it.

        ``construct_id`` is ``stack_name`` in CamelCase (:func:`~cdk_mate.utils.to_camel`),
        ``stack_name`` is its slug (:func:`~cdk_mate.utils.to_slug`), and the
        account and region come from ``bsm``. Override this classmethod in a
        subclass to change the naming, or add fields to the returned dict.

        :param stack_name: The name of the stack, such as ``"my-app-dev"``
        :param bsm: The boto session that deploys the stack; reading its
            account id makes one ``sts:GetCallerIdentity`` call

        :returns: The keyword arguments of :class:`StackCtx`
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
    ) -> T.Self:
        """
        Create a new StackCtx instance from one name and a boto session, with
        the keyword arguments of :meth:`make_stack_ctx_kwargs`.

        :param stack_name: The name of the stack, such as ``"my-app-dev"``
        :param bsm: The boto session that deploys the stack
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
        cmd = build_cmd(Synth, [self], **kwargs)
        return _run_cmd_for_many(cmd, [self], dir_cdk=dir_cdk)

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
        cmd = build_cmd(Diff, [self], **kwargs)
        return _run_cmd_for_many(cmd, [self], dir_cdk=dir_cdk)

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
        cmd = build_cmd(Deploy, [self], prompt=prompt, **kwargs)
        return _run_cmd_for_many(cmd, [self], dir_cdk=dir_cdk)

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
        cmd = build_cmd(Destroy, [self], prompt=prompt, **kwargs)
        return _run_cmd_for_many(cmd, [self], dir_cdk=dir_cdk)


T_CMD = T.TypeVar("T_CMD", bound=BaseCommand)


def build_cmd(
    cmd_class: type[T_CMD],
    stack_ctx_list: list[StackCtx],
    prompt: bool = False,
    **kwargs: T_KWARGS,
) -> T_CMD:
    """
    Build the CDK command that targets the given stacks, without running it.

    Every ``cdk_*`` method of :class:`StackCtx` and every ``cdk_*_many``
    function builds its command here, then runs it. Call it yourself to
    inspect the command line (``build_cmd(...).to_args()``), or to adjust the
    command before ``.run()``.

    ``stacks`` is set to the construct ids of ``stack_ctx_list``, in order.
    ``prompt`` matters only for :class:`~cdk_mate.cli.cli_cmd.Deploy` and
    :class:`~cdk_mate.cli.cli_cmd.Destroy`: ``False`` (the default) passes
    ``--require-approval never`` or ``--force``, so nothing waits for a human;
    ``True`` passes neither, leaving the CLI to ask. Any field in ``kwargs``
    wins over these defaults, such as ``require_approval="broadening"``.

    Example::

        build_cmd(Deploy, [stack_ctx]).to_args()
        # ["cdk", "deploy", "MyStack", "--require-approval", "never"]

    :param cmd_class: A command class with a ``stacks`` field, such as
        :class:`~cdk_mate.cli.cli_cmd.Deploy`
    :param stack_ctx_list: The stacks the command targets
    :param prompt: Whether a deploy or destroy should ask for approval
    :param kwargs: Any other field of ``cmd_class``

    :raises ValueError: If ``stack_ctx_list`` is empty
    """
    if len(stack_ctx_list) == 0:
        raise ValueError("stack_ctx_list is empty, there is no stack to run")
    params = {"stacks": [stack_ctx.construct_id for stack_ctx in stack_ctx_list]}
    if issubclass(cmd_class, Deploy):
        params["require_approval"] = OPT if prompt else "never"
    elif issubclass(cmd_class, Destroy):
        params["force"] = OPT if prompt else True
    params.update(kwargs)
    return cmd_class(**params)


def _get_bsm_for_many(
    stack_ctx_list: list[StackCtx],
) -> BotoSesManager | None:
    """
    Pick the boto session that runs one CDK command for many stacks.

    All stacks run with the credentials of the first one. Stacks in other
    accounts or regions are allowed, because the CDK CLI can deploy them when
    those accounts trust this one (``cdk bootstrap --trust``), but a warning is
    printed, since a mixed list is more often a mistake.

    When the first stack has no ``bsm``, this returns ``None``, and the command
    runs with the default credentials of the environment, as
    :meth:`StackCtx.cdk_deploy` and its siblings do for a stack without ``bsm``.

    :raises ValueError: If ``stack_ctx_list`` is empty
    """
    if len(stack_ctx_list) == 0:
        raise ValueError("stack_ctx_list is empty, there is no stack to run")
    first = stack_ctx_list[0]
    targets = {(ctx.aws_account_id, ctx.aws_region) for ctx in stack_ctx_list}
    if len(targets) > 1:
        logger.warning(
            "Warning: these stacks target more than one AWS account or region, "
            f"and all of them run with the credentials of {first.stack_name!r}. "
            "This works only if the other accounts trust that account "
            "(cdk bootstrap --trust)."
        )
    return first.bsm


def _run_cmd_for_many(
    cmd: BaseCommand,
    stack_ctx_list: list[StackCtx],
    dir_cdk: T_PATH_ARG | None = None,
):  # pragma: no cover
    """
    Print the console URL of each stack, then run ``cmd`` with the
    credentials of the first stack.
    """
    bsm = _get_bsm_for_many(stack_ctx_list)
    logger.info("--- Preview in AWS Console ---")
    for stack_ctx in stack_ctx_list:
        logger.info(f"{stack_ctx.stack_name}: {stack_ctx.stack_console_url}")
    return cmd.run(bsm=bsm, dir_cdk=dir_cdk)


def cdk_synth_many(
    stack_ctx_list: list[StackCtx],
    dir_cdk: T_PATH_ARG | None = None,
    **kwargs: T_KWARGS,
):  # pragma: no cover
    """
    Synthesize multiple stacks in a single operation.

    The CDK CLI runs the whole app either way; naming the stacks selects
    which templates (and dependencies) it reports. To synthesize every stack
    of the app, run ``cdk_mate.api.cli.Synth().run(dir_cdk=...)`` instead.

    - `Usage Example <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/deploy.py>`__

    :param stack_ctx_list: List of stack contexts to synthesize
    :param dir_cdk: Optional directory path for CDK synthesis context

    :raises ValueError: If ``stack_ctx_list`` is empty
    """
    cmd = build_cmd(Synth, stack_ctx_list, **kwargs)
    return _run_cmd_for_many(cmd, stack_ctx_list, dir_cdk=dir_cdk)


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

    :raises ValueError: If ``stack_ctx_list`` is empty
    """
    cmd = build_cmd(Diff, stack_ctx_list, **kwargs)
    return _run_cmd_for_many(cmd, stack_ctx_list, dir_cdk=dir_cdk)


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

    :raises ValueError: If ``stack_ctx_list`` is empty
    """
    cmd = build_cmd(Deploy, stack_ctx_list, prompt=prompt, **kwargs)
    return _run_cmd_for_many(cmd, stack_ctx_list, dir_cdk=dir_cdk)


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

    :raises ValueError: If ``stack_ctx_list`` is empty
    """
    cmd = build_cmd(Destroy, stack_ctx_list, prompt=prompt, **kwargs)
    return _run_cmd_for_many(cmd, stack_ctx_list, dir_cdk=dir_cdk)
