.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.2 (2025-05-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Use class based command system to implement CDK CLI commands.
- Add the following public APIs:
    - ``cdk_mate.api.cli.Bootstrap``
    - ``cdk_mate.api.cli.Diff``
    - ``cdk_mate.api.cli.Synth``
    - ``cdk_mate.api.cli.Deploy``
    - ``cdk_mate.api.cli.Destroy``
- Removed the following public APIs:
    - ``cdk_mate.api.cli.synth``
    - ``cdk_mate.api.cli.deploy``
    - ``cdk_mate.api.cli.destroy``

**Miscellaneous**

- Improve code coverage test to 100%.


0.1.1 (2025-05-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Add the following public APIs:
    - ``cdk_mate.api.cli.synth``
    - ``cdk_mate.api.cli.deploy``
    - ``cdk_mate.api.cli.destroy``
    - ``cdk_mate.api.StackCtx``
    - ``cdk_mate.api.to_camel``
    - ``cdk_mate.api.to_slug``
