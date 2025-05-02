# -*- coding: utf-8 -*-

from cdk_mate.utils import to_camel


def test_to_camel():
    assert to_camel("Hello_world") == "HelloWorld"
    assert to_camel("hello-World") == "HelloWorld"
    assert to_camel("HELLO WORLD") == "HelloWorld"


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.utils",
        preview=False,
    )
