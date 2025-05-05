# -*- coding: utf-8 -*-

from cdk_mate.cli.cli_cmd import (
    Synth,
)


class TestSynth:
    def test_synth(self):
        synth = Synth()
        synth.to_args()


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_cmd",
        preview=False,
    )
