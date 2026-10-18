Manage many stacks in one place
==============================================================================
This folder is a real deployment playground for ``cdk_mate``. It uses the example stacks in ``cdk_mate/tests/stacks/`` and the environments in ``cdk_mate/tests/bsm_enum.py``, and it deploys to **real AWS accounts**.

How ``cdk_mate`` is tested
------------------------------------------------------------------------------
- **Unit tests** (``tests/``, ``mise run cov``, and CI): no AWS account needed. ``cdk_mate.tests.mock_aws.BaseMockAwsTest`` starts a moto mock and switches ``bsm_enum`` to mock sessions, so ``StackCtx.new(...)`` and ``cdk.App().synth()`` run offline. They need ``node`` on ``PATH``, because aws-cdk-lib runs through jsii.
- **This folder** (manual, maintainer only): runs the real ``cdk`` CLI through ``cdk_mate`` against the AWS profiles ``esc_app_dev_us_east_1`` and ``esc_app_test_us_east_1``.

Run it
------------------------------------------------------------------------------
``mise.toml`` installs ``node``, the ``cdk`` CLI (``npm:aws-cdk``), and ``awscli``. Each ``cdk.json`` runs its app with ``.venv/bin/python``, so run ``mise run inst`` first, and run everything from a shell where mise is active:

.. code-block:: bash

    # all stacks: synth, deploy, then destroy (edit deploy.py to pick the steps)
    .venv/bin/python cdk/deploy.py

    # one stack at a time: uncomment the steps you want first
    .venv/bin/python cdk/stack1/stack1_deploy.py
    .venv/bin/python cdk/stack2/stack2_deploy.py
