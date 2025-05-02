# -*- coding: utf-8 -*-

from cdk_mate.cli.cli_cmd import synth, deploy
from cdk_mate.tests.bsm import bsm

# synth(bsm=bsm, dir_cdk=__file__)
deploy(bsm=bsm, dir_cdk=__file__)
