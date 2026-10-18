.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.0 (2026-10-18)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**💥Breaking Changes**

- Drop Python 3.9 and 3.10; Python 3.11 or newer is now required.
- Require ``boto-session-manager>=2.1.1,<3.0.0`` (was ``>=1.7.2,<2.0.0``). In 2.x, import the session class with ``from boto_session_manager.api import BotoSesManager``; ``from boto_session_manager import BotoSesManager`` no longer works.
- Remove ``cdk_mate.__version__``, ``__short_description__``, ``__license__``, ``__author__``, ``__author_email__``, ``__maintainer__`` and ``__maintainer_email__``. Use ``importlib.metadata.version("cdk_mate")`` for the version.
- Rename the global option field ``builder`` to ``build`` on every command class. It used to pass ``--builder``, which the CDK CLI does not know and silently ignored; ``build`` passes the real ``--build`` option.
- For custom subclasses of ``BaseCommand`` only: the private hook ``_cdk_cmd()``, which returned ``["cdk", "<subcommand>"]``, is replaced by ``_subcommand()``, which returns ``["<subcommand>"]``.

**Features and Improvements**

- Add the ``cdk_cmd`` field to every command class: the executable that runs the subcommand, ``["cdk"]`` by default. Set it to pin a CLI version per project, such as ``["npx", "aws-cdk@2.1145.0"]``.
- Add the ``extra_args`` field to every command class: arguments appended verbatim at the end of the command line, for options this library does not define yet, such as ``["--tags", "team=data"]``.
- Add the global options ``region`` and ``unstable`` to every command class. ``unstable`` used to exist on ``GC`` only; ``GC(unstable=["gc"])`` keeps working.
- Add the ``stacks`` positional argument to ``Synth``, to synthesize selected stacks.
- Cover every command of the CDK CLI except ``cdk docs`` and ``cdk lsp``. Add the following public APIs:
    - ``cdk_mate.api.cli.CliTelemetry``
    - ``cdk_mate.api.cli.Diagnose``
    - ``cdk_mate.api.cli.Doctor``
    - ``cdk_mate.api.cli.Drift``
    - ``cdk_mate.api.cli.Flags``
    - ``cdk_mate.api.cli.List``
    - ``cdk_mate.api.cli.Metadata``
    - ``cdk_mate.api.cli.Migrate``
    - ``cdk_mate.api.cli.Notices``
    - ``cdk_mate.api.cli.Orphan``
    - ``cdk_mate.api.cli.PublishAssets``
    - ``cdk_mate.api.cli.Refactor``
    - ``cdk_mate.api.cli.Rollback``
    - ``cdk_mate.api.cli.Validate``
    - ``cdk_mate.api.cli.Watch``
- Add the options of CDK CLI 2.1145.0 that the existing command classes were missing:
    - global (every command): ``color``, ``debug_app``, ``debug_cli``, ``telemetry_file``, ``yes``
    - ``Bootstrap``: ``deny_external_id``, ``express``, ``import_existing_resources``, ``untrust``
    - ``Deploy``: ``asset_build_concurrency``, ``execute``, ``express``, ``hotswap_ecs_maximum_healthy_percent``, ``hotswap_ecs_minimum_healthy_percent``, ``hotswap_ecs_stabilization_timeout_seconds``, ``revert_drift``, ``tags``
    - ``Destroy``: ``concurrency``, ``express``
    - ``Diff``: ``change_set_name``, ``fail_on``, ``import_existing_resources``, ``include_moves``, ``method``
    - ``GC``: ``toolkit_stack_name``
    - ``Import``: ``notification_arns``, ``resource_mapping_inline``
    - ``Init``: ``from_path``, ``lib_version``, ``package_manager``, ``project_name``, ``template_path``
    - ``Synth``: ``watch``
- Report progress (console URLs, the AWS identity, the CDK directory, the command line) through the standard ``logging`` module under the logger name ``cdk_mate``, instead of ``print``. By default it still writes plain messages to stdout, so the output looks the same; ``logging.getLogger("cdk_mate").setLevel(logging.WARNING)`` silences it.
- Every option field is documented with the CDK CLI's own description, its CLI default, and whether it is deprecated, so the API reference lists them all. Options with fixed choices are typed as ``Literal``, such as ``Deploy.require_approval``.

**Minor Improvements**

- ``Command.run()``, ``StackCtx.cdk_*()`` and ``cdk_*_many()`` no longer change the working directory or ``os.environ`` of the calling process: ``dir_cdk`` and the credentials of ``bsm`` are passed to the ``cdk`` subprocess only, so these calls are safe to use from threads.
- A session created from a named profile passes ``AWS_PROFILE`` to the ``cdk`` subprocess; any other session passes a frozen snapshot of its access key, secret key and session token. ``AWS_REGION`` is always set.
- The AWS identity reported before a command needs only ``sts:GetCallerIdentity``: it shows the masked account, principal ARN and region, and no longer calls ``iam:ListAccountAliases`` (no more ``User Id`` and ``AWS Account Alias`` lines). A failure, such as expired credentials, logs a warning and the command still runs. When the ``cdk_mate`` logger is quieter than ``INFO``, no AWS call is made.
- ``cdk_diff_many()``, ``cdk_deploy_many()`` and ``cdk_destroy_many()`` raise ``ValueError`` on an empty list (was ``IndexError``), and print a warning when the stacks target more than one AWS account or region, since all of them run with the credentials of the first stack.
- ``Deploy.rollback`` and ``Import.rollback`` default to ``OPT`` like every other option (was ``None``); both pass nothing to the CLI.
- Lower the floor of ``aws-cdk-lib`` to ``>=2.0.0`` (was ``>=2.179.0``): cdk_mate only needs ``aws_cdk.Environment``, so it no longer forces an ``aws-cdk-lib`` upgrade. Declare ``constructs>=10.0.0,<11.0.0`` explicitly, and raise the floor of ``func-args`` to ``>=1.0.2`` (was ``>=1.0.0``).

**Bugfixes**

- A boolean option set to ``False`` now passes ``--no-<option>``, so options that are on by default can be turned off, such as ``Deploy(rollback=False)`` for ``--no-rollback`` and ``GC(confirm=False)`` for ``--no-confirm``. ``False`` used to pass nothing, which left the CLI default on.
- A field with a trailing underscore, used to avoid a Python keyword, now passes the option name without it: ``Init(list_=True)`` passes ``--list`` instead of ``--list-``.
- Fix the reference link in the ``Destroy`` docstring, and the wrong ``to_slug()`` docstring example.

**Miscellaneous**

- ``cdk_mate/cli/cli_cmd.py`` is now generated from ``lib/cli/cli-type-registry.json`` of the ``aws-cdk`` npm package by ``mise run gen-cli-cmd``; after a CLI upgrade, the diff of the regenerated file shows which options changed. The behavior shared by all commands moves to ``cdk_mate/cli/cli_cmd_base.py``. A test keeps every option field name of 0.1.6.
- CI adds a job that installs every direct dependency at its declared floor (``uv sync --resolution lowest-direct``) on Python 3.11 and 3.14, so the floors in ``pyproject.toml`` stay tested versions.
- The example stacks behind ``cdk/`` and the tests each create a free SSM parameter, ``/<stack name>/example``, instead of being empty.
- Move the project tooling from Poetry to uv, mise and setuptools, following the pywf open-source template; CI and Read the Docs build with uv.
- The unit tests run without any AWS account: they synthesize the example stacks under a moto mock, locally and in CI alike. They need ``node``, which aws-cdk-lib runs on; CI and Read the Docs now install it.
- Document how options reach the CLI: unset options, ``False``, ``extra_args``, ``cdk_cmd``, and the CDK CLI ignoring unknown options.


0.1.6 (2025-05-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Add ``StackCtx.make_stack_ctx_kwargs`` method to make it more extensible.


0.1.5 (2025-05-06)
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
