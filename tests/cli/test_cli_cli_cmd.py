# -*- coding: utf-8 -*-

from cdk_mate.cli import cli_cmd

import dataclasses

#: Global option fields of cdk_mate 0.1.6, except ``builder`` (renamed to ``build``).
FIELDS_0_1_6_GLOBAL = [
    "app",
    "asset_metadata",
    "ca_bundle_path",
    "ci",
    "context",
    "debug",
    "ec2creds",
    "help",
    "ignore_errors",
    "json",
    "lookups",
    "no_color",
    "notices",
    "output",
    "path_metadata",
    "plugin",
    "profile",
    "proxy",
    "role_arn",
    "staging",
    "strict",
    "trace",
    "verbose",
    "version",
    "version_reporting",
]

#: Command option fields of cdk_mate 0.1.6, by class name.
FIELDS_0_1_6_COMMAND = {
    "Acknowledge": [
        "notice_id",
    ],
    "Bootstrap": [
        "aws_environment",
        "bootstrap_bucket_name",
        "bootstrap_customer_key",
        "bootstrap_kms_key_id",
        "cloudformation_execution_policies",
        "custom_permissions_boundary",
        "example_permissions_boundary",
        "execute",
        "force",
        "previous_parameters",
        "public_access_block_configuration",
        "qualifier",
        "show_template",
        "tags",
        "template",
        "termination_protection",
        "toolkit_stack_name",
        "trust",
        "trust_for_lookup",
    ],
    "Context": [
        "clear",
        "force",
        "reset",
    ],
    "Deploy": [
        "stacks",
        "all",
        "asset_parallelism",
        "asset_prebuild",
        "build_exclude",
        "change_set_name",
        "concurrency",
        "exclusively",
        "force",
        "hotswap",
        "hotswap_fallback",
        "ignore_no_stacks",
        "import_existing_resources",
        "logs",
        "method",
        "notification_arns",
        "outputs_file",
        "parameters",
        "previous_parameters",
        "progress",
        "require_approval",
        "rollback",
        "toolkit_stack_name",
        "watch",
    ],
    "Destroy": [
        "stacks",
        "all",
        "exclusively",
        "force",
    ],
    "Diff": [
        "stacks",
        "change_set",
        "context_lines",
        "exclusively",
        "fail",
        "processed",
        "quiet",
        "security_only",
        "template",
    ],
    "GC": [
        "aws_environment",
        "action",
        "bootstrap_stack_name",
        "confirm",
        "created_buffer_days",
        "rollback_buffer_days",
        "type",
        "unstable",
    ],
    "Import": [
        "stacks",
        "change_set_name",
        "execute",
        "force",
        "record_resource_mapping",
        "resource_mapping",
        "rollback",
        "toolkit_stack_name",
    ],
    "Init": [
        "template_type",
        "generate_only",
        "language",
        "list_",
    ],
    "Synth": [
        "exclusively",
        "quiet",
        "validation",
    ],
}


def _command_classes() -> list[type[cli_cmd.BaseCommand]]:
    return [
        value
        for value in vars(cli_cmd).values()
        if isinstance(value, type)
        and issubclass(value, cli_cmd.BaseCommand)
        and value is not cli_cmd.BaseCommand
    ]


def test_every_command():
    classes = _command_classes()
    assert len(classes) == 25
    for klass in classes:
        assert klass.__doc__
        subcommand = klass()._subcommand()
        assert klass().to_args() == ["cdk", *subcommand]


def test_every_option_has_an_arg_type():
    for klass in [cli_cmd.BaseCommand, *_command_classes()]:
        for field in dataclasses.fields(klass):
            if field.name in ("cdk_cmd", "extra_args"):
                assert "t" not in field.metadata
            else:
                assert "t" in field.metadata, (klass, field.name)


def test_field_names_kept_from_0_1_6():
    """
    Regenerating cli_cmd.py from a newer CDK CLI must not drop a field that
    users of cdk_mate 0.1.x may set.
    """
    global_names = {field.name for field in dataclasses.fields(cli_cmd.BaseCommand)}
    assert set(FIELDS_0_1_6_GLOBAL) <= global_names
    for class_name, names in FIELDS_0_1_6_COMMAND.items():
        klass = getattr(cli_cmd, class_name)
        field_names = {field.name for field in dataclasses.fields(klass)}
        missing = set(names) - field_names
        assert not missing, (class_name, missing)


if __name__ == "__main__":
    from cdk_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "cdk_mate.cli.cli_cmd",
        preview=False,
    )
