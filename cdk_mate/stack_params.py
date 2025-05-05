# -*- coding: utf-8 -*-

"""

"""

import typing as T
import dataclasses

import aws_cdk as cdk
from constructs import Construct

from .exc import ParamError
from .arg import _REQUIRED, REQ, NA, rm_na, T_KWARGS


@dataclasses.dataclass
class BaseParams:
    def _validate(self):
        for field in dataclasses.fields(self.__class__):
            if field.init:
                k = field.name
                if getattr(self, k) is REQ:  # pragma: no cover
                    raise ParamError(f"Field {k!r} is required for {self.__class__}.")

    def __post_init__(self):
        self._validate()

    @classmethod
    def _split_req_opt(cls, kwargs: T_KWARGS) -> T.Tuple[T_KWARGS, T_KWARGS]:
        req_kwargs, opt_kwargs = dict(), dict()
        for field in dataclasses.fields(cls):
            if isinstance(field.default, _REQUIRED):
                try:
                    req_kwargs[field.name] = kwargs[field.name]
                except KeyError:  # pragma: no cover
                    raise ParamError(
                        f"{field.name!r} is a required parameter for {cls}!"
                    )
            else:
                try:
                    opt_kwargs[field.name] = kwargs[field.name]
                except KeyError:
                    pass
        opt_kwargs = rm_na(**opt_kwargs)
        return req_kwargs, opt_kwargs

    def to_dict(self) -> T_KWARGS:
        """
        Convert the dataclass to a dictionary of keyword arguments.
        """
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not NA}


@dataclasses.dataclass
class ConstructParams(BaseParams):
    scope: Construct = dataclasses.field(default=REQ)
    id: str = dataclasses.field(default=REQ)

    def to_construct_kwargs(self) -> T_KWARGS:
        return rm_na(
            scope=self.scope,
            id=self.id,
        )


@dataclasses.dataclass
class StackParams(ConstructParams):
    analytics_reporting: bool = dataclasses.field(default=NA)
    cross_region_references: bool = dataclasses.field(default=NA)
    description: str = dataclasses.field(default=NA)
    env: T.Union[cdk.Environment, dict[str, T.Any]] = dataclasses.field(default=NA)
    notification_arns: T.Sequence[str] = dataclasses.field(default=NA)
    permissions_boundary: cdk.PermissionsBoundary = dataclasses.field(default=NA)
    stack_name: str = dataclasses.field(default=NA)
    suppress_template_indentation: bool = dataclasses.field(default=NA)
    synthesizer: cdk.IStackSynthesizer = dataclasses.field(default=NA)
    tags: T.Mapping[str, str] = dataclasses.field(default=NA)
    termination_protection: bool = dataclasses.field(default=NA)

    def to_stack_kwargs(self) -> T_KWARGS:
        return rm_na(
            scope=self.scope,
            id=self.id,
            analytics_reporting=self.analytics_reporting,
            cross_region_references=self.cross_region_references,
            description=self.description,
            env=self.env,
            notification_arns=self.notification_arns,
            permissions_boundary=self.permissions_boundary,
            stack_name=self.stack_name,
            suppress_template_indentation=self.suppress_template_indentation,
            synthesizer=self.synthesizer,
            tags=self.tags,
            termination_protection=self.termination_protection,
        )
