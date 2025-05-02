# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate",
        is_folder=True,
        preview=False,
    )
