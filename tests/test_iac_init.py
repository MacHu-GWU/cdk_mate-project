# -*- coding: utf-8 -*-

from cdk_mate.tests.iac_init import app


def test():
    app.synth()


if __name__ == "__main__":
    from cdk_mate.tests import run_unit_test

    run_unit_test(__file__)
