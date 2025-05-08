.. _multi-stack-multi-environment-best-practices:

Multi Stack Multi Environment Best Practices
==============================================================================


Overview
------------------------------------------------------------------------------
The Multi-Stack, Multi-Environment CDK Deployment Pattern provides a scalable and flexible approach to managing many AWS CDK stacks across multiple environments (accounts, regions, stages). This pattern addresses several common challenges in enterprise-level infrastructure as code:

- **Complexity Management**: Separate stack implementation from deployment configuration
- **Deployment Flexibility**: Deploy individual stacks, groups of stacks, or all stacks as needed
- **Environment Consistency**: Ensure consistent stack configurations across environments
- **Resource Isolation**: Keep resource definitions clean and focused
- **Credential Management**: Safely handle AWS credentials for different environments
- **Testing Granularity**: Test infrastructure at various levels of integration

This pattern scales effectively by:

1. Using lightweight context objects to reference stack configurations without loading full CDK code
2. Implementing lazy loading for AWS session credentials
3. Separating stack definition from stack instantiation
4. Providing reusable deployment utilities at both individual and group levels
5. Centralizing environment configuration for consistency


Code Architecture
------------------------------------------------------------------------------


Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

    project/
    ├── cdk/                           # Deployment scripts
    │   ├── app.py                     # Main CDK app entrypoint
    │   ├── deploy.py                  # Multi-stack deployment script
    │   ├── stack1/                    # Stack1-specific deployment
    │   │   ├── stack1_app.py          # Stack1 app entry point
    │   │   └── stack1_deploy.py       # Stack1 deployment script
    │   └── stack2/                    # Stack2-specific deployment
    │       ├── stack2_app.py          # Stack2 app entry point
    │       └── stack2_deploy.py       # Stack2 deployment script
    ├── cdk_mate/                      # Core library
    │   ├── stack_ctx.py               # Stack context implementation
    │   └── tests/                     # Example implementations
    │       ├── stacks.py              # CDK stack definition
    │       │   ├── stack1/                             # Stack1-specific definition
    │       │   │   ├── iac_define.py                   # Stack1 entry point
    │       │   │   └── iac_define_01_everything.py     # Stack1 mixin class
    │       │   └── stack2/                             # Stack2-specific definition
    │       │       ├── iac_define.py                   # Stack2 entry point
    │       │       └── iac_define_01_everything.py     # Stack2 mixin class
    │       ├── bsm_enum.py            # AWS session enumerations
    │       ├── stack_ctx_enum.py      # Stack context enumerations
    │       └── stack_enum.py          # CDK stack initialization
    └── tests/                         # Unit tests
        └── test_stack_enum.py         # Tests for stack initialization


Core Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. **Stack Implementation**: Each stack is implemented in a dedicated module using a mixin pattern to manage complexity
2. **BSM Enum**: Defines AWS session configurations for different environments
3. **Stack Context Enum**: Defines metadata for each stack instance (stack name, AWS account, region)
4. **IAC Initialization**: Creates CDK stack instances using context objects
5. **Deployment Scripts**: Provides flexible deployment options


Implementation Details
------------------------------------------------------------------------------
Reference:

- Stack definition source code: `cdk_mate/tests <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk_mate/tests>`_


Stack Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The :class:`~cdk_mate.stack_ctx.StackCtx` class provides essential metadata for each stack instance.

.. dropdown:: stack_ctx.py

    .. literalinclude:: ../../../cdk_mate/stack_ctx.py
       :language: python
       :linenos:


Environment Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The BSM (Boto Session Manager) enum provides lazy-loaded AWS session objects:

.. dropdown:: bsm_enum.py

    .. literalinclude:: ../../../cdk_mate/tests/bsm_enum.py
       :language: python
       :linenos:


Stack Context Enumeration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The :class:`~cdk_mate.tests.stack_ctx_enum.StackCtxEnum` class provides lightweight stack configuration objects:

.. dropdown:: stack_ctx_enum.py

    .. literalinclude:: ../../../cdk_mate/tests/stack_ctx_enum.py
       :language: python
       :linenos:


Stack Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The stack initialization module creates CDK stack instances using the context objects:

.. dropdown:: stack_enum.py

    .. literalinclude:: ../../../cdk_mate/tests/stack_enum.py
       :language: python
       :linenos:


Deployment Options
------------------------------------------------------------------------------
This pattern supports three flexible deployment approaches:


1. Single Stack, Multiple Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use stack-specific deployment scripts to deploy a single stack to one or more environments:

.. dropdown:: cdk.json

    .. literalinclude:: ../../../cdk/stack1/cdk.json
       :language: javascript
       :linenos:

.. dropdown:: stack1_app.py

    .. literalinclude:: ../../../cdk/stack1/stack1_app.py
       :language: python
       :linenos:

.. dropdown:: stack1_deploy.py

    .. literalinclude:: ../../../cdk/stack1/stack1_deploy.py
       :language: python
       :linenos:


2. Multiple Stacks, Same Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deploy multiple stacks to the same environment:

.. dropdown:: cdk.json

    .. literalinclude:: ../../../cdk/cdk.json
       :language: javascript
       :linenos:

.. dropdown:: app.py

    .. literalinclude:: ../../../cdk/app.py
       :language: python
       :linenos:

.. dropdown:: deploy.py

    .. literalinclude:: ../../../cdk/deploy.py
       :language: python
       :linenos:


Testing
------------------------------------------------------------------------------
The pattern includes a testing approach that synthesizes stacks without deployment (`tests/test_stack_enum.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/tests/test_stack_enum.py>`_):

.. dropdown:: test_stack_enum.py

    .. literalinclude:: ../../../tests/test_stack_enum.py
       :language: python
       :linenos:


Usage Guide
------------------------------------------------------------------------------


Setting Up New Stacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. **Define Stack Implementation**: Create a new module in the `stacks (cdk_mate/tests/stacks) <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk_mate/tests/stacks>`_ module to implement your CDK stack.
2. **Add Stack Context**: Add new stack context entries to the `stack_ctx_enum.py (cdk_mate/tests/stack_ctx_enum.py) <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk_mate/tests/stack_ctx_enum.py>`_ module for each environment.
3. **Update Initialization**: Add the new stack to the `stack_enum.py module (cdk_mate/tests/stack_enum.py) <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk_mate/tests/stack_enum.py>`_ module.
4. **Create Deployment Scripts**: Add deployment scripts for the new stack in `cdk <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk>`_.


Deployment Workflows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Individual Stack Development
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
First ensure that you enabled the stack you want to deploy in the ``xyz_app.py`` script like this:

.. dropdown:: stack1_app.py

    .. literalinclude:: ../../../cdk/stack1/stack1_app.py
       :language: python
       :linenos:

When working on a specific stack, use the stack-specific deployment script ``xyz_deploy.py``, comment in and out the right line like this:

.. dropdown:: stack1_deploy.py

    .. literalinclude:: ../../../cdk/stack1/stack1_deploy.py
       :language: python
       :linenos:

Then run the deployment script from the command line:

.. code-block:: bash

    # you don't have to cd to it
    python /path/to/cdk/stack1/stack1_deploy.py


Environment Deployment
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
To deploy all stacks for a specific environment:

.. code-block:: bash

    # you don't have to cd to it
    python /path/to/cdk/deploy.py


Developer Workflow Guide
------------------------------------------------------------------------------
This guide provides step-by-step instructions for common development workflows when working with the Multi-Stack Multi-Environment pattern.


Adding a New AWS Account or Region
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When you need to deploy resources to a new AWS account or region:

1. Open the `bsm_enum.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk_mate/tests/bsm_enum.py>`_.
2. Add a new boto session entry to the ``BsmEnum`` class.
3. Follow the existing naming conventions (e.g., dev, test, prod)


Creating a New CloudFormation Stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Follow these steps to implement and deploy a new CloudFormation stack:

1. Create stack implementation:
    - Create a new subfolder in the `stacks <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk_mate/tests/stacks>`_ directory
    - Use the `stack1 <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk_mate/tests/stacks/stack1>`_ folder as a template
    - Implement your CloudFormation resources following the established pattern
2. Define stack contexts:
    - Open `stack_ctx_enum.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk_mate/tests/stack_ctx_enum.py>`_
    - Add new ``StackCtx`` objects for each environment (e.g., dev, test, prod)
3. Register stack instances:
    - Open `stack_enum.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk_mate/tests/stack_enum.py>`_
    - Add your new stack instances to the enum
4. Test your stack:
    - Update `test_stack_enum.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/tests/test_stack_enum.py>`_
    - Add and run tests for your new stack to verify it synthesizes correctly
5. Set up deployment scripts:
    - Option 1: Create a dedicated subfolder in the `cdk <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk>`_ directory for your stack
    - Option 2: Update the existing `app.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/app.py>`_ and `deploy.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/cdk/deploy.py>`_ files to include your stack


Updating an Existing CloudFormation Stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To update an existing stack, follow these key steps:

1. Modify the stack implementation in its respective folder under ``stacks``
2. Verify your changes with the unit tests in ``test_stack_enum.py``
3. Update the deployment scripts in the ``cdk`` folder as needed

This process allows you to make incremental changes while maintaining the overall deployment structure.


Best Practices
------------------------------------------------------------------------------
1. **Keep Stack Implementation Clean**: Focus on the CDK resources in stack implementation modules.
2. **Use Context Objects**: Always use the context objects for stack configuration.
3. **Lazy Loading**: Use lazy loading for AWS sessions to improve performance.
4. **Deployment Automation**: Use the deployment utilities instead of raw CDK CLI commands.
5. **Testing**: Always include tests that synthesize stacks before deployment.


Conclusion
------------------------------------------------------------------------------
The Multi-Stack, Multi-Environment CDK Deployment Pattern provides a scalable and flexible approach to managing complex infrastructure as code across multiple environments. By separating stack implementation from deployment configuration and providing reusable utilities, this pattern enables teams to efficiently manage infrastructure at scale.
