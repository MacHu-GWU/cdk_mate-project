.. _multi-stack-multi-environment-best-practices:

Multi Stack Multi Environment Best Practices
==============================================================================
A real CDK project has several stacks, each deployed to several environments (dev, test, prod, often in different AWS accounts). This page shows a project layout for that, and why it is split the way it is. Every file it shows is real: the example project lives in `cdk_mate/tests <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk_mate/tests>`_ and its deploy scripts in `cdk <https://github.com/MacHu-GWU/cdk_mate-project/tree/main/cdk>`_, and it is deployed to two real AWS accounts.


The Example Project
------------------------------------------------------------------------------
Two stacks, two environments, so four CloudFormation stacks. Every resource is free.

- **Stack1, the alerts stack:** an SNS topic that other stacks publish alerts to, and an SSM parameter holding the log level of its environment: ``DEBUG`` in dev, ``INFO`` in test.
- **Stack2, the publisher stack:** an IAM role allowed to publish to the alert topic of Stack1, and an SSM parameter holding that topic's ARN. So Stack2 depends on Stack1 in the same environment.

These two needs, an argument that differs per environment and a reference from one stack to another, are what every real project has, and they shape the layout below.

.. code-block::

    cdk_mate/tests/
    ├── bsm_enum.py                 # one boto session per environment (AWS account and region)
    ├── stack_ctx_enum.py           # layer 1: one StackCtx per (stack, environment)
    ├── stack_enum.py               # layer 2: one CDK stack per (stack, environment)
    └── stacks/                     # the stack definitions
        ├── stack1/
        │   ├── iac_define.py               # class Stack1, its __init__ and arguments
        │   ├── iac_define_01_alerts.py     # mixin: the SNS topic
        │   └── iac_define_02_config.py     # mixin: the SSM parameter
        └── stack2/
            ├── iac_define.py               # class Stack2, takes alert_topic
            ├── iac_define_01_publisher.py  # mixin: the IAM role
            └── iac_define_02_config.py     # mixin: the SSM parameter
    cdk/
    ├── cdk.json, app.py, deploy.py         # all stacks, one environment at a time
    ├── stack1/                             # Stack1 only
    │   └── cdk.json, stack1_app.py, stack1_deploy.py
    └── stack2/                             # Stack2 only (and Stack1, its dependency)
        └── cdk.json, stack2_app.py, stack2_deploy.py


Two Layers: Stack Contexts and Stacks
------------------------------------------------------------------------------
The project keeps two enums, each with one entry per (stack, environment) pair, under the same name, such as ``stack2_dev``:

.. list-table::
    :header-rows: 1

    * - Layer
      - Each entry is
      - Used by
    * - ``stack_ctx_enum.py``
      - a :class:`~cdk_mate.stack_ctx.StackCtx`: plain data, the construct id, stack name, AWS account, region, and the boto session that deploys it
      - the deploy scripts: synth, diff, deploy, destroy
    * - ``stack_enum.py``
      - the CDK stack itself, created in a given ``cdk.App`` from the matching stack context
      - the CDK app scripts that ``cdk.json`` runs

Four stacks take eight entries. That is the price of the split; here is what it buys.

**The deploy scripts need only stack contexts.** ``cdk diff``, ``cdk deploy`` and ``cdk destroy`` need to know which stacks to target and with which credentials, not the stack objects. The deploy scripts import ``stack_ctx_enum`` alone and never load a stack definition, so they stay fast and simple however large the stacks grow. The CDK CLI loads the stacks itself, in its own process, by running the app script.

**Each stack's arguments are written out by name.** A stack's ``__init__`` takes the standard arguments from :meth:`StackCtx.to_stack_kwargs <cdk_mate.stack_ctx.StackCtx.to_stack_kwargs>` (``id``, ``stack_name``, ``env``) plus its own. In ``stack_enum.py`` each entry is its own method, so its own arguments are passed explicitly:

.. literalinclude:: ../../../cdk_mate/tests/stack_enum.py
   :language: python
   :pyobject: StackEnum.stack1_dev

A generic "create the stack of this context" helper would have to forward such arguments through ``**kwargs``, which hides the signature from the reader and the IDE. With one method per entry, adding an argument to ``Stack1`` makes every method that does not pass it fail at synth.

**Dependencies between stacks are plain attribute access.** ``Stack2`` takes the alert topic of ``Stack1`` as an explicit argument:

.. literalinclude:: ../../../cdk_mate/tests/stack_enum.py
   :language: python
   :pyobject: StackEnum.stack2_dev

CDK turns this reference into a CloudFormation export in Stack1 and an import in Stack2, and records that Stack2 depends on Stack1.

**Every entry is created once, on first use.** Both enums use ``cached_property``. Using ``stack2_dev`` creates ``stack1_dev`` too, and only once, however many stacks depend on it; creating the same construct id twice in one ``cdk.App`` is an error. An app script creates just the stacks it names, plus their dependencies. A stack context is also built on first use, so no AWS call is made (:meth:`StackCtx.new <cdk_mate.stack_ctx.StackCtx.new>` reads the account id of the boto session) until an entry is needed.

**The app is passed in.** ``StackEnum(app=cdk.App())`` takes the app as an argument instead of creating one at import time, so every app script and every test starts from a fresh app.


The Files
------------------------------------------------------------------------------


Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
One boto session per environment, named after it. The unit tests switch them to a moto mock, so they need no AWS account.

.. dropdown:: bsm_enum.py

    .. literalinclude:: ../../../cdk_mate/tests/bsm_enum.py
       :language: python
       :linenos:


Layer 1: Stack Contexts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:meth:`StackCtx.new <cdk_mate.stack_ctx.StackCtx.new>` derives the construct id and the CloudFormation stack name from one name, and the account and region from the boto session.

.. dropdown:: stack_ctx_enum.py

    .. literalinclude:: ../../../cdk_mate/tests/stack_ctx_enum.py
       :language: python
       :linenos:


Layer 2: Stacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. dropdown:: stack_enum.py

    .. literalinclude:: ../../../cdk_mate/tests/stack_enum.py
       :language: python
       :linenos:


Stack Definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each stack is a class in ``iac_define.py`` that mixes in one class per group of resources, each in its own ``iac_define_NN_<topic>.py`` file, so a large stack stays split into small files. Its ``__init__`` stores its own arguments and calls one ``create_*`` method per mixin.

.. dropdown:: stacks/stack1/iac_define.py

    .. literalinclude:: ../../../cdk_mate/tests/stacks/stack1/iac_define.py
       :language: python
       :linenos:

.. dropdown:: stacks/stack1/iac_define_01_alerts.py

    .. literalinclude:: ../../../cdk_mate/tests/stacks/stack1/iac_define_01_alerts.py
       :language: python
       :linenos:

.. dropdown:: stacks/stack2/iac_define.py

    .. literalinclude:: ../../../cdk_mate/tests/stacks/stack2/iac_define.py
       :language: python
       :linenos:

.. dropdown:: stacks/stack2/iac_define_01_publisher.py

    .. literalinclude:: ../../../cdk_mate/tests/stacks/stack2/iac_define_01_publisher.py
       :language: python
       :linenos:


Deploying
------------------------------------------------------------------------------
Each folder in ``cdk/`` has a ``cdk.json``, whose ``app`` runs an app script with the project's Python, and a deploy script that runs the CDK CLI through cdk_mate. The deploy scripts pass ``dir_cdk=__file__``, so they run from any working directory:

.. code-block:: bash

    python /path/to/cdk/deploy.py


All Stacks, One Environment at a Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``app.py`` creates every stack. ``deploy.py`` keeps one list of stack contexts per environment and runs one ``cdk`` command per list with :func:`~cdk_mate.stack_ctx.cdk_deploy_many` and its siblings, using the credentials of that environment.

.. dropdown:: app.py

    .. literalinclude:: ../../../cdk/app.py
       :language: python
       :linenos:

.. dropdown:: deploy.py

    .. literalinclude:: ../../../cdk/deploy.py
       :language: python
       :linenos:


One Stack, All Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A folder per stack keeps a short feedback loop while you work on that stack. Its app script names only that stack, and the deploy script calls the ``cdk_*`` methods of its stack contexts; uncomment the step you want.

.. dropdown:: stack2/stack2_app.py

    .. literalinclude:: ../../../cdk/stack2/stack2_app.py
       :language: python
       :linenos:

.. dropdown:: stack2/stack2_deploy.py

    .. literalinclude:: ../../../cdk/stack2/stack2_deploy.py
       :language: python
       :linenos:


Order of Dependent Stacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The CDK CLI orders dependent stacks itself:

- ``cdk deploy`` of Stack2 also deploys Stack1 first, since Stack2 needs it; pass ``exclusively=True`` to deploy Stack2 only.
- ``cdk destroy`` of Stack1 also destroys Stack2 first, since Stack2 imports from it; with ``exclusively=True`` it fails while Stack2 exists.
- A list of stacks in one command, such as ``cdk_deploy_many([stack2_dev, stack1_dev])``, runs in dependency order whatever the order of the list. ``deploy.py`` still writes its lists in creation and deletion order, so the order is visible.

Run a list of stacks with the credentials of one environment: :func:`~cdk_mate.stack_ctx.cdk_deploy_many` uses the boto session of the first stack, and logs a warning when the list spans accounts or regions. :ref:`build-cdk-commands` shows the exact command line each method and function runs.


Testing
------------------------------------------------------------------------------
``TestStackCtxSynth`` in `tests/test_stack_ctx.py <https://github.com/MacHu-GWU/cdk_mate-project/blob/main/tests/test_stack_ctx.py>`_ creates every stack in a fresh ``cdk.App`` under a moto mock and synthesizes it, so it needs no AWS account, only ``node`` for aws-cdk-lib. It checks the per-environment log level, and that Stack2 depends on and imports from Stack1.

.. dropdown:: test_stack_ctx.py

    .. literalinclude:: ../../../tests/test_stack_ctx.py
       :language: python
       :pyobject: TestStackCtxSynth


Adding to the Project
------------------------------------------------------------------------------


A New Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Add a boto session to ``BsmEnum`` in ``bsm_enum.py``, named after the environment, such as ``prod``.
2. Add a ``<stack>_prod`` entry for each stack to ``stack_ctx_enum.py`` and to ``stack_enum.py``, passing that environment's arguments.
3. Add the new entries to the app scripts and to a new list in the deploy scripts.


A New Stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Create ``stacks/<stack>/`` with an ``iac_define.py`` class and one mixin per group of resources, following ``stack1``. Take the stack's own settings and the resources of other stacks as explicit ``__init__`` arguments.
2. Add one entry per environment to ``stack_ctx_enum.py``.
3. Add one entry per environment to ``stack_enum.py``, passing those arguments, with ``self.<other stack>_<environment>.<resource>`` for a dependency.
4. Add the stack to ``TestStackCtxSynth`` and run the tests.
5. Add the entries to ``cdk/app.py`` and ``cdk/deploy.py``, or give the stack its own folder in ``cdk/`` like ``stack1``.
