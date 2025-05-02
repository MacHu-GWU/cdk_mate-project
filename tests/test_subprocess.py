# -*- coding: utf-8 -*-

import pytest
import subprocess
from cdk_mate.cli.cli_utils import run_cmd


def test_run_cmd():
    run_cmd(["pip", "list"])

    with pytest.raises(subprocess.CalledProcessError):
        run_cmd(["pip", "install"])

    with pytest.raises(FileNotFoundError):
        run_cmd(["invalid-command"])


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_utils",
        preview=False,
    )
