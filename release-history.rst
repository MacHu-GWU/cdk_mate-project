.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.5 (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add the following public APIs:
    - ``cdk_mate.api.cli.BaseCommand``
    - ``cdk_mate.api.cli.Acknowledge``
    - ``cdk_mate.api.cli.Context``
    - ``cdk_mate.api.cli.GC``
    - ``cdk_mate.api.cli.Import``
    - ``cdk_mate.api.cli.Init``

**Minor Improvements**

- Use ``func_args.REQ`` as default value for ``StackCtx`` to make it extensible.


0.1.4 (2025-05-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**💥Breaking Changes**

- The following APIs are removed, and are moved to `func_args <https://github.com/MacHu-GWU/func_args-project>`_:
    - ``cdk_mate.api.ParamError``
    - ``cdk_mate.api.REQ``
    - ``cdk_mate.api.NA``
    - ``cdk_mate.api.rm_na``
    - ``cdk_mate.api.T_KWARGS``
- The following APIs are removed, and are moved to `cdkit <https://github.com/MacHu-GWU/cdkit-project>`_:
    - ``cdk_mate.api.BaseStack``
    - ``cdk_mate.api.BaseParams``
    - ``cdk_mate.api.ConstructParams``
    - ``cdk_mate.api.StackParams``

**Minor Improvements**

- Refactor the code base
- Improve the example


0.1.3 (2025-05-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add the following public APIs:
    - ``cdk_mate.api.cli.REQ``
    - ``cdk_mate.api.cli.NA``
    - ``cdk_mate.api.cli.rm_na``
    - ``cdk_mate.api.cli.T_KWARGS``
    - ``cdk_mate.api.cli.BaseStack``
    - ``cdk_mate.api.cli.BaseParams``
    - ``cdk_mate.api.cli.ConstructParams``
    - ``cdk_mate.api.cli.StackParams``


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
