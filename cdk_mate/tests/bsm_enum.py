# -*- coding: utf-8 -*-

"""
This module provides an enumeration of pre-configured Boto Session Manager
instances for different AWS environments and accounts.
"""

from functools import cached_property

from boto_session_manager.api import BotoSesManager


class BsmEnum:
    """
    Use lazy loading to create enum values.

    The named AWS profiles exist only on the maintainer's machine, and are used
    by the real deploy scripts in ``cdk/``. Unit tests set ``use_mock = True``
    (see :class:`~cdk_mate.tests.mock_aws.BaseMockAwsTest`), so every session
    resolves to moto's fake account and the tests need no AWS account at all.
    """

    def __init__(self):
        self.use_mock: bool = False

    def _get_bsm(self, profile: str) -> BotoSesManager:
        if self.use_mock:
            return BotoSesManager(region_name="us-east-1")
        else:
            return BotoSesManager(profile_name=profile)

    @cached_property
    def dev(self) -> BotoSesManager:
        return self._get_bsm("esc_app_dev_us_east_1")

    @cached_property
    def test(self) -> BotoSesManager:
        return self._get_bsm("esc_app_test_us_east_1")


bsm_enum = BsmEnum()
