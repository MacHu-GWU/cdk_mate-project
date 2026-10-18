# -*- coding: utf-8 -*-

import moto

from .bsm_enum import bsm_enum


class BaseMockAwsTest:
    """
    Base class for test classes that touch AWS.

    It always starts a moto mock, locally and in CI alike, and switches
    :data:`~cdk_mate.tests.bsm_enum.bsm_enum` to mock sessions, so no real
    AWS credentials are needed. Real deployments live in ``cdk/``.
    """

    mock_aws: "moto.mock_aws | None" = None

    @classmethod
    def setup_class(cls):
        cls.mock_aws = moto.mock_aws()
        cls.mock_aws.start()
        bsm_enum.use_mock = True
        cls.setup_class_post_hook()

    @classmethod
    def setup_class_post_hook(cls):
        pass

    @classmethod
    def teardown_class(cls):
        bsm_enum.use_mock = False
        cls.mock_aws.stop()
