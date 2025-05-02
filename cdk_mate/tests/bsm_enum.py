# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager


class BsmEnum:
    dev = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
    test = BotoSesManager(profile_name="bmt_app_test_us_east_1")
