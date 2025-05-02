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
The CLI commands are implemented in :mod:`cdk_mate.cli.cli_cmd`, providing function wrappers for common CDK operations:

- :func:`cdk_mate.cli.cli_cmd.synth` - Synthesize CloudFormation templates
- :func:`cdk_mate.cli.cli_cmd.deploy` - Deploy stacks to AWS
- :func:`cdk_mate.cli.cli_cmd.destroy` - Remove stacks from AWS

.. dropdown:: cli_cmd.py

    .. literalinclude:: ../../../cdk_mate/cli/cli_cmd.py
       :language: python
       :linenos:


Credential Management
------------------------------------------------------------------------------
The CLI wrapper integrates with Boto Session Manager to provide enhanced credential management:

1. **Context Manager for Credentials**: When a BSM object is provided, the wrapper uses its ``awscli()`` context manager to set the
   appropriate environment variables before running the CDK command, ensuring the command
   uses the specified AWS credentials.
2. **Explicit Account Selection**: This approach guarantees deployment to the correct AWS account by overriding the default credential chain, providing more reliability than profile-based selection.

Example::

    from boto_session_manager import BotoSesManager
    import cdk_mate.api as cdk_mate

    # Create a session for a specific AWS account and region
    bsm = BotoSesManager(
        profile_name="dev",
        region_name="us-east-1"
    )

    # Deploy using this session
    cdk_mate.cli.deploy(
        bsm=bsm,
        stacks=["MyStack"],
        require_approval="never"
    )


Directory Context Management
------------------------------------------------------------------------------
The CLI wrapper handles directory context automatically:

1. **Automatic Directory Location**: The ``dir_cdk`` parameter allows specifying the location of the ``cdk.json`` file, and the wrapper handles changing to that directory before executing commands.
2. **Path Resolution**: If a file path is provided, the wrapper uses its parent directory, ensuring flexibility in how paths are specified.

Example::

    import cdk_mate.api as cdk_mate

    # Synthesize from any location
    cdk_mate.cli.synth(dir_cdk="/path/to/my/cdk/project")

    # Using a file path (will use the file's directory)
    cdk_mate.cli.synth(dir_cdk="/path/to/my/cdk/project/stack1_app.py")


Usage Examples
------------------------------------------------------------------------------


Basic Synthesis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Synthesize a CDK application without changing directories:

.. code-block:: python

    import cdk_mate.api as cdk_mate

    cdk_mate.cli.synth(dir_cdk="/path/to/cdk/project")


Deploying with Specific Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deploy a stack using explicit AWS credentials:

.. code-block:: python

    from boto_session_manager import BotoSesManager
    import cdk_mate.api as cdk_mate

    bsm = BotoSesManager(
        profile_name="dev",
        region_name="us-east-1"
    )

    cdk_mate.cli.deploy(
        bsm=bsm,
        dir_cdk="/path/to/cdk/project",
        stacks=["MyStack"],
        require_approval="never"
    )


Destroying Multiple Stacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Remove multiple stacks with forced deletion:

.. code-block:: python

    import cdk_mate.api as cdk_mate

    cdk_mate.cli.destroy(
        dir_cdk="/path/to/cdk/project",
        stacks=["Stack1", "Stack2"],
        force=True
    )


Conclusion
------------------------------------------------------------------------------
The CDK CLI in Python module provides a robust Pythonic interface to AWS CDK operations,
addressing key limitations of the native CLI. By combining credential management, directory
context handling, and a comprehensive parameter interface, it enables more reliable and
maintainable infrastructure deployment automation.
