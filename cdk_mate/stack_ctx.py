# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args import NOTHING
from boto_session_manager import BotoSesManager

from .cli.cli_cmd import deploy, destroy

if T.TYPE_CHECKING:  # pragma: no cover
    from pathlib_mate import T_PATH_ARG


@dataclasses.dataclass
class StackCtx:
    construct_id: str = dataclasses.field()
    stack_name: str = dataclasses.field()
    aws_account_id: str = dataclasses.field()
    aws_region: str = dataclasses.field()
    bsm: T.Optional["BotoSesManager"] = dataclasses.field(default=NOTHING)

    @property
    def stack_console_url(self) -> str:
        return (
            f"https://{self.aws_region}.console.aws.amazon.com/cloudformation"
            f"/home?region={self.aws_region}#/stacks?"
            f"filteringStatus=active&filteringText={self.stack_name}&viewNested=true"
        )

    def cdk_deploy(
        self,
        dir_cdk: T.Optional["T_PATH_ARG"] = None,
        prompt: bool = False,
    ):
        print("--- Preview in AWS Console ---")
        print(self.stack_console_url)
        return deploy(
            bsm=self.bsm,
            dir_cdk=dir_cdk,
            stacks=[self.construct_id],
            require_approval=NOTHING if prompt else "never",
        )

    def cdk_destroy(
        self,
        dir_cdk: T.Optional["T_PATH_ARG"] = None,
        prompt: bool = False,
    ):
        print("--- Preview in AWS Console ---")
        print(self.stack_console_url)
        return destroy(
            bsm=self.bsm,
            dir_cdk=dir_cdk,
            stacks=[self.construct_id],
            force=NOTHING if prompt else True,
        )
