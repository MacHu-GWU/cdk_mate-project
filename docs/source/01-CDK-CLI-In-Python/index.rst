CDK CLI in Python
==============================================================================


Overview
------------------------------------------------------------------------------
The CDK CLI in Python module provides a Pythonic interface to AWS Cloud Development Kit (CDK) commands, offering significant improvements over directly using the CLI. This module addresses several common challenges in managing CDK deployments programmatically.


Key Features
------------------------------------------------------------------------------
1. **Pythonic Interface to CDK CLI**: Convert CLI options into Python function parameters for better code readability, IDE support, and type checking.
2. **AWS Credential Management**: Integration with Boto Session Manager (BSM) to ensure CDK commands use specific AWS credentials, overcoming the limited credential management of the native CDK CLI.
3. **Directory Context Management**: Automatically locate and use the right ``cdk.json`` file without changing directories, enabling CDK operations from any location.


CLI Command Modules
------------------------------------------------------------------------------
The CLI commands are implemented in :mod:`cdk_mate.cli.cli_cmd`: one class per CDK CLI command, one field per option. It covers every command of the CDK CLI except ``cdk docs`` (opens a browser) and ``cdk lsp`` (a language server for editors). The most common ones:

- :class:`cdk_mate.cli.cli_cmd.Bootstrap` - Prepare an AWS environment for CDK deployments
- :class:`cdk_mate.cli.cli_cmd.Synth` - Synthesize CloudFormation templates
- :class:`cdk_mate.cli.cli_cmd.Diff` - Compare deployed stacks with current state
- :class:`cdk_mate.cli.cli_cmd.Deploy` - Deploy stacks to AWS
- :class:`cdk_mate.cli.cli_cmd.Destroy` - Remove stacks from AWS
- :class:`cdk_mate.cli.cli_cmd.List`, :class:`cdk_mate.cli.cli_cmd.Rollback`, :class:`cdk_mate.cli.cli_cmd.Drift`, :class:`cdk_mate.cli.cli_cmd.Watch`, and the rest of :mod:`cdk_mate.cli.cli_cmd`

``cli_cmd.py`` is generated from the option registry that ships with the CDK CLI (``lib/cli/cli-type-registry.json`` in the ``aws-cdk`` npm package), so every field is documented with the CLI's own description, and options with fixed choices are typed as ``Literal``. The behavior shared by all commands is in :mod:`cdk_mate.cli.cli_cmd_base`.

.. dropdown:: cli_cmd.py

    .. literalinclude:: ../../../cdk_mate/cli/cli_cmd.py
       :language: python
       :linenos:


Credential Management
------------------------------------------------------------------------------
The CLI wrapper integrates with Boto Session Manager to provide enhanced credential management:

1. **Credentials for the subprocess only**: When a BSM object is provided, :func:`~cdk_mate.cli.cli_utils.get_aws_cli_env` builds
   the environment of the ``cdk`` subprocess from it (``AWS_PROFILE``, or the access key, secret key, and session token, plus ``AWS_REGION``).
   ``dir_cdk`` becomes the subprocess's working directory in the same way. Your own process never changes its
   ``os.environ`` or its working directory.
2. **Explicit Account Selection**: This approach guarantees deployment to the correct AWS account by overriding the default credential chain, providing more reliability than profile-based selection.

Example:

.. code-block:: python

    from boto_session_manager.api import BotoSesManager
    import cdk_mate.api as cdk_mate

    # Create a session for a specific AWS account and region
    bsm = BotoSesManager(
        profile_name="dev",
        region_name="us-east-1"
    )

    # Deploy using this session
    cdk_mate.cli.Deploy(
        stacks=["MyStack"],
        require_approval="never"
    ).run(bsm=bsm)


Directory Context Management
------------------------------------------------------------------------------
The CLI wrapper handles directory context automatically:

1. **Automatic Directory Location**: The ``dir_cdk`` parameter allows specifying the location of the ``cdk.json`` file, and the wrapper runs the ``cdk`` subprocess in that directory (your own working directory does not change).
2. **Path Resolution**: If a file path is provided, the wrapper uses its parent directory, ensuring flexibility in how paths are specified.

Example::

    import cdk_mate.api as cdk_mate

    # Synthesize from any location
    cdk_mate.cli.Synth().run(dir_cdk="/path/to/my/cdk/project")

    # Using a file path (will use the file's directory)
    cdk_mate.cli.Synth().run(dir_cdk="/path/to/my/cdk/project/stack1_app.py")


Options and CLI Versions
------------------------------------------------------------------------------
Every option defaults to "not set", and an option that is not set never reaches the command line, so the CDK CLI uses its own default. A newer ``cdk_mate`` therefore works with an older CDK CLI, as long as you only set options that CLI knows.

- **Booleans:** ``True`` passes ``--name`` and ``False`` passes ``--no-name``, so options that are on by default can be turned off, such as ``Deploy(rollback=False)`` for ``--no-rollback`` or ``GC(confirm=False)`` for ``--no-confirm``.
- **Options this library does not define yet:** pass them verbatim with ``extra_args``; they go at the end of the command line.
- **A specific CLI version:** set ``cdk_cmd``, the executable that runs the subcommand (``["cdk"]`` by default).

.. code-block:: python

    import cdk_mate.api as cdk_mate

    cdk_mate.cli.Deploy(
        stacks=["MyStack"],
        rollback=False,  # --no-rollback
        extra_args=["--tags", "team=data"],  # an option not defined in Deploy
        cdk_cmd=["npx", "aws-cdk@2.1145.0"],  # pin the CLI version
    ).run(dir_cdk=__file__)

.. important::

    The CDK CLI does not fail on an option it does not know: it prints ``Unknown option(s): ... These will be ignored.`` and carries on with exit code 0. When you set an option, make sure your CLI version supports it, for example by pinning the CLI version in your project.


Output and Logging
------------------------------------------------------------------------------
Before running a command, cdk_mate reports what it is about to do: the AWS console URL of each stack, the masked AWS account, principal and region of ``bsm``, the CDK directory, and the command line. It reports through the standard :mod:`logging` module, under the logger name ``cdk_mate`` (see :mod:`cdk_mate.logger`), and by default writes plain messages to stdout. The output of the ``cdk`` command itself always goes straight to your terminal.

.. code-block:: python

    import logging

    # keep only warnings; this also skips the sts:GetCallerIdentity call behind the identity report
    logging.getLogger("cdk_mate").setLevel(logging.WARNING)


Usage Examples
------------------------------------------------------------------------------


Bootstrapping an AWS Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Prepare an AWS environment for CDK deployments:

.. code-block:: python

    from boto_session_manager.api import BotoSesManager
    import cdk_mate.cli as cdk_mate

    bsm = BotoSesManager(
        profile_name="dev",
        region_name="us-east-1"
    )

    cdk_mate.cli.Bootstrap(
        aws_environment="123456789012/us-east-1",
        bootstrap_bucket_name="my-cdk-bootstrap-bucket",
        qualifier="hnb659fds"  # Custom qualifier
    ).run(bsm=bsm)


Basic Synthesis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Synthesize a CDK application without changing directories:

.. code-block:: python

    import cdk_mate.api as cdk_mate

    cdk_mate.cli.Synth().run(dir_cdk="/path/to/cdk/project")


Comparing Stacks with Diff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Compare local CDK stacks with deployed versions:

.. code-block:: python

    import cdk_mate.cli as cdk_mate

    # Basic diff
    cdk_mate.cli.Diff(
        stacks=["MyStack"]
    ).run(dir_cdk="/path/to/cdk/project")

    # Advanced diff options
    cdk_mate.cli.Diff(
        stacks=["MyStack"],
        quiet=True,
        security_only=True,
        change_set=False  # Faster but less accurate diff
    ).run(dir_cdk="/path/to/cdk/project")


Deploying with Specific Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deploy a stack using explicit AWS credentials:

.. code-block:: python

    from boto_session_manager.api import BotoSesManager
    import cdk_mate.api as cdk_mate

    bsm = BotoSesManager(
        profile_name="dev",
        region_name="us-east-1"
    )

    cdk_mate.cli.Deploy(
        stacks=["MyStack"],
        require_approval="never"
    ).run(
        bsm=bsm,
        dir_cdk="/path/to/cdk/project",
    )


Destroying Multiple Stacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Remove multiple stacks with forced deletion:

.. code-block:: python

    import cdk_mate.api as cdk_mate

    cdk_mate.cli.Destroy(
        stacks=["Stack1", "Stack2"],
        force=True
    ).run(
        bsm=bsm,
        dir_cdk="/path/to/cdk/project",
    )


Conclusion
------------------------------------------------------------------------------
The CDK CLI in Python module provides a robust Pythonic interface to AWS CDK operations,
addressing key limitations of the native CLI. By combining credential management, directory
context handling, and a comprehensive parameter interface, it enables more reliable and
maintainable infrastructure deployment automation.
