# -*- coding: utf-8 -*-

from cdk_mate.utils import to_camel, to_slug


def test_to_camel():
    assert to_camel("Hello_world") == "HelloWorld"
    assert to_camel("hello-World") == "HelloWorld"
    assert to_camel("HELLO WORLD") == "HelloWorld"
    assert to_camel("hello world") == "HelloWorld"
    assert to_camel("HELLO  WORLD") == "HelloWorld"
    assert to_camel("hello  world") == "HelloWorld"


def test_to_slug():
    assert to_slug("Hello_world") == "Hello-world"
    assert to_slug("hello-World") == "hello-World"
    assert to_slug("HELLO WORLD") == "HELLO-WORLD"
    assert to_slug("hello world") == "hello-world"
    assert to_slug("HELLO  WORLD") == "HELLO-WORLD"
    assert to_slug("hello  world") == "hello-world"


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.utils",
        preview=False,
    )
