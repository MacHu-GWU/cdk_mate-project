# -*- coding: utf-8 -*-

from cdk_mate import api


def test():
    _ = api


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.api",
        preview=False,
    )
