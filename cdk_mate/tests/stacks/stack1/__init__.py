# -*- coding: utf-8 -*-

"""
Infrastructure as Code (IaC) Module for OpenSearch Migration Project

This module provides a structured approach to defining and deploying infrastructure
for the OpenSearch Migration Proof of Concept (POC) using
`AWS Cloud Development Kit (CDK) <https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html>`_.

Design Philosophy:

- Separation of Concerns: The infrastructure definition is cleanly separated from
  its concrete instantiation.
- Modularity: Each infrastructure component is defined in its own mixin class,
  promoting code reusability and maintainability.

Key Components:

- iac_define.py: Contains the core stack definition with modular mixins for
  different AWS resources (SQS, IAM, S3, Lambda)
- Individual mixin files (e.g., ``iam_define_01_abc.py``, ``iam_define_01_xyz.py``):
  Implement specific infrastructure resource configurations
"""
